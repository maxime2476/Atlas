# ATLAS — Dictionnaire des variables des panels blé et maïs

Fichiers :

- `data/processed/panel_ble.parquet` : 85 départements × récoltes 2010-2025 = 1 360 lignes (spécification principale) ;
- `data/processed/panel_ble_long.parquet` : 85 × 1990-2025 = 3 060 lignes (robustesse) ;
- `data/processed/panel_ble_1959.parquet` : 85 × 1959-2025 = 5 695 lignes (Q2, phase 4 bis) : voir § 4 ;
- `data/processed/panel_mais_long.parquet` et `panel_mais.parquet` : panels maïs (Q1 et phase 6) : voir § 5.

Les trois fichiers blé ont **les mêmes colonnes** (99). Seul écart de type : `production_q` est un entier dans le panel principal et un réel dans le panel long, à cause des valeurs manquantes avant 2010. Ils sont construits par `scripts/09_build_panel.py`.

**Clé :** (`dep_code`, `annee`), unique, panel équilibré.

**Population :** départements métropolitains dont la surface moyenne 2010-2012 de blé tendre d'hiver (SAA) est d'au moins 1 000 ha. Dix départements de la SAA sont exclus : 06, 13, 2A, 2B, 34, 66, 83, 92, 93, 94. Paris (75) est absent de la SAA.

**Échantillon principal :** `echantillon_principal = True`, soit les 83 départements en statut qualité 1. Belfort (90) et l'Essonne (91), en statut 2, ne servent qu'à la robustesse.

**Remarque sur la période de référence :** la surface 2010-2012 appartient aux trois premières années de la période d'estimation, et non à une période extérieure comme l'écrivait le cadrage (`phase0_cadrage.md`, § 3.4). Elle reste fixe par département, ce qui suffit à empêcher qu'une surface annuelle dépendant de la météo serve de poids ou de critère de sélection.

## 1. Identifiants et rendement

