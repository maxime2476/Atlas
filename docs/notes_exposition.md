# ATLAS — Construction de l'exposition climatique (phase 2)

*Rédigé le 2026-10-10. Aucun lien entre météo et rendement n'a été estimé à ce stade.*

> *Document historique (phase 2), non réécrit : il décrit la chaîne sur SIM 2009-2025 (1989-2025 pour la période longue). Elle a ensuite été étendue à 1958-2025 et au masque maïs ; voir `data/README.md`.*

## 1. Chaîne de traitement

| Étape | Script | Entrée | Sortie | Contrôles |
|---|---|---|---|---|
| Poids spatiaux | `04_build_spatial_weights.py` | Grille SIM, ADMIN EXPRESS 2026 | `data/processed/weights_cell_dep_area.parquet` | Tableau de jointure ci-dessous ; `tests/test_spatial.py` |
| Indicateurs mensuels | `05_build_weather_monthly.py` | SIM 2009-2025 | `data/interim/weather_cell_month.parquet`, `data/processed/weather_dep_month_area.parquet` | Mois incomplets comptés ; `tests/test_degree_days.py`, `tests/test_weather.py` |
| Fenêtres et exposition | `06_exposure_check.py` | Tables mensuelles, SAA | `data/processed/weather_dep_harvest_<area|wheat>[_1990].parquet` | Règle de repli ; tests sur la table finale |
| Masque blé | `07_build_wheat_mask.py` | RPG 2015-2017 (parcelles BTH), table maille × mois | `weights_cell_dep_wheat.parquet`, `weather_dep_month_wheat.parquet` | Comparaison RPG/SAA ; `tests/test_rpg_schauberger.py` |
| Période longue | `08_check_schauberger.py` | Schauberger et al. (RAW), SAA | `data/interim/schauberger_wheat_winter_raw.parquet` | Critères de compatibilité pré-spécifiés |

Durée : environ 15 min pour l'étape 5 (37 années, 1989-2025, environ 121 millions de lignes maille-jour), environ 1,5 min pour l'étape 7, quelques secondes pour les autres.

## 2. Correspondance spatiale

- **CRS** : EPSG:27572 (NTF Paris / Lambert zone II étendu), celui de la grille SIM. Les départements ADMIN EXPRESS (WGS84) sont reprojetés dans ce CRS.
- **Contrôle du CRS** : les centres de mailles reprojetés vers WGS84 diffèrent des latitudes et longitudes fournies par Météo-France de 50 m en médiane (70 m au 99e percentile, 74 m au maximum), soit moins de 1 % d'une maille. L'écart vient probablement de l'arrondi à 4 décimales et de la transformation de datum NTF → WGS84.
- **Mailles** : carrés de 8 km centrés sur les points de grille. Le pas observé est de 80 hm dans les deux directions ; c'est une approximation de la maille SAFRAN réelle.
- **Prédicat** : intersection de polygones. Poids = surface de l'intersection, normalisée par département.

