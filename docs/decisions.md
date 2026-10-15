# ATLAS — Journal des décisions

Chaque entrée indique la date, la décision, qui l'a prise et la justification. Une décision modifiant une spécification déjà fixée doit renvoyer à la version précédente.

| Date | Décision | Par | Justification / conditions |
|---|---|---|---|
| 2026-10-10 | Direction de la phase 0 validée : cœur explicatif (blé tendre d'hiver), module prédictif séparé, maïs irrigué exploratoire, récoltes 2010-2025, population à surface moyenne 2010-2012 ≥ 1 000 ha, *T\** = 32 °C avec repli documenté | Utilisateur | `docs/phase0_cadrage.md` |
| 2026-10-10 | Contribution principale recentrée sur la décomposition chaleur / humidité du sol ; masque RPG rétrogradé en robustesse | Proposé par Claude, validé avec la phase 1 | `docs/litterature.md`, § 7 |
| 2026-10-10 | Identité Git du dépôt : « Maxime Gourguechon » (configuration locale au dépôt). | Utilisateur | — |
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

Demandés par une relecture externe, dans un second temps ; **non pré-spécifiés** dans `specification_phase4bis.md`. Ils sont déclarés ici avant d'être calculés, avec leur règle de lecture. Script : `R/19_q1_power_size.R` ; sortie : `reports/tables/phase4bis_q1_puissance.csv`.

- **Méthode commune** (celle de la taille de H1, `R/14`) : placebo = champ réel `dd_32_ja` à années permutées (dérangement, même permutation pour tous les départements), modèle A1 (`swi_ja` en contrôle, poids `surface_ref_ha`), WCR par année unilatéral à droite au seuil de 5 %, R = 300, B = 399, graines 20261013 puis r.
- **D1, puissance de H1 (2000-2025, 17 départements) :** on ajoute un vrai effet β × placebo à `ecart_log`, pour β = 0 (contrôle : doit redonner une taille proche de 3,7 %), 0,008 (la moitié de l'estimation) et 0,016 (environ l'estimation).
- **D2, taille et puissance de la réplication 2000-2009 (10 grappes) :** même placebo, permutations des seules années 2000-2009 ; β = 0 (taille) et β = 0,011 (environ l'estimation de la réplication).
- **Règle de lecture, fixée avant calcul :**
  - D1 est descriptif : il dit quelle chance le test avait de détecter un effet de cet ordre ; il ne change pas le statut de H1 ;
  - D2 : si la taille dépasse 10 % (le seuil de la règle de décision de la phase 4 bis), la p-valeur de la réplication (0,049) est déclarée non interprétable comme test ; si elle est au plus de 10 %, elle est rapportée avec sa taille. La réplication n'a jamais été une hypothèse principale ; son statut de « même signe » ne change pas.

## Reproduction propre depuis les fichiers bruts (2026-10-12)

- **Procédure :** clone vierge du dépôt dans un autre dossier (état du 2026-10-12, avant les vérifications complémentaires) ; fichiers bruts reliés par liens symboliques (aucun téléchargement) ; environnements recréés par `uv sync --frozen` et `renv::restore()` ; toute la chaîne de `data/README.md` exécutée dans l'ordre (extraction RPG comprise, sans les étapes 01 et 17 de téléchargement), soit environ 1 h 30.
- **Résultat :**
  - les 24 fichiers intermédiaires et finaux de `data/interim/` et `data/processed/` sont identiques à ceux du dépôt de travail, dont le panel maïs (435 paires de l'échantillon principal) ;
  - toutes les tables de `reports/tables/` sont identiques à l'octet, sauf 7 tables de prévision (phases 5 et 6), qui diffèrent d'au plus 5 × 10⁻¹⁵ (arrondis de calcul en virgule flottante) ;
  - `memoire/tables/numbers.tex` et les autres tables du mémoire sont identiques ; les trois figures régénérées donnent un rendu identique (seule la date de création du PDF change) ;
  - 564 tests passent dans le clone, dont les 457 contrôles d'empreinte : les fichiers bruts n'ont pas changé.
- **Limite :** la reproduction utilise les fichiers bruts téléchargés les 10 et 11 octobre 2026 ; un nouveau téléchargement peut donner des fichiers révisés par les producteurs (`data/README.md`).

## Vérification de la mesure de chaleur de Q1 avec E-OBS, déclarée avant calcul (2026-10-12)

Demandée par une relecture externe (sensibilité de H1 à la mesure de chaleur) ; **non pré-spécifiée** dans `specification_phase4bis.md`, exploratoire, ajoutée dans un second temps. Elle sera rapportée quel que soit son résultat. Scripts : `scripts/27_eobs_heat.py`, puis `R/20_q1_eobs.R` ; sorties : `data/processed/weather_dep_eobs_ja.parquet`, `reports/tables/phase4bis_q1_eobs.csv` et `phase4bis_q1_eobs_departement.csv`.

- **Source :** E-OBS v33.0e, Tmin et Tmax journalières, moyenne d'ensemble, grille 0,1° (`docs/sources.md`, § 8 bis). Choisie plutôt qu'Open-Meteo (quotas incompatibles avec 1 784 mailles) et qu'ERA5-Land (compte Copernicus nécessaire ; réanalyse de modèle plutôt qu'interpolation de stations).
- **Seule la température change :** `dd_32_ja_eobs` reprend exactement la définition de `dd_32_ja` (double sinus avec Tmin du jour, Tmax du jour et Tmin du lendemain ; 1er juillet - 31 août de l'année de récolte ; poids du masque maïs RPG 2015-2017). Chaque maille SIM reçoit le point E-OBS le plus proche ; pas de point de remplacement : une maille manquante rend le département-année manquant.
- **Modèle :** A1 identique (écart log ~ `dd_32_ja_eobs` + `swi_ja` | département + année, poids `surface_ref_ha`, 17 départements, 2000-2025, 435 paires) ; `swi_ja` reste celui de SIM, E-OBS n'ayant pas d'indice d'humidité du sol. Seul A1 est réestimé : ni les robustesses, ni la réplication 2000-2009.
- **Test :** WCR par année, unilatéral à droite, 9 999 tirages (`summarise_term`, comme Q1-R9).
- **Lecture fixée d'avance :**
  - si β > 0 et p < 0,05, H1 ne dépend pas de la source de température (SAFRAN) ;
  - sinon, H1 est déclarée sensible à la source de température, et le résumé, le README et le chapitre 7 le disent. Le statut de H1 issu des analyses pré-spécifiées n'est pas réécrit.
- **Lecture descriptive associée (sans règle de décision) :** le niveau des degrés-jours n'est pas comparable entre sources (E-OBS lisse davantage les extrêmes), donc β non plus. Sont rapportés : l'écart-type intra-département de chaque mesure, l'effet d'un écart-type intra-département, la corrélation des deux mesures (brute et intra-département), et une table par département (moyenne 2000-2025 et 2003).
- **Contrôles faits avant cette déclaration, sans calculer de degré-jour :** structure des fichiers (grille, unités, valeur manquante) ; distance maille SIM - point E-OBS d'au plus 0,07° ; 106 mailles littorales du masque sans valeur (point en mer), aucune dans les 17 départements de l'échantillon principal.

**Résultat de Q1-E (2026-10-12) :** β = 0,0148 (1,49 % par °C·jour), p WCR unilatérale = 0,0054, 435 paires (A1 : 0,0158, p = 0,007). Selon la lecture fixée d'avance, H1 ne dépend pas de la source de température (SAFRAN). Lecture descriptive :
- les deux mesures sont corrélées à 0,952 (0,953 en intra-département) ;
- contrairement à ce que la déclaration supposait, E-OBS donne **plus** de degrés-jours > 32 °C que SIM (moyennes départementales 2,6 à 7,3 contre 1,0 à 3,9 ; écart-type intra-département 4,87 contre 3,63) ; la supposition « E-OBS lisse davantage les extrêmes » était fausse pour cette variable, ce qui ne change ni le modèle ni la règle ;
- effet d'un écart-type intra-département : environ 7,5 % avec E-OBS, environ 5,9 % avec SIM.
- **Réserve de procédure :** à la demande de l'utilisateur, la déclaration n'a pas été horodatée de façon externe avant le calcul. Son empreinte SHA-256 (`docs/decisions.md` avant l'ajout de ce résultat) était `2251e0ffca6ffae8bef58b40e1c018700b1cc70e7aecd5b93ce1d4629a288759`, calculée juste avant de lancer `scripts/27_eobs_heat.py` ; c'est une trace locale, pas un horodatage indépendant.

## Relecture simulée (skill academic-research-skills) : tri et corrections de texte (2026-10-12)

Relecture du mémoire par le skill tiers `academic-paper-reviewer` (mode full, copie locale non versionnée) : cinq relecteurs simulés en sous-agents séparés (adéquation, méthodologie, domaine, eau et reproductibilité, avocat du diable). **Les cinq tournent sur le même modèle que celui qui a rédigé une grande partie du texte** : leurs erreurs ne sont pas indépendantes. Décision : révision majeure, sans défaut fatal ni point critique. Les faits décisifs ont été revérifiés dans le dépôt ; un point de l'avocat du diable (magnitudes « probablement surestimées ») a été rejeté après vérification : avec le masque maïs, retirer 2003 augmente les estimations (0,0243 sur 2000-2025, 0,0380 sur 2000-2009), donc la baisse sur 2000-2009 vient de 2003. Rapports et lettre de décision conservés hors dépôt (dossier de travail).

**Tri retenu par l'auteur :** corrections de texte maintenant, quatre calculs déclarés ci-dessous, restructuration en article et documentation de la méthode SAA reportées.

**Corrections de texte faites (aucun résultat recalculé) :**
- résumé (et `memoire/arxiv_abstract.txt`), introduction et conclusion : hiérarchie des preuves (62 % de paires exploratoires ; réplication 2000-2009 seule preuve neuve, faible, écart dû à 2003) ; tailles 3,7 % et 5,3 % citées ensemble ; exclusion du Sud-Ouest ; H3 de signe opposé ; message méthodologique ramené à une leçon connue mais décisive ici ;
- datation : les spécifications, le journal et les résultats sont publiés ensemble ; les empreintes attestent la non-modification depuis la publication, pas l'antériorité, qui repose sur le journal (intro, §5.4, §10.5) ;
- Conley : « noyau uniforme, sans composante temporelle, tel qu'implémenté par fixest » ; matrices corrigées gardées dans les placebos, p-valeurs mises à NA dans les tables principales (§6, résumé, README) ;
- §5 : équation de H3 ; le SWI lu comme humidité du sol non irrigué (la documentation SIM2 ne mentionne pas l'irrigation) ;
- §7 : tailles de H2b et H2c non mesurées ; hypothèses possibles pour H3, non testées ; l'explication par le relief décrite pour 2003 seulement, avec l'argument d'échelle et la prémisse non testée d'une chaleur commune aux deux modes ; contrôle ensilage possible avec la surface de maïs fourrage, non fait ; valorisation : « because » retiré, surestimation de 2003 chiffrée (≈ 17 %, nouvelle macro `ValOverPct`), ce que le chiffre n'est pas, fourchette qui n'est pas un intervalle de confiance ;
- §10 : chaleur ou étés chauds et secs (corrélation annuelle DD>32 / SWI de −0,59 sur l'échantillon) ; H3 ; E-OBS ; construction statistique possible du partage irrigué / non irrigué (signalée dès `docs/phase0_cadrage.md`) comme principale limite non testée de la variable expliquée ;
- annexe A : reconstruction propre limitée à l'état antérieur aux vérifications complémentaires ; données brutes ≈ 26 Go ; README harmonisé ; `NOTICE.md` nomme les tables dérivées d'E-OBS et leur clause non commerciale.

## Quatre analyses issues de la relecture, déclarées avant calcul (2026-10-12)

**Non pré-spécifiées**, ajoutées après les résultats à la suite de la relecture simulée. Elles seront rapportées quel que soit leur résultat. Modèle de base : A1 (écart log ~ `dd_32_ja` + `swi_ja` | département + année, poids `surface_ref_ha`, échantillon principal de 17 départements, 435 paires), WCR par année avec poids de Webb, 9 999 tirages, graine de `summarise_term`. Script prévu : `R/21_q1_revue.R` ; sorties : `reports/tables/phase4bis_q1_revue_*.csv`.

- **E1, intervalle de β par inversion du WCR.** Intervalles à 90 % et 95 % (bilatéraux) de β pour A1 : ensemble des β0 pour lesquels le WCR de H0 : β = β0 (sur `ecart_log` − β0·`dd_32_ja`) n'est pas rejeté ; grille de pas 0,0005 de −0,02 à 0,06, affinée par bissection aux bornes. Même calcul pour l'intervalle à 95 % de H1 de la phase 4 (blé 2010-2025), prévu par sa spécification et jamais calculé. La fourchette de valorisation de 2003 sera recalculée aux bornes de l'intervalle à 90 % de E1, à la place de l'intervalle groupé par année. Lecture : descriptive (pas de règle de décision).
- **E2, dépendance aux départements.** (a) A1 en retirant chaque département tour à tour (17 estimations, WCR unilatéral) ; (b) A1 sans les six départements de relief du tableau 5 (01, 26, 38, 39, 63, 69 ; 11 départements restants). **Lecture fixée d'avance pour (b) :** si β > 0 et p unilatérale < 0,05, H1 ne dépend pas des départements de relief ; sinon, H1 est déclarée dépendante de ces départements, et le résumé le dit. (a) est descriptif : on rapporte l'étendue des β et le nombre de p < 0,05.
- **E3, chaleur ou sécheresse.** (a) A1 sans `swi_ja` ; (b) A1 avec le bilan hydrique climatique `prec_ja` − `etp_ja` (mm, juillet-août, masque maïs) à la place de `swi_ja` ; corrélation intra-département entre `dd_32_ja` et ce bilan. **Lecture fixée d'avance :** si β > 0 et p < 0,05 dans (a) et dans (b), l'association ne dépend pas du contrôle d'humidité retenu ; sinon, elle est déclarée sensible à ce contrôle. Dans tous les cas, le texte continue de parler d'étés chauds et secs : ces modèles ne séparent pas la chaleur de la sécheresse.
- **E4, différence entre décennies.** A1 avec l'interaction `dd_32_ja` × 1{année ≤ 2009} (l'effet principal de la décennie est absorbé par les effets année) ; WCR bilatéral sur l'interaction ; même modèle sans 2003. Lecture : descriptive (« différence détectée » ou « non détectée » au seuil de 5 %), sans changer le statut de H1 ni de la réplication.

**Résultats de E1-E4 (2026-10-12).** Calculs lancés à la demande de l'auteur sans horodatage externe de la déclaration ; empreinte SHA-256 de `docs/decisions.md` juste avant le lancement : `598cfc5fc4b2b88be9563eadddea708871581a19b5f97557c3781822f4a13ef9` (trace locale, pas un horodatage indépendant). La grille du blé (±0,06 prévue) s'est révélée trop étroite pour l'intervalle à 95 % ; elle a été élargie à ±0,2 au pas de 0,001 avant tout résultat sur le blé.
- E1 : maïs, 90 % [0,0055 ; 0,0438], 95 % [0,0045 ; 0,0490] ; blé phase 4, 95 % [−0,0801 ; +0,0239] (erroné : calculé sur les 85 départements ; corrigé dans l'entrée « Audit complet »). Valorisation 2003 : 16 à 170 M€.
- E2 : sans chaque département, β de 0,0117 à 0,0185, 17 p < 0,05 ; **sans les six départements de relief, β = 0,0098, p = 0,146 : selon la règle fixée, H1 est déclarée dépendante de ces départements**, ce que disent le résumé, l'introduction, le chapitre 7, la discussion, la conclusion et le README.
- E3 : sans SWI, β = 0,0173 (p = 0,001) ; avec P − ETP, β = 0,0124 (p = 0,035) : selon la règle fixée, l'association ne dépend pas du contrôle d'humidité retenu.
- E4 : interaction −0,0113 (p = 0,50) ; sans 2003, +0,0106 (p = 0,77) : aucune différence détectée.

## Audit complet : corrections (2026-10-12)

Relecture intégrale du mémoire (47 pages), des scripts R et Python de la phase 4 bis, du README et des documents de résultats. Aucune règle de décision, spécification ni résultat principal n'est modifié.

**Erreur de calcul corrigée (E1, blé).** `R/21_q1_revue.R` estimait l'intervalle du blé sur les 85 départements (`load_panel()` sans filtre, c'est-à-dire la robustesse R4 : β = −0,0151) au lieu de l'échantillon de M1 (83 départements de statut 1, 1 328 observations, β = −0,0149). La déclaration de E1 visait « l'intervalle à 95 % de H1 de la phase 4 », donc M1. Corrigé (`subset(..., echantillon_principal)`), avec deux contrôles : 1 328 lignes, et β identique à `phase4_principal.csv` (dans `R/21` et dans `scripts/26_tables_memoire.py`). Le script a été relancé en entier ; les résultats du maïs (E1 à E4) sont identiques à l'octet près (tables `_departements`, `_humidite`, `_decennies` et lignes du maïs de `_intervalles`). Nouvel intervalle du blé à 95 % : [−0,0795 ; +0,0241], soit −7,6 % à +2,4 % par °C·jour (au lieu de [−0,0801 ; +0,0239]) ; à 90 % : [−0,0695 ; +0,0181]. La conclusion ne change pas (l'intervalle contient zéro).

**Écart de procédure consigné.** La déclaration de E1 annonçait pour le maïs une grille de −0,02 à 0,06 ; le script utilise β̂ ± 0,04 (−0,024 à 0,056), affinée par bissection. Les bornes obtenues (0,0045 à 0,0490) sont intérieures aux deux grilles ; sans effet.

**Incohérences du mémoire corrigées :**
- « Three checks » suivi de cinq puces (introduction) ;
- taille de la réplication : la note du tableau 10 et le § 6.5 disaient « non mesurée » pour les tests à 10 grappes, alors que D2 l'a mesurée (5,7 %) ; corrigé ;
- légende de la figure 1 : « les seuls intervalles disponibles sont ceux du cluster par année » n'était plus vrai depuis E1 ;
- § 3.2 et § 4.1 : « non vérifié » sur le lissage des extrêmes par SIM, alors que la comparaison E-OBS (plus de degrés-jours > 32 °C dans chacun des 17 départements, en moyenne 2000-2025) en fournit une vérification partielle ;
- E2 (b) : « le résultat repose sur ces départements » remplacé par la lecture de la règle déclarée, avec la réserve que la différence de pente entre les deux groupes n'a pas été testée (perte de précision possible, 11 départements et 281 paires) ;
- valorisation : ajout que la formule applique à toute la chaleur excédentaire de l'été, part nationale comprise, une pente identifiée par les écarts entre départements une même année ;
- chapitre 8 : l'intervalle du blé (prévu par la spécification de la phase 4) est désormais cité dans le texte, pas seulement en annexe C ;
- annexe A : les analyses E1-E4 s'ajoutent à la liste de celles qui n'ont pas été reconstruites sur un clone vierge ;
- typographie : signes moins des nombres négatifs hors mode mathématique (−0,0009, −0,47, intervalle du blé) ; guillemet fermant manquant (« soft wheat ») ; 1 674 avec séparateur ; écart de chaleur des départements de relief donné à une décimale (7,5 à 10,3 au lieu de 7 à 10, cohérent avec le tableau 5) ; « mountains » / « uplands » harmonisés ;
- Q1-R9 : « declared after review » remplacé par « added later, declared before » (la relecture visée était celle de la phase 0 ter, à ne pas confondre avec la relecture simulée).

**Documents :** README (phrase orpheline « celle-ci » sur le relief ; R/14-21 ; E1-E4 non reconstruites sur clone ; durée de R/21 ; décompte des robustesses blé : 11 des 12 spécifications qui changent le coefficient) ; `resultats_phase4bis.md` (fourchette de valorisation restée sur l'IC CR1 du premier calcul : 16-170, 3-27, 5-40 M€ ; +2,5 % au lieu de +2,4 % sur 2010-2025) ; `resultats_phase4.md` (intervalle du blé).

## Analyses complémentaires, déclarées avant calcul (2026-10-12)

Demandées par l'auteur après l'audit : pistes d'amélioration, variables nouvelles et méthodes nouvelles. **Aucune n'est pré-spécifiée** dans `specification_phase4bis.md` ; toutes sont exploratoires et seront rapportées quel que soit leur résultat. Elles ne changent ni le statut de H1 ni celui des autres hypothèses de la phase 4 bis. Modèle de base, sauf mention : A1 (écart log ~ `dd_32_ja` + `swi_ja` | département + année, poids `surface_ref_ha`, 17 départements, 435 paires) ; WCR par année, poids de Webb, 9 999 tirages (`summarise_term`) ; placebos à R = 300, B = 399 comme en `R/14`.

**Choix des variables nouvelles.** Seules sont retenues les variables complètes sur la période et l'échantillon utilisés, et jugées faisables : (i) la part irriguée du maïs grain du département (SAA, moyenne 2010-2012, fixe ; complète pour les 17 départements) ; (ii) les surfaces de maïs fourrage irrigué et non irrigué (SAA, feuille FOU, 2010-2025) ; (iii) la puissance éolienne raccordée cumulée (registre national RTE / ODRÉ au 30/06/2026, Licence Ouverte 2.0). Écartées : volumes BNPE (seuil de déclaration, ruptures), dates de semis (pas de série départementale), assurance récolte et aides PAC (pas de série départementale trouvée), retenues de substitution. Les corrélations entre départements des variables retenues (part irriguée, écart d'altitude masque / département, puissance éolienne) sont rapportées ; deux variables corrélées à plus de 0,7 en valeur absolue ne sont pas mises dans le même modèle.

- **G1, relief.** A1 + `dd_32_ja` × 1{département de relief} (01, 26, 38, 39, 63, 69). WCR bilatéral sur l'interaction. Lecture : « différence de pente détectée » si p < 0,05, sinon « non détectée » ; descriptif.
- **G2, ensilage.** 2010-2025, 17 départements : part du maïs non irrigué récolté en fourrage, `s = fourrage non irrigué / (fourrage non irrigué + grain non irrigué)` (surfaces), régressée sur `dd_32_ja` et `swi_ja` | département + année, WCR unilatéral à droite (H : plus de chaleur, plus d'ensilage). Si p < 0,05, le passage du grain à l'ensilage est déclaré « détecté » comme menace plausible et l'estimation de A1 sur 2010-2025 est refaite avec `s` en contrôle (descriptif, `s` étant une conséquence possible de la chaleur) ; sinon « non détecté », sans conclure à l'absence.
- **G3, placebo intra-année (relecture W4).** (a) Taille de H1 quand, chaque année, les valeurs de `dd_32_ja` sont permutées au hasard entre départements (le champ reste sur son année ; R = 300) ; lecture : si ≤ 10 %, la règle de décision est confortée, sinon H1 est requalifiée « non établie » au sens de la règle ; (b) taux de rejet du placebo à années permutées selon l'année qui reçoit le champ de 2003 (permutations de `R/14` rejouées) ; (c) part de chaque année dans Σ x̃² (levier partiel par grappe) ; N_eff et part de 2003 sur 2000-2009 (relecture W8).
- **G4, taille de H2b et H2c.** Même placebo que H1 (dérangement des années), WCR unilatéral à gauche, R = 300, B = 399. Lecture : rapportée à côté de H2b et H2c ; si > 10 %, leurs p-valeurs sont signalées comme non fiables.
- **G5, intensité d'irrigation.** A1 + `dd_32_ja` × (part irriguée − moyenne). WCR bilatéral. Descriptif.
- **G6, pentes départementales (mise en commun partielle).** Pente de `dd_32_ja` propre à chaque département (interactions, mêmes effets année et SWI), puis rétrécissement empirique bayésien vers la moyenne pondérée (estimateur des moments de la variance entre départements). Rapportés : variance entre départements estimée, pentes rétrécies, corrélation avec la part irriguée et l'écart d'altitude. Descriptif.
- **G7, forêt causale.** `grf::causal_forest` sur les variables désaisonnalisées (Y et `dd_32_ja` résidualisés sur les effets département et année et sur `swi_ja`), covariables : part irriguée, écart d'altitude, chaleur moyenne, SWI moyen, latitude ; grappes = années ; test de calibration de `grf` pour l'hétérogénéité. Lecture : hétérogénéité « détectée » si le coefficient de « differential forest prediction » a p < 0,05 ; sinon non détectée. Exploratoire (435 observations).
- **G8, double apprentissage automatique (DML).** Modèle partiellement linéaire : après retrait des effets département et année, Y et `dd_32_ja` sont prédits par une forêt aléatoire à partir de `swi_ja`, `prec_ja`, `etp_ja`, `gdd_0_32_ja`, avec validation croisée par blocs d'années (5 plis) ; β = régression des résidus ; inférence WCR par année sur les résidus. Lecture : comparer β à A1 ; descriptif.
- **G9, autres inférences pour H1.** (a) Jackknife par année (CV3) avec t de Student à G − 1 degrés de liberté, unilatéral ; (b) inférence par randomisation : 5 000 dérangements des années du champ `dd_32_ja`, statistique β̂, p = part des β̂ placebo ≥ β̂ observé ; (c) nombre de matrices de Conley corrigées par fixest dans les placebos de H1 (relecture W5). Lecture : descriptive ; le statut de H1 reste fixé par le WCR.
- **G10, éolien (Kaffine 2019).** Puissance raccordée cumulée au 31 décembre de chaque année (MW, filière éolienne terrestre, par département, d'après la date de mise en service ; installations déraccordées non connues : erreur de mesure sur les premières années), rapportée à la surface agricole (MW pour 10 000 ha de SAU 2010-2012, SAA feuille TER). Modèles : log rendement du maïs irrigué, du maïs non irrigué (17 départements, 2000-2025) et du blé (83 départements, 2010-2025) ~ éolien + météo du modèle correspondant | département + année ; WCR bilatéral. Lecture : descriptive (la croissance de l'éolien suit des tendances départementales que les effets fixes n'absorbent pas).
- **G11, température de surface MODIS (Zhu et Burney 2022 ; Siebert et al. 2017).** MOD11A2 v6.1 (LST de jour, 8 jours, 1 km), juillet-août 2000-2025, agrégée par le masque maïs. Analyses : corrélation avec `dd_32_ja` ; A1 avec la LST moyenne à la place de `dd_32_ja` ; pente de la LST sur `dd_32_ja` selon la part irriguée (refroidissement). Conditionnée à un jeton AppEEARS valide (expiré le 2026-10-12) ; sinon reportée.
- **G12, prévision.** (a) Intervalles conformes à origine glissante : pour l'année test t, quantile 90 % des |résidus| des années test antérieures (à partir de 2018), couverture empirique par modèle ; (b) modèles corrigeant B0 au lieu de B1 (mêmes 36 variables, mêmes réglages), évalués sur 2016-2025 : ces années ont déjà été vues, le résultat est donc exploratoire et ne vaut pas test.

Scripts prévus : `R/22_q1_complements.R` (G1-G7, G9, G10), `scripts/28_complements_python.py` (préparation des variables, G8, G12), `scripts/29_eolien.py` (registre). Sorties : `reports/tables/phase7_*.csv`.

**Résultats des analyses complémentaires (2026-10-12).** Empreinte du journal juste avant le premier calcul : `44054e8a40a4ce1cdce0e1532caae83eff936daac0e159fe5ce17ff5decc1426` (trace locale, sans horodatage externe, à la demande de l'auteur). Détail : `docs/resultats_complements.md`.
- G1 : interaction chaleur × relief +0,0087, p = 0,78 : différence non détectée. G5 : interaction avec la part irriguée, p = 0,42 : non détectée.
- G2 : part fourrage du maïs non irrigué ~ chaleur, p unilatérale = 0,43 : passage à l'ensilage non détecté ; A1 avec ce contrôle non estimé (condition non remplie).
- G3a : taille du placebo intra-année 3,7 % ≤ 10 % : règle confortée. G3b : pas d'année anormale. G3c : 2003 = 41 % du levier (N_eff 4,8) ; 80 % sur 2000-2009 (N_eff 1,5).
- G4 : tailles de H2b 4,0 % et de H2c 2,3 %.
- G6 : τ = 0,0045, Q p = 0,20 ; pentes rétrécies corrélées à −0,44 avec la part irriguée, +0,42 avec l'écart d'altitude.
- G7 : forêt causale, hétérogénéité non détectée (p = 0,99), effet moyen imprécis.
- G8 : DML β = 0,0155, p unilatérale = 0,016.
- G9 : CV3 p = 0,074 ; randomisation p = 0,001 ; 24 % des matrices de Conley des placebos corrigées par fixest.
- G10 : éolien, une seule p < 0,05 (maïs irrigué, signe négatif), qui ne survit pas à Holm sur les 4 tests.
- G11 : non fait (jeton AppEEARS expiré).
- G12 : intervalles conformes trop larges (couverture 95 à 100 % pour 90 % visés) ; modèles d'arbres corrigeant B0 : +11 à +18 % sur B0, intervalle excluant zéro dans 3 cas sur 4, exploratoire (années déjà vues).
- Écarts d'exécution : le contrôle de rejeu des placebos de R/14 a d'abord échoué, à cause d'une tolérance comparée à la valeur arrondie (0,037 au lieu de 11/300) et de l'ordre des tirages ; corrigé avant tout résultat de G3 et G4. `grf` 2.6.1 ajouté à renv (DESCRIPTION, renv.lock). Les fichiers `scripts/29_eolien.py` et `--eolien` dans `scripts/01_download_raw.py` sont nouveaux ; le registre est inscrit au manifeste.

## G11, température de surface MODIS : protocole fixé avant réception des données (2026-10-12)

Commande AppEEARS soumise le 2026-10-12 (tâche `0b1bbe88-8fbf-47c5-b36c-a27fb91934f9`, `scripts/30_lst_appeears.py`) : MOD11A2 v6.1, couches `LST_Day_1km` et `QC_Day`, composites de 8 jours commençant entre le 1er juillet et le 31 août, 2000-2025, contour de la France métropolitaine, GeoTIFF en EPSG:4326. Fichiers bruts dans `data/raw/nasa_appeears_lst/` (séparés du NDVI).

- **Pixels valides :** LST ≠ 0 (valeur manquante) ; bits 0-1 de `QC_Day` = 00 (bonne qualité), ou = 01 avec une erreur de LST d'au plus 2 K (bits 6-7 ≤ 01). LST en °C = valeur × 0,02 − 273,15.
- **Agrégation (comme le NDVI) :** pixel → maille SIM par son centre ; maille valide si au moins 25 % de ses pixels sont valides ; maille → département avec les poids du **masque maïs** RPG 2015-2017, renormalisés sur les mailles valides ; valeur départementale manquante si moins de 50 % du poids est valide.
- **Variable annuelle :** `lst_ja` = moyenne des composites départementaux valides de l'été ; manquante si moins de 6 composites valides.
- **Analyses (lecture descriptive, aucune règle de décision) :**
  - (a) corrélations brute et intra-département de `lst_ja` avec `dd_32_ja` (17 départements) ;
  - (b) A1 avec `lst_ja` à la place de `dd_32_ja` (β par °C de LST ; WCR unilatéral à droite) ;
  - (c) refroidissement, sur les 38 départements de la population : `lst_ja` ~ `dd_32_ja` + `dd_32_ja` × (part irriguée − moyenne) + `swi_ja` | département + année, poids `surface_ref_ha` ; WCR bilatéral sur l'interaction. Une interaction négative est attendue si les surfaces irriguées réchauffent moins la surface par degré-jour d'air (Zhu et Burney 2022). La LST mêle parcelles irriguées et non irriguées dans un même pixel de 1 km, et la mesure est faite vers 10 h 30 (passage de Terra), pas au maximum de température.
- Scripts prévus : `scripts/31_lst_aggregate.py` ; analyses dans `R/23_q1_lst.R` ; tables `reports/tables/phase7_lst_*.csv`.

## Mémoire : intégration des ajouts réorganisée (2026-10-12)

Relecture de l'intégration des vérifications ajoutées dans un second temps. Aucun chiffre ni aucune affirmation ne change ; seule l'organisation du texte change.
- Chapitre 7 réorganisé par question au lieu de l'ordre chronologique des ajouts : résultat principal et précision ; force de l'inférence (nouvelle sous-section, tableau des trois inférences) ; réplication ; robustesses, dont le contrôle d'humidité et le DML ; mesure de la chaleur, dont E-OBS et les départements de relief ; hétérogénéité ; composition des surfaces et ensilage ; valorisation. La convention « added later » et le renvoi à l'annexe C remplacent les mentions de date dispersées ; le tableau récapitulatif des analyses complémentaires est supprimé.
- Éolien déplacé dans la discussion (§ 10.2, « Other changes in the departments ») ; refroidissement par l'irrigation relié à la littérature au § 10.1 ; leçon sur la pluralité des inférences ajoutée au § 10.5.
- Cohérence des chiffres de levier : la part de 2003 (26 % sans pondération au chapitre 4, 41 % dans le modèle pondéré) est expliquée aux deux endroits ; renvois ajoutés aux chapitres 4 et 6.
- Introduction : le jackknife a désormais sa propre puce (« Six checks ») ; résumé reformulé.

## README : diagramme de la chaîne de données (2026-10-12)

Le schéma texte de la section « Architecture et flux de données » du README est remplacé par un diagramme SVG (variantes claire et sombre, choisies par GitHub selon le thème du lecteur), généré par `scripts/32_diagrammes_readme.py`. Mise en page : type « Medallion » de diagram-design (Cathryn Lavery, MIT), retenu parmi les 45 types proposés parce qu'il représente des étages de données de qualité croissante avec leur outil, leur format et leur auteur, ce qui correspond à `raw` → `interim` → `processed` → `reports/tables` → mémoire. Palette par défaut du système (accent mandarine pour l'étage focal, les résultats ; vert olive « publication » pour le mémoire). Adaptations pour GitHub : texte sans `foreignObject`, polices système, étages raccourcis. Aucun fichier du projet diagram-design n'est copié ; attribution dans `NOTICE.md`.

- **Ajout (même jour) :** deux autres diagrammes du même système, générés par le même script (renommé `scripts/32_diagrammes_readme.py`) : un logigramme (type « Flowchart ») de la règle de décision de la phase 4 bis, avec deux exemples réels lus dans `reports/tables/` (maïs H1 : p = 0,007, taille 3,7 % ; blé 1959-2025 : p = 0,125), et une frise (type « Timeline ») des étapes du projet. La frise suit l'échelle réelle par jour (10, 11 et 12 octobre 2026, d'après ce journal) ; dans une journée, seul l'ordre est représenté, ce que dit la légende, pour ne pas espacer également des étapes de durées différentes.

**Résultats de G11 (2026-10-13).** Commande AppEEARS terminée ; 474 fichiers téléchargés et inscrits au manifeste (un composite de 2001, jour 177, sans fichier LST, hors fenêtre) ; 2 413 département-années sur 2 418. Règles appliquées telles que fixées avant réception. (a) Corrélation LST / `dd_32_ja` : 0,63. (b) A1 avec la LST : β = 0,0413 (+4,2 % par °C), p unilatérale = 0,002. (c) Pente de la LST sur `dd_32_ja` : 0,21 °C par degré-jour ; interaction avec la part irriguée −0,149, p bilatérale = 0,051 (signe attendu, non significatif au seuil de 5 %). Détail : `docs/resultats_complements.md`. Le README brut de la commande est exclu du dépôt (`.gitignore`), comme pour le NDVI.

## Trois tests supplémentaires (T1-T3), déclarés avant calcul (2026-10-13)

Demandés par l'auteur ; **non pré-spécifiés**, exploratoires, rapportés quel que soit leur résultat ; aucun ne change le statut de H1. WCR par année (Webb, 9 999 tirages) sauf mention ; placebos comme en `R/14` (R = 300, B = 399).

- **T1, réplication sur le maïs fourrage (2010-2025).** SAA, feuille FOU : lignes 04 (irrigué) et 05 (non irrigué), rendements. Population : départements où les deux modes couvrent au moins 1 000 ha en moyenne sur 2010-2012 (règle du maïs grain ; 28 départements). Seuls 5 ont le statut qualité 1 : l'échantillon principal est donc **les 28 départements**, signalé comme de qualité moindre ; les 5 en statut 1 sont rapportés pour information. Variable expliquée : log rendement irrigué − log rendement non irrigué. Chaleur et SWI : juillet-août, masque du **maïs ensilage** du RPG 2015-2017 (code `MIE`, même méthode que `MIS`) ; si ce code est absent du RPG, le masque du maïs grain est utilisé, et ce choix est consigné. Poids : surface totale de maïs fourrage 2010-2012. Test : WCR unilatéral à droite (16 grappes) ; taille mesurée par placebo. **Lecture fixée d'avance :** si β > 0, p < 0,05 et taille ≤ 10 %, l'association « se réplique sur le maïs fourrage » ; sinon « ne se réplique pas », ce qui ne réfute pas H1 (autre culture, autre récolte, données de moindre qualité). Comparaison descriptive avec A1 du maïs grain sur 2010-2025 (β = 0,0242).
- **T2, falsification par le calendrier (échantillon A1, 435 paires).** (a) A1 avec, ensemble, les degrés-jours > 32 °C de juin, de juillet-août et de septembre de l'année de récolte (masque maïs), et le SWI de juillet-août ; WCR bilatéral sur chaque terme ; lecture descriptive (attendu : effet surtout en juillet-août ; septembre n'est pas un placebo parfait, le remplissage des variétés tardives pouvant s'y prolonger). (b) Placebo pur : A1 + degrés-jours de juillet-août de l'année suivante (t + 1 ; 2000-2024), puis de l'année précédente (t − 1) ; WCR bilatéral sur ces termes. **Lecture fixée d'avance :** une p < 0,05 sur la chaleur de t + 1 est une alerte (l'association capterait un facteur persistant, et non l'été de la récolte) ; pour t − 1, une p < 0,05 est lue comme un effet possible de report (réserves en eau, décisions de surface), non comme une alerte.
- **T3, correction de l'erreur de mesure par variables instrumentales.** A1 où `dd_32_ja` (SAFRAN) est instrumenté (i) par `dd_32_ja_eobs`, (ii) par `lst_ja` (MODIS) ; `fixest`, mêmes effets fixes et poids. Rapportés : β IV, F de première étape (cluster par année), et la forme réduite (écart sur l'instrument) testée par WCR unilatéral à droite, qui est le test valide de β = 0 sous l'hypothèse d'exclusion. **Lecture descriptive :** un β IV supérieur à β MCO est compatible avec une atténuation par l'erreur de mesure. Limites fixées d'avance : E-OBS et SAFRAN partagent des stations, leurs erreurs sont donc corrélées et l'IV E-OBS reste biaisé vers les MCO ; la LST peut agir sur l'écart par un autre canal que la chaleur de l'air (le refroidissement des parcelles irriguées), ce qui menace l'exclusion.

Scripts prévus : `scripts/33_mais_fourrage.py` (masque `MIE`, panel fourrage), `R/24_q1_tests_t1_t3.R` ; tables `reports/tables/phase7_t1_*.csv`, `phase7_t2_*.csv`, `phase7_t3_*.csv`.

**Résultats de T1-T3 (2026-10-13).** Empreinte du journal juste avant le premier calcul : `f2f33eb1780db223669af8db547ace4a8eea371acc0d971d89f52a297186b3cd` (trace locale). Le code RPG `MIE` existe (1,26 à 1,32 Mha selon le millésime) : le masque du maïs ensilage est utilisé comme prévu (`scripts/07_build_wheat_mask.py --culture MIE`).
- T1 : 28 départements, 448 paires 2010-2025 ; β = 0,0160 (+1,6 % par °C·jour), p unilatérale = 0,006, taille du placebo 3,0 % : **selon la règle fixée d'avance, l'association se réplique sur le maïs fourrage**. Statut 1 seulement (5 départements) : +4,0 %, p = 0,083 (information).
- T2 : chaleur de l'été suivant, p = 0,35 (pas d'alerte) ; de l'été précédent, p = 0,17 ; avec juin et septembre dans le même modèle, juillet-août reste à +1,3 % (p = 0,026), juin +4,7 % (p = 0,13), septembre p = 0,45. Constaté après calcul : septembre dépasse presque jamais 32 °C (0,04 degré-jour en moyenne), ce test n'a donc pas de puissance ; il est présenté comme tel.
- T3 : IV par E-OBS, β = 0,0208 (1,3 fois les MCO), F = 65, forme réduite p = 0,005 ; IV par la LST, β = 0,0386 (2,5 fois), F = 13, forme réduite p = 0,002. Lecture comme déclarée : compatible avec une atténuation ; l'exclusion de la LST est douteuse.

## Tests 4 et 5 : non-linéarité, extrêmes combinés, récoltes futures (déclarés avant calcul, 2026-10-13)

Demandés par l'auteur ; **non pré-spécifiés**, exploratoires, rapportés quel que soit leur résultat ; ils ne changent pas le statut de H1. Échantillon A1 (435 paires), WCR par année bilatéral sur les termes testés, sauf mention.

- **N1, forme de la relation (Schlenker et Roberts 2009).** (a) A1 + `dd_32_ja`² ; (b) A1 avec trois tranches de degrés-jours de juillet-août à la place de `dd_32_ja` : 30-32 °C (`dd_30` − `dd_32`), 32-34 °C (`dd_32` − `dd_34`) et > 34 °C (`dd_34`), masque maïs, construites à partir de `weather_dep_month_maize`. Lecture descriptive : la pente croît-elle avec le seuil ? (c) Le 2003 « surestimé de 17 % » est réexaminé avec (a) : valeur prédite de l'écart de 2003 par le modèle quadratique, comparée à l'observé et au linéaire.
- **N2, chaleur et sécheresse combinées (Haqiqi et al. 2021 ; Lesk et al. 2022).** A1 + `dd_32_ja` × (`swi_ja` − moyenne pondérée). Attendu : interaction négative (la chaleur creuse davantage l'écart quand le sol est sec). Lecture descriptive (« détectée » si p < 0,05).
- **N3, déficit de pression de vapeur (Lobell et al. 2013).** Variable nouvelle, construite au niveau maille-jour depuis SIM2 (`TSUP_H`, `T`, `HU`) pour juillet-août 2000-2025 : VPD = es(`TSUP_H`) − `HU`/100 × es(`T`), en kPa, es par la formule de Tetens (0,6108 exp(17,27 T / (T + 237,3))) ; moyenne des jours de juillet-août par maille, puis masque maïs. Modèles : (a) A1 avec `vpd_ja` à la place de `dd_32_ja` ; (b) A1 + `vpd_ja` (chaleur et VPD ensemble) ; corrélation intra-département avec `dd_32_ja`. Lecture descriptive ; si les deux restent séparément significatifs dans (b), le texte dira que la chaleur extrême et la sécheresse de l'air contribuent chacune ; sinon, qu'on ne peut les séparer.
- **P, test sur les récoltes futures.** Une spécification figée, `docs/specification_recoltes_futures.md`, fixe dès maintenant : (i) H1 réestimée chaque année sur 2000 à la dernière récolte, sans rien changer ; (ii) dès que 5 nouvelles récoltes (2026 et suivantes) sont publiées en définitif, test de β > 0 sur ces seules années, WCR unilatéral, même règle (p < 0,05 et taille ≤ 10 %) ; (iii) en prévision, les modèles RF_B0 et GBM_B0 (mêmes réglages que dans `scripts/28_complements_python.py`) comparés à B0 au 1er juillet de chaque nouvelle année, conclusion après 5 années par le bootstrap par blocs d'années. Son empreinte est consignée ici ; un dépôt horodaté par un tiers (OSF ou Zenodo) est recommandé à l'auteur.

Scripts prévus : `scripts/34_vpd.py` (VPD), `R/25_q1_tests_n1_n3.R` ; tables `reports/tables/phase7_n1_*.csv`, `phase7_n2_*.csv`, `phase7_n3_*.csv`.
- **Empreinte de `docs/specification_recoltes_futures.md` (test P), écrite le 2026-10-13 avant toute donnée de la récolte 2026 :** `c4321182e691b6f41cec2d9d9064f665988da00ede56c72330f2fd925f08948a`.

**Résultats de N1-N3 (2026-10-13).** Empreinte du journal juste avant le premier calcul : `75976daad36a1ef96a5aa304f09e2786a93aa7ece0ac01c517fedff4fb04daf2`.
- N1 : terme quadratique −0,0011 (p = 0,13), linéaire 0,0356 ; 2003 prédit 0,203 (quadratique) contre 0,202 (linéaire) et 0,172 observé : la courbure ne corrige pas 2003 ; tranches 30-32 (p = 0,58), 32-34 (+7,9 %, p = 0,14), > 34 °C (p = 0,37) : trop imprécises.
- N2 : interaction chaleur × SWI centré −0,109 (p = 0,20) : signe attendu, non détectée.
- N3 : VPD seul +60 % par kPa (p unilatérale = 0,001) ; avec la chaleur : VPD +64 % (p = 0,002), chaleur −0,2 % (p = 0,76) ; corrélation intra-département 0,76. Selon la règle déclarée, chaleur et VPD **ne peuvent être séparés** ; constat descriptif ajouté au texte : dans le modèle commun, l'association passe au VPD (Lobell et al. 2013). Le résumé, l'introduction, le § 7.7, la discussion et la conclusion lisent désormais le résultat comme portant sur les étés chauds et secs.
- P : `docs/specification_recoltes_futures.md` écrite et empreinte consignée ; dépôt horodaté par un tiers à faire par l'auteur.
- Exécution : champs `month` des notices Crossref retirés de `references.bib` (non reconnus par biber).

## Tests S1-S4, déclarés avant calcul (2026-10-13)

Demandés par l'auteur ; **non pré-spécifiés**, exploratoires, rapportés quel que soit leur résultat ; ils ne changent pas le statut de H1.

- **S1, le VPD sur le maïs fourrage.** VPD de juillet-août (définition de N3) agrégé sur le masque `MIE` ; panel de T1 (28 départements, 2010-2025). Modèles : (a) écart fourrage ~ `vpd_ja` + `swi_ja` ; (b) ~ `dd_32_ja` + `vpd_ja` + `swi_ja`. WCR par année, unilatéral à droite pour (a), bilatéral pour (b). **Lecture fixée d'avance :** si, dans (b), le VPD garde p < 0,05 et les degrés-jours non, la lecture « étés chauds et secs » est confirmée sur une seconde culture ; sinon, elle reste propre au maïs grain.
- **S2, influence de chaque année (maïs grain, A1).** A1 réestimé en retirant chaque année tour à tour (26 estimations, WCR unilatéral à droite) ; rapportés : étendue des β, nombre de p < 0,05, et l'année dont le retrait change le plus β. Descriptif.
- **S3, taille du bootstrap sous corrélation sérielle.** Simulation sur la structure réelle (435 paires, `dd_32_ja` et `swi_ja` réels, mêmes poids et effets fixes) avec un vrai β = 0 : y = facteur commun de l'année × poids départemental tiré N(1 ; 0,5²) + composante propre AR(1) au sein du département, de coefficient ρ ∈ {0 ; 0,3 ; 0,6}, variances égales des deux composantes. R = 300 panels par valeur de ρ, WCR par année unilatéral à droite (B = 399), graines fixées. **Lecture :** si la taille dépasse 10 % pour ρ = 0,3, la règle de décision est déclarée fragile face à une autocorrélation de cet ordre (l'autocorrélation estimée des résidus est 0,08, cf. chapitre 6) ; sinon, confortée.
- **S4, analyse multivers (Simonsohn, Simmons et Nelson 2020).** Toutes les combinaisons disponibles de : mesure (masque maïs 2015-2017, pondération surfacique) × seuil (30, 32 °C) × fenêtre (juillet-août, juillet) × pondération (oui, non) × échantillon (17, 38 départements) × 2003 (inclus, exclu) = 64 spécifications ; plus, pour 32 °C et juillet-août, le masque 2008 (17 départements) et E-OBS × pondération × échantillon × 2003, soit 12 de plus (76 en tout). Le SWI suit chaque fois la mesure et la fenêtre (le masque 2015-2017 pour E-OBS). WCR unilatéral à droite. Rapportés : part des β positifs, part des p < 0,05, médiane des β, et une courbe des spécifications (figure). Descriptif ; aucune spécification n'est substituée à A1.

Scripts prévus : `scripts/34_vpd.py` étendu au masque fourrage, `R/26_q1_tests_s1_s4.R` ; tables `reports/tables/phase7_s1_*.csv` à `phase7_s4_*.csv`, figure `memoire/figures/fig6_multivers.pdf`.

**Résultats de S1-S4 (2026-10-13).** Empreinte du journal juste avant le premier calcul : `d82f70facdfce4ec64ddfc9a8c23ec16d93df61315ac4585957bacb9c97571bb`.
- S1 : fourrage, VPD seul +0,215 par kPa (p unilatérale = 0,012) ; ensemble, chaleur p = 0,30 et VPD p = 0,12 (corrélation 0,77) : **selon la règle fixée, la lecture « étés chauds et secs » n'est pas confirmée sur le maïs fourrage** ; elle reste propre au maïs grain.
- S2 : sans chaque année, β de 0,0134 à 0,0243 ; 26 p < 0,05 sur 26 ; la plus forte variation vient du retrait de 2003 (+0,0085).
- S3 : taille 6,3 % (ρ = 0), 3,7 % (ρ = 0,3), 9,3 % (ρ = 0,6) : selon la règle, confortée pour ρ = 0,3 ; proche de la limite pour ρ = 0,6.
- S4 : 76 spécifications, 76 β > 0, 68 p < 0,05, médiane 0,0242 ; les 8 non significatives utilisent toutes la pondération surfacique (24 significatives sur 32).
- Exécution : axe vertical de la figure étendu jusqu'à zéro après un premier rendu (résultats inchangés, graines fixées).

## Réserve utile des sols et eau d'irrigation (R1, W1, W2), déclarés avant calcul (2026-10-13)

Demandés par l'auteur après l'audit des sources (`docs/sources.md`, § 8 sexies) ; **non pré-spécifiés**, exploratoires, rapportés quel que soit leur résultat ; ils ne changent pas le statut de H1. Déjà vu pendant l'audit, donc avant cette déclaration : les parts du maïs grain dans les surfaces irriguées de 2020 (17 % à 73 %) et quelques volumes BNPE de la Drôme ; aucune RU, aucune régression.

- **R1, hétérogénéité selon la réserve utile des sols.** Donnée : `AWCr_mm_0_200.tif` (INRAE, doi:10.15454/9IRARJ, RU 0-200 cm en mm, éléments grossiers inclus, 90 m, Lambert 93), contrôlé par sa somme MD5 publiée. RU du département = moyenne des pixels dont le centre tombe dans une parcelle `MIS` du RPG, chaque millésime 2015, 2016 et 2017 comptant une fois (le masque maïs de la chaîne, mais à 90 m au lieu de la maille de 8 km) ; département du pixel donné par ADMIN EXPRESS rastérisé sur la même grille ; pixels sans donnée exclus et leur part rapportée. Modèle : A1 + `dd_32_ja` × (RU − moyenne des 17 RU départementales), WCR par année bilatéral sur l'interaction. **Attendu : interaction négative** (sur les sols à faible réserve, la culture non irriguée souffre plus vite et l'avantage de l'irrigation croît davantage avec la chaleur). Rapportés aussi : la corrélation entre RU et part irriguée (G5) ; le modèle avec les deux interactions ; le modèle où le VPD remplace `dd_32_ja` (lecture « étés chauds et secs », N3) ; les 38 départements, pour information. **Limite fixée d'avance :** la RU ne varie qu'entre départements (17 valeurs) ; une interaction non détectée ne montre pas l'absence d'hétérogénéité.
- **W1, les volumes d'irrigation suivent-ils la chaleur ?** Donnée : Hub'Eau « Prélèvements en eau » (BNPE), usage `IRR`, tous ouvrages, statut et mode d'obtention confondus (parts des volumes mesurés rapportées), sommés par département et par année ; fenêtre 2012-2023, commune à toutes les agences. Modèle sur les 17 départements : log volume ~ `dd_32_ja` + `swi_ja` | département + année, poids comme A1, WCR par année (12 grappes) unilatéral à droite ; puis le VPD à la place de `dd_32_ja`. Descriptif (les volumes portent sur toutes les cultures irriguées ; c'est un test du mécanisme supposé, pas un effet).
- **W2, valeur apparente du m³ dans les départements où le maïs domine l'irrigation.** Départements de l'échantillon principal où le maïs grain occupe plus de la moitié des surfaces irriguées en 2020 (RA2020_0052, toutes exploitations) : 01, 03, 18, 63, 67, 68 ; années 2012-2023. Par département et par an : volume attribué au maïs = volume BNPE × part du maïs grain dans la surface irriguée (2020 ; 2010 en sensibilité) ; dose = ce volume / surface de maïs grain irrigué de la SAA (m³/ha) ; écart de rendement observé irrigué − non irrigué (q/ha) ; kg de grain par m³ = 100 × écart / dose ; euros par m³ = écart × prix du maïs (même raccord IPPAP-Eurostat que `scripts/24_valorisation_mais.py`) / dose. **Contrôle de plausibilité fixé d'avance :** une dose hors de 500-3 000 m³/ha (référence : 1 410 m³/ha pour le maïs grain en Occitanie en 2021, enquête Pratiques culturales) exclut le département-année du calcul de valeur, et le nombre d'exclusions est rapporté. Rapportés aussi, en descriptif : les pentes de l'écart (q/ha) et de la dose (m³/ha) sur `dd_32_ja` (mêmes effets fixes, WCR bilatéral) et leur rapport, valeur apparente du m³ supplémentaire des étés chauds. **Lecture :** l'écart observé mêle l'effet de l'eau et les différences entre parcelles irriguées et non irriguées, et la dose repose sur une clé de surface ; c'est une **valeur brute apparente** (sans coûts), comparée sans plus à la marge de 0,20-0,28 €/m³ de la DRAAF Occitanie (2012-2014), qui est une marge nette.

Scripts prévus : `scripts/01_download_raw.py` (options `--ru`, `--bnpe`, `--ra2020`), `scripts/35_reserve_utile.py`, `scripts/36_volumes_irrigation.py`, `R/27_q1_sol_eau.R` ; tables `reports/tables/phase7_r1_*.csv`, `phase7_w1_*.csv`, `phase7_w2_*.csv`.

**Résultats de R1, W1 et W2 (2026-10-13).** Empreinte du journal juste avant le premier calcul : `cf13058b44be375ecfc905a54ed2ead890ebdc58341ca4840def9a9bda824829`.
- Exécution : 36 fichiers bruts téléchargés et inscrits au manifeste (RU, RA2020, 34 extractions BNPE dont le nombre de lignes est contrôlé contre celui annoncé par l'API) ; l'archive 2020 du RA contient aussi le fichier 2010, le script lit donc le fichier qui porte le nom de l'archive. RU rastérisée : 1,632 Mha de maïs en moyenne 2015-2017, contre 1,634 Mha au RPG ; pixels sans donnée ≤ 0,23 % par département. BNPE : 75 ouvrage-années en deux lignes (2,8 Mm³, additionnées comme prévu) ; 99,8 % des volumes mesurés (médiane départementale) ; constaté sans correction : le Rhône tombe à 6,9 Mm³ en 2019 (environ 20 les autres années).
- R1 : RU sous le maïs des 17 départements de 87 à 134 mm (corrélation avec la part irriguée −0,29). Chaleur × RU −0,00008 par mm (p = 0,65) : signe attendu, **non détectée** ; avec la part irriguée, p = 0,53 ; 38 départements (information) p = 0,41, signe inverse. Variante VPD : VPD × RU −0,0026 (p = 0,006), soit une pente du VPD de +66 % par kPa à 87 mm et de +47 % à 134 mm ; test secondaire parmi cinq, sur 17 valeurs de RU : signalé, à confirmer.
- W1 (202 département-années) : log volume ~ chaleur +0,4 % par degré-jour (p unilatérale = 0,28), **non détectée** ; VPD +11,7 % par kPa (p = 0,11) ; SWI −1,60 (p bilatérale = 0,0007) : les volumes suivent la sécheresse du sol plus que la chaleur.
- W2 (6 départements, 72 département-années) : 8 exclues par la règle de dose (6 dans le Puy-de-Dôme, dont la dose médiane est 2 948 m³/ha) ; dose médiane 1 524 m³/ha ; écart médian 31,9 q/ha ; 2,2 kg de grain par m³ ; **valeur brute apparente 0,55 €/m³** (0,46 avec la part de 2010), de 0,17 (63) à 0,96 (18). Étés chauds : dose +74 m³/ha par degré-jour (p = 0,04), écart +0,36 q/ha (p = 0,86), soit environ 0,5 kg par m³ supplémentaire, très imprécis.

## Projections DRIAS (D1), déclarées avant calcul (2026-10-13)

Demandées par l'auteur ; **non pré-spécifiées**, descriptives, sans prise en compte de l'adaptation (Mérel et Gammans 2021) ; elles ne changent pas le statut de H1.

- **Données.** DRIAS, « Simulations EXPLORE2-Climat 2022 : données quotidiennes corrigées par ADAMONT » (NetCDF), licence Etalab (conditions d'utilisation du portail), mention « Drias, données Météo-France, CERFACS, IPSL ». Les 17 couples GCM/RCM disponibles en historique et en RCP 8.5 ; variables `tasminAdjust`, `tasmaxAdjust`, `hussAdjust` ; les 1 582 mailles SAFRAN du masque maïs des 17 départements de l'échantillon principal (même grille que SIM2, vérifiée sur une commande test : coordonnées identiques à 10⁻⁴ ° près). Périodes : historique 1976-2005 ; RCP 8.5 de la première à la dernière année des trois fenêtres TRACC du modèle (fenêtres de 20 ans fournies par le formulaire DRIAS : France +2,0, +2,7 et +4,0 °C ; début ramené à 2021 si plus tôt). Commandes passées par un script Playwright avec le compte de l'auteur (identifiants lus localement dans `.env`, jamais affichés ni versionnés).
- **Variables construites, comme les observées.** Degrés-jours > 32 °C de juillet-août par double sinus (`tasmin`, `tasmax`), moyenne pondérée par le masque maïs ; VPD de juillet-août = es(`tasmax`) − e, avec e = `huss` · p / (0,622 + 0,378 `huss`) et p la pression standard à l'altitude de la maille (FAO-56). Le VPD observé est recalculé de la même façon à partir de `Q` de SIM2 pour la comparaison (le VPD de N3, construit avec `HU`, reste celui du texte).
- **Sorties.** Par modèle, horizon (historique, +2,0, +2,7, +4,0 °C) et département : moyennes de `dd_32_ja` et du VPD ; puis médiane et étendue entre modèles. Contrôle : écart entre l'historique 1976-2005 des modèles et SIM2 sur la même période (attendu faible, ADAMONT étant corrigé sur SAFRAN). Ordre de grandeur, **descriptif** : variation de l'écart log irrigué − non irrigué associée au changement de `dd_32_ja` moyen entre 1976-2005 et chaque horizon, β × Δ, avec l'intervalle à 90 % de β (E1). Ce n'est pas une prévision de rendement : β est estimé sur 2000-2025, l'extrapolation hors du support observé (en particulier à +4 °C) et l'adaptation des pratiques sont des limites fixées d'avance.

Scripts prévus : `scripts/37_drias_telechargement.py` (commandes et téléchargements), `scripts/38_drias_indicateurs.py` ; tables `reports/tables/phase7_d1_*.csv`.

**Résultats de D1 (2026-10-14).** Empreinte du journal juste avant le premier calcul : `f87406bb3964f6ad1f81a18c92087f0c43ac431213ddce176b5739d7a9dbf90f`.
- Exécution : 34 commandes passées et livrées (`data/raw/drias/commandes.csv`), 34 archives (21 Go) inscrites au manifeste ; les archives dépassant 512 Mo, elles sont téléchargées en flux par `atlas.download` à partir des liens de livraison relevés dans la session. Constaté à la lecture : chaque archive couvre toutes les mailles terrestres du rectangle englobant la sélection (5 063) ; les 1 582 mailles du masque y sont toutes, et seules elles sont gardées. Fichiers NetCDF-4 lus avec h5py (dépendance existante) ; résultats identiques à netCDF4 sur une archive test. Plusieurs fenêtres TRACC « +2,0 °C » commencent avant 2021 et sont donc raccourcies (jusqu'à 9 ans pour HadGEM2/HadREM3), comme le fait le portail.
- Contrôle 1976-2005 (moyenne des 17 départements pondérée comme A1) : SIM2 1,02 degré-jour > 32 °C et 1,52 kPa ; modèles 1,00 à 1,51 (médiane 1,28) et 1,42 à 1,68 kPa. Les modèles sont un peu plus chauds que SIM2 dans la queue de distribution ; les écarts sont donc calculés par rapport à l'historique de chaque modèle.
- Horizons (médiane des 17 modèles, étendue entre crochets) : `dd_32_ja` 1,28 [1,00 ; 1,51] en 1976-2005 ; 3,8 [0,8 ; 10,5] à +2,0 °C ; 7,2 [1,5 ; 12,1] à +2,7 °C ; 17,9 [8,9 ; 31,0] à +4,0 °C. Repères observés (SIM2, mêmes poids) : moyenne 2000-2025 1,9 ; 2019 et 2022 environ 4 ; 2003 14,7. VPD : +0,25, +0,42 et +0,78 kPa (médianes).
- β × Δ (médiane de Δ) : écart irrigué − non irrigué +4,2 % à +2,0 °C, +9,7 % à +2,7 °C, +29,7 % à +4,0 °C (intervalle de β à 90 % : 1,4-12,0 %, 3,2-29,2 %, 9,4-106 %). À +4,0 °C, l'été moyen dépasse 2003, seul été aussi chaud du support de β : l'extrapolation est hors du support observé, comme annoncé.

## Relecture critique du mémoire : trois figures (2026-10-14)

Ajoutées à la demande de l'auteur pendant la relecture, par `scripts/39_figures_complements.py` ; **descriptives, sans nouvelle estimation** : (i) écart et chaleur résidualisés sur les effets fixes et le SWI (la pente des résidus est vérifiée égale au β de H1 à 10⁻¹⁰ près ; 2003 porte 41 % de la variance résiduelle pondérée, comme dans le texte) ; (ii) degrés-jours > 32 °C de juillet-août observés 1976-2025 et médianes DRIAS par niveau TRACC (2003 vérifié à 14,7) ; (iii) carte de la population, de l'échantillon principal et des six départements à relief (contours simplifiés à 800 m).

**Corrections du texte issues de la relecture (2026-10-14), sans nouveau calcul.** Contradiction corrigée en discussion (« hot summers » → « dry summers », d'après W1) ; tableau des sources complété (RU INRAE, BNPE/Hub'Eau, RA2020, DRIAS) et mis en flottant ; annexe A mise à jour (taille des données brutes et nombre de tests désormais générés depuis le manifeste et pytest ; DRIAS exige un compte personnel non cessible) ; limites des projections ajoutées (β des degrés-jours alors que le VPD porte l'association ; le modèle linéaire surestimait déjà 2003) ; résumé raccourci ; introduction harmonisée sur six départements à relief (écart de 4,0 à 10,3 degrés-jours) ; écart entre la dose (W2, six départements, par hectare de maïs) et les volumes (W1, 17 départements, toutes cultures) expliqué ; dictionnaire des variables complété ; phrase sur les projections en conclusion. Les détails des §§ 7.8 (hétérogénéité) et 7.9 (composition) passent en annexe G ; le texte principal en garde le résumé et les mêmes p-valeurs.

## Revues simulées du 2026-10-14 : deux analyses déclarées avant calcul (V1, V2)

Quatre revues simulées du mémoire (`docs/revues/`) ont demandé deux calculs. Ils sont déclarés ici avant d'être faits ; ils sont **non pré-spécifiés et descriptifs**, et ne changent pas le statut de H1.

**V1 — Taille et puissance du jackknife CV3 (H1).**
- Statistique : β̂ / se_CV3, avec se_CV3 = √((G−1)/G · Σ_g (β̂_(−g) − β̂)²) sur les G = 26 années, p unilatéral à droite par une loi de Student à G − 1 degrés de liberté (comme G9a dans `R/22_q1_complements.R`).
- Taille : les 300 permutations de R/14 rejouées à l'identique (même construction que dans R/22 ; contrôle : le WCR doit retrouver 3,7 %), avec le placebo dans la régression à la place de `dd_32_ja` ; taux de rejet à 5 %.
- Puissance : les permutations de R/19 (graine 20261013), écart + β_vrai × placebo, β_vrai = 0,008 et 0,016 ; taux de rejet du CV3, comparé à celui du WCR (24 % et 66 % dans R/19).
- Règle de lecture fixée d'avance : taille < 2 % → « le CV3 est conservateur sur ces données ; son p = 0,074 tient surtout à sa faible puissance » ; entre 2 et 8 % → « le CV3 est à peu près calibré ; le désaccord avec le WCR reste une réserve » ; > 8 % → « le CV3 rejette trop souvent sur ces données ».

**V2 — Signatures d'imputation dans la ventilation irrigué / pluvial de la SAA.**
- Données : les paires département-année (échantillon principal, 435 ; population, 981 en complément), rendements en q/ha.
- S1, arrondis : part de rendements entiers par mode et par période de source (série ancienne 2000-2009, SAA 2010-2025). *Constaté avant cette déclaration, lors de la lecture des colonnes : sur les 981 paires, 95 % des rendements irrigués et 61 % des rendements pluviaux sont entiers ; les rapports Y_I/Y_R arrondis au centième les plus fréquents (1,35 à 1,38 ; 1,20 ; 1,25) ont aussi été vus. Aucun autre calcul de V2 n'a été fait.*
- S2, répétition : part des département-années dont le rapport Y_I/Y_R arrondi au centième égale celui de l'année précédente du même département.
- S3, rapports ronds : part des rapports multiples de 0,05.
- Référence de S2 et S3 : 1 000 permutations des années du rendement pluvial à l'intérieur de chaque département (graine 20261018), qui gardent les distributions marginales et les arrondis de chaque mode. Signature retenue si la valeur observée dépasse le 95ᵉ centile des permutations.
- S4, raccord de 2010 : pour chaque département, rang de |Δ écart log| entre 2009 et 2010 parmi les 25 variations annuelles ; part des départements où c'est la plus grande, comparée à 1/25.
- S5 : la répétition (S2) ou un rapport rond (S3) est-elle plus fréquente les étés chauds ? Probabilité linéaire sur `dd_32_ja` avec effets fixes département, p bilatéral par WCR par année.
- S6, conditionnel : si un département a au moins un quart de ses années signalées par S2 ou S3 et que la signature est retenue, H1 est réestimé sans ces départements (WCR unilatéral, 9 999 tirages).
- Règle de lecture fixée d'avance : sans signature (S2 et S3 sous le 95ᵉ centile), « aucune trace d'imputation mécanique n'est détectée ; cela ne prouve pas que la ventilation est mesurée ». Avec signature, on la rapporte et on lit S6 : H1 « n'en dépend pas » si l'estimation reste positive avec p < 0,05, sinon la menace est déclarée « active ». S1 reste descriptif : un arrondi plus rare pour le pluvial est compatible avec un rendement pluvial calculé comme un résidu (production totale moins production irriguée) ; ce n'est pas testé.

Script prévu : `R/28_q1_revues.R` ; tables `reports/tables/phase7_v1_cv3.csv`, `phase7_v2_signatures.csv`.

**Résultats de V1 et V2 (2026-10-14).** Empreinte du journal juste avant le premier calcul : `55c1a73c78fc1f8fa1e894de5e09c3002c602aed7d274c6db1c905ae261a6720`. Script `R/28_q1_revues.R` ; contrôles internes passés (le p du CV3 sur les données réelles redonne 0,074 ; les permutations rejouées redonnent la taille du WCR, 3,7 %, et ses puissances de R/19, 24 % et 66 %).
- **V1.** Taille du CV3 à 5 % : **7,3 %** (300 placebos ; erreur de Monte-Carlo 1,5 point), contre 3,7 % pour le WCR sur les mêmes permutations. Puissance : 32 % (β = 0,008) et 66 % (β = 0,016), contre 24 % et 66 % pour le WCR. Lecture selon la règle : **« à peu près calibré ; le désaccord avec le WCR reste une réserve »**. Le CV3 n'est pas conservateur sur ces données ; sa taille est proche de la borne haute de la zone « calibré ».
- **V2.**
  - S1 : rendements entiers, échantillon principal : irrigué 100 % (2000-2009) et 97 % (2010-2025) ; pluvial 46 % et 53 %.
  - S2 : rapport Y_I/Y_R identique à celui de l'année précédente dans **4,3 %** des 418 transitions, contre une médiane de 0,96 % et un 95ᵉ centile de 1,9 % sous permutation (p de permutation < 0,001) ; population : 2,7 % contre 0,95 % (95ᵉ centile 1,5 %). **Signature retenue.**
  - S3 : rapports multiples de 0,05 : 20,7 %, contre une médiane de 20,6 % sous permutation (p = 0,50) : pas de signature.
  - S4 : la variation 2009-2010 n'est la plus grande variation annuelle dans aucun des 17 départements (attendu sous hasard : 4 %) : pas de rupture visible au raccord.
  - S5 : la part des années signalées ne dépend pas détectablement de la chaleur (pente +0,005 par degré-jour, p bilatéral = 0,18).
  - S6 (déclenché) : 7 départements ont au moins un quart de leurs années signalées (28, 37, 38, 41, 45, 69, 89). Sans eux (10 départements), β̂ = 0,0101 (1,0 %), p unilatéral = **0,063**. Lecture selon la règle : **menace « active »**.
  - Description, sans nouveau test : sur les 18 répétitions, 15 sont dans l'ancienne série (2000-2009), soit environ 10 % de ses transitions, contre 3 dans la série longue (environ 1 %, le niveau du hasard). Deux d'entre elles portent sur 2003 (Eure-et-Loir et Loiret : même rapport qu'en 2002). Les signalements de S6 viennent surtout des rapports ronds (S3), qui ne dépassent pas le hasard pris isolément ; la règle les comptait néanmoins.
- Ce que cela dit, sans aller plus loin : une partie de la ventilation de l'ancienne série semble reconduite d'une année sur l'autre, ce qui est compatible avec une imputation. Une imputation qui reconduit l'écart de l'année précédente tend à **atténuer** la réponse de l'écart à la chaleur (cas de 2003 dans deux départements) plutôt qu'à la créer, mais ce sens n'est pas testé, et la règle déclarée classe la menace comme active.

**Remarques mineures des revues, traitées (2026-10-14), sans nouvelle estimation.**
- Notation : coefficient des jours de crise renommé κ (éq. 5), contrôles du blé φ₁-φ₃ (éq. 6), θ reste l'angle de l'éq. 1 ; poids w_d explicites dans l'éq. 7 ; « 1/(N_years − 1) » au lieu de « 1/(T − 1) ».
- Termes : SIM2 pour le produit (et non « SIM » ou « SAFRAN measure ») ; « department-wide weather » partout, défini au § 4.3 ; « soil wetness index » là où la variable est en jeu.
- Formulations : « resists », « helps » et « the mechanism is » remplacés par des formulations d'association (§§ 7.7, 10.1) ; rapport de sensibilité 2,6 présenté comme un rapport de deux estimations imprécises ; tests et côtés indiqués pour les p ajoutés (dose, volumes, composition) ; égalités du § 7.1 explicites (431, 3, 1).
- Chiffres descriptifs ajoutés (macros, depuis les panels) : SWI de juillet-août 2003, 2019 et 2022 (0,19, 0,27, 0,21 contre 0,38 en moyenne ; parmi les six étés les plus secs depuis 2000) ; valeur de toute la production de maïs grain des 17 départements en 2003 (548 M€ ; la valorisation de 49 M€ correspond à environ 9 % des volumes).
- Valeur par m³ : sens du biais de l'hypothèse « même dose pour toutes les cultures » écrit correctement (si le maïs reçoit plus d'eau, la dose est sous-estimée et la valeur par m³ surestimée). La revue 2 l'avait inversé.
- Tableaux : notes ajoutées aux tableaux 5, 11, 13 et 16. Figures : barre d'échelle et source des contours sur la carte ; attribution DRIAS sur la figure des projections ; intervalle de β rappelé sous la figure des résidus ; courbe des spécifications refaite avec le panneau des choix (`fig10_multivers_choix.pdf`, `scripts/39_figures_complements.py`, depuis `phase7_s4_multivers.csv`, sans nouveau calcul), qui remplace `fig6_multivers.pdf` dans le texte.
- § 7.11 : bilan qualitatif des vérifications ajoutées (celles qui soutiennent, celles qui ne peuvent pas trancher, celles qui nuancent).
- Non faits, parce que ce sont des analyses nouvelles et non des remarques : moyenne SAFRAN/E-OBS, hétérogénéité selon le statut de qualité, humidité du sol dans les projections, réplication sur la récolte 2026.

## Analyses suggérées par les revues (P1-P4), déclarées avant calcul (2026-10-14)

Non pré-spécifiées et exploratoires ; elles ne changent pas le statut de H1. Audit des sources : `docs/sources.md`, § 8 septies.

**P1 — Chaleur moyenne SIM2 / E-OBS.** A1 sur l'échantillon principal (435 couples), avec `dd_32_ja` remplacé par la moyenne de `dd_32_ja` (SIM2) et de `dd_32_ja_eobs` (même masque, même double sinus) ; SWI de SIM2 inchangé. WCR par année unilatéral à droite, 9 999 tirages, taille mesurée par le placebo habituel (300 dérangements des années). Effet aussi exprimé pour un écart-type intra-département de la mesure moyenne. Lecture : association « soutenue avec la mesure moyenne » si p < 0,05 et taille ≤ 10 % ; sinon « non soutenue avec cette mesure ».

**P2 — Hétérogénéité selon le statut de qualité.** Les 38 départements (981 couples) ; A1 avec, en plus, `dd_32_ja` × 1[statut 2] et `swi_ja` × 1[statut 2] (effets fixes département et année inchangés, poids de A1). Test bilatéral par WCR par année de l'interaction chaleur × statut 2 ; β des 21 départements de statut 2 seuls (WCR unilatéral) en complément. Lecture : « les pentes diffèrent » si p < 0,05 ; sinon « pas de différence détectable », sans conclure à l'égalité.

**P3 — Humidité du sol dans les projections.**
- Données : DRIAS-Eau, produit « Indicateurs mensuels 'Eau' par niveau de réchauffement, modèles individuels Explore2 / SIM2 », indicateur `NORSWIAV` (SWI moyen), juillet et août, période de référence et niveaux TRACC France +2,0, +2,7 et +4,0 °C, pour les 17 simulations, sur les 1 582 mailles du masque maïs des 17 départements (mêmes points que D1). Commandes passées par script avec le compte de l'auteur, comme pour D1.
- Construction : par simulation et département, SWI de juillet-août = moyenne des deux mois, moyenne pondérée par le masque maïs ; ΔSWI = niveau − référence de la même simulation. Contrôle : SWI de référence comparé au SWI observé (SIM2) sur la même période, comme dans D1.
- Projection : par simulation, variation de l'écart = β̂ · ΔDD + δ̂ · ΔSWI (β̂ et δ̂ de A1 ; ΔDD de D1, moyenne des 17 départements pondérée comme A1), puis médiane et étendue entre simulations ; on rapporte aussi les deux termes séparément. Intervalle : celui de β (inversion du WCR) avec δ̂ fixé ; aucune incertitude jointe n'est calculée.
- Lecture : descriptive, ordre de grandeur. Si |δ̂ · ΔSWI| médian dépasse la moitié de |β̂ · ΔDD| médian à un niveau, le texte dira que l'humidité du sol change l'ordre de grandeur de la projection à ce niveau.

**P4 — Récolte 2026 : pré-lecture exploratoire, et enregistrement de la prévision figée du blé.**
- Données : Agreste, Conjoncture – Infos rapides Grandes cultures n° 2026-131, fichier départemental (estimations précoces au 1er octobre 2026) ; SIM2 2026, mêmes calculs (double sinus, masque maïs, juillet-août) par un script séparé qui ne modifie aucun fichier existant. La spécification figée exige des chiffres **définitifs** : rien de ce qui suit n'est le test de la spécification figée, qui reste à faire à l'automne 2027 au plus tôt.
- (a) Contrôle : rendements 2025 du fichier (SAA définitive) comparés à ceux du panel (SAA 2025 provisoire), 17 départements.
- (b) Pente transversale de 2026 : pour chaque département, écart 2026 moins effet département et δ̂ · SWI 2026 estimés par A1 sur 2000-2025 ; régression pondérée de ce résidu sur `dd_32_ja` 2026 avec une constante (qui joue l'effet année) ; pente comparée à β̂ et à son intervalle à 90 %, sans inférence propre (17 points, une année).
- (c) A1 réestimé sur 2000-2026 avec 2026 provisoire (WCR unilatéral), présenté comme exploratoire.
- (d) Prévision figée du blé (spécification figée, § 2) : RF_B0 et GBM_B0 entraînés sur 2010-2025, prévision de 2026 au 1er juillet, enregistrée avec son empreinte avant toute comparaison ; comparaison exploratoire aux estimations de conjoncture 2026, la comparaison prévue restant celle au rendement définitif.
- Lecture de (b) et (c) : « cohérent avec H1 » si la pente 2026 est positive et (c) garde p < 0,05 ; sinon on le dit, en rappelant que les données sont provisoires et qu'une seule année ne teste rien.

Scripts prévus : `scripts/40_recolte_2026.py`, `scripts/41_drias_eau.py`, `R/29_q1_suggestions.R` ; tables `reports/tables/phase7_p1_*.csv` à `phase7_p4_*.csv`.

**Résultats de P1, P2 et P4 (2026-10-14).** Empreinte du journal juste avant le premier calcul : `d972032e33bd46c9c8028d8697e2c11565ddf98081835d93c0f2b961bf5e4c57`. Scripts `scripts/40_recolte_2026.py` et `R/29_q1_suggestions.R`.
- **P1.** Chaleur moyenne SIM2/E-OBS (corrélation entre les deux mesures 0,95) : β̂ = 0,0162 par degré-jour (1,6 %), p unilatéral = 0,004 ; taille du placebo 6,0 % (300 dérangements distincts) ; un écart-type intra-département (4,2 degrés-jours) va avec un écart plus large de 7,0 %. Lecture selon la règle : **soutenue avec la mesure moyenne**.
- **P2.** 38 départements : pente des 17 départements de statut 1 dans le modèle joint 1,7 % par degré-jour ; écart de pente du statut 2 +0,8 point, p bilatéral = 0,45 : **pas de différence détectable**. Les 21 départements de statut 2 seuls : 2,2 % par degré-jour, p unilatéral = 0,015.
- **P4.**
  - Données : les rendements 2026 du fichier de conjoncture sont très arrondis et souvent extrêmes pour le pluvial (20 q/ha dans le Cher, la Drôme, l'Indre et l'Indre-et-Loire ; rapports irrigué/pluvial de 1,6 à 4,75, contre une médiane de 1,61 en 2003). Écart médian 2026 : 150 %.
  - Chaleur : 10,6 degrés-jours > 32 °C en juillet-août 2026 en moyenne pondérée sur les 17 départements, 8,7 de plus que leur moyenne 2000-2025 : le deuxième été le plus chaud de la série après 2003.
  - (a) Contrôle 2025 : SAA définitive identique à la provisoire pour l'irrigué sauf dans le Rhône (+3 q/ha) ; pluvial révisé de −4 à +1,5 q/ha, vers des valeurs entières dans le Cher, la Drôme et l'Indre.
  - (b) Pente transversale 2026 : 4,4 % par degré-jour (17 points, sans inférence), dans l'intervalle à 90 % de β (0,55 à 4,5 %), près de sa borne haute. En 2026, l'écart a dépassé la moyenne de chaque département de 0,53 en log, contre 0,14 prédit par β̂ : l'inverse de 2003, où la prédiction dépassait l'observé.
  - (c) A1 sur 2000-2026 : β̂ = 0,0237 (2,4 %), p unilatéral = 0,0009. Lecture selon la règle : **cohérent avec H1**, sur des données provisoires dont la partie pluviale semble établie à dire d'experts ; une seule année ne teste rien, et le test de la spécification figée attend les chiffres définitifs.
  - (d) Prévision du blé 2026 au 1er juillet (RF_B0, GBM_B0, B0) enregistrée dans `reports/tables/phase7_p4_prevision_ble_2026.csv`, SHA-256 `27cb25dfc1c36c4f96d067626d4c2b54202078f1b5ecae2c8f69afcde0427030`, avant toute comparaison ; la comparaison prévue se fera au rendement définitif.
- Précision sur la spécification figée : elle se dit écrite « avant la publication de toute donnée de la récolte 2026 ». C'est inexact pour les estimations de conjoncture, qu'Agreste publie dès août (Infos rapides des 7 août et 1er septembre 2026, au niveau national). Le projet ne les avait pas consultées avant le 2026-10-14 ; la spécification porte sur les chiffres définitifs, qui ne sont pas publiés. Le fichier figé n'est pas modifié.
- **P3.** 68 commandes DRIAS-Eau passées et livrées (`data/raw/drias_eau/commandes.csv`, 68 fichiers texte de 1 582 points × 2 mois, inscrits au manifeste) ; points associés aux mailles du masque par leurs coordonnées (identiques à 10⁻⁴ °). Les fichiers ne précisent pas les années de la période de référence (« Référence »).
  - Contrôle : SWI de juillet-août de référence, médiane des simulations 0,377, contre 0,411 pour le SIM2 observé en 1976-2005 (mêmes poids) ; d'où l'usage des seuls écarts, comme prévu.
  - ΔSWI de juillet-août (médiane, étendue entre simulations) : −0,036 [−0,102 ; +0,037] à +2,0 °C ; −0,059 [−0,119 ; +0,036] à +2,7 °C ; −0,100 [−0,189 ; −0,026] à +4,0 °C.
  - Écart projeté avec la chaleur seule puis avec la chaleur et le sol (médianes) : 4,2 % puis 5,3 % à +2,0 °C ; 9,7 % puis 11,4 % à +2,7 °C ; 29,7 % puis 34,4 % à +4,0 °C (étendue entre simulations à +4,0 °C : 14 à 71 % ; intervalle de β avec δ̂ fixé : 12 à 117 %).
  - Lecture selon la règle : le terme du sol (médiane 0,013 à 0,035 en log) reste inférieur à la moitié du terme de chaleur à chaque niveau : **l'humidité du sol ne change pas l'ordre de grandeur** ; elle élargit l'écart projeté, dans le sens attendu (δ̂ < 0, sols plus secs).

## Audit des dates (2026-10-15)

Dates du dépôt examinées : journal, spécifications, cadrage et littérature, manifeste, commandes DRIAS et DRIAS-Eau, mémoire, bibliographie, NOTICE, CITATION, métadonnées des fichiers. Elles s'échelonnent du 2026-10-10 au 2026-10-15 ; aucune ne se rapporte à une date antérieure au 2026-10-10, hormis des dates de sources externes (versions de données, dépôts de paquets). Aucune entrée passée du journal n'est modifiée.

Corrections (texte du mémoire et bibliographie, sources : fichiers du dépôt) :
- § 7.4 : les estimations Agreste ne sont pas « publiées le 1er octobre 2026 » : ce sont des données arrêtées au 1er octobre (note du fichier), téléchargées le 14 octobre ; la date de publication de l'Infos rapides n'a pas été vérifiée.
- Bibliographie, `drias2022` : « Extraction du 13 octobre 2026 » remplacé par « Commandes du 13 octobre 2026, archives téléchargées les 13 et 14 octobre 2026 » (`data/raw/drias/commandes.csv`, manifeste : 31 archives le 13, 3 le 14).
- § 3 : ajout de la date de lecture des conditions d'utilisation de DRIAS-Eau et de la conjoncture Agreste (14 octobre 2026, NOTICE).
- Références ajoutées pour deux sources utilisées sans notice : DRIAS-Eau (`driaseau2024`) et la conjoncture Agreste (`agreste2026conjoncture`).

Non modifié : la spécification figée, qui se dit écrite « avant la publication de toute donnée de la récolte 2026 » (inexactitude déjà consignée le 2026-10-14) ; les dates des commits ; les dates de formalisation des spécifications.