| Colonne | Type | Unité | Définition / source |
|---|---|---|---|
| `dep_code` | texte | — | Code INSEE du département (« 01 », « 2A ») |
| `dep_libelle` | texte | — | Nom du département (SAA) |
| `reg_libelle` | texte | — | Région (« code - nom », SAA, régions 2016) |
| `annee` | entier | — | Année de **récolte** *t* |
| `rendement_q_ha` | réel | q/ha (1 q = 100 kg) | Rendement du blé tendre d'hiver et de l'épeautre (SAA code 01). Dans le panel long, avant 2010 : Schauberger et al. (2022) RAW, converti de t/ha en q/ha. **Arrondi** : 86,6 % des valeurs 2010-2025 sont des entiers (25 départements sur 85 n'ont que des entiers), et 95,6 % sur 1990-2009. L'erreur d'arrondi est d'au plus ±0,5 q/ha, soit environ 1 % du log-rendement : c'est une erreur sur la variable expliquée, qui réduit la puissance sans biaiser |
| `log_rendement` | réel | log(q/ha) | ln(`rendement_q_ha`) : **variable expliquée** |
| `source_rendement` | texte | — | `SAA` (2010-2025) ou `Schauberger_RAW` (1990-2009 dans le panel long ; 1959-2009 dans le panel 1959) |
| `provisoire` | booléen | — | Vrai pour 2025 (SAA provisoire, données arrêtées au 30/03/2026) |
| `statut_qualite` | texte | — | Statut qualité SAA (seuls 1 et 2 sont observés dans la population), qui ne vaut **que pour la dernière année publiée** ; vide avant 2010 |
| `echantillon_principal` | booléen | — | Vrai si le département est en statut 1 (83 départements) : échantillon de la spécification principale |
| `surface_ha` | réel | ha | Surface de l'année (SAA). **Non utilisée comme contrôle** : elle dépend de la météo d'automne (mauvais contrôle). Vide avant 2010 |
| `production_q` | entier | q | Production de l'année (SAA), ≈ surface × rendement. Vide avant 2010 |
| `lat_centroide`, `lon_centroide` | réel | degrés (WGS84) | Centroïde du département (ADMIN EXPRESS 2026, calculé en Lambert 93) ; sert aux distances des erreurs de Conley |
| `surface_ref_ha` | réel | ha | Surface moyenne 2010-2012 (SAA), **fixe** par département : critère de population et poids de régression |

## 2. Variables météo

**Origine et construction :**

- source : SIM2 quotidienne (Météo-France), mailles de 8 km ;
- pondération par le **masque blé** RPG 2015-2017 (parcelles BTH, moyenne des trois millésimes) ;
- calcul au niveau maille-jour, agrégation mensuelle, puis par fenêtre (`src/atlas/weather.py`) ;
- nom des colonnes : `<variable>_<fenêtre>`.

**Fenêtres** (année de récolte *t*) :

| Suffixe | Mois |
|---|---|
| `_automne` | septembre à novembre de *t*−1 (61 + 30 = 91 jours) |
| `_hiver` | décembre de *t*−1, janvier et février de *t* (90 ou 91 jours) |
| `_printemps` | mars et avril de *t* (61 jours) |
| `_remplissage` | mai et juin de *t* (61 jours) |

| Préfixe | Agrégation | Unité | Définition |
|---|---|---|---|
| `dd_<b>` (*b* = 0, 28 à 34) | somme | °C·jour | Degrés-jours au-dessus de *b* °C, double sinus entre `TINF_H`(J), `TSUP_H`(J) et `TINF_H`(J+1) (`docs/notes_methodologiques.md`). `dd_32` est l'exposition extrême de référence |
| `gdd_0_32`, `gdd_0_30` | somme | °C·jour | Degrés-jours de croissance entre 0 et 32 °C (ou 30 °C) : `dd_0` − `dd_32` (ou − `dd_30`) |
| `hot_30`, `hot_32` | somme | jours | Nombre de jours avec `TSUP_H` > 30 °C (> 32 °C) |
| `prec` | somme | mm | Précipitations liquides et solides (`PRELIQ` + `PRENEI`) |
| `etp` | somme | mm | Évapotranspiration potentielle (Penman-Monteith FAO-56) |
| `swi` | moyenne pondérée par les jours | sans dimension | Soil Wetness Index (≈ 0 au point de flétrissement, ≈ 1 à la capacité au champ) ; la notice indique « % » à tort (`docs/sources.md`) |
| `swi_dry` | somme | jours | Nombre de jours avec SWI < 0,4 (seuil conventionnel pré-spécifié) |
| `swi_deficit` | somme | indice·jour | Σ max(0 ; 0,4 − SWI) |
| `wg_racine` | moyenne | m³/m³ | Contenu en eau liquide de la couche racinaire, à 06 UTC |
| `tmin`, `tmax`, `tmean` | moyenne | °C | `TINF_H`, `TSUP_H`, `T` |

**Variantes de pondération** (non incluses dans le panel, à joindre par (`dep_code`, `annee`)) :

- `data/processed/weather_dep_harvest_area.parquet` (2010-2025) : pondération par la surface ;
- `weather_dep_harvest_wheat_1990.parquet` : masque blé sur 1990-2025 (identique au panel long).

## 3. Règles d'usage

- **Spécification principale :** `log_rendement` ~ effets fixes département et année + `gdd_0_32_<f>` + `dd_32_<f>` + eau. Poids `surface_ref_ha`. Seuil de 32 °C confirmé par la règle de repli (`docs/decisions.md`).
- **Ne jamais utiliser comme régresseur** `surface_ha` ni `production_q` (réponses à la météo ; la production est dérivée du rendement), ni `statut_qualite`, `echantillon_principal` ou `provisoire` (constants par département ou par année, donc absorbés par les effets fixes).
- **Colinéarité mécanique** : `gdd_0_32_<f>` et `dd_0_<f>` sont quasi identiques (r ≈ 1,000) ; `tmean_<f>` leur est très corrélé (r de 0,983 à 0,998 selon la fenêtre ; correction du 2026-10-12, la version précédente indiquait r ≥ 0,998 pour les trois). Un seul des trois dans un même modèle.
- **Pondération** : la spécification principale est pondérée par `surface_ref_ha`. Sans poids, le Vaucluse (84) et le Gard (30), environ 1 600 ha chacun, portent 17 % et 12 % de la variance résiduelle de `dd_32_remplissage`. La régression non pondérée n'est donc qu'une robustesse, à accompagner d'une variante sans 84, 30 et 48.
- **Variables d'eau :** un modèle avec `swi_*` donne un effet **partiel** de la chaleur (le SWI est en partie un médiateur). Rapporter aussi le modèle sans les variables d'eau.
- **2025** est provisoire : robustesse sans 2025.
- **Panel long :** 1990-2009 non recalé sur le RA 2020, et le masque blé 2015-2017 est appliqué à des années anciennes. Usage limité à la robustesse.


## 4. Panel blé 1959-2025 (`panel_ble_1959.parquet`, question Q2)

Construit par `scripts/09_build_panel.py`, avec les mêmes 99 colonnes et les mêmes définitions que les panels ci-dessus (§§ 1 à 3).

- **Lignes :** 85 départements × 67 récoltes (1959-2025) = 5 695 lignes ; clé (`dep_code`, `annee`) unique.
- **Rendement :** `Schauberger_RAW` sur 1959-2009 (4 335 lignes), `SAA` sur 2010-2025 (1 360 lignes). 27 rendements manquent, tous entre 1959 et 1967, dont 18 dans l'échantillon principal ; ils ne sont pas imputés.
- **Colonnes SAA vides avant 2010 :** `statut_qualite`, `surface_ha` et `production_q` (4 335 valeurs manquantes chacune).
- **Météo :** `data/processed/weather_dep_harvest_wheat_1959.parquet`, masque blé 2015-2017 appliqué à toute la période (anachronique, voir `docs/phase2bis_donnees.md`). La fenêtre d'automne de la récolte 1959 utilise septembre-novembre 1958, couverts par SIM depuis le 1er août 1958.
- **Effets fixes de période de source :** ils ne sont pas stockés dans le panel. `R/15_q2_wheat.R` construit le facteur département × période (1959-1988, 1989-2009, 2010-2025).

## 5. Panels maïs

### 5.1 `panel_mais_long.parquet` (question Q1, phase 4 bis)

Construit par `scripts/22_build_panel_mais.py`. **Format long :** une ligne par département × année × modalité. **Clé :** (`dep_code`, `annee`, `modalite`), unique. 1 969 lignes, 38 départements, 2000-2025. Le panel n'est pas équilibré : 7 rendements manquants ou nuls ont été retirés (dont le Jura irrigué en 2016 et 2018). L'échantillon principal compte 17 départements et 435 paires irrigué / non irrigué.

**Population :** départements dont les surfaces moyennes 2010-2012 de maïs grain irrigué **et** non irrigué (SAA) atteignent chacune 1 000 ha (38 départements).

| Colonne | Type | Unité | Définition / source |
|---|---|---|---|
| `dep_code` | texte | — | Code INSEE du département |
| `annee` | entier | — | Année de récolte |
| `modalite` | texte | — | `irrigue` (SAA code 14, « Maïs grain irrigué ») ou `non_irrigue` (code 15) |
| `rendement_q_ha` | réel | q/ha | Rendement de la modalité |
| `log_rendement` | réel | log(q/ha) | ln(`rendement_q_ha`). La variable expliquée de A1, l'écart log irrigué − non irrigué, est calculée dans `R/14_q1_maize.R` |
| `surface_ha` | réel | ha | Surface de la modalité, l'année considérée. **Ne pas utiliser comme régresseur** (elle répond aux conditions de l'année) |
| `source` | texte | — | `SAA_ancienne_serie` (2000-2009, `FDS_DEVELOPPE_2`, non recalée sur le RA 2020) ou `SAA_series_longues` (2010-2025) |
| `surface_ref_ha` | réel | ha | Surface moyenne 2010-2012 de maïs grain, irrigué + non irrigué, **fixe** par département : poids de régression |
| `statut_irrigue` | texte | — | Statut qualité SAA du maïs grain irrigué (code 14) publié en 2025, appliqué à toute la période |
| `echantillon_principal` | booléen | — | Vrai si `statut_irrigue` vaut 1 (17 départements) |
| `lat_centroide`, `lon_centroide` | réel | degrés (WGS84) | Centroïde du département, comme pour le blé |

