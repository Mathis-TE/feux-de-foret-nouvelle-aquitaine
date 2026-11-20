# **Feux de forêt Nouvelle-Aquitaine : sources et stack technique** 

**Équipe :** Mathis TE, Ahmed ABBADI, Amine ASBANE **Dépôt GitHub :** <u>https://github.com/Mathis-TE/feux-de-foret-nouvelle-aquitaine</u> 

## **1. Sources de données** 

### **Sources déjà dans le dépôt** 

|**Source**|**Producteur**|**Rôle dans le projet**|**Fichier dans****`data/`**|
|---|---|---|---|
|BDIFF (incendies de<br>forêt)|Ministère de<br>l'Agriculture / IGN|Cible : où et quand les feux<br>partent, causes|`incendies.csv`|
|Archives Météo des<br>forêts|Météo-France|Indice de danger à évaluer<br>(niveaux 1 à 4, J+1 et J+2)|`meteo_foret_na.csv`|
|API Métadonnées<br>(INSEE)|INSEE|Liste officielle des communes<br>et des départements (noms et<br>codes), pour relier les sources<br>entre elles|`Accès par l'API INSEE`|
|Open-Meteo (réanalyse<br>ERA5)|Open-Meteo /<br>ECMWF|Variables explicatives :<br>température, pluie, vent,<br>humidité du sol|`meteo_quotidienne/<dep>.csv`|
|Interventions des SIS|DGSCGC (ministère<br>de l'Intérieur)|Activité des pompiers, 2008 à<br>2024 (17 CSV)|`interventions/`|
|Comptes des SDIS<br>2012-2025|OFGL (d'après la<br>DGFiP)|Budgets et moyens financiers<br>des SDIS|`comptes_sdis/`|



### **Sources prévues ou à confirmer** 

|**Source**|**Producteur**|**Intérêt**|**Statut**|
|---|---|---|---|
|Fire Weather Index<br>(FWI)|Copernicus / EFFIS|Indice météo standard couvrant<br>toute la période BDIFF, utile pour<br>juger le seuil de la Météo des<br>forêts|À évaluer : données de grille,<br>compte Copernicus nécessaire|
|NASA FIRMS|NASA|Détection de feux par satellite|Citée dans le sujet, non<br>téléchargée à ce jour|
|Météo des forêts,<br>France entière|Météo-France|Comparer la Gironde au reste du<br>territoire|Fichier<br>`meteo_foret_france.csv`<br>annoncé dans les docs, à<br>produire|
||||Piste : données|
|BD Forêt V2|IGN|Type de végétation par zone|cartographiques, jointure<br>géographique nécessaire|
|SWI (humidité des sols)|Météo-France|Contrôle de l'humidité du sol<br>d'Open-Meteo|Piste secondaire : fichiers très<br>volumineux|



|**Source**|**Producteur**|**Intérêt**|**Statut**|
|---|---|---|---|
|Points d'eau et pistes<br>DFCI|DFCI Aquitaine / GIP<br>ATGeRi|Équipements de défense contre<br>l'incendie|Piste : pas de jeu de données<br>ouvert trouvé, accès à<br>demander|



## **3. Choix de stack technique** 

|**Besoin**|**Outil retenu**|**Rôle**|
|---|---|---|
|Stockage et entrepôt|PostgreSQL|Base de données centrale : tables brutes, tables nettoyées,<br>schéma en étoile (faits et dimensions)|
|Visualisation|Power BI|Tableaux de bord pour présenter les indicateurs au SDIS, avec un<br>public non technique|
|Collecte et transformation|Python (pandas)|Script de téléchargement`pipeline/telecharger_sources.py`,<br>nettoyage et chargement vers PostgreSQL|
|Exploration|Notebook Jupyter|`nouvelle_aquitaine.ipynb`: statistiques descriptives et<br>premières analyses|
|Versioning|Git et GitHub|Une branche par membre, Pull Request relue avant fusion dans<br>`main`|



Chaîne de traitement prévue : sources (CSV et API) → téléchargement avec Python → chargement dans PostgreSQL → tables prêtes pour l'analyse → Power BI. 

