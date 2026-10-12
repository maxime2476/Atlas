# ATLAS — Résultats de la phase 4 bis

*Estimations du 2026-10-11, conformes à `docs/specification_phase4bis.md` (pré-spécifiée, SHA-256 `88e15f62…d443`).*

**Scripts et sorties :**

- `Rscript R/14_q1_maize.R` puis `uv run python scripts/24_valorisation_mais.py` (Q1) ;
- `Rscript R/15_q2_wheat.R` (Q2) ;
- tables : `reports/tables/phase4bis_*.csv`.

**Inférence :** seule la p-valeur du wild cluster bootstrap restreint par année (WCR, 9 999 tirages) fonde les conclusions. Le cluster par département et Conley sont donnés pour information ; leurs tailles empiriques, mesurées ci-dessous sur ces mêmes données, sont de 16 à 26 %.

---

## Q1 : irrigation et chaleur, maïs grain

**Échantillon :** 17 départements (statut qualité 1), 2000-2025, 435 paires département-année.

**Taille du test principal** (placebo à années permutées, R = 300, B = 399, unilatéral à 5 %) :

| Inférence | Taille empirique |
|---|---|
| Cluster département | 16,3 % |
| Conley 200 km | 22,0 % |
| **WCR par année** | **3,7 %** |

Le test WCR respecte son niveau nominal ; les deux autres sont fortement surdimensionnés.

### Hypothèse principale et réplication

| | β (`dd_32_ja`, écart log irrigué − non irrigué) | Effet par °C·jour | IC 90 % (CR1 année) | p WCR unilatérale | n |
|---|---|---|---|---|---|
| **H1, 2000-2025** | **+0,0158** | **+1,6 %** | [0,0030 ; 0,0286] | **0,007** | 435 |
| Réplication 2000-2009 (années jamais utilisées) | +0,0108 | +1,1 % | non rapporté (CR1 non fiable à 10 grappes) | 0,049 | 165 |

**Résultat observé :**

- **H1 est établie selon la règle pré-spécifiée** (p = 0,007 < 0,05 et taille de 3,7 % ≤ 10 %), au sens de cette règle seulement : 270 des 435 paires (62 %) appartiennent à 2010-2025, la période dont l'analyse exploratoire (phase 6) a suggéré l'hypothèse. La seule preuve nouvelle est la décennie 2000-2009, ci-dessous.
- Chaque degré-jour au-dessus de 32 °C en juillet-août est associé à un écart de rendement plus large d'environ 1,6 % en faveur du maïs irrigué.
- Sur les dix années 2000-2009, que l'analyse exploratoire de la phase 6 n'avait pas vues, l'estimation garde **le même signe avec le masque maïs, pour un effet environ deux fois plus faible** (+1,1 % contre +2,4 % sur 2010-2025 avec le même masque).
- **Cette réplication dépend de la mesure de la chaleur.** Avec la pondération surfacique utilisée en phase 6, l'estimation sur 2000-2009 est nulle (−0,0009 ; § « Diagnostics exploratoires »). Elle n'est donc pas convergente avec la mesure de la phase 6.
- Avec 10 grappes, la taille du WCR n'a pas été vérifiée ; la p bilatérale vaut 0,10.

**Interprétation :** une association significative selon la règle pré-spécifiée, mais **sensible à la mesure de la chaleur**. Ce n'est pas un effet causal de l'irrigation. Les parcelles irriguées diffèrent des autres (sols, exploitations, variétés). Les effets fixes département et année absorbent ces différences seulement si elles sont stables, et non si elles varient avec la chaleur de l'année.

### Hypothèses secondaires (Holm, 4 tests)