**Météo** (`<variable>_<fenêtre>[_surf]`), mêmes définitions qu'au § 2 :

- variables : `dd_32`, `dd_30`, `gdd_0_32` (= `dd_0` − `dd_32`), `swi`, `prec`, `etp`, `hot_30` ;
- fenêtres de l'année de récolte : `_ja` (juillet et août, 62 jours) et `_juillet` (juillet, 31 jours) ;
- pondération sans suffixe : **masque maïs** RPG 2015-2017 (parcelles `MIS`, `weather_dep_month_maize.parquet`), mesure principale ;
- suffixe `_surf` : pondération par la **surface du département** (`weather_dep_month_area.parquet`), robustesse ;
- les deux modalités d'un même département et d'une même année reçoivent la même météo : le masque ne distingue pas les parcelles irriguées.

**Restrictions d'eau** (`scripts/23_vigieau_indicators.py`, juillet-août), vides avant 2012 (907 lignes) :

| Colonne | Type | Unité | Définition |
|---|---|---|---|
| `jours_vigilance_plus_ja` | réel | jours (0 à 62) | Jours de juillet-août où au moins un arrêté du département est au niveau vigilance ou plus |
| `jours_ar_plus_ja` | réel | jours | Idem, niveau alerte renforcée ou crise |
| `jours_crise_ja` | réel | jours | Idem, niveau crise : variable de H3 |
| `part_arretes_sans_niveau` | réel | proportion | Part des arrêtés de l'année sans niveau de gravité (non comptés, d'où une sous-estimation des jours avant 2016) |
| `periode_principale` | booléen, stocké en `object` | — | Vrai pour 2016-2025, période principale de H3 ; vide avant 2012, en raison de la jointure |

Le niveau d'un département un jour donné est le plus sévère des arrêtés en vigueur, toutes zones confondues (« au moins une zone du département »).

### 5.2 `panel_mais.parquet` (phase 6, exploratoire)

Construit par `scripts/16_phase6_build.py`. **Format large :** une ligne par département × année, 2010-2025, 606 lignes (38 départements). Les colonnes `rdt_irrigue`, `rdt_non_irrigue` (q/ha), `surf_irrigue` et `surf_non_irrigue` (ha) donnent les deux modalités ; `ecart_log` = ln(`rdt_irrigue`) − ln(`rdt_non_irrigue`). La météo (`dd_32_ja`, `swi_ja`, `prec_ja`) est **pondérée par la surface du département**, sans masque maïs : c'est la différence principale avec le panel de Q1. Les autres colonnes ont la même définition qu'au § 5.1.
