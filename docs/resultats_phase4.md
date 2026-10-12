# ATLAS — Résultats économétriques (phase 4)

*2026-10-10. Spécification fixée **avant** estimation : `docs/specification_phase4.md` (SHA-256 consigné dans `docs/decisions.md`).*

**Reproduction :**

```bash
Rscript R/10_fe_models.R
Rscript R/11_robustness.R
```

Environnement R figé par `renv.lock` : R 4.5.2, fixest 0.14.2, nanoparquet 0.5.2, image Posit Package Manager du 2026-09-26.

## 1. Résultats observés

**Échantillon :**

- 83 départements (statut qualité 1) × récoltes 2010-2025 = 1 328 observations ;
- poids : surface de blé 2010-2012 ;
- effets fixes département et année ;
- météo pondérée par le masque blé.

### Modèles principaux

| Modèle | Terme | Estimation | p, cluster département (83) | p, Conley 200 km | p, bootstrap WCR par année (16) | Effet |
|---|---|---|---|---|---|---|
| M1 | `dd_32_remplissage` | −0,0149 | 0,004 | 0,047 | 0,374 | −1,5 % par °C·jour ; −1,7 % pour l'exposition moyenne de 2019 (1,18 °C·jour) |
| M1 | `gdd_0_32_remplissage` | −0,00051 | 0,001 | 0,041 | 0,259 | −0,05 % par °C·jour |
| M1 | `prec_printemps` | −0,00045 | < 0,001 | 0,026 | 0,093 | −0,045 % par mm |
| M1 | `dd_0_automne` | +0,00023 | 0,007 | 0,189 | 0,508 | +0,02 % par °C·jour |
| M1 | `prec_automne` | −0,00030 | < 0,001 | < 0,001 | 0,189 | −0,03 % par mm |
| M2 | `dd_32_remplissage` | −0,0152 | 0,007 | 0,111 | 0,327 | −1,5 % par °C·jour |
| M2 | `swi_remplissage` | +0,79 | < 0,001 | < 0,001 | 0,205 | — |
| M2 | `swi_remplissage`² | −0,96 | < 0,001 | < 0,001 | 0,147 | — |

R² *within* : 0,084 (M1), 0,203 (M2). Les p-valeurs de Conley utilisent les degrés de liberté par défaut de `fixest` (noyau uniforme, sans dimension temporelle).

**H2, test joint des termes SWI dans M2 :**

| Inférence | Statistique | p |
|---|---|---|
| Cluster département | F = 24,7 | 4 × 10⁻⁹ |
| Conley 200 km | F = 10,1 | 4 × 10⁻⁵ |
| Cluster année, analytique (ajouté après relecture) | F = 1,91 | **0,18** |
| WCR joint par année, Wald, poids de Webb, 9 999 tirages (ajouté après relecture) | W = 4,36 | **0,32** |

Forme de la relation SWI (description) : le sommet est à SWI ≈ 0,41. Seuls 16,6 % de l'échantillon sont en dessous (minimum 0,20, médiane 0,57). Sur la majorité de l'échantillon, un SWI de mai-juin plus élevé est donc **associé** à un rendement plus faible. Le WCR individuel sur δ₁ (p = 0,21) figure dans les tableaux pour conformité à la spécification, mais il n'est **pas interprétable** : δ₁ est la pente à SWI = 0, hors du support observé.

**p-valeur unilatérale pour H1** (WCR, P(t* ≤ t)) : 0,19 dans M1, 0,16 dans M2.

*Écart non déclaré à l'origine (consigné le 2026-10-12) : la spécification prévoyait de rapporter H1 « avec l'intervalle à 95 % bilatéral ». Cet intervalle n'a pas été calculé. La seule forme cohérente avec l'inférence retenue serait un intervalle obtenu en inversant le WCR par année ; il reste à calculer.*