| Code | Estimation | p WCR unilatérale | p Holm | Conclusion |
|---|---|---|---|---|
| H2a : un sol plus humide est associé à un écart plus faible (`swi_ja`) | −0,352 par unité de SWI | 0,012 | 0,024 | Soutenue |
| H2b : la chaleur est associée à un rendement non irrigué plus faible | −2,5 % par °C·jour | < 1/9 999 (aucun tirage n'atteint t ; le CSV affiche 0) | ≤ 4/9 999 | Soutenue |
| H2c : la chaleur pénalise aussi le maïs irrigué | −1,0 % par °C·jour | 0,002 | 0,005 | Soutenue |
| H3 : les jours de crise VigiEau réduisent la protection (2016-2025) | Interaction **positive** (+0,0008) | 0,961 | 0,961 | **Non soutenue**, signe opposé |

- **Lecture d'ensemble :** le maïs irrigué présente une sensibilité à la chaleur plus faible, mais non nulle. Son rendement est associé à −1 % par °C·jour, contre −2,5 % pour le non irrigué.
- **H3 :** le signe opposé n'est pas interprétable causalement. Une conjecture, **non testée**, est que les arrêtés de crise sont pris lors des étés les plus secs, où l'écart est le plus grand. L'indicateur de crise est grossier (« au moins une zone du département »), il n'y a que 10 années (taille du WCR non vérifiée à 10 grappes), et l'IC CR1 de la table n'est pas fiable.

### Robustesses de A1 (terme `dd_32_ja`, p WCR unilatérale)

| Spécification | β | p | n |
|---|---|---|---|
| Principal | 0,0158 | 0,007 | 435 |
| R1 : 38 départements | 0,0217 | 0,006 | 981 |
| R2 : 2010-2025 | 0,0242 | 0,030 | 270 |
| **R3 : météo pondérée par la surface** | **0,0104** | **0,221** | 435 |
| R4 : seuil de 30 °C | 0,0104 | 0,007 | 435 |
| R5 : juillet seul | 0,0575 | 0,013 | 435 |
| R6 : sans pondération | 0,0185 | 0,021 | 435 |
| R7 : sans 2025 | 0,0157 | 0,015 | 418 |
| R8 : sans 2003 | 0,0243 | 0,029 | 418 |

- **Signe :** positif dans les 9 spécifications.
- **Significativité :** 8 sur 9 au seuil de 5 %.
- **Exception :** avec la météo pondérée par la surface (R3), le coefficient n'est pas significatif (p = 0,22).
  - Ce n'est **pas** une simple atténuation par erreur de mesure. Avec cette pondération, l'estimation sur 2010-2025 est même **plus forte** (0,038 contre 0,024). L'écart vient de 2000-2009 (−0,0009 contre +0,011), une période dominée par 2003.
  - Le résultat de Q1 dépend donc de la mesure de la chaleur pour les années 2000-2009. **Le qualificatif « robuste » n'est pas justifié.**
- **2003 :** le résultat ne repose pas uniquement sur la canicule de 2003 (R8 : 0,024 sans 2003, taille non vérifiée pour cette variante). Sur 2000-2009 sans 2003, les deux mesures de la chaleur divergent toujours (0,038 avec le masque, 0,009 avec la pondération surfacique ; `phase4bis_q1_exploratoire.csv`, exploratoire).

### Valorisation descriptive (17 départements, conditionnelle à β̂)

**Prix :** IPPAP maïs × 0,2192 €/q par point ; raccord stable sur 2012-2016 (écart maximal 0,0009 < 0,002).

| Été | Écart moyen à la normale de `dd_32_ja` (°C·jour, pondéré) | Quintaux associés à l'irrigation | Valeur (M€) | Fourchette IC 90 % (M€) |
|---|---|---|---|---|
| 2003 | +13,7 | 2,98 millions | **49** | 8 à 98 |
| 2019 | +2,5 | 0,43 million | 9 | 2 à 17 |
| 2022 | +1,9 | 0,33 million | 14 | 3 à 25 |

- **Ce que mesurent ces chiffres :** des **quintaux associés** à l'irrigation lors d'un été plus chaud que la normale de chaque département, pour les 17 départements de l'échantillon (160 847 à 212 786 ha irrigués selon l'année).
- **Convention de calcul :** la formule s'applique au rendement non irrigué, ce qui est prudent. Appliquée au rendement irrigué, Y_I × (1 − exp(−βΔ)), elle donnerait environ 29 % de plus en 2003 (`\ValAltPct` du mémoire, script 26).
- **Euros courants :** 2022 vaut plus que 2019 malgré moins de quintaux, parce que le prix passe de 21 à 41 €/q. Ce n'est **pas** la valeur totale de l'irrigation, qui inclut aussi l'avantage moyen de l'irrigué, ni un gain causal.
- **Pourquoi 2022 pèse peu :** sa sécheresse est mal captée par la seule chaleur au-dessus de 32 °C dans ces départements.
- **Fourchette :** elle repose sur l'IC du cluster par année (CR1) ; c'est une indication seulement.

