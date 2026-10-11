# ATLAS — Sources de données : provenance, licences, empreintes

*Mis à jour le 2026-10-10 (phase 1).*

- **Manifeste machine :** `docs/manifest_raw.csv`, mis à jour automatiquement par `scripts/01_download_raw.py`.
- **Données brutes :** dans `data/raw/<source>/`. Elles ne sont jamais modifiées ni versionnées ; on les retrouve avec `uv run python scripts/01_download_raw.py --sim-years 2009-2025`.
- **Comparaison :** `tests/test_manifest.py` compare la taille et le SHA-256 de **chaque** fichier brut présent au manifeste. Par ailleurs, `01_download_raw.py` refuse de réécrire le manifeste si un fichier local a changé sans nouveau téléchargement.

---

## 1. Statistique agricole annuelle (SAA) : séries longues départementales

| Champ | Valeur |
|---|---|
| Producteur | SSP, ministère chargé de l'agriculture (Agreste), avec les services régionaux (SRISE) |
| Page officielle | https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/ |
| Fichier | `SAA-SeriesLongues-2010-2025_DonneesProvisoires-DepartementalesRegionales.zip` (2 xlsx : départemental et régional) |
| Méthodologie | https://agreste.agriculture.gouv.fr/agreste-web/methodon/S-SAA/methodon/ (PDF « Méthodologie » de 37 pages et note « Statut qualité », lus) |
| Licence | **Présumée Licence Ouverte (Etalab).** La fiche data.gouv de la SAA publiée par le ministère indique `fr-lo` (https://www.data.gouv.fr/datasets/5369a047a3a729239d20631f/). La page des séries longues n'affiche pas de licence. **À confirmer.** Attribution : « Agreste — Statistique agricole annuelle, SSP / ministère chargé de l'agriculture » |
| Accès | Téléchargement direct HTTPS. **Le serveur n'envoie pas son certificat intermédiaire** : voir `certs/README.md`. On ajoute l'intermédiaire au magasin système, en retirant le drapeau Python `VERIFY_X509_PARTIAL_CHAIN` : la chaîne doit remonter à la racine HARICA, et le nom d'hôte est vérifié. |
| Couverture | Récoltes 2010-2025 ; 95 départements métropolitains (Paris absent) + 5 DROM ; annuelle |
| Unités | Surface en ha ; production en quintaux (q) ; rendement en q/ha (1 q = 100 kg) |
| Utilisé | Feuille `COP` (céréales, oléagineux, protéagineux) → `data/interim/saa_cop_departements_long.parquet` |

### Données provisoires, révisions, ruptures

- **2025 est provisoire** : données arrêtées au 30/03/2026. La version définitive est publiée en novembre. Selon la méthodologie, la version définitive de l'année précédente peut « très marginalement » être corrigée. Le fichier téléchargé correspond à la version provisoire 2025 ; **il faudra le retélécharger après novembre 2026** et comparer les empreintes et les valeurs.
- **Rétropolation 2010-2019** : les séries ont été mises en cohérence avec le recensement agricole 2020. D'après la méthodologie, le recalage a été fait en 2022, puis complété en 2025 pour les prairies et la SAU. Les séries ne sont donc **pas** celles publiées à l'époque : c'est une information postérieure, importante pour la validation prédictive.
- **Rupture avant 2010** : les données 2000-2010 (tableaux interactifs) n'ont pas été rétropolées ; elles ne sont pas comparables telles quelles.
- **Nature des chiffres** : opération de **synthèse multi-sources** (enquêtes, PAC, informations locales). Les rendements sont « plus difficiles à établir » que les surfaces. Pour certaines productions, les régions peu productrices sont estimées en appliquant l'évolution nationale.
- **Statut qualité** (1 = raisonnablement fiable ; 2 = fragile, à utiliser en totaux ; 3 = extrapolé) : il ne reflète que la **dernière année publiée**.
- **Rattachement géographique** : les terres sont rattachées au département du **siège de l'exploitation**, pas à celui de la parcelle.
- **Non-récolte** : une surface non récoltée (aléa sans resemis) est comptée avec un rendement nul.
- **Précision constatée** :
  - environ 66 % des rendements de la feuille COP sont des entiers (q/ha) ; pour le blé tendre d'hiver de la population, c'est 86,6 % ;
  - production ≈ surface × rendement à 0,5 % près pour 99,98 % des lignes.

  La production est donc essentiellement dérivée du rendement.
- **Valeurs particulières (feuille COP)** : 3 680 lignes ont le statut « NC » (presque toujours avec des valeurs nulles) et 1 600 lignes (culture 28, « PAILLES ») n'ont pas de surface. À traiter explicitement lors de la sélection du panel.

## 2. SIM2 quotidienne (SAFRAN-ISBA), Météo-France

| Champ | Valeur |
|---|---|
| Producteur | Météo-France |
| Page officielle | https://www.data.gouv.fr/datasets/donnees-changement-climatique-sim-quotidienne |
| Documentation | `sim-quotidienne-parametres-20260331.pdf` (paramètres, unités, fenêtres horaires) ; `climatologie-presentation-modele-sim-20260602.pdf` (modèle). Toutes deux téléchargées. |
| Licence | **Licence Ouverte / Open Licence 2.0** (`lov2` sur data.gouv). Mention : « Source : Météo-France » |
| Accès | HTTPS direct, un fichier csv.gz par an : `https://meteofrance.s3.sbg.io.cloud.ovh.net/data/REF_CC/SIM/QUOT_SIM2_<année>.csv.gz` |
| Fichiers | 1989 à 2025 (37 fichiers, ≈ 5,1 Go compressés ; 1989-2008 pour la robustesse sur période longue, 2009 pour les semis de la récolte 2010) + grille `coordonnees_grille_safran_lambert-2-etendu.csv` |
| Couverture | France métropolitaine, 9 892 mailles de 8 km (0,072°), quotidien. Contrôlée pour **chacune des 37 années** : 365 ou 366 jours × 9 892 mailles, sans doublon ni valeur manquante sur `T`, `TINF_H`, `TSUP_H`, `SWI` |
| Coordonnées | `LAMBX`, `LAMBY` en **hectomètres**, Lambert II étendu (centre de maille) ; la grille fournit aussi la latitude et la longitude en degrés décimaux (virgule décimale) |
| Séparateur, format | `;`, en-tête en première ligne, `DATE` au format AAAAMMJJ |

### Révisions et points d'attention

- **Mise à jour bimensuelle des quatre dernières années, quotidienne sur 60 jours glissants.** Les fichiers 2022-2025 peuvent encore changer. Le script ne retélécharge pas un fichier présent : pour intégrer une révision, il faut renommer l'ancien fichier, relancer le téléchargement, puis comparer. `tests/test_manifest.py` détecte toute modification locale non tracée.
- SIM est une **réanalyse** : interpolation optimale par massif et tranche d'altitude, à partir d'un réseau de stations variable dans le temps. Ce n'est pas une observation.
- **Fenêtres horaires différentes selon les variables** (notice) : `T` sur ]00-00 UTC] ; `TINF_H` sur ]18-18 UTC] ; `TSUP_H`, précipitations, `SWI` et `EVAP` sur ]06-06 UTC] ; `WG_RACINE` à 06 UTC.
  - La notice ne dit pas à quel jour civil se rattache une fenêtre à cheval sur deux dates.
  - Cette convention a été **déterminée empiriquement** : voir `docs/notes_methodologiques.md`, § 1.
