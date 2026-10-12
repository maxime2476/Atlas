# ATLAS — Journal des décisions

Chaque entrée indique la date, la décision, qui l'a prise et la justification. Une décision modifiant une spécification déjà fixée doit renvoyer à la version précédente.

| Date | Décision | Par | Justification / conditions |
|---|---|---|---|
| 2026-10-10 | Direction de la phase 0 validée : cœur explicatif (blé tendre d'hiver), module prédictif séparé, maïs irrigué exploratoire, récoltes 2010-2025, population à surface moyenne 2010-2012 ≥ 1 000 ha, *T\** = 32 °C avec repli documenté | Utilisateur | `docs/phase0_cadrage.md` |
| 2026-10-10 | Contribution principale recentrée sur la décomposition chaleur / humidité du sol ; masque RPG rétrogradé en robustesse | Proposé par Claude, validé avec la phase 1 | `docs/litterature.md`, § 7 |
| 2026-10-10 | Identité Git du dépôt : « Maxime Gourguechon » (configuration locale au dépôt). **Pas de commit pour l'instant.** | Utilisateur | — |
| 2026-10-10 | **Python 3.12** (3.12.14 géré par `uv`, `requires-python = ">=3.12,<3.13"`) au lieu de 3.14 | Utilisateur | Compatibilité plus large des roues binaires (géospatial, éventuelles bibliothèques GPU) ; version maintenue jusqu'à fin 2028. Aucun besoin GPU démontré à ce stade (voir ci-dessous) |
| 2026-10-10 | Décompression du RPG par un outil système 7z (et non `py7zr`) | Utilisateur | Sur Ubuntu 26.04, `p7zip-full` n'existe plus : paquet équivalent `7zip` (7-Zip officiel 26.00). Installation par l'utilisateur : `sudo apt install 7zip`. **En attente.** *Suite : installé par l'utilisateur et utilisé pour le RPG 2015-2017 et 2008 (7-Zip 26.00, constaté le 2026-10-12).* |
| 2026-10-10 | Allongement vers ~1990 avec Schauberger et al. (2022) : **conditionnel**, évalué en début de phase 2 | Utilisateur (« oui si cela a vraiment une utilité ») | Critères ci-dessous |
| 2026-10-10 | Si les verdicts de repli diffèrent entre pondération surfacique et masque blé, **celui du masque blé prévaut** | Proposé par Claude, validé par l'utilisateur | Le masque blé est la pondération de la spécification principale. Dans les faits, verdicts identiques (32 °C) |
| 2026-10-10 | **Allongement 1990-2025 retenu en robustesse** (Schauberger RAW 1990-2009 + SAA 2010-2025) | Utilisateur | Critère 1 constaté ; critère 2 satisfait ; N_eff(32) = 5,43 (4,11 sans 2025) |
| 2026-10-10 | Échantillon principal = **83 départements en statut qualité 1** (colonne `echantillon_principal`) ; 90 et 91 (statut 2) seulement en robustesse | Protocole de la phase 0, validé par l'utilisateur ; correction relevée par l'audit de la phase 3 | Le filtre avait été omis dans le panel construit ; l'exposition est inchangée (N_eff(32) = 4,13 non pondéré, 4,74 pondéré) |
| 2026-10-10 | Robustesses supplémentaires à prévoir en phase 4 : régression non pondérée, sans 84, 30 et 48, et sans 2025 | Proposé après l'audit de la phase 3 | Sans poids, 84 et 30 (≈ 1 600 ha chacun) portent 17 % et 12 % de la variance résiduelle de `dd_32_remplissage` |

## Règle opérationnelle de repli du seuil thermique (fixée le 2026-10-10, AVANT le comptage)

Variable : `dd_32_remplissage`, degrés-jours au-dessus de 32 °C cumulés en mai-juin (double sinus, poids surfaciques ; recalculée ensuite avec le masque blé), pour les 85 départements de la population, récoltes 2010-2025.

1. Résidus après effets fixes département et année : *r_dt* = *x_dt* − *x̄_d* − *x̄_t* + *x̄* (panel équilibré).
2. Part de chaque année dans la variance résiduelle : *s_t* = Σ_d *r_dt*² / Σ_dt *r_dt*².
3. Nombre effectif d'années contributives : **N_eff = 1 / Σ_t *s_t*²**.
4. **Si N_eff < 4, la spécification principale passe à 30 °C** (`dd_30_remplissage`), sinon elle reste à 32 °C. La règle est mécanique et n'utilise pas les rendements.
5. Effet minimal détectable (à titre informatif, n'intervient pas dans la règle) : MDE₈₀ ≈ 2,8 × σ_ε / √(Σ *r_dt*²), avec σ_ε l'écart-type résiduel du log-rendement après les deux effets fixes, **sans aucune variable météo**. C'est une borne basse : la corrélation spatiale des erreurs n'est pas prise en compte.

**Résultats (2026-10-10)** :

- pondération surfacique : N_eff(32) = 4,42 ;
- **masque blé (référence) : N_eff(32) = 4,13 → seuil de 32 °C conservé**.

Sans 2025 (provisoire), N_eff(32) = 2,89 et 2,64 respectivement : information consignée sans modifier la règle (`docs/notes_exposition.md`, § 6-7).

**Version pondérée** (ajoutée après l'audit, informative ; la règle reste non pondérée, telle qu'écrite) : avec les poids `surface_ref_ha`, N_eff(32) = 4,75 (3,20 sans 2025) sur 85 départements ; 4,74 (3,19) sur les 83 en statut 1 ; 4,88 (3,34) sans 84, 30 et 48.

## Critères pour l'allongement de la période (Schauberger et al., 2022)

**Données :**

- GFZ Data Services, DOI 10.5880/PIK.2021.001, CC-BY 4.0 ;
- rendements départementaux 1900-2018, versions « FILTERED » et « RAW » ;
- les années 1989-2018 proviennent de l'ancienne base Agreste, **non recalée sur le RA 2020**.

L'allongement n'a d'intérêt que pour la **puissance statistique sur la chaleur extrême**. Il ne sera retenu que si les deux conditions suivantes sont réunies :

1. **Utilité.** Le comptage obligatoire de la phase 2 (département-années exposés au-delà de 32 °C pendant le remplissage, par année) montre que l'exposition 2010-2025 est trop concentrée : la même règle que le repli, soit moins d'environ 4 années contributives, ou un effet minimal détectable jugé trop élevé.
2. **Compatibilité.** Sur le recouvrement 2010-2018, les rendements Schauberger (ancienne version Agreste) et SAA (rétropolée) sont cohérents : on comparera les écarts de niveau et la corrélation des anomalies par département.

**Critère 1 (utilité) :** constaté le 2026-10-10. Avec le masque blé, N_eff(32) = 4,13, mais 2,64 sans 2025 (année provisoire). L'utilisateur a validé l'allongement en robustesse.

**Critère 2 (compatibilité), seuils fixés le 2026-10-10 AVANT le calcul.** Blé tendre d'hiver, 85 départements, recouvrement 2010-2018, Schauberger « FILTERED » face à la SAA code 01. Les séries sont **compatibles** si :

- (a) la corrélation des résidus du log-rendement après effets fixes département et année est **≥ 0,90** ;
- (b) l'écart relatif médian, en valeur absolue, entre niveaux de rendement est **≤ 3 %**.

Si (a) est satisfait mais pas (b), l'allongement reste possible avec un effet fixe département × source. Si (a) échoue, l'allongement est abandonné.

**Écart au protocole (2026-10-10) : version RAW au lieu de FILTERED.**

- Le critère 2 avait été écrit pour la version FILTERED.
- Au premier calcul, 59 valeurs manquaient sur le recouvrement. L'examen a montré que le filtre des auteurs masque surtout des **années de pertes** : 119 valeurs sur 1990-2018, dont 39 départements en 2016 et 16 en 2003, et les valeurs masquées sont en médiane 22 % sous la médiane mobile du département.
- Utiliser FILTERED reviendrait à **sélectionner sur la variable expliquée**. Le motif est donc extérieur à toute estimation d'effet.
- Résultat du critère 2 sur FILTERED, consigné : corrélation des résidus 0,988 (38 départements équilibrés), écart médian 0 → compatible.
- **Résultat sur RAW, retenu** : 761 paires utilisables sur 765, corrélation des résidus **0,994** (83 départements équilibrés), écart relatif médian **0,0 %**, 97,5 % des paires identiques à ±0,5 q/ha → **COMPATIBLE**.

**Si l'allongement est retenu :**

- il reste une **analyse de robustesse** ; la spécification principale demeure 2010-2025 ;
- un effet fixe département × période absorbe la rupture de 2010 ;
- la tendance doit pouvoir plafonner, puisque Gouache et al. (2015) et Brisson et al. (2010) signalent un plafonnement des rendements depuis le milieu des années 1990 ;
- il faudra télécharger SIM 1989-2008 (environ 2,7 Go supplémentaires).

## État du GPU et de CUDA (constaté le 2026-10-10)

- Sous WSL, ni `nvidia-smi` ni `libcuda.so` ne sont visibles ; seules les bibliothèques D3D12 sont présentes dans `/usr/lib/wsl/lib/`.
- Le panel compte environ 1 360 observations : les modèles prévus (MCO à effets fixes, ridge, forêt aléatoire, gradient boosting de scikit-learn) s'exécutent en quelques secondes sur CPU.
- Un GPU ne se justifierait que pour des traitements d'images satellitaires (NDVI, phase 6 optionnelle).

## Spécification de la phase 4 (pré-spécifiée)

`docs/specification_phase4.md` a été écrite le 2026-10-10 à 12:43 (heure de Paris), avant toute estimation. SHA-256 : `2a63ada2115682864477fc22d2d5dc081dde61565aa2ff6544a2a04b7a4e6ced`. Toute modification ultérieure de ce fichier doit être justifiée ici.

## Écarts et ajouts par rapport à la spécification de la phase 4 (2026-10-10)

Tous ces écarts ont été décidés après la relecture de l'agent `econometrics-reviewer`, et les résultats initiaux restent rapportés :

1. **H2 sous inférence par année** (Wald analytique et WCR joint) : omission corrigée, car la règle de conclusion exige les trois inférences.
2. **Termes SWI** : le WCR individuel sur δ₁ est conservé mais déclaré non interprétable (pente hors support). Le WCR sur δ₂ est un complément non pré-spécifié.
3. **p-valeur unilatérale du WCR** pour H1, prévue (test unilatéral) mais initialement omise.
4. **Valeurs non interprétables mises à NA dans les CSV** : Conley « corrigé » par `fixest` (R1, R7, R9) et « effet en % » des termes polynomiaux.
5. **Diagnostics non pré-spécifiés** : *leave-one-year-out*, et simulation de taille et de puissance (placebo = champ `dd_32` à années permutées).
6. **Bugs corrigés avant toute interprétation** :
   - y* non re-projeté dans le WCR (taille 8,7 % → 6,6 %) ;
   - priorité de l'opérateur `<` dans le script de simulation.

## Compléments de la phase 4, fixés AVANT estimation (2026-10-10)

À la demande de l'utilisateur (« fais le reste à faire »), trois robustesses reportées sont ajoutées. Leurs définitions sont fixées ici, avant tout calcul de coefficient :

- **R11 / R12 : fenêtre de remplissage décalée de −2 / +2 semaines.**
  - Fenêtres : 16 avril - 15 juin, et 16 mai - 15 juillet.
  - Calcul par demi-mois à partir des données quotidiennes SIM ; même spécification M1.
  - Justification phénologique : floraison fin mai - début juin dans la plupart des départements, et remplissage d'environ 45 jours ensuite (Nóia Júnior et al. 2025 ; bulletins de santé du végétal régionaux).
- **R13 : sans les départements « de montagne ».**
  - Définition : au moins 25 % du blé (poids du masque RPG 2015-2017) dans des mailles SIM d'altitude moyenne ≥ 600 m.
  - Altitude moyenne de maille : moyenne de 16 points (sous-grille 4 × 4, pas de 2 km), donnés par le service de calcul altimétrique IGN (ressource `ign_rge_alti_wld`).
  - Le seuil de 600 m est le plus bas de la définition réglementaire de la zone de montagne (600 m dans les Vosges, 700 m ailleurs, 800 m en zone méditerranéenne).
- **R14 : classes de température** (Schlenker & Roberts 2009 ; Gammans et al. 2017).
  - Temps passé, en jours, dans chaque classe de 3 °C de la température horaire approchée par le double sinus, en mai-juin : < 9, 9-12, 12-15, 15-18, 18-21, 21-24, 24-27, 27-30, 30-33, ≥ 33 °C.
  - Classe de référence omise : 15-18 °C. Le temps total est fixé (61 jours), d'où l'omission d'une classe.
  - Mêmes contrôles et même inférence que M1. Lecture : forme de la réponse, et en particulier les classes 30-33 et ≥ 33 °C.

## Spécification de la phase 5 (pré-spécifiée)

`docs/specification_phase5.md` a été écrite le 2026-10-10 à 13:46, avant tout calcul de prévision. SHA-256 : `4c9e7787216580430f8324cccffde66e673be71d81fd79205bfcf011d274f416`.

## Écarts et ajouts par rapport à la spécification de la phase 5 (2026-10-10)

1. **Comparaison à B0 ajoutée** (écart de MSE, bootstrap par blocs d'années, `reports/tables/phase5_synthese_vs_B0.csv`) et mise au premier plan dans `docs/resultats_phase5.md`. Motif : B1, référence du critère pré-spécifié, s'est révélée plus faible que B0 sur les 10 années test. Juger les modèles contre B1 seul surestimerait leur gain. Les résultats contre B1 restent rapportés.
2. **Aucun réglage a posteriori :** grille d'α, variables et hyperparamètres restent ceux de la spécification, malgré l'instabilité observée de RIDGE.

## Spécification de la phase 6 (pré-spécifiée)

`docs/specification_phase6.md` a été écrite le 2026-10-10 à 14:32, avant les calculs A et B. SHA-256 : `843f8531055afc8c2e586730c66e90c5181fcf0ead7beecc8ab679699cfc6f87`.

Informations déjà connues au moment de la rédaction :

- le raccord IPPAP / Eurostat (rapport 0,2504), calculé pour choisir la source de prix ;
- les statuts qualité du maïs (phase 0).

## Écarts et ajouts par rapport à la spécification de la phase 6 (2026-10-10)

1. **Maïs** : 2 observations retirées, Jura 2016 et 2018, où la surface irriguée est nulle. Le traitement des rendements manquants n'était pas prévu dans la spécification.
2. **Maïs** : diagnostic de taille des inférences sur ces données (placebo à années permutées), non pré-spécifié, rapporté comme tel.
3. **Prix** : la valeur unitaire implicite des comptes de l'agriculture (Eurostat `aact_eaa01`) a été testée puis écartée avant la rédaction de la spécification. Son rapport au prix Eurostat variait de 0,65 à 1,14.

## NDVI : protocole fixé AVANT réception des données (2026-10-10)

L'utilisateur a fourni un accès NASA Earthdata et un jeton AppEEARS ; l'extension C de la phase 6 est donc engagée.

1. **Produit :** MOD13Q1 v6.1 (250 m, composites de 16 jours), couches NDVI et `pixel_reliability`, avril-juin, 2010-2025, via AppEEARS (GeoTIFF, EPSG:4326). Une commande de test sur 2022 précède la commande complète.
2. **Qualité :** on garde les pixels de fiabilité 0 (bon) et 1 (marginal) ; on rejette 2 (neige ou glace), 3 (nuage) et les valeurs de remplissage. NDVI = valeur × 0,0001.
3. **Agrégation :**
   - pixel → maille SIM (centre du pixel), moyenne des pixels valides ;
   - maille → département avec les **poids du masque blé** ; les poids sont renormalisés sur les mailles valides ;
   - valeur manquante si moins de 50 % du poids de blé est valide.
4. **Disponibilité à la date de prévision (pas de fuite) :** un composite qui commence le jour *s* couvre *s* à *s* + 15. Il n'est utilisable au 1er juin (ou au 1er juillet) que si *s* + 15 tombe avant le 1er juin (ou le 1er juillet).
5. **Variables :** NDVI moyen des composites utilisables par mois de début (avril, mai, juin) et NDVI maximal des composites utilisables.
6. **Évaluation (prédictive uniquement) :**
   - mêmes plis, mêmes références (B0, B1) et mêmes modèles (RIDGE, RF, GBM, réglages de la phase 5) ;
   - deux versions : météo seule, et météo + NDVI ;
   - critère : écart de MSE par rapport à B0 **et** par rapport à la version sans NDVI, bootstrap par blocs d'années ;
   - variante principale (entraînement 2010-) seulement.
7. **Interprétation :** le NDVI est un indicateur de l'état du couvert, en partie conséquence de la météo. Aucune lecture causale.

**Précision d'exécution (NDVI).** Le protocole ne disait pas comment traiter les valeurs NDVI manquantes au niveau départemental, rares (≤ 1,1 % par variable). Elles sont imputées dans chaque pli par la moyenne du département sur les années d'entraînement, puis par la moyenne générale d'entraînement. Aucune autre déviation.

## Phase 0 bis (2026-10-11)

- Recentrage validé par l'utilisateur : Q1 (maïs et irrigation) en principale, Q2 (blé 1959-2025) en secondaire (`docs/phase0bis_cadrage.md`).
- Q1 : échantillon principal en statut qualité 1 (17 départements) ; les 38 tous statuts en robustesse. Recommandation de Claude, validée par l'utilisateur.
- Nouvelles sources au manifeste :
  - SIM 1958-1988 ;
  - VigiEau (arrêtés 2012-2024) ;
  - IPPAP maïs ;
  - SAA « anciennes séries » 2000-2020 (partage maïs irrigué / non irrigué avant 2010, cohérent avec les séries rétropolées sur 2010-2020).

## Phase 2 bis (2026-10-11)

- Le code RPG `MIS` correspond au **maïs grain** (corrélation de 0,993 avec la SAA grain) : correction du cadrage, qui le croyait mêlé à l'ensilage.
- VigiEau : 2010-2011 exclues (niveau de gravité manquant) ; H3 en principal sur 2016-2025.
- Panel maïs 2000-2025 : le statut qualité de 2025 est appliqué à toute la période (pas de statut avant 2010).

## Spécification de la phase 4 bis (pré-spécifiée)

`docs/specification_phase4bis.md` a été écrite le 2026-10-11 à 17:40, **avant toute estimation** sur les données de la phase 2 bis. SHA-256 : `88e15f6290deeb0ed419221e97c48654bbf93850dc9ebd575dfd198c1ba7d443`.

Informations déjà connues au moment de la rédaction :

- les résultats exploratoires de la phase 6 (maïs 2010-2025) ;
- les statistiques d'exposition (N_eff) de la phase 2 bis.

Aucune estimation n'a été faite sur 2000-2009 pour le maïs, ni sur 1959-1989 pour le blé.

**Précision factuelle (2026-10-11, avant estimation) :** la spécification indique « 27 rendements manquants retirés » pour Q2. Ce chiffre vaut pour la population de 85 départements. Dans l'échantillon principal (83 départements en statut 1), il y en a **18**, tous en 1959-1967. Le modèle n'est pas modifié. Q1, échantillon principal : 435 paires département-année sur 26 années.

## Phase 4 bis : estimations (2026-10-11)

- La spécification a été appliquée sans écart de modèle ; résultats dans `docs/resultats_phase4bis.md`.
- Corrections d'exécution sans effet sur les modèles :
  - variable expliquée de la simulation de taille de Q1 (`ecart_log`) ;
  - colonnes de la table Q2-H2.
- Matrice de Conley non définie positive pour plusieurs termes de Q1 (H1, réplication, H2a, H3) : p-valeurs mises à NA (information seulement).
- Prix du maïs : la série Eurostat maïs (`prod_veg=01500000`) a été ajoutée au téléchargement (`--prix`). Raccord à l'IPPAP de 0,2192 €/q par point, stable sur 2012-2016 (écart 0,0009).
- Graine du WCR : 20261010 (valeur par défaut de `wcr_pvalue`) au lieu de 20261011 (spécification). Écart non déclaré, relevé par la relecture ; effet négligeable (erreur de Monte-Carlo ≈ 0,002 pour p ≈ 0,05).
- Relecture économétrique : « validable après corrections importantes ». Corrections d'interprétation appliquées à `docs/resultats_phase4bis.md` :
  - dépendance de Q1 à la mesure de la chaleur ;
  - réplication non convergente avec la mesure de la phase 6 ;
  - IC CR1 à 10 grappes retiré ;
  - formulations causales retirées ;
  - limite de composition ajoutée.
  Diagnostics exploratoires dans `R/16_q1_exploratoire.R`.

## Phase 5 bis (2026-10-11)

- README réécrit : Q1 (maïs) en résultat principal, avec la réserve sur la mesure de la chaleur.
- Figures 4 (coefficients de Q1 par spécification) et 5 (taille des tests de la phase 4 bis).
- `data/README.md` remis dans un ordre exécutable de bout en bout.
- Corrections issues de la relecture du README appliquées :
  - titre non causal ;
  - divergence entre les deux mesures persistante sans 2003 ;
  - réserves sur la réplication ;
  - gain du NDVI précisé ;
  - ordre des commandes.

## Phase 0 ter : audit (2026-10-11)

Voir `docs/phase0ter_audit.md`.

- **RPG 1.0 (îlots 2007-2014) :** source validée. Un masque maïs de 2008 donne une exposition proche du masque 2015-2017 dans les départements de l'échantillon. La divergence de Q1 vient de la géographie intra-départementale (maïs en plaine dans des départements de relief), pas de l'âge du masque. C'est une explication a posteriori.
- **BNPE (Hub'Eau) :** source validée avec réserves :
  - période commune 2012-2023 ;
  - ruptures de déclaration ;
  - volumes toutes cultures confondues.
- Aucune donnée ajoutée à `data/raw/` ; les échantillons ont été supprimés.

## Robustesse Q1-R9 : masque maïs 2008 (déclarée le 2026-10-11, avant estimation)

Ajout **non pré-spécifié en phase 4 bis**, motivé par la relecture et l'audit de la phase 0 ter. Elle sera rapportée quel que soit son résultat.

- **Masque :** îlots RPG 1.0 de 2008, groupe de cultures 02 (« maïs grain et ensilage »). Un îlot entier est attribué à son groupe majoritaire. Règle d'agrégation identique au masque 2015-2017 (centroïde → maille SIM et département). Régions R84, R24, R27 et R44, qui couvrent les 17 départements de l'échantillon principal.
- **Modèle :** A1 identique (écart log ~ `dd_32_ja` + `swi_ja` | département + année, poids `surface_ref_ha`, 17 départements, 2000-2025). Seule la météo change : elle est pondérée par le masque 2008.
- **Test :** WCR par année, unilatéral à droite, 9 999 tirages.
- **Lecture fixée d'avance :**
  - si β reste positif et que p < 0,05, l'anachronisme du masque ne menace pas H1 ;
  - sinon, H1 est déclarée sensible au masque.
- **Table descriptive associée :** pour chaque département, moyenne de `dd_32_ja` en 2000-2025 selon les trois mesures (masque 2008, masque 2015-2017, pondération surfacique).

**Résultat de Q1-R9 :** β = 0,0153, p WCR unilatérale = 0,0069 (A1 : 0,0158, p = 0,0074). Selon la lecture fixée d'avance, l'anachronisme du masque ne menace pas H1. Documents mis à jour : `docs/resultats_phase4bis.md`, README, figure 4.

## Mémoire : vérifications consignées (2026-10-11)

- Passage du code du bootstrap dans le module `R/wcr/wcr.R` : `R/14_q1_maize.R` et `R/15_q2_wheat.R` ont été relancés. Les tables d'hypothèses de Q1 et de Q2 (test de Wald compris) sont identiques à leur version précédente (`all.equal` vrai), et aucune table de `reports/tables/` n'a changé.
- Simulation de taille de Q1 : 300 permutations distinctes sur 300, vérifiées en rejouant la boucle de `R/14_q1_maize.R`.
- Relecture scientifique finale du mémoire : « prêt après corrections ». Corrections appliquées :
  - pré-enregistrement requalifié en « pré-spécification » (journal privé) ;
  - attributions bibliographiques ramenées aux résumés lus (`docs/litterature.md`, § 9) ;
  - annexe C complétée ;
  - règle SAA des surfaces non récoltées prise en compte dans la discussion.

## Audit avant HAL : écarts et corrections consignés (2026-10-11 et 2026-10-12)

Audit complet en lecture seule par quatre relecteurs (code, économétrie, données et publication, textes publics), puis corrections en trois lots. Aucune estimation n'a changé.

- **Phase 4, H1 :** l'intervalle à 95 % bilatéral prévu par la spécification n'a jamais été calculé ; l'omission n'avait pas été déclarée. Il reste à calculer (inversion du WCR par année).
- **Phase 4, WCR sur les contrôles de M1 :** calculé en plus de β₂ et δ₁, sans être prévu. Sans conséquence sur les conclusions.
- **Validation du WCR (`resultats_phase4.md`) :** l'affirmation « −0,967 contre −0,973 » était fausse. Le t du WCR (CR0) vaut −1,040, identique au t CR0 de `fixest` ; le t CR1 vaut −0,973.
- **Liste des Conley mis à NA (entrée « Phase 4 bis : estimations ») :** elle est incomplète. Sont aussi concernés Q1-R2, Q1-R4, Q1-R7 et Q1-R9 ; en phase 4, R1, R7, R9 et R14 ; en Q2, R1 (colonne `conley_non_dp_corrigee`).
- **VigiEau (entrée « Phase 2 bis ») :** les indicateurs couvrent 2012-2025, et non 2012-2024.
- **Diagnostics ajoutés pour le mémoire, non journalisés jusqu'ici :** `R/18_residual_autocorr.R` (autocorrélation d'ordre 1 des résidus, `diag_autocorr_residus.csv`) et `R/wcr/exemple.R` (Monte Carlo autonome, `wcr_exemple_montecarlo.csv`). Ce sont des descriptions, sans règle de décision.
- **Prévision :** `phase5_synthese_vs_B0.csv` n'était produit par aucun script ; il l'est désormais par `scripts/15_forecast_cv.py --synthese`, avec des valeurs identiques.
- **Mémoire et résumés :** réserves ajoutées (62 % des paires de Q1 viennent des années exploratoires ; « moitié » rapportée à l'estimation 2010-2025 ; explication par le relief présentée comme a posteriori) ; une affirmation fausse corrigée (l'irrigué dépasse le non irrigué dans 431 paires sur 435, pas dans toutes) ; licences des sources vérifiées en ligne le 2026-10-11.
- **Ensilage et abandon :** harmonisés dans tous les textes. L'abandon est compté avec un rendement nul ; seul le passage du grain à l'ensilage peut biaiser l'écart, vers le bas si ce sont les pires parcelles qui partent.
- **Lot 3 (points mineurs, 2026-10-12) :**
  - arrondis corrigés dans les documents de résultats (phases 3 à 6) ; une p-valeur de bootstrap nulle se lit p < 1/B (H2b : p < 1/9 999) ; 2016 : RIDGE fait un peu mieux que B0 en RMSE départementale, ce qui n'était pas dit ;
  - libellés : H2a et H2b reformulés en associations ; R8 « ne repose pas uniquement sur 2003 » ; la robustesse de H3 sur 2012-2025 envisagée en phase 2 bis n'a été ni spécifiée ni exécutée ;
  - prévision : trois réserves écrites (pseudo-temps réel par la sélection de l'échantillon ; TINF_H du lendemain pour le dernier jour avant la date de prévision ; validation interne non chronologique de l'α de la ridge), sans fuite vers l'année test ;
  - code sans effet sur les résultats (sorties des scripts 11, 12, 14, 16, 22, 23, 24 et 25 relancées et identiques) : contrôles `assert` remplacés par `if ... raise` ; masquage strict des demi-mois (12) ; liste des départements VigiEau prise avant le filtre sur le niveau (23) ; `validate="many_to_one"` sur la grille (rpg.py) ; pivot renommé par (mesure, code) (16) ; suppression limitée aux fichiers extraits (25) ; fichiers fermés ;
  - commentaires : convention de la p-valeur et de l'erreur de Monte-Carlo (`wcr.R`, `R/12`), distance de Conley par défaut de `fixest` (`common.R`), biais de Nickell sur ρ AR(1) (`R/18`), substitutions de variables dans les robustesses (R/11, R/14, R/15) ;
  - un test ajouté (fenêtre « mai » de la prévision) ; `monkeypatch` dans `test_phase6.py` ;
  - errata datés dans les documents de cadrage (phases 0 et 0 bis) et notes « document historique » en tête des notes des phases 1 et 2 ;
  - reste à calculer : l'intervalle à 95 % de H1 en phase 4 ; l'erreur de Monte-Carlo des lignes de puissance de `phase4_simulation_inference.csv` reste celle d'une taille de 5 % (commentée, non recalculée).

## Diagnostics de puissance et de taille de Q1, déclarés avant calcul (2026-10-12)

Demandés par une relecture externe après la publication de la v1.0.0 ; **non pré-spécifiés** dans `specification_phase4bis.md`. Ils sont déclarés ici avant d'être calculés, avec leur règle de lecture. Script : `R/19_q1_power_size.R` ; sortie : `reports/tables/phase4bis_q1_puissance.csv`.

- **Méthode commune** (celle de la taille de H1, `R/14`) : placebo = champ réel `dd_32_ja` à années permutées (dérangement, même permutation pour tous les départements), modèle A1 (`swi_ja` en contrôle, poids `surface_ref_ha`), WCR par année unilatéral à droite au seuil de 5 %, R = 300, B = 399, graines 20261013 puis r.
- **D1, puissance de H1 (2000-2025, 17 départements) :** on ajoute un vrai effet β × placebo à `ecart_log`, pour β = 0 (contrôle : doit redonner une taille proche de 3,7 %), 0,008 (la moitié de l'estimation) et 0,016 (environ l'estimation).
- **D2, taille et puissance de la réplication 2000-2009 (10 grappes) :** même placebo, permutations des seules années 2000-2009 ; β = 0 (taille) et β = 0,011 (environ l'estimation de la réplication).
- **Règle de lecture, fixée avant calcul :**
  - D1 est descriptif : il dit quelle chance le test avait de détecter un effet de cet ordre ; il ne change pas le statut de H1 ;
  - D2 : si la taille dépasse 10 % (le seuil de la règle de décision de la phase 4 bis), la p-valeur de la réplication (0,049) est déclarée non interprétable comme test ; si elle est au plus de 10 %, elle est rapportée avec sa taille. La réplication n'a jamais été une hypothèse principale ; son statut de « même signe » ne change pas.

## Reproduction propre depuis les fichiers bruts (2026-10-12)

- **Procédure :** clone vierge du commit 9f65cb4 dans un autre dossier ; fichiers bruts reliés par liens symboliques (aucun téléchargement) ; environnements recréés par `uv sync --frozen` et `renv::restore()` ; toute la chaîne de `data/README.md` exécutée dans l'ordre (extraction RPG comprise, sans les étapes 01 et 17 de téléchargement), soit environ 1 h 30.
- **Résultat :**
  - les 24 fichiers intermédiaires et finaux de `data/interim/` et `data/processed/` sont identiques à ceux du dépôt de travail, dont le panel maïs (435 paires de l'échantillon principal) ;
  - toutes les tables de `reports/tables/` sont identiques à l'octet, sauf 7 tables de prévision (phases 5 et 6), qui diffèrent d'au plus 5 × 10⁻¹⁵ (arrondis de calcul en virgule flottante) ;
  - `memoire/tables/numbers.tex` et les autres tables du mémoire sont identiques ; les trois figures régénérées donnent un rendu identique (seule la date de création du PDF change) ;
  - 564 tests passent dans le clone, dont les 457 contrôles d'empreinte : les fichiers bruts n'ont pas changé.
- **Limite :** la reproduction utilise les fichiers bruts téléchargés les 10 et 11 octobre 2026 ; un nouveau téléchargement peut donner des fichiers révisés par les producteurs (`data/README.md`).

## Vérification de la mesure de chaleur de Q1 avec E-OBS, déclarée avant calcul (2026-10-12)

Demandée par une relecture externe (sensibilité de H1 à la mesure de chaleur) ; **non pré-spécifiée** dans `specification_phase4bis.md`, exploratoire, prévue pour une v1.1. Elle sera rapportée quel que soit son résultat. Scripts : `scripts/27_eobs_heat.py`, puis `R/20_q1_eobs.R` ; sorties : `data/processed/weather_dep_eobs_ja.parquet`, `reports/tables/phase4bis_q1_eobs.csv` et `phase4bis_q1_eobs_departement.csv`.

- **Source :** E-OBS v33.0e, Tmin et Tmax journalières, moyenne d'ensemble, grille 0,1° (`docs/sources.md`, § 8 bis). Choisie plutôt qu'Open-Meteo (quotas incompatibles avec 1 784 mailles) et qu'ERA5-Land (compte Copernicus nécessaire ; réanalyse de modèle plutôt qu'interpolation de stations).
- **Seule la température change :** `dd_32_ja_eobs` reprend exactement la définition de `dd_32_ja` (double sinus avec Tmin du jour, Tmax du jour et Tmin du lendemain ; 1er juillet - 31 août de l'année de récolte ; poids du masque maïs RPG 2015-2017). Chaque maille SIM reçoit le point E-OBS le plus proche ; pas de point de remplacement : une maille manquante rend le département-année manquant.
- **Modèle :** A1 identique (écart log ~ `dd_32_ja_eobs` + `swi_ja` | département + année, poids `surface_ref_ha`, 17 départements, 2000-2025, 435 paires) ; `swi_ja` reste celui de SIM, E-OBS n'ayant pas d'indice d'humidité du sol. Seul A1 est réestimé : ni les robustesses, ni la réplication 2000-2009.
- **Test :** WCR par année, unilatéral à droite, 9 999 tirages (`summarise_term`, comme Q1-R9).
- **Lecture fixée d'avance :**
  - si β > 0 et p < 0,05, H1 ne dépend pas de la source de température (SAFRAN) ;
  - sinon, H1 est déclarée sensible à la source de température, et la v1.1 le dit dans le résumé, le README et le chapitre 7. Le statut de H1 dans la v1.0 n'est pas réécrit.
- **Lecture descriptive associée (sans règle de décision) :** le niveau des degrés-jours n'est pas comparable entre sources (E-OBS lisse davantage les extrêmes), donc β non plus. Sont rapportés : l'écart-type intra-département de chaque mesure, l'effet d'un écart-type intra-département, la corrélation des deux mesures (brute et intra-département), et une table par département (moyenne 2000-2025 et 2003).
- **Contrôles faits avant cette déclaration, sans calculer de degré-jour :** structure des fichiers (grille, unités, valeur manquante) ; distance maille SIM - point E-OBS d'au plus 0,07° ; 106 mailles littorales du masque sans valeur (point en mer), aucune dans les 17 départements de l'échantillon principal.

**Résultat de Q1-E (2026-10-12) :** β = 0,0148 (1,49 % par °C·jour), p WCR unilatérale = 0,0054, 435 paires (A1 : 0,0158, p = 0,007). Selon la lecture fixée d'avance, H1 ne dépend pas de la source de température (SAFRAN). Lecture descriptive :
- les deux mesures sont corrélées à 0,952 (0,953 en intra-département) ;
- contrairement à ce que la déclaration supposait, E-OBS donne **plus** de degrés-jours > 32 °C que SIM (moyennes départementales 2,6 à 7,3 contre 1,0 à 3,9 ; écart-type intra-département 4,87 contre 3,63) ; la supposition « E-OBS lisse davantage les extrêmes » était fausse pour cette variable, ce qui ne change ni le modèle ni la règle ;
- effet d'un écart-type intra-département : environ 7,5 % avec E-OBS, environ 5,9 % avec SIM.
- **Réserve de procédure :** à la demande de l'utilisateur, la déclaration n'a pas été commitée avant le calcul. Son empreinte SHA-256 (`docs/decisions.md` avant l'ajout de ce résultat) était `2251e0ffca6ffae8bef58b40e1c018700b1cc70e7aecd5b93ce1d4629a288759`, calculée juste avant de lancer `scripts/27_eobs_heat.py` ; c'est une trace locale, pas un horodatage indépendant.

## Relecture simulée (skill academic-research-skills) : tri et corrections de texte (2026-10-12)

Relecture du mémoire par le skill tiers `academic-paper-reviewer` (mode full, copie locale non versionnée au commit d1e5171) : cinq relecteurs simulés en sous-agents séparés (adéquation, méthodologie, domaine, eau et reproductibilité, avocat du diable). **Les cinq tournent sur le même modèle que celui qui a rédigé une grande partie du texte** : leurs erreurs ne sont pas indépendantes. Décision : révision majeure, sans défaut fatal ni point critique. Les faits décisifs ont été revérifiés dans le dépôt ; un point de l'avocat du diable (magnitudes « probablement surestimées ») a été rejeté après vérification : avec le masque maïs, retirer 2003 augmente les estimations (0,0243 sur 2000-2025, 0,0380 sur 2000-2009), donc la baisse sur 2000-2009 vient de 2003. Rapports et lettre de décision conservés hors dépôt (dossier de travail).

**Tri retenu par l'auteur :** corrections de texte maintenant (v1.1), quatre calculs déclarés ci-dessous, restructuration en article et documentation de la méthode SAA reportées.

**Corrections de texte faites (aucun résultat recalculé) :**
- résumé (et `memoire/arxiv_abstract.txt`), introduction et conclusion : hiérarchie des preuves (62 % de paires exploratoires ; réplication 2000-2009 seule preuve neuve, faible, écart dû à 2003) ; tailles 3,7 % et 5,3 % citées ensemble ; exclusion du Sud-Ouest ; H3 de signe opposé ; message méthodologique ramené à une leçon connue mais décisive ici ;
- datation : les spécifications, le journal et les premiers résultats sont entrés dans le dépôt par le même commit (9945a59 sur la branche, ed07d5d sur l'étiquette d'archive) ; les empreintes attestent la non-modification depuis, pas l'antériorité ; seules D1-D2 ont été commitées avant calcul (intro, §5.4, §10.5) ;
- Conley : « noyau uniforme, sans composante temporelle, tel qu'implémenté par fixest » ; matrices corrigées gardées dans les placebos, p-valeurs mises à NA dans les tables principales (§6, résumé, README) ;
- §5 : équation de H3 ; le SWI lu comme humidité du sol non irrigué (la documentation SIM2 ne mentionne pas l'irrigation) ;
- §7 : tailles de H2b et H2c non mesurées ; hypothèses possibles pour H3, non testées ; l'explication par le relief décrite pour 2003 seulement, avec l'argument d'échelle et la prémisse non testée d'une chaleur commune aux deux modes ; contrôle ensilage possible avec la surface de maïs fourrage, non fait ; valorisation : « because » retiré, surestimation de 2003 chiffrée (≈ 17 %, nouvelle macro `ValOverPct`), ce que le chiffre n'est pas, fourchette qui n'est pas un intervalle de confiance ;
- §10 : chaleur ou étés chauds et secs (corrélation annuelle DD>32 / SWI de −0,59 sur l'échantillon) ; H3 ; E-OBS ; construction statistique possible du partage irrigué / non irrigué (signalée dès `docs/phase0_cadrage.md`) comme principale limite non testée de la variable expliquée ;
- annexe A : reconstruction propre limitée au commit 9f65cb4 ; données brutes ≈ 26 Go ; README harmonisé ; `NOTICE.md` nomme les tables dérivées d'E-OBS et leur clause non commerciale.

## Quatre analyses issues de la relecture, déclarées avant calcul (2026-10-12)

**Non pré-spécifiées**, ajoutées après les résultats à la suite de la relecture simulée. Elles seront rapportées quel que soit leur résultat. Modèle de base : A1 (écart log ~ `dd_32_ja` + `swi_ja` | département + année, poids `surface_ref_ha`, échantillon principal de 17 départements, 435 paires), WCR par année avec poids de Webb, 9 999 tirages, graine de `summarise_term`. Script prévu : `R/21_q1_revue.R` ; sorties : `reports/tables/phase4bis_q1_revue_*.csv`.

- **E1, intervalle de β par inversion du WCR.** Intervalles à 90 % et 95 % (bilatéraux) de β pour A1 : ensemble des β0 pour lesquels le WCR de H0 : β = β0 (sur `ecart_log` − β0·`dd_32_ja`) n'est pas rejeté ; grille de pas 0,0005 de −0,02 à 0,06, affinée par bissection aux bornes. Même calcul pour l'intervalle à 95 % de H1 de la phase 4 (blé 2010-2025), prévu par sa spécification et jamais calculé. La fourchette de valorisation de 2003 sera recalculée aux bornes de l'intervalle à 90 % de E1, à la place de l'intervalle groupé par année. Lecture : descriptive (pas de règle de décision).
- **E2, dépendance aux départements.** (a) A1 en retirant chaque département tour à tour (17 estimations, WCR unilatéral) ; (b) A1 sans les six départements de relief du tableau 5 (01, 26, 38, 39, 63, 69 ; 11 départements restants). **Lecture fixée d'avance pour (b) :** si β > 0 et p unilatérale < 0,05, H1 ne dépend pas des départements de relief ; sinon, H1 est déclarée dépendante de ces départements, et le résumé le dit. (a) est descriptif : on rapporte l'étendue des β et le nombre de p < 0,05.
- **E3, chaleur ou sécheresse.** (a) A1 sans `swi_ja` ; (b) A1 avec le bilan hydrique climatique `prec_ja` − `etp_ja` (mm, juillet-août, masque maïs) à la place de `swi_ja` ; corrélation intra-département entre `dd_32_ja` et ce bilan. **Lecture fixée d'avance :** si β > 0 et p < 0,05 dans (a) et dans (b), l'association ne dépend pas du contrôle d'humidité retenu ; sinon, elle est déclarée sensible à ce contrôle. Dans tous les cas, le texte continue de parler d'étés chauds et secs : ces modèles ne séparent pas la chaleur de la sécheresse.
- **E4, différence entre décennies.** A1 avec l'interaction `dd_32_ja` × 1{année ≤ 2009} (l'effet principal de la décennie est absorbé par les effets année) ; WCR bilatéral sur l'interaction ; même modèle sans 2003. Lecture : descriptive (« différence détectée » ou « non détectée » au seuil de 5 %), sans changer le statut de H1 ni de la réplication.

**Résultats de E1-E4 (2026-10-12).** Calculs lancés à la demande de l'auteur sans commit préalable de la déclaration ; empreinte SHA-256 de `docs/decisions.md` juste avant le lancement : `598cfc5fc4b2b88be9563eadddea708871581a19b5f97557c3781822f4a13ef9` (trace locale, pas un horodatage indépendant). La grille du blé (±0,06 prévue) s'est révélée trop étroite pour l'intervalle à 95 % ; elle a été élargie à ±0,2 au pas de 0,001 avant tout résultat sur le blé.
- E1 : maïs, 90 % [0,0055 ; 0,0438], 95 % [0,0045 ; 0,0490] ; blé phase 4, 95 % [−0,0801 ; +0,0239]. Valorisation 2003 : 16 à 170 M€.
- E2 : sans chaque département, β de 0,0117 à 0,0185, 17 p < 0,05 ; **sans les six départements de relief, β = 0,0098, p = 0,146 : selon la règle fixée, H1 est déclarée dépendante de ces départements**, ce que disent le résumé, l'introduction, le chapitre 7, la discussion, la conclusion et le README.
- E3 : sans SWI, β = 0,0173 (p = 0,001) ; avec P − ETP, β = 0,0124 (p = 0,035) : selon la règle fixée, l'association ne dépend pas du contrôle d'humidité retenu.
- E4 : interaction −0,0113 (p = 0,50) ; sans 2003, +0,0106 (p = 0,77) : aucune différence détectée.