---

## Q2 : sensibilité du blé à la chaleur, 1959-2025

**Échantillon :** 83 départements, 5 543 observations, 67 récoltes (18 rendements manquants retirés, tous en 1959-1967).

**Taille de Q2-H1 :** WCR 4,3 % ; cluster département 26,3 % ; Conley 16,3 %.

| | β₂ (`dd_32_remplissage`) | Effet par °C·jour | p WCR unilatérale | p cluster département (information) |
|---|---|---|---|---|
| **Q2-H1, 1959-2025** | **−0,0108** | **−1,1 %** | **0,125** | 0,014 |

**Résultat observé :** **Q2-H1 n'est pas établie.** Le signe est négatif et l'ordre de grandeur proche de la phase 4 (−1,5 %). Mais un résultat aussi négatif n'est pas rare sous l'hypothèse nulle (environ une fois sur huit) quand on tient compte de la dépendance par année. L'échantillon inclut celui de la phase 4 : ce n'est donc pas une réplication indépendante.

Quadrupler le nombre d'années (67 contre 16) n'a augmenté N_eff que de 4,1 à 6,2 : l'exposition reste concentrée sur quelques étés.

### Q2-H2 : la sensibilité a-t-elle changé ? (descriptif)

| Période | Pente | p WCR bilatérale |
|---|---|---|
| 1959-1981 | −0,0014 | 0,79 |
| 1982-2003 | −0,0279 | 0,17 |
| 2004-2025 | −0,0113 | 0,50 |

Test WCR joint d'égalité des pentes : Wald = 1,80, **p = 0,49**. Aucune évolution de la sensibilité n'est détectable. L'absence de preuve n'est pas une preuve de stabilité : la puissance est faible.

### Robustesses de B1 (p WCR unilatérale à gauche)

| Spécification | β₂ | p |
|---|---|---|
| Principal | −0,0108 | 0,125 |
| R1 : + tendances régionales | −0,0119 | 0,103 |
| R2 : sans 2025 | −0,0165 | 0,028 |
| R3 : 1968-2025 | −0,0113 | 0,109 |
| R4 : effet fixe département unique | −0,0113 | 0,112 |
| R5 : seuil de 30 °C | −0,0062 | 0,095 |

- **Signe :** négatif partout.
- **Significativité :** une seule robustesse est significative, sans 2025 (données provisoires). Ce n'est **pas** une raison de modifier la conclusion principale, fixée avant estimation : retenir la spécification qui « marche » serait de la recherche de spécification.

---

## Diagnostics exploratoires (non pré-spécifiés, ajoutés après la relecture)

Script `R/16_q1_exploratoire.R` ; table `reports/tables/phase4bis_q1_exploratoire.csv`. Ce sont des estimations ponctuelles, **sans inférence**.

| β de A1 | Masque maïs | Pondération surfacique |
|---|---|---|
| 2000-2025 | 0,0158 | 0,0104 |
| 2000-2009 | 0,0108 | −0,0009 |
| 2010-2025 | 0,0242 | 0,0381 |
| Sans 2003 | 0,0243 | 0,0365 |
| 2000-2009 sans 2003 | 0,0380 | 0,0091 |

Les deux mesures concordent hors 2000-2009. La divergence se concentre sur cette décennie, et en particulier sur la façon dont chaque mesure traite 2003.

## Robustesse Q1-R9 : masque maïs d'époque (2008)

Cette robustesse a été déclarée dans `docs/decisions.md` avant estimation, après la relecture et l'audit de la phase 0 ter (`docs/phase0ter_audit.md`). Elle n'était pas pré-spécifiée en phase 4 bis.

**Méthode :**

