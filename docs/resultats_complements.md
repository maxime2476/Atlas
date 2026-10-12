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
| G9a : jackknife par année (CV3), t à 25 ddl | **0,074** | Plus conservateur ; recommandé par MacKinnon, Nielsen et Webb (2023) avec peu de grappes |
| G9b : randomisation (5 000 dérangements des années, statistique β̂) | 0,001 | L'effet réel éventuel reste dans l'erreur du placebo |
| G8 : DML (forêts aléatoires sur SWI, P, ETP, GDD ; 5 plis par blocs d'années) + WCR | 0,016 (β = 0,0155) | Contrôles météo non linéaires : β inchangé |

**Lecture :** le statut de H1 reste fixé par le WCR (règle de la phase 4 bis). Mais la significativité au seuil de 5 % **dépend de la méthode d'inférence** : le jackknife par grappes, plus conservateur, donne p = 0,074. C'est une réserve à citer.

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

## Non fait

- **G11, température de surface MODIS :** le jeton AppEEARS a expiré (HTTP 403 le 2026-10-12). Il faut un jeton renouvelé par l'auteur (compte Earthdata). L'analyse est déclarée et reportée.
- **Méthode SAA (partage irrigué / non irrigué) :** les sources publiques consultées décrivent la SAA comme une synthèse des services régionaux, combinant enquêtes (structure, Terres, vergers) et données administratives (ASP, PAC). Elles ne définissent pas « irrigué » : surface irriguée l'année, ou équipée pour l'irrigation. Les PDF méthodologiques d'Agreste demandent désormais une session. La question reste à poser directement au SSP ou à un SRISE. L'enquête Pratiques culturales grandes cultures (2017, 2021, 2025) relève l'irrigation et le rendement à la parcelle : ce serait une source de validation possible, au niveau régional.