- **Unité de `SWI`** : la notice indique « % », mais les valeurs observées vont de −0,035 à 2,075, avec un ordre de grandeur de 1. C'est un indice sans dimension. Écart à signaler et à garder à l'esprit pour tout seuil.

## 3. ADMIN EXPRESS COG CARTO (IGN) : contours départementaux

| Champ | Valeur |
|---|---|
| Producteur | IGN |
| Page officielle | https://www.data.gouv.fr/datasets/admin-express-admin-express-cog-admin-express-cog-carto-admin-express-cog-carto-pe-admin-express-cog-carto-plus-pe ; flux : https://data.geopf.fr/telechargement/resource/ADMIN-EXPRESS-COG-CARTO |
| Édition | `ADMIN-EXPRESS-COG-CARTO_4-0__GEOPARQUET_WGS84G_FRA_2026-01-01`, couche `departement.parquet` |
| Licence | **Licence Ouverte 2.0** (`lov2`). Attribution : « IGN — ADMIN EXPRESS » |
| Format | GeoParquet 1.1, géométrie WKB `MultiPolygon` en WGS84 (CRS par défaut OGC:CRS84) ; 101 départements, DROM compris |
| Clé | `code_insee` (« 01 », « 2A », « 971 »), compatible avec les codes SAA normalisés. Test : `tests/test_saa.py::test_codes_match_admin_express` |
| Pourquoi ce format | Le GeoPackage n'existe qu'en archive `.7z`, et aucun outil 7z n'est installé. Le GeoParquet se lit avec `pyarrow`, déjà présent. |
| Limite | Version cartographique **généralisée** (CARTO) : précision suffisante pour des mailles de 8 km, à vérifier en phase 2 pour les mailles côtières et frontalières. Les contours 2026 sont appliqués à toute la période : aucun changement de département métropolitain n'est connu sur 2010-2025, à confirmer avec le COG. |

