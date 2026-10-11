# ATLAS — Phase 2 bis : données du recentrage maïs et de la série blé longue

*2026-10-11. Construction des données uniquement, **sans estimation**. Cadrage : `docs/phase0bis_cadrage.md`.*

## 1. Chaîne et contrôles

| Étape | Script | Sortie | Contrôle |
|---|---|---|---|
| Météo 1958-2025 | `05_build_weather_monthly.py` (années étendues) | `data/interim/weather_cell_month.parquet` (7,27 M lignes) | 1958 : août à décembre (début de SIM) ; aucun mois incomplet hors décembre 2025 |
| Masque blé (BTH) | `07_build_wheat_mask.py` | `weights_cell_dep_wheat.parquet` | **Identique** au masque des phases 2-6 (9 471 lignes, écart maximal des poids nul) |
| Masque maïs (MIS) | `07_build_wheat_mask.py --culture MIS` | `weights_cell_dep_maize.parquet`, `weather_dep_month_maize.parquet` | 1,53 à 1,79 Mha selon le millésime ; corrélation départementale avec la SAA **maïs grain** de 0,993 (avec le fourrage : 0,04) |
| Restrictions d'eau | `23_vigieau_indicators.py` | `vigieau_dep_ete.parquet` (100 départements × 2012-2025) | Voir § 3 |
| Fenêtres du blé 1959-2025 | `06_exposure_check.py --weights wheat --first-year 1959` | `weather_dep_harvest_wheat_1959.parquet` | 85 départements × 67 récoltes |
| Panel blé 1959-2025 | `09_build_panel.py` | `panel_ble_1959.parquet` (5 695 lignes) | 1990-2025 identique à `panel_ble_long` ; 27 rendements manquants (1959-1967), non imputés |
| Panel maïs 2000-2025 | `22_build_panel_mais.py` | `panel_mais_long.parquet` (format long : département × année × modalité) | Voir § 2 |

Tests : `tests/test_phase2bis.py`.

## 2. Panel maïs irrigué et non irrigué 2000-2025

| Étape | Lignes avant | Lignes après |
|---|---|---|
| Rendements 2000-2025, deux modalités → population (38 départements) | 5 020 | 1 976 |
| Retrait des rendements manquants ou nuls | 1 976 | 1 969 |
| Jointure météo (maïs et surface), VigiEau, centroïdes | 1 969 | 1 969 |

- **Observations retirées :** 03 en 2004-2006 (non irrigué) ; 58 et 89 en 2007 (irrigué) ; 39 en 2016 et 2018 (irrigué).
- **Effectifs :** 981 département-années avec les deux modalités ; 38 départements, dont 17 en statut qualité 1 (statut de 2025, appliqué à toute la période).
- **Sources :** 2000-2009, SAA « anciennes séries » ; 2010-2025, séries longues. Le raccord a été validé en phase 0 bis (94-95 % de paires identiques sur 2010-2020).

**Exposition à la chaleur extrême (`dd_32_ja`, masque maïs, maïs non irrigué) :**

| Échantillon | Période | N_eff | Écart-type résiduel | Principales années |
|---|---|---|---|---|
| Principal (17) | 2010-2025 | 6,40 | 1,33 | 2023, 2015, 2025, 2022 |
| Principal (17) | 2000-2025 | **7,11** | 1,34 | **2003**, 2023, 2015, 2025 |
| Tous statuts (38) | 2000-2025 | 7,52 | 1,50 | 2003, 2022, 2023, 2025 |

Avec le masque maïs, l'exposition résiduelle est plus forte qu'avec la pondération surfacique de la phase 6 (1,33 contre 1,00) : le maïs grain est concentré dans les zones chaudes.

## 3. Restrictions d'eau (VigiEau)

- **Source :** fichier global `arretes.csv` (12 823 arrêtés, de 2010 à 2026).
- **Indicateurs :** nombre de jours de juillet-août où au moins une zone du département est à un niveau donné. On distingue « au moins vigilance », « au moins alerte renforcée » et « crise ».
- **Qualité :** le niveau de gravité manque pour 99,6-100 % des arrêtés en 2010-2011 (années exclues), 13-21 % en 2012-2015, 5-11 % en 2016-2022 et ≤ 1 % depuis 2023.
- **Conséquence :** H3 est étudiée en principal sur 2016-2025 (`periode_principale`), avec 2012-2025 en robustesse.
- **Moyenne nationale des jours de crise en juillet-août :** 32,0 en 2022 ; 21,2 en 2023 ; 19,3 en 2019 et en 2025 ; 3,1 en 2013-2014.

## 4. Série blé 1959-2025

- **Population :** 85 départements × 67 récoltes = 5 695 lignes.
- **Rendements :** Schauberger RAW (1959-2009) et SAA (2010-2025).
- **Exposition :** N_eff(32 °C, mai-juin) = **6,17**, contre 4,13 sur 2010-2025 et 5,43 sur 1990-2025.
- **Limites :** 27 rendements manquants avant 1968 ; ruptures de source en 1989 et 2010 ; masque blé 2015-2017 appliqué à 1959 (anachronique).

## 5. Fichiers dérivés supprimés

Les couches RPG extraites (`data/interim/rpg/`, environ 13 Go) ont été supprimées après usage. Elles se régénèrent depuis les archives (`data/raw/ign_rpg/README.md`).
