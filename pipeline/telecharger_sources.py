"""
Téléchargement unique de toutes les sources accessibles par API, stockées localement dans data/.

Une fois les fichiers présents, ni le notebook ni le pipeline n'appellent plus les API :
on ne paie les limites de requêtes qu'une seule fois. Le script est reprenable : chaque
fichier déjà présent est sauté, et une coupure ne fait perdre que le fichier en cours.

Usage (depuis la racine du dépôt) :
    python pipeline/telecharger_sources.py                      # toutes les sources possibles
    python pipeline/telecharger_sources.py --sources mdf,firms  # seulement certaines
    python pipeline/telecharger_sources.py --forcer mdf         # retélécharger une source

Sources : communes, mdf, openmeteo, firms
  - firms : clé NASA dans .env (FIRMS_MAP_KEY=...) ou variable d'environnement
La 5e source, la BDIFF, n'a pas d'API : export manuel depuis bdiff.agriculture.gouv.fr.

Chaque fichier écrit est consigné dans data/_journal_telechargements.csv
(source, fichier, date, nombre de lignes, empreinte SHA-256) : c'est la traçabilité de la couche bronze.
"""
import argparse
import csv
import gzip
import hashlib
import io
import os
import sys
import time
from datetime import datetime, timezone

import pandas as pd
import requests

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "data")
JOURNAL = os.path.join(DATA, "_journal_telechargements.csv")

DEP_NA = ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"]
DEBUT, FIN = "2006-01-01", "2025-12-31"
BBOX_NA = "-1.8,42.75,2.65,47.2"                     # ouest, sud, est, nord

SESSION = requests.Session()
SESSION.headers["User-Agent"] = "feux-de-foret-nouvelle-aquitaine (projet etudiant HETIC)"


# --------------------------------------------------------------------------- outils
def chemin(*parties):
    return os.path.join(DATA, *parties)


def lire_cle(nom, fichier=os.path.join(RACINE, ".env")):
    """Variable d'environnement en priorité, sinon ligne NOM=valeur du fichier .env (non versionné)."""
    if os.environ.get(nom):
        return os.environ[nom].strip()
    if os.path.exists(fichier):
        with open(fichier, encoding="utf-8") as f:
            for ligne in f:
                cle, _, valeur = ligne.strip().partition("=")
                if cle.strip() == nom and valeur.strip():
                    return valeur.strip().strip('"').strip("'")
    return None


def requete(url, params=None, essais=6, timeout=180, attente_429=60):
    """GET avec relances : erreurs réseau et 5xx (attente croissante), 429 (attente longue)."""
    for i in range(1, essais + 1):
        try:
            r = SESSION.get(url, params=params, timeout=timeout)
        except requests.RequestException as e:
            print(f"    essai {i}/{essais} : {e.__class__.__name__}, nouvel essai dans {10 * i} s")
            time.sleep(10 * i)
            continue
        if r.status_code == 429:
            attente = attente_429 * i
            print(f"    limite de requêtes atteinte (429), attente {attente} s")
            time.sleep(attente)
            continue
        if r.status_code >= 500:
            print(f"    erreur serveur {r.status_code}, nouvel essai dans {10 * i} s")
            time.sleep(10 * i)
            continue
        r.raise_for_status()
        return r
    raise RuntimeError(f"Échec après {essais} essais : {url}")


def ecrire(df, fichier, source):
    """Écriture atomique (fichier temporaire puis renommage) + ligne de journal."""
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    tmp = fichier + ".partiel"
    df.to_csv(tmp, index=False)
    os.replace(tmp, fichier)
    journaliser(source, fichier, len(df))