| Contrôle | Valeur |
|---|---|
| Mailles SIM | 9 892 |
| Mailles intersectant au moins un département | 8 984. Les 908 autres sont toutes à plus de 4,2 km du territoire, en mer ou dans les pays voisins (longitude jusqu'à 10° E) |
| Lignes (maille, département) | 11 673 |
| Mailles sur 1 / 2 / 3 départements ou plus | 6 522 / 2 243 / 219 |
| Départements couverts | 96 / 96 |
| Part de la surface départementale couverte | minimum 0,9942 (Haute-Corse), médiane 1,0000 |
| Mailles par département | de 7 (Paris) à 203 |
| Somme des poids par département | 1,000000 |
| Géométries invalides | 0 |

## 3. Indicateurs quotidiens, puis mensuels, par maille

Tout est calculé **au niveau maille-jour**, puis agrégé, ce qui préserve les non-linéarités.

- **Degrés-jours au-dessus de *b*** (*b* = 0, 28 à 34 °C) : double sinus (`src/atlas/degree_days.py`) avec Tmin(J) = `TINF_H`(J), Tmax(J) = `TSUP_H`(J), Tmin(J+1) = `TINF_H`(J+1). Le 31 décembre utilise le 1er janvier du fichier suivant.
  - Validation : formule fermée de Baskerville & Emin (1969), testée contre une intégration numérique indépendante (écart < 10⁻⁴), plus des cas limites et la monotonie.
- **Jours chauds** : nombre de jours avec `TSUP_H` > 30 °C et > 32 °C.
- **Eau** :
  - précipitations (`PRELIQ` + `PRENEI`), ETP ;
  - SWI moyen ;
  - jours avec SWI < 0,4, et déficit cumulé Σ max(0 ; 0,4 − SWI).
  
  Le seuil de 0,4 est **une convention pré-spécifiée**. Il fait écho au seuil de 40 % d'eau extractible utilisé pour le blé par Laurent et al. (2025), mais le SWI de SIM porte sur la colonne de sol et ne coïncide pas exactement avec cette eau extractible. Ce n'est pas un seuil agronomique validé.
- **Mois incomplets** : le masquage se fait **par variable**. Seul décembre 2025 est concerné (degrés-jours du 31/12 sans Tmin du 01/01/2026) ; il n'entre dans aucune fenêtre des récoltes 2010-2025.

## 4. Fenêtres de l'année de récolte *t* (pré-spécifiées en phase 0)

| Fenêtre | Mois |
|---|---|
| automne | septembre à novembre de *t*−1 |
| hiver | décembre de *t*−1, janvier et février de *t* |
| printemps | mars et avril |
| remplissage | mai et juin |

Les sommes sont additionnées sur les mois. Les moyennes sont pondérées par le nombre de jours de chaque mois. Une fenêtre dont un mois manque est manquante.

La table mensuelle est conservée : elle permet de tronquer à la date de prévision (31 mai ou 30 juin) sans recalcul.

## 5. Confrontation à une référence publiée

Référence : indicateur thermique national de Météo-France (moyenne de 30 stations), 10 années les plus chaudes depuis 1900, d'après le *Bilan climatique 2025* (https://meteofrance.fr/sites/meteofrance.fr/files/files/editorial/bilan_climatique_2025-V3.4-web.pdf).

L'extraction PDF du graphique mélange l'ordre des étiquettes. L'attribution des valeurs suit le texte, qui indique : « 2025 […] derrière les années 2022, 2023 et 2020, devant 2024 ».

| Année | SIM (moyenne surfacique, °C) | Indicateur thermique national (°C) | Écart |
|---|---|---|---|
| 2022 | 12,65 | 14,5 | −1,85 |
| 2023 | 12,42 | 14,4 | −1,98 |
| 2020 | 12,27 | 14,1 | −1,83 |
| 2025 | 12,16 | 14,0 | −1,84 |
| 2018 | 12,00 | 13,9 | −1,90 |
| 2024 | 12,00 | 13,9 | −1,90 |
| 2014 | 11,80 | 13,8 | −2,00 |
| 2019 | 11,76 | 13,7 | −1,94 |
| 2011 | 11,79 | 13,6 | −1,81 |
| 2015 | 11,69 | 13,5 | −1,81 |

- Corrélation de Pearson : **0,977**.
- Écart moyen : −1,89 °C, avec un écart-type de seulement 0,069 °C.
- Le décalage de niveau est attendu : la moyenne surfacique inclut le relief, alors que les 30 stations sont surtout en plaine.
- Le classement est identique, à des quasi-égalités près (≤ 0,05 °C).

Ce contrôle valide la **cohérence interannuelle** de la chaîne, pas la justesse des extrêmes locaux.

## 6. Comptage de l'exposition et règle de repli

Règle fixée **avant** le calcul (`docs/decisions.md`) : N_eff = 1/Σ *s_t*², où *s_t* est la part de l'année *t* dans la variance résiduelle de `dd_32_remplissage` après effets fixes département et année. Si N_eff < 4, le seuil passe à 30 °C.

Population : 85 départements × 16 récoltes = 1 360. Pondération : **surfacique** (le masque blé est en attente, § 7).

**N_eff selon le seuil** (mai-juin) :

| Seuil | 28 | 29 | 30 | 31 | 32 | 33 | 34 |
|---|---|---|---|---|---|---|---|
| N_eff | 5,19 | 4,98 | 4,95 | 4,87 | **4,42** | 3,58 | 2,75 |

**Résultat de la règle : N_eff(32) = 4,42 ≥ 4, le seuil de 32 °C est conservé.**

### Années contributives à 32 °C

| Année | Départements exposés (> 0,5 °C·jour) | Moyenne (°C·jour) | Maximum (°C·jour) | Part de la variance résiduelle |
|---|---|---|---|---|
| 2019 | 57 | 1,40 | 7,4 | 0,377 |
| 2025 (provisoire) | 51 | 1,18 | 5,0 | 0,254 |
| 2022 | 51 | 1,00 | 3,4 | 0,116 |
| 2011 | 33 | 0,50 | 1,8 | 0,045 |
| 2017 | 34 | 0,55 | 1,8 | 0,022 |
| 12 autres années | 0 à 14 | ≤ 0,19 | ≤ 1,2 | ≤ 0,019 chacune |

### Points de vigilance (observés, non interprétés)

1. **Concentration.** Trois années (2019, 2025, 2022) portent 75 % de la variance résiduelle utile à l'identification.
2. **Dépendance à une année provisoire.** Sans 2025, N_eff(32) = **2,89**, sous le seuil de 4 ; N_eff(30) = 4,24. La règle reste appliquée telle qu'elle a été fixée. Mais l'analyse de robustesse « sans 2025 » à 32 °C sera fragile, et il faudra le dire.
3. **Faiblesse des niveaux.** Exposition maximale de 7,4 °C·jour au-delà de 32 °C (pondération surfacique ; 8,9 avec le masque blé). Écart-type résiduel : 0,49 °C·jour à 32 °C, 1,00 °C·jour à 30 °C. C'est cohérent avec Gammans et al. (2017) (« little exposure above 34 °C ») et probablement accentué par le lissage d'une réanalyse à 8 km (hypothèse non vérifiée).
4. **Effet minimal détectable** (informatif). σ résiduel du log-rendement, après les seuls effets fixes : 0,1035. MDE₈₀ à 32 °C ≈ 1,6 % de rendement par °C·jour, soit environ 2,3 % pour une exposition de 1,4 °C·jour (moyenne de 2019). À 30 °C : 0,8 % par °C·jour. **C'est une borne basse**, car la corrélation spatiale des erreurs n'est pas prise en compte.

## 7. Masque blé (RPG 2015-2017) : pondération de la spécification principale

**Construction :**

- parcelles `BTH` rattachées par leur centroïde à une maille SIM (arithmétique sur la grille) et à un département (test point-dans-polygone) ;
- surface moyenne 2015-2017 (une maille absente un millésime compte pour 0), normalisée par département ;
- 95 départements ont du blé (Paris en est exclu).

**Pertes de rattachement :** 1 ha hors département et 391 à 571 ha hors grille par millésime, pour 4,9 à 5,1 Mha.

**Validation :** voir `docs/sources.md`, § 4. RPG/SAA = 0,994 à 0,996 au niveau national ; corrélation départementale 0,9999.

**Comparaison avec la pondération surfacique** (85 départements, 2010-2025) :

| Variable | Corrélation des niveaux | Corrélation des résidus (effets fixes département et année) |
|---|---|---|
| `dd_32_remplissage` | 0,977 | 0,962 |
| `dd_0_remplissage` | 0,821 | 0,984 |
| `swi_remplissage` | 0,964 | 0,976 |
| `prec_printemps` | 0,962 | 0,957 |

Les niveaux diffèrent (le blé est en plaine : +36 °C·jour de degrés-jours au-dessus de 0 °C en mai-juin), mais une fois les effets fixes retirés, les deux pondérations sont très proches. Ce résultat est cohérent avec Ben-Ari et al. (2018) et confirme que le masque n'est pas une contribution en soi.

**Règle de repli avec le masque blé** (pondération de référence) :

| Seuil | 28 | 29 | 30 | 31 | 32 | 33 | 34 |
|---|---|---|---|---|---|---|---|
| N_eff | 5,23 | 4,93 | 4,79 | 4,62 | **4,13** | 3,33 | 2,53 |

**N_eff(32) = 4,13 ≥ 4 → seuil de 32 °C conservé**, même verdict qu'avec la pondération surfacique.

- Sans 2025 : 2,64 à 32 °C, 4,10 à 30 °C.
- Parts de la variance résiduelle à 32 °C : 2019 = 0,39 ; 2025 = 0,27 ; 2022 = 0,10.
- MDE₈₀ (informatif, borne basse) : 1,45 % par °C·jour à 32 °C.

## 8. Période longue 1990-2025 (robustesse, masque blé)

Les rendements Schauberger RAW (1990-2009) sont compatibles avec la SAA (`docs/decisions.md`).

| Seuil | N_eff 1990-2025 | Sans 2025 | Principales années (part de la variance résiduelle) |
|---|---|---|---|
| 32 °C | **5,43** | **4,11** | 2019 = 0,30 ; 2025 = 0,22 ; 2003 = 0,20 ; 2022 = 0,09 |
| 30 °C | 6,66 | 5,59 | 2003 = 0,25 ; 2025 = 0,24 ; 2019 = 0,16 ; 2022 = 0,08 |

**Conséquences :**

- L'allongement ajoute surtout **2003** comme année d'identification.
- Il rend viable une robustesse « sans 2025 » à 32 °C (4,11 contre 2,64 sur 2010-2025).
- Il reste une **robustesse**, et ses limites sont à reconnaître :
  - les années 1990-2009 ne sont pas recalées sur le RA 2020 ;
  - le masque blé 2015-2017 est appliqué à des années plus anciennes ;
  - la tendance des rendements plafonne depuis le milieu des années 1990 (Gouache et al. 2015).
