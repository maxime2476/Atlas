# Spécification figée : test du résultat principal et de la prévision sur les récoltes futures

*Écrite le 2026-10-13, avant la publication de toute donnée de la récolte 2026. Son empreinte SHA-256 est consignée dans `docs/decisions.md`. Elle ne doit plus être modifiée ; tout écart futur sera consigné comme tel. Pour un horodatage indépendant de l'auteur, ce fichier est à déposer tel quel sur un service tiers (OSF ou Zenodo), qui en conservera la date.*

## Pourquoi

La pré-spécification du projet repose sur le journal de l'auteur, sans horodatage externe, et 62 % de l'échantillon de H1 vient des années qui ont suggéré l'hypothèse. Les récoltes 2026 et suivantes sont les seules données que personne n'a encore vues : c'est le test le plus propre du résultat.

## 1. Maïs grain : H1 sur les nouvelles années

- **Données :** SAA, maïs grain irrigué (code 14) et non irrigué (code 15), chiffres **définitifs** de chaque récolte ≥ 2026 ; même population (38 départements) et même échantillon principal (les 17 départements de statut qualité 1 retenus aujourd'hui, liste fixe : 01, 03, 18, 26, 28, 36, 37, 38, 39, 41, 45, 58, 63, 67, 68, 69, 89).
- **Météo :** SIM2, degrés-jours > 32 °C (double sinus) et SWI de juillet-août, masque maïs RPG 2015-2017 inchangé.
- **Modèle :** A1 inchangé : log rendement irrigué − log rendement non irrigué ~ `dd_32_ja` + `swi_ja` | département + année, poids = surface de maïs grain 2010-2012.
- **(i) Chaque année :** A1 réestimé sur 2000 à la dernière récolte définitive, rapporté avec le WCR unilatéral ; aucune autre spécification n'est ajoutée à ce rapport annuel.
- **(ii) Test sur les seules nouvelles années**, dès que **5 récoltes définitives** (2026-2030) sont disponibles : A1 estimé sur ces 5 années ; WCR par année unilatéral à droite (5 grappes, poids de Webb, 9 999 tirages) ; taille mesurée par le même placebo (années permutées). **Règle :** H1 est confirmée sur les nouvelles années si β > 0, p < 0,05 et taille ≤ 10 % ; sinon elle n'est pas confirmée. Avec 5 grappes, la puissance sera faible : un résultat non confirmé ne réfute pas H1, et cela est dit d'avance. Si aucun été chaud (moyenne de `dd_32_ja` < 2 degrés-jours) ne survient sur ces 5 années, le test est déclaré non informatif et reporté à 10 récoltes.

## 2. Prévision du blé : modèles corrigeant la moyenne du département

- **Modèles :** RF_B0 et GBM_B0 tels que définis dans `scripts/28_complements_python.py` (fonction `b0_corrected`), variante principale (entraînement depuis 2010), date du **1er juillet**, mêmes 36 variables météo et mêmes réglages ; référence B0 (moyenne du département sur les années d'entraînement).
- **Chaque année t ≥ 2026 :** entraînement sur 2010 à t − 1, prévision de t avant la publication du rendement provisoire, puis comparaison des MSE (log rendement, pondérés par la surface) au rendement définitif.
- **Conclusion après 5 années :** écart de MSE moyen par rapport à B0 et intervalle à 95 % par bootstrap par blocs d'années. **Règle :** un modèle « bat B0 sur des années nouvelles » si l'intervalle exclut zéro du bon côté ; sinon non.

## 3. Ce qui n'est pas permis

Changer le masque, la fenêtre, le seuil, l'échantillon, les poids, les modèles ou leurs réglages pour ces tests. Toute analyse supplémentaire sur les nouvelles années sera présentée comme exploratoire.
