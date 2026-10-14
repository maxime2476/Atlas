# Analyses complémentaires : résultats

Déclarées avant calcul dans `docs/decisions.md` (« Analyses complémentaires ») ; **non pré-spécifiées, exploratoires**. Aucune ne change le statut des hypothèses de la phase 4 bis. Scripts : `scripts/28_complements_python.py`, `scripts/29_eolien.py`, `R/22_q1_complements.R` ; tables : `reports/tables/phase7_*.csv` (le préfixe `phase7_` désigne ce lot d'analyses, pas une phase du plan initial).

Modèle de base : A1 (écart log irrigué − non irrigué ~ `dd_32_ja` + `swi_ja` | département + année, poids `surface_ref_ha`, 17 départements, 435 paires, β = 0,0158).

## Variables retenues et corrélations

Seules des variables complètes sur la période et l'échantillon ont été retenues : part irriguée du maïs grain (SAA, 2010-2012), maïs fourrage (SAA, feuille FOU, 2010-2025) et puissance éolienne terrestre (registre RTE / ODRÉ). Corrélations entre les 17 départements (`phase7_correlations_variables.csv`) :

| | Part irriguée | Écart d'altitude | Relief | Éolien 2025 |
|---|---|---|---|---|
| Part irriguée | 1 | −0,21 | −0,23 | 0,41 |
| Écart d'altitude (surface − masque) | | 1 | **0,86** | −0,35 |
| Relief (6 départements) | | | 1 | −0,31 |

L'écart d'altitude et l'indicatrice de relief dépassent le seuil déclaré de 0,7 : ils ne sont jamais mis dans le même modèle.

## Hétérogénéité de la pente

| Analyse | Estimation | p WCR bilatérale | Lecture |
|---|---|---|---|
| G1 : chaleur × relief | +0,0087 | 0,78 | **Différence non détectée** |
| G1 : pente hors relief (11 départements) | +0,0103 | 0,25 | — |
| G5 : chaleur × part irriguée (centrée) | −0,0212 par unité de part | 0,42 | Non détectée |

- **G1 répond à la question laissée ouverte par E2 :** sans les six départements de relief, l'estimation (1,0 %) n'est pas significative, mais la pente des deux groupes ne diffère pas de façon détectable. La perte de significativité est donc compatible avec une simple perte d'information (11 départements), pas nécessairement avec une pente plus faible hors relief.
- **G6, pentes départementales rétrécies (empirique bayésien, DerSimonian-Laird) :** moyenne 0,0163 ; écart-type entre départements τ = 0,0045 ; test Q d'homogénéité p = 0,20 (erreurs-types hétéroscédastiques, qui ignorent la dépendance entre départements une même année : le test est donc plutôt trop permissif). Les pentes rétrécies vont de 0,012 (Indre) à 0,021 (Isère). Elles sont corrélées à −0,44 avec la part irriguée et à +0,42 avec l'écart d'altitude (17 points, descriptif).
- **G7, forêt causale (`grf` 2.6.1, 4 000 arbres, grappes = années) :** test de calibration, coefficient de la prédiction différentielle −0,88 (p = 0,99) : **aucune hétérogénéité détectée**. L'effet partiel moyen estimé par la forêt (−0,0015, erreur-type 0,023) est très imprécis : avec 435 observations et une variable continue, la forêt n'apporte pas d'information utile. Elle est rapportée comme résultat négatif sur la méthode.

## Menaces sur la mesure du rendement

- **G2, ensilage (2010-2025, 270 paires) :** la part du maïs non irrigué récolté en fourrage (27,7 % en moyenne pondérée) ne varie pas avec la chaleur : +0,0005 par °C·jour, p unilatérale = 0,43. **Passage grain → ensilage non détecté** au niveau départemental. Ce n'est pas une preuve d'absence : les surfaces de fourrage peuvent être déclarées avant la récolte, et 2003 est hors de la période.

## Inférence sur H1

| Méthode | p unilatérale | Remarque |
|---|---|---|
| WCR par année (référence, règle de décision) | 0,007 | — |
| G9a : jackknife par année (CV3), t à 25 ddl | **0,074** | Recommandé par MacKinnon, Nielsen et Webb (2023) avec peu de grappes ; taille mesurée ensuite (V1) : 7,3 %, donc pas plus conservateur que le WCR sur ces données |
| G9b : randomisation (5 000 dérangements des années, statistique β̂) | 0,001 | L'effet réel éventuel reste dans l'erreur du placebo |
| G8 : DML (forêts aléatoires sur SWI, P, ETP, GDD ; 5 plis par blocs d'années) + WCR | 0,016 (β = 0,0155) | Contrôles météo non linéaires : β inchangé |

**Lecture :** le statut de H1 reste fixé par le WCR (règle de la phase 4 bis). Mais la significativité au seuil de 5 % **dépend de la méthode d'inférence** : le jackknife par grappes donne p = 0,074, et sa taille (7,3 %, V1) montre qu'il n'est pas plus conservateur sur ces données. C'est une réserve à citer.

## Taille et levier (relecture W4, W5, W8)

| Diagnostic (R = 300) | Taux de rejet à 5 % |
|---|---|
| G3a : H1, placebo intra-année (chaleur permutée entre départements chaque année) | 3,7 % |
| G4 : H2b (non irrigué), dérangement des années | 4,0 % |
| G4 : H2c (irrigué), dérangement des années | 2,3 % |
| Rappel : H1, dérangement (R/14, rejoué à l'identique) | 3,7 % |
| G9c : matrices de Conley corrigées par fixest dans ces placebos | 24 % des répétitions |

- G3a ≤ 10 % : selon la règle déclarée, **la règle de décision est confortée**. G4 : les tailles de H2b et H2c sont proches du nominal ; leurs p-valeurs peuvent être lues normalement.
- G3b : selon l'année qui reçoit le champ de 2003, le taux de rejet varie de 0 à 15 %, sur 4 à 19 permutations par année : pas d'année anormale (`phase7_placebo_par_annee_2003.csv`).
- G3c, levier partiel dans le modèle A1 pondéré : 2003 porte **41 %** de Σ w x̃² sur 2000-2025 (N_eff = 4,8) et **80 %** sur 2000-2009 (N_eff = 1,5). La réplication 2000-2009 repose donc presque entièrement sur un seul été. Ces chiffres diffèrent de ceux du chapitre 4 (26 % et N_eff = 7,1), calculés sur la variance résiduelle non pondérée, sans le SWI.

## Éolien (G10)

| Rendement | Effet de 1 MW pour 10 000 ha de SAU | p WCR bilatérale |
|---|---|---|
| Maïs irrigué (2000-2025) | −0,59 % | 0,026 |
| Maïs non irrigué | −0,80 % | 0,28 |
| Écart | +0,22 % | 0,70 |
| Blé (2010-2025) | +0,12 % | 0,39 |

Aucune association positive du type de Kaffine (2019) n'apparaît. La seule p < 0,05 (maïs irrigué, de signe négatif) ne survit pas à une correction de Holm sur les quatre tests (p ≈ 0,10), et la croissance de l'éolien suit des tendances départementales que les effets fixes n'absorbent pas. **Pas intéressant pour la suite du projet** : le registre ne recense que les installations en service en 2026, et l'échelle départementale est trop grossière pour un effet de microclimat local.

## Prévision (G12)

- **Intervalles conformes à origine glissante (90 %, années 2018-2025) :** couverture empirique de 95 à 100 % selon le modèle, soit **trop large**. Le quantile est dominé par 2016, année de perte exceptionnelle (écart médian absolu à B0 de 0,23 en log, contre 0,03 à 0,15 les autres années). La méthode est simple et honnête, mais sur 10 années elle n'apporte pas d'intervalle calibré.
- **Modèles corrigeant B0 au lieu de B1 (variante 2010, exploratoire, années test déjà vues) :**

| Date | Modèle | Gain sur B0 | IC 95 % de l'écart de MSE | Années meilleures |
|---|---|---|---|---|
| 1er juin | Ridge | −9 % | [−0,0044 ; +0,0082] | 5/10 |
| 1er juin | Forêt aléatoire | +16 % | [−0,0086 ; −0,0001] | 8/10 |
| 1er juin | Gradient boosting | +11 % | [−0,0069 ; +0,0011] | 6/10 |
| 1er juillet | Ridge | −41 % | [−0,0044 ; +0,0278] | 4/10 |
| 1er juillet | Forêt aléatoire | +16 % | [−0,0083 ; −0,0009] | 8/10 |
| 1er juillet | Gradient boosting | +18 % | [−0,0093 ; −0,0001] | 6/10 |

**Lecture :** c'est le résultat le plus intéressant de ce lot pour la prévision. Construits sur B0, les modèles d'arbres font mieux que B0, avec un intervalle qui exclut zéro (forêt aux deux dates, boosting au 1er juillet). Mais cette variante a été choisie après avoir vu que B1 était faible, sur les mêmes années test. Elle doit être **confirmée sur les récoltes 2026 et suivantes**, avec ce protocole figé.

## Température de surface MODIS (G11)

Protocole fixé avant réception des données (`docs/decisions.md`). MOD11A2 v6.1, LST de jour, composites de 8 jours commençant entre le 1er juillet et le 31 août, masque maïs ; 2 413 département-années sur 2 418 (5 manquantes) ; 434 paires sur 435 dans l'échantillon principal. Table `reports/tables/phase7_lst.csv`.

| Analyse | Résultat |
|---|---|
| (a) Corrélation de la LST avec `dd_32_ja` | 0,63 (0,63 en intra-département) |
| (b) A1 avec la LST à la place des degrés-jours | +4,2 % d'écart par °C de LST (β = 0,0413), p unilatérale = 0,002 |
| (c) Pente de la LST sur `dd_32_ja` (38 départements), à part irriguée moyenne | 0,21 °C par degré-jour, p bilatérale = 0,001 |
| (c) Interaction avec la part irriguée (centrée) | −0,149, p bilatérale = 0,051 ; pente de 0,23 °C au premier quartile de la part irriguée, 0,19 au troisième |

**Lecture (descriptive) :** l'association tient avec une mesure satellitaire de la chaleur, indépendante de SAFRAN et d'E-OBS (mais prise vers 10 h 30 et sur ciel clair). La surface se réchauffe un peu moins par degré-jour d'air là où la part irriguée est forte, dans le sens d'un refroidissement par l'irrigation (Zhu et Burney 2022), sans que la différence soit significative au seuil de 5 % ; la part irriguée varie aussi avec d'autres caractéristiques des départements. **Intéressant :** oui pour la robustesse de la mesure ; le canal du refroidissement reste non établi.

## Tests T1-T3 : réplication, calendrier, variables instrumentales

Déclarés avant calcul (`docs/decisions.md`). Tables `reports/tables/phase7_t1_fourrage.csv`, `phase7_t2_calendrier.csv`, `phase7_t3_iv.csv`.

| Test | Résultat | Intéressant ? |
|---|---|---|
| T1 : même modèle sur le maïs fourrage irrigué / non irrigué (28 départements, 2010-2025, masque `MIE`) | +1,6 % par °C·jour, p = 0,006, taille 3,0 % : **se réplique** selon la règle déclarée | **Oui, fortement** : autre culture, autre récolte, autres statistiques, autre masque ; estimation presque identique au maïs grain |
| T2 : chaleur de l'été suivant (placebo pur) | p = 0,35 : pas d'alerte | Oui : écarte un facteur persistant |
| T2 : juin + juillet-août + septembre | juillet-août +1,3 % (p = 0,026) ; juin +4,7 % (p = 0,13), exposition faible ; septembre sans chaleur (0,04 degré-jour) | Partiellement : septembre n'est pas un test |
| T3 : IV par E-OBS | β = 0,0208, 1,3 fois les MCO, F = 65 | Oui : l'atténuation par l'erreur de mesure est d'environ un tiers ; correction plutôt trop faible (stations communes) |
| T3 : IV par la LST | β = 0,0386, 2,5 fois les MCO, F = 13 | Peu : exclusion douteuse (refroidissement par l'irrigation) |

## Tests N1-N3 : forme, extrêmes combinés, déficit de pression de vapeur ; test P

Déclarés avant calcul. Tables `reports/tables/phase7_n1_forme.csv`, `phase7_n1_2003.csv`, `phase7_n2_combines.csv`, `phase7_n3_vpd.csv` ; VPD construit par `scripts/34_vpd.py`.

| Test | Résultat | Intéressant ? |
|---|---|---|
| N1 : terme quadratique ; tranches 30-32, 32-34, > 34 °C | Courbure non détectée (p = 0,13) ; elle ne corrige pas 2003 ; tranches trop imprécises | Peu : les données ne disent pas où la réponse s'accentue |
| N2 : chaleur × humidité du sol | −0,109, p = 0,20 : signe attendu, non détecté | Peu : étés chauds et secs confondus |
| N3 : VPD à la place des degrés-jours | +60 % par kPa, p = 0,001 ; un écart-type : +17,5 % (contre +5,9 % pour les degrés-jours) | **Oui, fortement** |
| N3 : VPD et degrés-jours ensemble | VPD +64 % par kPa (p = 0,002) ; degrés-jours −0,2 % (p = 0,76) ; corrélation 0,76 | **Oui** : l'association porte sur la sécheresse de l'air plutôt que sur la chaleur seule (Lobell et al. 2013) ; non séparables selon la règle |
| P : spécification figée pour les récoltes 2026 et suivantes | `docs/specification_recoltes_futures.md` | À déposer sur OSF ou Zenodo pour un horodatage externe |

## Tests S1-S4 : VPD sur le fourrage, influence des années, corrélation sérielle, multivers

Déclarés avant calcul. Tables `reports/tables/phase7_s1_vpd_fourrage.csv` à `phase7_s4_multivers.csv` ; figure `memoire/figures/fig6_multivers.pdf`.

| Test | Résultat | Intéressant ? |
|---|---|---|
| S1 : VPD sur le maïs fourrage | Seul : p = 0,012 ; avec les degrés-jours, ni l'un ni l'autre significatif (p = 0,12 et 0,30) | Oui, comme limite : la lecture « air sec » n'est pas confirmée sur une seconde culture |
| S2 : retrait de chaque année | β de 0,0134 à 0,0243, significatif 26 fois sur 26 ; 2003 est l'année la plus influente (son retrait augmente β) | Oui : aucune année ne porte seule la significativité |
| S3 : corrélation sérielle simulée | Taille 6,3 %, 3,7 % et 9,3 % pour ρ = 0, 0,3 et 0,6 | Oui : la règle de décision tient, à la limite pour une forte autocorrélation |
| S4 : 76 spécifications (multivers) | Toutes positives, 68 significatives ; les 8 autres utilisent la pondération surfacique | **Oui** : seule la mesure de la chaleur compte vraiment |

## Réserve utile des sols et eau d'irrigation (R1, W1, W2)

Déclarés avant calcul. Données : RU INRAE à 90 m (Román Dobarco et al. 2019), volumes BNPE (Hub'Eau), RA2020_0052 (Agreste). Scripts `scripts/35_reserve_utile.py`, `scripts/36_volumes_irrigation.py`, `R/27_q1_sol_eau.R` ; tables `reports/tables/phase7_r1_*.csv`, `phase7_w1_*.csv`, `phase7_w2_*.csv`.

| Test | Résultat | Intéressant ? |
|---|---|---|
| R1 : chaleur × RU (17 départements, RU de 87 à 134 mm) | −0,00008 par mm, p = 0,65 ; avec la part irriguée, p = 0,53 ; 38 départements, p = 0,41 | Non : signe attendu mais rien de détecté, la RU varie peu entre ces départements |
| R1, variante VPD × RU | −0,0026 par mm et par kPa, p = 0,006 : pente du VPD de +66 % par kPa à 87 mm, +47 % à 134 mm | À confirmer : test secondaire, 17 valeurs de RU |
| W1 : log volume prélevé ~ chaleur (202 département-années, 2012-2023) | +0,4 % par degré-jour, p unilatérale = 0,28 ; VPD p = 0,11 ; SWI −1,60, p = 0,0007 | **Oui** : les volumes suivent la sécheresse du sol, pas la chaleur extrême |
| W2 : valeur apparente du m³ (01, 03, 18, 63, 67, 68) | Dose médiane 1 524 m³/ha ; 2,2 kg de grain et 0,55 € bruts par m³ (0,17 à 0,96 selon le département) ; 8 département-années sur 72 exclus par la règle de dose | Oui, comme ordre de grandeur : au-dessus de la marge de 0,20-0,28 €/m³ estimée par la DRAAF Occitanie sur 2012-2014 (Analyses & Études n° 3, 2017, hors amortissement du matériel ; la même étude donne 1 900 m³/ha et 1,4 kg de maïs par m³), ce qui est attendu pour une valeur brute |
| W2, étés chauds | Dose +74 m³/ha par degré-jour (p = 0,04) ; écart +0,36 q/ha (p = 0,86) | Non : le m³ supplémentaire des étés chauds n'est pas mesurable ainsi |

Lecture : la valeur par m³ est **descriptive**. L'écart de rendement observé mêle l'effet de l'eau et les différences entre parcelles irriguées et non irriguées ; la dose repose sur une clé de surface (part du maïs dans la surface irriguée en 2020), ce qui suppose que le maïs reçoit autant d'eau par hectare que les autres cultures irriguées du département ; s'il en reçoit plus, la dose est sous-estimée et la valeur par m³ surestimée. Elle ne compte ni l'énergie, ni le matériel, ni la main-d'œuvre.

## Projections DRIAS (D1)

Déclarées avant calcul. 17 simulations Explore2-Climat 2022 corrigées par ADAMONT (historique et RCP 8.5), 1 582 mailles du masque maïs des 17 départements ; scripts `scripts/37_drias_telechargement.py`, `scripts/38_drias_indicateurs.py` ; tables `reports/tables/phase7_d1_*.csv`. Moyennes des 17 départements pondérées comme A1 ; médiane des modèles [étendue].

| Horizon | Degrés-jours > 32 °C (juillet-août) | VPD (kPa) | Écart irrigué − non irrigué impliqué par β × Δ (IC 90 % de β) |
|---|---|---|---|
| 1976-2005 (modèles ; SIM2 : 1,02) | 1,28 [1,00 ; 1,51] | 1,55 | référence |
| France +2,0 °C | 3,8 [0,8 ; 10,5] | 1,78 | +4 % (1-12 %) |
| France +2,7 °C | 7,2 [1,5 ; 12,1] | 1,94 | +10 % (3-29 %) |
| France +4,0 °C | 17,9 [8,9 ; 31,0] | 2,35 | +30 % (9-106 %) |

Repères observés : moyenne 2000-2025 1,9 ; 2019 et 2022 environ 4 ; 2003 14,7. **Lecture :** descriptive ; pratiques, variétés et règles d'eau tenues fixes ; à +4 °C, l'été moyen dépasse 2003 et l'extrapolation sort du support de β. Les fenêtres +2,0 °C de plusieurs modèles sont raccourcies au début (2021).

## Non fait

- **Méthode SAA (partage irrigué / non irrigué) :** les sources publiques consultées décrivent la SAA comme une synthèse des services régionaux, combinant enquêtes (structure, Terres, vergers) et données administratives (ASP, PAC). Elles ne définissent pas « irrigué » : surface irriguée l'année, ou équipée pour l'irrigation. Les PDF méthodologiques d'Agreste demandent désormais une session. La question reste à poser directement au SSP ou à un SRISE. L'enquête Pratiques culturales grandes cultures (2017, 2021, 2025) relève l'irrigation et le rendement à la parcelle : ce serait une source de validation possible, au niveau régional.

## Revues simulées du 2026-10-14 (V1, V2 ; déclarées avant calcul)

- **V1, taille du CV3** : 7,3 % (300 placebos, erreur de Monte-Carlo 1,5 point), contre 3,7 % pour le WCR sur les mêmes permutations ; puissance 32 % et 66 % (β = 0,008 et 0,016), contre 24 % et 66 %. Lecture selon la règle : à peu près calibré ; le désaccord avec le WCR reste une réserve.
- **V2, ventilation SAA** : rapport Y_I/Y_R identique à celui de l'année précédente dans 4,3 % des transitions (référence par permutation : 1,0 %, 95ᵉ centile 1,9 %), dont 15 sur 18 dans l'ancienne série (2000-2009) et 2 en 2003 ; pas d'excès de rapports ronds (p = 0,50), pas de rupture en 2010, pas de lien avec la chaleur (p = 0,18). Signature retenue ; sans les 7 départements signalés par la règle, β = 1,0 % par degré-jour, p = 0,063 : menace « active » selon la règle déclarée.
- Détail et règles de lecture : `docs/decisions.md` ; tables `reports/tables/phase7_v1_cv3.csv`, `phase7_v2_signatures.csv` ; script `R/28_q1_revues.R`.