- îlots RPG 1.0 de 2008, groupe « maïs grain et ensilage », régions des 17 départements ;
- scripts `scripts/25_build_maize_mask_2008.py` et `R/17_q1_mask2008.R`.

| | β (`dd_32_ja`) | Effet par °C·jour | p WCR unilatérale | n |
|---|---|---|---|---|
| A1, masque 2015-2017 (principal) | 0,0158 | +1,6 % | 0,007 | 435 |
| **Q1-R9, masque 2008** | **0,0153** | **+1,5 %** | **0,007** | 435 |

- **Corrélation des expositions (toutes années) :** 0,997 entre les deux masques maïs, contre 0,955 entre le masque 2015-2017 et la pondération surfacique.
- **Lecture fixée d'avance :** l'anachronisme du masque ne menace pas H1.
- **Origine de la divergence avec R3** (table `phase4bis_q1_mesures_departement.csv`) : elle est concentrée dans les départements de relief. En 2003, la pondération surfacique donne beaucoup moins de chaleur que le masque maïs : −10,3 °C·jour pour le Puy-de-Dôme, −8,5 pour l'Isère, −8,0 pour la Drôme, −7,5 pour le Jura, −4,2 pour le Rhône et −4,0 pour l'Ain. Dans les départements de plaine (Centre-Val de Loire, Bourgogne), l'écart est inférieur à 1,2 °C·jour.
- **Interprétation (a posteriori) :** dans ces départements, le maïs est cultivé dans les plaines et les vallées chaudes. La pondération surfacique y mesure surtout la chaleur des reliefs, sans maïs. Le masque maïs, désigné avant estimation comme mesure principale, mesure vraisemblablement mieux la chaleur subie par les surfaces en maïs ; aucune vérité terrain ne permet de le démontrer.
- **Ce qui reste inexpliqué :** pourquoi la pondération surfacique donne un coefficient plus fort sur 2010-2025.

## Synthèse

| Question | Conclusion pré-spécifiée | Statut |
|---|---|---|
| Q1-H1 : la chaleur creuse l'écart irrigué / non irrigué | p = 0,007, taille 3,7 % ; réplication 2000-2009 de même signe avec le masque maïs seulement ; inchangé avec un masque d'époque (R9 : p = 0,007) | **Établie** selon la règle, sur un échantillon qui inclut à 62 % les années exploratoires (association ; non significative avec la pondération surfacique, qui semble sous-mesurer la chaleur dans les départements de relief, explication a posteriori) |
| Q2-H1 : la chaleur en fin de cycle réduit le rendement du blé | p = 0,125, taille 4,3 % | **Non établie** |
| Q2-H2 : la sensibilité du blé a changé depuis 1959 | p = 0,49 | Non détectée |

**Limites principales :**

- **Composition et sélection :** lors des sécheresses, une partie du maïs non irrigué semé pour le grain peut être récoltée en ensilage, ce qui modifie le rendement observé du maïs grain non irrigué. L'abandon, lui, reste dans les statistiques : la SAA compte les surfaces non récoltées avec un rendement nul. Si ce sont les pires parcelles non irriguées qui partent en ensilage, le rendement non irrigué observé est surestimé les années chaudes et l'écart est biaisé vers le bas, contre le résultat ; sans cette hypothèse, le sens du biais n'est pas connu.
  - Contrôle descriptif : la part irriguée de l'année n'est pas liée de façon détectable à `dd_32_ja` (−0,0025 par °C·jour, p = 0,58 en cluster année, information seulement).
  - Ce contrôle ne couvre pas le passage du grain à l'ensilage, décidé après le semis.

- **Interprétation :** associative pour l'irrigation.
- **Statut qualité :** celui de 2025 est appliqué à 2000-2009.
- **Sensibilité à la mesure :** Q1 n'est pas significatif avec la météo pondérée par la surface, et la réplication 2000-2009 n'existe qu'avec le masque maïs, choisi après la phase 6.
- **Masques :** le masque maïs est fixe (2015-2017) ; le masque blé est appliqué à 1959, ce qui est anachronique.
- **Ruptures de source :** en 1989 et 2010, absorbées en niveau mais pas en pente.
- **VigiEau :** indicateur grossier.