def journaliser(source, fichier, nb_lignes):
    h = hashlib.sha256()
    with open(fichier, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    nouveau = not os.path.exists(JOURNAL)
    with open(JOURNAL, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nouveau:
            w.writerow(["source", "fichier", "telecharge_le", "nb_lignes", "sha256"])
        w.writerow([source, os.path.relpath(fichier, RACINE).replace(os.sep, "/"),
                    datetime.now(timezone.utc).isoformat(timespec="seconds"), nb_lignes, h.hexdigest()])


def deja_la(fichier, forcer):
    if os.path.exists(fichier) and not forcer:
        print(f"  = {os.path.relpath(fichier, RACINE)} déjà présent")
        return True
    return False


# --------------------------------------------------------------------------- sources
def communes(forcer=False):
    """Référentiel des communes (geo.api.gouv.fr) : centre, surface, population."""
    fichier = chemin("communes_na.csv")
    if deja_la(fichier, forcer):
        return
    lignes = []
    for dep in DEP_NA:
        r = requete(f"https://geo.api.gouv.fr/departements/{dep}/communes",
                    {"fields": "nom,code,centre,surface,population"})
        for c in r.json():
            lon, lat = c["centre"]["coordinates"] if c.get("centre") else (None, None)
            lignes.append({"code_insee": c["code"], "commune": c["nom"], "departement": dep,
                           "lat": lat, "lon": lon, "surface_ha": c.get("surface"),
                           "population": c.get("population")})
    ecrire(pd.DataFrame(lignes), fichier, "geo.api.gouv.fr")
    print(f"  + communes : {len(lignes)}")


# Archives Météo des forêts : un fichier csv.gz par saison sur data.gouv.fr
MDF_DATASET = "archives-de-la-meteo-des-forets"
MDF_RESSOURCES_CONNUES = [   # repli si l'API data.gouv ne répond pas (relevé le 18/11/2026)
    "59f2c103-f8d5-4216-9e46-de2327f4dc5a",
    "c1f8f7c8-e8cc-4d70-9372-43da3c878c81",
    "14f5607c-68b1-4b91-be36-b1265f309c51",
]


def mdf(forcer=False):
    """Toutes les saisons archivées de la Météo des forêts (France entière), puis extrait NA."""
    dossier = chemin("brut", "meteo_des_forets")
    os.makedirs(dossier, exist_ok=True)
    try:
        meta = requete(f"https://www.data.gouv.fr/api/1/datasets/{MDF_DATASET}/").json()
        ressources = [(r["id"], r["url"]) for r in meta["resources"] if r.get("type") == "main"]
    except Exception as e:  # noqa: BLE001
        print(f"  ! liste des fichiers indisponible ({e})")
        ressources = []
    if not ressources:
        print("  ! utilisation des identifiants de fichiers connus")
        ressources = [(i, f"https://www.data.gouv.fr/api/1/datasets/r/{i}") for i in MDF_RESSOURCES_CONNUES]

    tables = []
    for rid, url in ressources:
        fichier = os.path.join(dossier, f"{rid}.csv.gz")
        if not deja_la(fichier, forcer):
            r = requete(url)
            contenu = r.content
            if not contenu[:2] == b"\x1f\x8b":          # pas compressé : on compresse pour stocker
                contenu = gzip.compress(contenu)
            with open(fichier + ".partiel", "wb") as f:
                f.write(contenu)
            os.replace(fichier + ".partiel", fichier)
            journaliser("Météo des forêts (archive brute)", fichier, -1)
            print(f"  + archive {rid}")
        df = pd.read_csv(fichier, compression="gzip", sep=None, engine="python", dtype=str)
        df.columns = [c.strip().lower() for c in df.columns]
        tables.append(df)

    tout = pd.concat(tables, ignore_index=True)
    manquantes = {"date", "num_dep", "niveau_j1", "niveau_j2"} - set(tout.columns)
    if manquantes:
        raise ValueError(f"Colonnes inattendues dans les archives MdF : {list(tout.columns)}")
    tout = tout.drop(columns=["__id"], errors="ignore")
    # Le libellé du département s'appelle `nom_dep` en 2024 et 2026, mais `dep_nom` en 2025
    if "nom_dep" not in tout:                       # colonne lue par le pipeline (dim_departement)
        tout["nom_dep"] = None
    if "dep_nom" in tout:
        tout["nom_dep"] = tout["nom_dep"].fillna(tout["dep_nom"])
        tout = tout.drop(columns="dep_nom")
    tout["num_dep"] = tout["num_dep"].str.zfill(2)
    tout = tout.drop_duplicates(["date", "num_dep"], keep="last").sort_values(["date", "num_dep"])
    ecrire(tout, chemin("meteo_foret_france.csv"), "Météo des forêts (France)")
    na = tout[tout["num_dep"].isin(DEP_NA)]
    ecrire(na, chemin("meteo_foret_na.csv"), "Météo des forêts (NA)")
    print(f"  + Météo des forêts : {len(tout)} lignes France, {len(na)} NA, "
          f"du {tout['date'].min()[:10]} au {tout['date'].max()[:10]}")


VARIABLES_OPENMETEO = ["temperature_2m_max", "temperature_2m_mean", "precipitation_sum",
                       "wind_speed_10m_max", "wind_gusts_10m_max", "relative_humidity_2m_min",
                       "et0_fao_evapotranspiration", "soil_moisture_0_to_7cm_mean"]


def centres_departements():
    c = pd.read_csv(chemin("communes_na.csv"), dtype={"departement": str})
    return c.groupby("departement")[["lat", "lon"]].mean()


def openmeteo(forcer=False):
    """Météo quotidienne ERA5, un point par département (même point que le notebook)."""
    if not os.path.exists(chemin("communes_na.csv")):
        communes()
    for dep, (lat, lon) in centres_departements().iterrows():
        fichier = chemin("meteo_quotidienne", f"{dep}.csv")
        if deja_la(fichier, forcer):
            continue
        # 20 ans x 8 variables ~ 400 « appels » au sens d'Open-Meteo : 429 => attente 10 min
        r = requete("https://archive-api.open-meteo.com/v1/archive", {
            "latitude": lat, "longitude": lon, "start_date": DEBUT, "end_date": FIN,
            "daily": ",".join(VARIABLES_OPENMETEO), "timezone": "Europe/Paris",
        }, attente_429=600, essais=8)
        df = pd.DataFrame(r.json()["daily"]).rename(columns={"time": "date"})
        df["departement"] = dep
        ecrire(df, fichier, "Open-Meteo ERA5")
        print(f"  + Open-Meteo {dep} : {len(df)} jours")
        time.sleep(5)


def firms(forcer=False, capteurs=("VIIRS_SNPP_SP", "MODIS_SP")):
    """Points chauds NASA FIRMS (archives « SP »), un fichier par capteur et par année."""
    cle = lire_cle("FIRMS_MAP_KEY")
    if not cle:
        print("  ! pas de clé FIRMS_MAP_KEY (fichier .env ou variable d'environnement) : source ignorée")
        return
    premiere = {"VIIRS_SNPP_SP": 2012, "MODIS_SP": 2006}
    for capteur in capteurs:
        for annee in range(premiere.get(capteur, 2006), int(FIN[:4]) + 1):
            fichier = chemin("firms", f"{capteur}_{annee}.csv")
            if deja_la(fichier, forcer):
                continue
            tables = []
            for debut in pd.date_range(f"{annee}-01-01", f"{annee}-12-31", freq="5D"):
                jours = min(5, (pd.Timestamp(f"{annee}-12-31") - debut).days + 1)
                url = (f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
                       f"{cle}/{capteur}/{BBOX_NA}/{jours}/{debut:%Y-%m-%d}")
                r = requete(url, timeout=120, attente_429=120)
                texte = r.text.strip()
                if texte.startswith("Invalid") or "error" in texte[:200].lower():
                    raise RuntimeError(f"Réponse FIRMS : {texte[:200]}")
                if texte and "\n" in texte:
                    tables.append(pd.read_csv(io.StringIO(texte)))
                time.sleep(0.5)
            df = pd.concat(tables, ignore_index=True) if tables else pd.DataFrame(
                columns=["latitude", "longitude", "acq_date", "acq_time", "satellite",
                         "instrument", "confidence", "frp", "daynight"])
            ecrire(df, fichier, f"NASA FIRMS {capteur}")
            print(f"  + FIRMS {capteur} {annee} : {len(df)} détections")


SOURCES = {"communes": communes, "mdf": mdf, "openmeteo": openmeteo, "firms": firms}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sources", default=",".join(SOURCES),
                   help="liste séparée par des virgules (défaut : toutes)")
    p.add_argument("--forcer", default="", help="sources à retélécharger même si présentes")
    args = p.parse_args()
    choisies = [s.strip() for s in args.sources.split(",") if s.strip()]
    forcees = {s.strip() for s in args.forcer.split(",") if s.strip()}
    inconnues = set(choisies) - set(SOURCES)
    if inconnues:
        p.error(f"sources inconnues : {sorted(inconnues)} (possibles : {list(SOURCES)})")

    echecs = []
    for nom in choisies:
        print(f"\n== {nom}")
        try:
            SOURCES[nom](forcer=nom in forcees)
        except Exception as e:  # noqa: BLE001  — on continue avec les autres sources
            print(f"  ✗ {nom} : {e}")
            echecs.append(nom)

    print("\nRappel : la BDIFF (data/incendies.csv) s'exporte à la main depuis bdiff.agriculture.gouv.fr")
    if echecs:
        print(f"Sources en échec (relancer le script, les fichiers déjà là sont conservés) : {echecs}")
        return 1
    print("Terminé. Les fichiers sont dans data/ ; le notebook et le pipeline les lisent sans appel réseau.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