## 4. RPG version 2.0 (IGN/ASP) : masque blé, millésimes 2015-2017

| Champ | Valeur |
|---|---|
| Producteur | IGN, à partir des déclarations PAC gérées par l'ASP |
| Page officielle | https://www.data.gouv.fr/datasets/rpg ; flux : https://data.geopf.fr/telechargement/resource/RPG |
| Licence | **Licence Ouverte 2.0** (`lov2`) |
| Fichiers | `RPG_2-0__SHP_LAMB93_FR-<année>_<année>-01-01.7z`, 2015, 2016 et 2017 (≈ 2,8 Go chacun) ; seule la couche `PARCELLES_GRAPHIQUES` est extraite, vers `data/interim/rpg/` |
| Contenu utilisé | Parcelles `CODE_CULTU = 'BTH'` (blé tendre d'hiver), `SURF_PARC` (ha), Lambert 93 (EPSG:2154) ; environ 1 million de parcelles et 4,9 à 5,1 Mha par millésime |
| Contrôle | Surface BTH du RPG / surface SAA (code 01) : 0,996, 0,996, 0,994 (2015-2017) ; corrélation départementale 0,9999 ; ratio médian 0,992 ; écarts les plus forts dans de petits départements du Sud (Vaucluse 0,74) |
| Limites | Déclarants PAC seulement ; localisation à la parcelle, alors que la SAA rattache les terres au siège de l'exploitation ; masque fixe (2015-2017) appliqué à toute la période |

## 5. Schauberger et al. (2022) : rendements départementaux 1900-2018 (robustesse sur période longue)

| Champ | Valeur |
|---|---|
| Producteurs | Schauberger, Kato, Kato, Watanabe & Ciais ; GFZ Data Services |
| Page officielle | https://doi.org/10.5880/PIK.2021.001 ; fichiers : https://datapub.gfz.de/download/10.5880.PIK.2021.001najvndf/ ; article : DOI 10.1038/s41597-022-01145-4 |
| Licence | **CC-BY 4.0** (citation obligatoire de l'article) |
| Version utilisée | **RAW** (pas FILTERED : voir `docs/decisions.md`) ; blé tendre d'hiver ; t/ha converties en q/ha |
| Provenance | 1989-2018 : ancienne base numérique Agreste, **non recalée** sur le RA 2020 |
| Compatibilité avec la SAA (2010-2018) | 761 paires sur 765 ; écart relatif médian 0,0 % ; 97,5 % des paires identiques à ±0,5 q/ha ; corrélation des résidus (effets fixes) 0,994 (`scripts/08_check_schauberger.py`) |

## 6. Altitude : service de calcul altimétrique de la Géoplateforme IGN (robustesse R13)

| Champ | Valeur |
|---|---|
| Producteur | IGN, RGE ALTI® (ressource `ign_rge_alti_wld`) |
| Service | `https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json` (POST) ; documentation : https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/calcul-altimetrique/ |
| Licence | Licence Etalab 2.0 (contenus de la Géoplateforme, d'après la page de documentation) |
| Limites d'usage | 5 000 points par requête ; 5 requêtes par seconde et par adresse IP |
| Requête | 143 744 points (16 par maille SIM française, sous-grille 4 × 4 de pas 2 km), le 2026-10-10 ; réponse brute conservée dans `data/raw/ign_altimetrie/` et inscrite au manifeste |
| Contrôles | Paris 34,8 m, mont Blanc 4 757 m. Hors couverture, le service renvoie −99 999, et des valeurs interpolées aberrantes sur les côtes (jusqu'à −6 080 361) : seules les altitudes de −50 à 4 810 m sont gardées (3 099 points exclus). 2 mailles côtières de blé (16 ha) sans point valide sont fixées à 0 m |
| Pourquoi ce choix | La BD ALTI (téléchargement) n'existe qu'au pas de 25 m et par département (≈ 15 Go). La grille SIM ne contient pas d'altitude |

## 7. Prix du blé tendre (phase 6, valorisation descriptive)

| Source | Détail | Licence | Contrôle |
|---|---|---|---|
| INSEE, IPPAP annuel « Blé tendre » | idbank 010776425, base 2020, 1949-2025 ; https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/010776425 | Licence Ouverte (Etalab) **[À VÉRIFIER pour la BDM]** | — |
| Eurostat `apri_ap_crpouta` | Prix absolu (€/100 kg), France, blé tendre ; **valeurs disponibles seulement jusqu'en 2016** | Réutilisation Eurostat (CC BY 4.0) **[À VÉRIFIER]** | Rapport à l'IPPAP de 0,2504 ± 0,0004 sur 2012-2016 ; 0,19 en 2010-2011 (rupture probable) |

## 8. NDVI MODIS MOD13Q1 v6.1 (NASA LP DAAC, via AppEEARS)

| Champ | Valeur |
|---|---|
| Producteur | NASA LP DAAC ; produit MOD13Q1 v6.1 (Terra MODIS, 250 m, composites de 16 jours) |
| Accès | API AppEEARS, https://appeears.earthdatacloud.nasa.gov/api/ (commande par zone ; GeoTIFF, EPSG:4326). Compte NASA Earthdata requis ; jeton AppEEARS (48 h) obtenu par l'utilisateur, rangé dans `.env` |
| Commandes | `ebe86b6f-8e1f-497a-a811-f92e5f4e2a22` (2022) ; `5a8a9750-f9e6-4b03-9fd3-619d84331cbd` (2010-2021, 2023-2025) ; contour simplifié de la France métropolitaine ; composites d'avril à juin (le premier commence fin mars) |
| Couches | `_250m_16_days_NDVI` (int16, facteur d'échelle 0,0001, -3000 = pas de donnée) ; `_250m_16_days_pixel_reliability` (0 bon, 1 marginal, 2 neige, 3 nuage) ; `VI_Quality` ajoutée d'office par AppEEARS, non utilisée |
| Licence | Données NASA, sans restriction d'usage (politique de données ouvertes de l'EOSDIS) **[À VÉRIFIER, citation du produit à faire]** |
| Limites | Terra/MODIS en fin de mission (continuité après 2025 incertaine) ; NDVI de maille, et non de parcelle |

## 9. Sources documentées mais non téléchargées

| Source | Statut | Raison |
|---|---|---|
| Prix Eurostat `apri_ap_crpouta` | Phase 6 (optionnel) | Valorisation descriptive |
| NDVI MODIS / VIIRS | Phase 6 (optionnel) | Continuité de la série incertaine |

## 10. Empreintes SHA-256 (générées depuis le manifeste)

Les 354 fichiers AppEEARS (5.02 Go) ne sont pas listés un par un : leurs empreintes sont dans `docs/manifest_raw.csv`, et `tests/test_manifest.py` les vérifie.

| Fichier (`data/raw/…`) | Taille | Accès | SHA-256 |
|---|---|---|---|
| `agreste_saa/SAA-SeriesLongues-2010-2025_DonneesProvisoires-DepartementalesRegionales.zip` | 7.08 Mo | 2026-10-10 | `46e2ea9493ae34fac5d343e6cef51ac08a455d970ce78611c5d3b2365650d76f` |
| `ign_admin_express/ADMIN-EXPRESS-COG-CARTO_4-0_2026-01-01_departement.parquet` | 12.92 Mo | 2026-10-10 | `ba44a327aaeb9df43b1f9fd52f13ca0ec67fe748c845131fedd6b3e6c1061bce` |
| `ign_altimetrie/sim_cells_subgrid_altitude.parquet` | 3.50 Mo | 2026-10-10 | `602ea33845e95950ed3332f9e6eeb599f67c36c3b3525e2e62b6b47e942dcfbf` |
| `ign_rpg/RPG_2-0__SHP_LAMB93_FR-2015_2015-01-01.7z` | 2821.30 Mo | 2026-10-10 | `c3e5960d7a7157dfab902ae7022e8ced6a080127cc6c9763ecc87e48c863fda8` |
| `ign_rpg/RPG_2-0__SHP_LAMB93_FR-2016_2016-01-01.7z` | 2840.98 Mo | 2026-10-10 | `54a410bae071b566ccb4b8e6aa5d53ed77b6cc2d0836b68f8da27238e95166ae` |
| `ign_rpg/RPG_2-0__SHP_LAMB93_FR-2017_2017-01-01.7z` | 2873.22 Mo | 2026-10-10 | `589420ae130314091f4ee9c9330cb22f5d232b0fde48e28aa6bae41f8edaba90` |
| `meteofrance_sim/QUOT_SIM2_1989.csv.gz` | 134.49 Mo | 2026-10-10 | `6620c7c0bcb7a343aa6a5aea21f664fcf6793a74fd4d736eb696a99b76493538` |
| `meteofrance_sim/QUOT_SIM2_1990.csv.gz` | 137.08 Mo | 2026-10-10 | `cc91bd7afbd18160a0035a70004a357274f1006baea285d0f02806121a19a84a` |
| `meteofrance_sim/QUOT_SIM2_1991.csv.gz` | 137.76 Mo | 2026-10-10 | `dc325dc6b064986a2314c0bf02cf0081866c03120735fdd9458fccca8da18d60` |
| `meteofrance_sim/QUOT_SIM2_1992.csv.gz` | 137.76 Mo | 2026-10-10 | `a9febaf44e513da182ea1611e2a1f0c3b058571d986a364be514d44aa1b7ec62` |
| `meteofrance_sim/QUOT_SIM2_1993.csv.gz` | 137.63 Mo | 2026-10-10 | `0b1799790acb8b0c8c191f0ec41ffe0a9da42665035e11ee4c13d58e947e2bc1` |
| `meteofrance_sim/QUOT_SIM2_1994.csv.gz` | 138.20 Mo | 2026-10-10 | `f019dcc34d281d449fe9125fb1da43fd4eb67fb2ed7b761b69eff45b06cc7d89` |
| `meteofrance_sim/QUOT_SIM2_1995.csv.gz` | 138.53 Mo | 2026-10-10 | `4c346e72f8286959be56954d37a8fed5f37163ade5563773ea329c82f04dfaa5` |
| `meteofrance_sim/QUOT_SIM2_1996.csv.gz` | 138.75 Mo | 2026-10-10 | `2ef6182512dcceb4fc7f96bb7ca7e9642c7ee8f7fba5f9293fb24476656b02d1` |
| `meteofrance_sim/QUOT_SIM2_1997.csv.gz` | 137.66 Mo | 2026-10-10 | `5f52b35f12cc4504a21c010fd0653c308a53701f30155b0e21ece88f33b1cfab` |
| `meteofrance_sim/QUOT_SIM2_1998.csv.gz` | 137.93 Mo | 2026-10-10 | `9db2106726b882f91264621234c2e0d6745bb93e28dfef5349deaf0f1f068c2b` |
| `meteofrance_sim/QUOT_SIM2_1999.csv.gz` | 139.75 Mo | 2026-10-10 | `6fffb36868974e88fab5a63bdfcd91959b6a740191bda40cfe4927edd3bc9610` |
| `meteofrance_sim/QUOT_SIM2_2000.csv.gz` | 138.20 Mo | 2026-10-10 | `103f26c2f36b79506a0790e3a3f8ae938100ffcd03a87d9a352843dcc4ed2861` |
| `meteofrance_sim/QUOT_SIM2_2001.csv.gz` | 139.06 Mo | 2026-10-10 | `cc6e74dbc04f2d661d81e4fc7212e083ef4a81fc257616f1a83546561aa4fbb7` |
| `meteofrance_sim/QUOT_SIM2_2002.csv.gz` | 136.78 Mo | 2026-10-10 | `e408a59d08d2d14c036867ab26216684b67d22d52a7ae0656170a11f669add55` |
| `meteofrance_sim/QUOT_SIM2_2003.csv.gz` | 138.45 Mo | 2026-10-10 | `073973fdd88e48d66be299ce033b132345d15b5f44c1e939bfc9376c48ecd84f` |
| `meteofrance_sim/QUOT_SIM2_2004.csv.gz` | 138.71 Mo | 2026-10-10 | `852e5f1e9d74fecf69c26b4834fd46e8c641859a8eeaecae7003029d0af567da` |
| `meteofrance_sim/QUOT_SIM2_2005.csv.gz` | 138.72 Mo | 2026-10-10 | `f0e63539825fc39b76bce24074426a5eb661ed5923f73f9f0294a2a25934335b` |
| `meteofrance_sim/QUOT_SIM2_2006.csv.gz` | 138.33 Mo | 2026-10-10 | `3ca1f229bd1094277cf1e6355a3cd7c483f828c66fcc14a18a56df47d4442b61` |
| `meteofrance_sim/QUOT_SIM2_2007.csv.gz` | 136.80 Mo | 2026-10-10 | `4df38ad0fe37102f38b7f9336d30268f7ca8e58ed4fc3060147839144c56aadb` |
| `meteofrance_sim/QUOT_SIM2_2008.csv.gz` | 138.44 Mo | 2026-10-10 | `1988f936bea693ed0dbeea64b3dc4cf08da898ec4c2955c026e4904621f09379` |
| `meteofrance_sim/QUOT_SIM2_2009.csv.gz` | 138.83 Mo | 2026-10-10 | `9c035647615ebdfdfeb47e039e5a02a0b1331db1a410bd9181af593b4cc1bc76` |
| `meteofrance_sim/QUOT_SIM2_2010.csv.gz` | 141.68 Mo | 2026-10-10 | `cae71381243051c59194283927ba7c15bb3c446f24d67fdc6999e46e359006df` |
| `meteofrance_sim/QUOT_SIM2_2011.csv.gz` | 135.38 Mo | 2026-10-10 | `d31a02ff6095a5299b5357a41e1bfd8a2e844c03cb342227153299eebe458a5e` |
| `meteofrance_sim/QUOT_SIM2_2012.csv.gz` | 139.33 Mo | 2026-10-10 | `851a00d67ccc8d51915caa38864a9b58a0394bcde479ed66decaa2d9b407fe64` |
| `meteofrance_sim/QUOT_SIM2_2013.csv.gz` | 140.65 Mo | 2026-10-10 | `90f4253be4d2a59ae79003536aff248686a810381e01c8396210543febc0f501` |
| `meteofrance_sim/QUOT_SIM2_2014.csv.gz` | 136.89 Mo | 2026-10-10 | `7e1f1e8d6e34cc13b93e30cf2dd39544c47e13bb85376063ed085a6ee07b19a4` |
| `meteofrance_sim/QUOT_SIM2_2015.csv.gz` | 136.90 Mo | 2026-10-10 | `e6db9413aa711102162ab98eb49e0df5499ece2e6b93b6e50c11b2c9b5adb0ad` |
| `meteofrance_sim/QUOT_SIM2_2016.csv.gz` | 137.30 Mo | 2026-10-10 | `46dc2de55a2d6f656f570579f343d37691b06d4016028461f083ac6598e88d79` |
| `meteofrance_sim/QUOT_SIM2_2017.csv.gz` | 137.06 Mo | 2026-10-10 | `cb3386e53814f4b305bad3d584afd404c1cec45ed1132c8af5c0795bcd44e233` |
| `meteofrance_sim/QUOT_SIM2_2018.csv.gz` | 138.30 Mo | 2026-10-10 | `fc3431f1a1308bfb1cde949fd7b027777d4d73895b11e0ea16148b9471d15a22` |
| `meteofrance_sim/QUOT_SIM2_2019.csv.gz` | 137.64 Mo | 2026-10-10 | `872962dab2f794f205a537786ca7e94842324e0634006d91d9f45b397b25d3bb` |
| `meteofrance_sim/QUOT_SIM2_2020.csv.gz` | 136.84 Mo | 2026-10-10 | `e87d437a733f942a81c4da787ded34a373d84f4c888768708752f2a59a8228d9` |
| `meteofrance_sim/QUOT_SIM2_2021.csv.gz` | 138.09 Mo | 2026-10-10 | `c42880007adb0bc292767dff3c9aa6c1519202b31f5e5c36dfbc3ac34c2d3b1e` |
| `meteofrance_sim/QUOT_SIM2_2022.csv.gz` | 136.00 Mo | 2026-10-10 | `f68410968d3afd7323d702fd296636c464c13aee782c3d774826ee44a701e9f1` |
| `meteofrance_sim/QUOT_SIM2_2023.csv.gz` | 137.39 Mo | 2026-10-10 | `d63976e44a3d31c186c5ff2739e3b4400bc929f8caabe9d71d0ccb7015bd18e2` |
| `meteofrance_sim/QUOT_SIM2_2024.csv.gz` | 137.94 Mo | 2026-10-10 | `7d1c9d4d1ab8b257cc856183f06c557badbace89074f412184174a5c125eb419` |
| `meteofrance_sim/QUOT_SIM2_2025.csv.gz` | 136.83 Mo | 2026-10-10 | `5656fb4b44531a504ecc86c755fc998e18d05a470f33fd666577f5c648f5e221` |
| `meteofrance_sim/climatologie-presentation-modele-sim-20260602.pdf` | 0.30 Mo | 2026-10-10 | `be46ea685eadd21d0e2c7f19e06389f9bdf24bf106dbea5fbc4242280b3bf97c` |
| `meteofrance_sim/coordonnees_grille_safran_lambert-2-etendu.csv` | 0.28 Mo | 2026-10-10 | `b02181e808c384ff4d713d46c584977ef4feada4509e72d5351d6a2fc29d6379` |
| `meteofrance_sim/sim-quotidienne-parametres-20260331.pdf` | 0.34 Mo | 2026-10-10 | `8f1ec72fbf765f0e480b768a54fe89338f29522172cd7b2c71045a7ae17c4f8b` |
| `pik_schauberger/2021-001_Schauberger-et-al_Data.zip` | 3.16 Mo | 2026-10-10 | `184fb3ddb62f01b646070629d8fc3667bcd95729ad40ecb1a8247f7730dab119` |
| `pik_schauberger/2021-001_Schauberger_et-al_Data-Description.pdf` | 0.60 Mo | 2026-10-10 | `b8e48e2a64b50f13cd1f031784938fe0bc5814001362670c3c40de01ebeca39f` |
| `prix/eurostat_apri_ap_crpouta_FR_ble_tendre.json` | 0.00 Mo | 2026-10-10 | `9856846063315894a32f81cfb93b131e272b27dae7efceb97439e2b723f82974` |
| `prix/insee_ippap_ble_tendre_010776425.xml` | 0.01 Mo | 2026-10-10 | `3df1b652790c178cd4e027cf1520abbb499593614d2368d408c5ad79255709e5` |

## Sources ajoutées en phase 0 bis (2026-10-11)

Détails, tests et décisions : `docs/phase0bis_cadrage.md` et `docs/phase2bis_donnees.md`. Empreintes au manifeste.

| Source | Accès | Couverture | Licence | Points d'attention |
|---|---|---|---|---|
| Agreste, SAA « anciennes séries », tableau « Cultures développées » (`SAANR_DEVELOPPE_2/FDS_DEVELOPPE_2.zip`) | ZIP direct (8,8 Mo), un CSV par année | 2000-2020, départements ; maïs grain irrigué / non irrigué | Licence Ouverte (présumée, comme la SAA) | Non recalée sur le RA 2020 ; identique aux séries actuelles pour 94-95 % des paires sur 2010-2020 ; pas de statut qualité |
| Météo-France SIM2, 1958-1988 | Mêmes fichiers csv.gz que 1989-2025 | 1er août 1958 → 1988 | Licence Ouverte 2.0 | 1958 partiel (début de la réanalyse) |
| VigiEau « Donnée Sécheresse » (MTE), data.gouv.fr | CSV des arrêtés (2012-2024 annuels, `arretes.csv` global, arrêtés-cadres) | 2010-2026, départements, zones d'alerte | Licence Ouverte 2.0 | Niveau de gravité manquant à 99,6-100 % en 2010-2011 et à 13-21 % en 2012-2015 |
| INSEE, IPPAP maïs (idbank 010776430) | SDMX BDM | 1970-2025, base 2020 | À vérifier pour la BDM (comme l'IPPAP blé) | Indice : raccordé à Eurostat pour obtenir des €/q |
| Eurostat `apri_ap_crpouta`, maïs (`prod_veg=01500000`), France | API JSON | 2000-2016 | Réutilisation Eurostat (à vérifier) | Série arrêtée en 2016 ; rapport à l'IPPAP stable sur 2012-2016 (0,2192 €/q par point) |
| RPG 2015-2017, code `MIS` | Archives déjà téléchargées (phase 2) | Parcelles de maïs grain | Licence Ouverte 2.0 | Ne distingue pas irrigué et non irrigué ; vérifié comme maïs grain (corrélation de 0,993 avec la SAA) |

Note : les sections 1 à 10 ci-dessus datent des phases 1 à 6. La liste exhaustive des fichiers téléchargés est le manifeste `docs/manifest_raw.csv`.