**Placebo** (chaleur extrême de *t*+1, récoltes 2010-2024, 1 245 observations, 15 grappes année) : −0,0018, p = 0,72 / 0,78 / 0,91. L'échantillon diffère de M1, et un placebo nul ne valide pas l'identification.

### Robustesses pour le coefficient de chaleur extrême (spécification M1)

| Code | Spécification | Estimation | p, cluster | p, Conley | p, WCR année |
|---|---|---|---|---|---|
| — | M1 (référence) | −0,0149 | 0,004 | 0,047 | 0,374 |
| R1 | Sans pondération | −0,0159 | 0,034 | *non fiable* † | 0,332 |
| R2 | Sans 84, 30, 48 | −0,0147 | 0,005 | 0,055 | 0,385 |
| R3 | Sans 2025 | **−0,0290** | < 0,001 | < 0,001 | 0,141 |
| R4 | 85 départements | −0,0151 | 0,003 | 0,042 | 0,367 |
| R5 | Seuil de 30 °C (`dd_30`) | −0,0070 | 0,004 | 0,076 | 0,398 |
| R6 | Météo pondérée par la surface | −0,0127 | 0,006 | 0,036 | 0,442 |
| R7 | + tendances régionales | −0,0125 | 0,038 | *non fiable* † | 0,444 |
| R8 | Panel long 1990-2025 (**36 grappes année**, l'inférence par année la mieux dotée) | −0,0100 | 0,038 | 0,171 | 0,416 |
| R9 | Conley 300 km | −0,0149 | 0,004 | *non fiable* † | 0,374 |
| R10 | Fenêtre mai-juillet | **+0,0036** | 0,243 | 0,499 | 0,663 |
| R11 | Fenêtre −2 semaines (16 avr. - 15 juin) ‡ | −0,158 | < 0,001 | 0,014 | 0,342 |
| R12 | Fenêtre +2 semaines (16 mai - 15 juil.) | −0,0065 | 0,167 | 0,354 | 0,573 |
| R13 | Sans montagne (04, 05, 12, 15, 43, 48, 73) | −0,0152 | 0,004 | 0,050 | 0,377 |
| R14 | Classes de température : jours à 30-33 °C | −0,017 | 0,291 | *non fiable* † | 0,738 |
| R14 | Classes de température : jours ≥ 33 °C | −0,021 | 0,298 | *non fiable* † | 0,697 |

† Matrice de Conley non définie positive, « corrigée » automatiquement par `fixest` : p-valeur non interprétée.

‡ Dans la fenêtre avancée, l'exposition au-delà de 32 °C est quasi nulle : moyenne 0,02 °C·jour, maximum 1,37, et seules 0,8 % des observations dépassent 0,5. Le coefficient par °C·jour n'est donc pas interprétable ; pour l'exposition moyenne de 2019, l'effet vaut −0,01 %.

**R11 à R14 ont été ajoutées après les premières estimations**, à la demande de l'utilisateur, mais leurs définitions ont été fixées dans `docs/decisions.md` avant tout calcul. Elles viennent de `scripts/12_build_semimonthly.py` (demi-mois et classes) et de `scripts/13_cell_altitude.py` (altitude).

**Exposition selon la fenêtre** (83 départements, 2010-2025) :

| Fenêtre | Moyenne de `dd_32` | Maximum | Part > 0,5 °C·jour | Écart-type résiduel | N_eff |
|---|---|---|---|---|---|
| 16 avr. - 15 juin | 0,02 | 1,37 | 0,8 % | 0,08 | 4,68 |
| Mai-juin (référence) | 0,37 | 8,89 | 20,0 % | 0,55 | 4,13 |
| 16 mai - 15 juil. | 0,57 | 11,97 | 28,7 % | 0,73 | 5,54 |
| Mai-juillet | 1,14 | 16,37 | 46,7 % | 1,01 | 4,84 |

**R14, toutes les classes** (jours passés dans la classe en mai-juin, référence 15-18 °C, `reports/tables/phase4_classes_temperature.csv`) :

| Classe | < 9 | 9-12 | 12-15 | 18-21 | 21-24 | 24-27 | 27-30 | 30-33 | ≥ 33 |
|---|---|---|---|---|---|---|---|---|---|
| Coefficient (log-rendement par jour) | +0,008 | +0,010 | +0,000 | +0,006 | +0,002 | −0,001 | −0,020 | −0,017 | −0,021 |
| Erreur-type, cluster année | 0,008 | 0,004 | 0,009 | 0,006 | 0,012 | 0,015 | 0,030 | 0,043 | 0,046 |

### Diagnostics ajoutés après la relecture (non pré-spécifiés)

**Leave-one-year-out** (β de `dd_32_remplissage`, M1, `reports/tables/phase4_loyo.csv`) :

- l'estimation varie de **−0,0290** (sans 2025) à **−0,0059** (sans 2022) ;
- elle reste négative dans les 16 cas ;
- sans 2012, 2016 ou 2022, elle s'affaiblit (−0,006 à −0,011) ; sans 2020 ou 2025, elle se renforce.

C'est un estimateur qui dépend de quelques années, comme le laissait prévoir la concentration de l'exposition.

**Taille et puissance des inférences sur ces données** (`R/12_diagnostics.R`, `phase4_simulation_inference.csv`).

Le régresseur placebo est le champ réel `dd_32_remplissage` dont on **permute les années**, avec la même permutation pour tous les départements et sans année fixe. Il garde la structure spatiale et la concentration de l'exposition, mais n'a plus de lien avec les rendements. R = 300 tirages, B = 399 pour le WCR. L'erreur Monte-Carlo sur un taux de 5 % est de 1,3 point.

| Effet réel ajouté | Cluster département | Conley 200 km | WCR par année |
|---|---|---|---|
| 0 (**taille**, attendue à 5 %) | **56,3 %** | **39,3 %** | **4,3 %** |
| −0,015 (puissance) | 69,0 % | 54,7 % | 12,3 % |
| −0,03 (puissance) | 87,3 % | 78,3 % | 29,3 % |

**Validation de l'implémentation du WCR :**

- la statistique t du WCR (variance CR0, sans facteur de petit échantillon) est identique au t CR0 de `fixest` en cluster par année : −1,040 (recalcul indépendant de l'audit du 2026-10-11 ; le t CR1 de `fixest` vaut −0,973). *Erratum du 2026-10-12 : la version précédente comparait −0,967 à −0,973, un chiffre hérité d'une version antérieure du code et faux en l'état.* ;
- un premier test de taille, avec un placebo iid, donnait 8,7 % de rejets à cause d'un **bug** : y* n'était pas re-projeté sur les effets fixes et les contrôles. Après correction, il donne 6,6 % (R = 500). Ce test était peu informatif, car son placebo, absorbé par l'effet fixe année, était un bruit iid ;
- la simulation ci-dessus le remplace. Un **second bug**, dans le script de simulation lui-même (priorité de l'opérateur `<`, qui donnait 0 % de rejets partout), a été corrigé avant toute lecture des résultats.

## 2. Interprétation

Relecture par l'agent `econometrics-reviewer` : aucun défaut bloquant ; ses corrections sont intégrées ci-dessus (H2 sous inférence par année, valeurs NA, leave-one-year-out, simulation réaliste, p unilatérale).

### Observé

- **Chaleur extrême.** À département et année donnés, 1 °C·jour de plus au-delà de 32 °C en mai-juin est associé à un log-rendement plus faible d'environ 0,015 (≈ −1,5 %). Le signe est négatif dans la spécification principale, dans 9 robustesses sur 10 et dans les 16 estimations *leave-one-year-out*. Il s'inverse avec la fenêtre mai-juillet (R10 : +0,0036, non significatif).
- **Inférence.** La simulation montre que, sur ces données, seule l'inférence par année (WCR) a la bonne taille. Le cluster par département et Conley rejettent à tort dans 56 % et 39 % des cas sous H0. Avec le WCR, aucun coefficient météo n'est significatif : p bilatérale ≥ 0,14 pour la chaleur extrême, quelle que soit la spécification (H1 étant unilatérale, la plus petite p unilatérale est 0,071, sans 2025 en R3 ; 0,19 pour M1) ; p = 0,32 pour le test joint du SWI.
- **Puissance.** Le WCR ne détecte un vrai effet de −1,5 % par °C·jour que dans 12 % des cas, et de −3 % que dans 29 %.

### Interprétation

1. **H1 (chaleur extrême) n'est pas établie** selon la règle pré-spécifiée : le résultat ne résiste pas aux trois inférences. Il est **compatible** avec un effet négatif de la chaleur extrême, mais il n'est ni démontré ni exclu.
2. **H2 (effet propre de l'eau) n'est pas établie non plus.** La forte significativité en cluster département et en Conley n'est pas crédible, puisque ces inférences sont fortement sur-dimensionnées sur ces données. De plus, le SWI est un produit de modèle qui dépend en partie de la température (médiateur) : son coefficient est associatif.
3. **La raison est structurelle, pas technique.** Les chocs de rendement sont corrélés entre départements une même année, au-delà de 200 km. Une fois les effets fixes retirés, l'information effective se réduit à quelques années (environ 3 à 4 pour la chaleur extrême). **Seize récoltes ne suffisent pas** pour une inférence fiable sur des effets de cet ordre : c'est un résultat de puissance, pas une preuve d'absence d'effet.
4. **Un profil décroissant avec la fenêtre, non significatif.** Le coefficient de chaleur extrême s'affaiblit à mesure que la fenêtre avance dans l'été : −0,015 (mai-juin), −0,0065 (16 mai - 15 juillet), +0,004 (mai-juillet). Ce profil est **compatible** avec une sensibilité maximale autour de la floraison (fin mai - début juin, d'après Nóia Júnior et al. 2025) plutôt qu'en fin de remplissage, mais aucune de ces estimations n'est significative avec le WCR, et les fenêtres, de longueurs et d'expositions différentes, donnent des coefficients par °C·jour peu comparables. La fenêtre de référence n'est pas changée a posteriori. La fenêtre avancée (R11) n'est pas informative, faute d'exposition.
5. **Classes de température (R14).** La forme est celle attendue, avec une réponse négative à partir de 27-30 °C et des classes fraîches légèrement positives, mais elle est **très imprécise** : erreurs-types en cluster année de 0,03 à 0,05 pour les classes chaudes. Elle concorde qualitativement avec les seuils publiés (Schlenker & Roberts 2009 ; Gammans et al. 2017), sans les confirmer.
6. **Montagne (R13).** Exclure les 7 départements où au moins 25 % du blé est cultivé au-dessus de 600 m ne change pas l'estimation (−0,0152). La moindre fiabilité de SAFRAN en altitude ne semble pas expliquer le résultat.

### Formulations à proscrire

- « la chaleur extrême réduit le rendement de 1,5 % par °C·jour » ;
- « H1 confirmée » ;
- « l'eau a un effet propre robuste » ;
- « placebo nul, donc identification validée » ;
- toute extrapolation au changement climatique.

### Formulation retenue

« Les départements plus exposés à la chaleur extrême en mai-juin, une même année, ont en moyenne des rendements plus faibles (environ −1,5 % par °C·jour au-delà de 32 °C). Mais, avec seize récoltes et des chocs corrélés à l'échelle nationale, cette association n'est pas distinguable de zéro par une inférence de taille correcte. »

### Conséquences pour la suite

- Le panel long (R8, 36 grappes) est la seule voie pour gagner en puissance, mais ses limites ont été documentées.
- Le module prédictif (phase 5) doit s'attendre à un gain faible de la météo sur une référence naïve.
