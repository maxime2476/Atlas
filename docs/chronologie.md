# Chronologie du projet ATLAS et traçabilité des décisions

Ce document distingue quatre choses que l'on confond facilement :

- **la conception** d'une décision, c'est-à-dire le moment où l'idée a été envisagée ;
- **sa formalisation**, la date à laquelle elle est écrite dans un document du dépôt ;
- **le calcul** qu'elle commande, la date d'exécution ;
- **la dernière modification** du fichier qui la porte.

Les dates de formalisation et de calcul proviennent du journal (`docs/decisions.md`), des spécifications et des documents datés du dépôt. Elles ne sont pas modifiées ici.

## Statuts de preuve

- **Documenté** : attesté par un fichier daté du dépôt (journal, spécification, document « Rédigé le… », manifeste, table de résultats, commit).
- **Déclaration rétrospective de l'auteur** : rapporté par l'auteur après coup, sans trace contemporaine identifiée dans le dépôt. La confiance indiquée est **subjective**, celle de l'auteur ; ce n'est pas une mesure.
- **Non documenté** : aucune trace et aucune déclaration.

## Synthèse : d'août au 14 octobre 2026

| Période | Activité | Statut | Confiance (subjective) |
|---|---|---|---|
| 11 au 31 août 2026 | Premières lectures et exploration de la littérature sur le sujet | Déclaration rétrospective de l'auteur ; aucune trace dans le dépôt | Déclarée par l'auteur comme un souvenir |
| Septembre 2026 | Approfondissement bibliographique ; réflexion sur les hypothèses et les approches empiriques envisageables | Déclaration rétrospective de l'auteur ; aucune décision individuelle datée | Déclarée par l'auteur comme un souvenir |
| Septembre 2026 | Premières recherches de sources de données et essais techniques préliminaires, distincts des traitements, calculs et spécifications documentés en octobre | Déclaration rétrospective de l'auteur ; aucun fichier, script ni téléchargement de cette période dans le dépôt | Déclarée par l'auteur comme un souvenir |
| 1er au 9 octobre 2026 | Consolidation du travail préparatoire avant la constitution des traces du dépôt | Déclaration rétrospective de l'auteur ; aucune décision datée | Déclarée par l'auteur comme un souvenir |
| 10 octobre 2026 | Cadrage (phase 0), revue de littérature (phase 1), audit des sources, environnement, masques et météo, spécifications des phases 4, 5 et 6, estimations du blé, de la prévision et du maïs exploratoire, protocole NDVI | Documenté | — |
| 11 octobre 2026 | Nouvelle question (écart irrigué / non irrigué), phase 0 bis, spécification 4 bis, estimations principales, audit (phase 0 ter), masque 2008, premiers commits | Documenté | — |
| 12 octobre 2026 | Taille et puissance des tests, reproduction sur une copie neuve, E-OBS, relecture simulée, audit complet, analyses complémentaires, température de surface | Documenté | — |
| 13 octobre 2026 | Tests T, N et S, spécification figée pour les récoltes futures, réserve utile et eau, projections DRIAS | Documenté | — |
| 14 octobre 2026 | Relecture critique et figures, revues simulées, analyses V1-V2 et P1-P4 | Documenté | — |
| 15 octobre 2026 | Audit des dates, présent document | Documenté | — |

**Lecture.**

- **Le dépôt ne contient aucune trace antérieure au 10 octobre 2026.** Cette absence ne permet pas, à elle seule, de conclure que le travail préparatoire déclaré par l'auteur n'a pas eu lieu : des lectures, des réflexions ou des essais ne laissent pas forcément de fichier. Elle ne permet pas non plus de le confirmer. Les périodes d'août à début octobre reposent uniquement sur la déclaration de l'auteur.
- **Le travail documenté du 10 au 15 octobre a été mené avec un assistant de programmation IA (Claude Code).** La colonne « Par » du journal le montre pour une partie des décisions (« proposé par Claude, validé par l'utilisateur ») ; `docs/revues/` décrit les revues simulées.
- **Aucune décision du tableau ci-dessous n'a de date de conception antérieure à octobre.** L'auteur n'en a confirmé aucune individuellement. On en ajoutera une seulement si l'auteur la confirme, avec le statut « déclaration rétrospective ».

## Dates des fichiers

Le 2026-10-15 vers 13 h 45, un outil externe (le plugin watermarks-remover) a réécrit la plupart des fichiers du dépôt. Leur contenu est resté identique, sauf les métadonnées PDF de `memoire/main.tex`. En revanche, leurs dates de création et de modification ont été remplacées par celle du 15 octobre. Les dates du système de fichiers ne renseignent donc plus sur l'âge des fichiers.

Plus tôt le même jour, avant cette réécriture, les dates suivantes ont été relevées lors de l'audit :

| Fichier | Date de création relevée |
|---|---|
| `docs/phase0_cadrage.md` | 2026-10-10 00:18 |
| `docs/litterature.md` | 2026-10-10 00:27 |
| `docs/specification_phase4.md` | 2026-10-10 12:43 |
| `reports/tables/phase4_principal.csv` | 2026-10-10 12:45 |
| `reports/tables/phase5_synthese.csv` | 2026-10-10 14:07 |
| `reports/tables/phase6_mais_taille.csv` | 2026-10-10 14:36 |
| `docs/specification_phase4bis.md` | 2026-10-11 17:40 |
| `docs/specification_recoltes_futures.md` | 2026-10-13 01:46 |

Les commits (à partir du 2026-10-11) et les empreintes SHA-256 des spécifications, consignées dans le journal et vérifiées par `scripts/26_tables_memoire.py`, ne dépendent pas du système de fichiers et restent valables.

## Tableau de traçabilité

« Conception » : « le jour même » quand le journal montre une décision prise et écrite dans la même séance (proposition validée, analyse déclarée après un audit ou une revue) ; « non documentée » sinon. « Calcul » : date d'exécution attestée par le journal, un document de résultats ou la date relevée d'une table.

| Décision | Conception | Formalisation | Calcul | Source | Statut |
|---|---|---|---|---|---|
| Direction de la phase 0 (blé, module prédictif, maïs exploratoire) | Non documentée | 2026-10-10 | — | Journal, tableau ; `docs/phase0_cadrage.md` (« Rédigé le 2026-10-10 ») | Documenté (formalisation) |
| Contribution recentrée sur la décomposition chaleur / humidité du sol | Le jour même (« proposé par Claude, validé ») | 2026-10-10 | — | Journal, tableau | Documenté |
| Python 3.12 avec `uv` ; décompression du RPG par 7z | Non documentée | 2026-10-10 | — | Journal, tableau | Documenté (formalisation) |
| Allongement vers 1990 (Schauberger), conditionnel puis retenu en robustesse | Non documentée | 2026-10-10 | 2026-10-10 (évaluation des critères) | Journal, tableau et § « Critères pour l'allongement » | Documenté (formalisation, calcul) |
| Priorité du masque blé en cas de verdicts divergents | Le jour même (« proposé par Claude, validé ») | 2026-10-10 | 2026-10-10 | Journal | Documenté |
| Échantillon principal blé : 83 départements de statut 1 | Non documentée | 2026-10-10 | — | Journal, tableau (« protocole de la phase 0 ») | Documenté (formalisation) |
| Robustesses supplémentaires de la phase 4 (sans pondération, sans 84, 30, 48, sans 2025) | Le jour même (« proposé après l'audit de la phase 3 ») | 2026-10-10 | 2026-10-10 | Journal | Documenté |
| Règle de repli du seuil thermique (32 °C, sinon 30 °C) | Non documentée | 2026-10-10, « AVANT le comptage » | 2026-10-10 | Journal | Documenté (formalisation, calcul) |
| Spécification de la phase 4 (blé 2010-2025) | Non documentée | 2026-10-10 (SHA-256 `2a63ada21156…`) | 2026-10-10 (table relevée à 12 h 45) | `docs/specification_phase4.md`, journal, `docs/resultats_phase4.md` | Documenté |
| Spécification de la phase 5 (prévision) | Non documentée | 2026-10-10 (`4c9e77872165…`) | 2026-10-10 (14 h 07) | `docs/specification_phase5.md`, `docs/resultats_phase5.md` | Documenté |
| Spécification de la phase 6 (maïs exploratoire, valorisation, NDVI) | Non documentée | 2026-10-10 (`843f8531055a…`) | 2026-10-10 (14 h 36) | `docs/specification_phase6.md`, `docs/resultats_phase6.md` | Documenté |
| Écarts et ajouts aux phases 4, 5 et 6, dont la comparaison à B0 | Le jour même, après les premiers résultats | 2026-10-10 | 2026-10-10 | Journal ; annexe C du mémoire | Documenté |
| Protocole NDVI fixé avant réception des données | Non documentée | 2026-10-10 | Après réception des données (phase 6) | Journal | Documenté (formalisation) |
| Phase 0 bis : question principale sur l'écart irrigué / non irrigué | Non documentée | 2026-10-11 | — | `docs/phase0bis_cadrage.md` (« Rédigé le 2026-10-11 »), journal | Documenté (formalisation) |
| Phase 2 bis : panels maïs 2000-2025 | Non documentée | 2026-10-11 | 2026-10-11 | `docs/phase2bis_donnees.md`, journal | Documenté |
| Spécification de la phase 4 bis (A1, M3, règle de décision) | Non documentée | 2026-10-11 (`88e15f6290de…`) | 2026-10-11 (« Estimations du 2026-10-11 ») | `docs/specification_phase4bis.md`, `docs/resultats_phase4bis.md` | Documenté |
| Phase 5 bis | Non documentée | 2026-10-11 | 2026-10-11 | Journal | Documenté |
| Audit de la phase 0 ter et corrections | Le jour même (audit) | 2026-10-11 | 2026-10-11 | `docs/phase0ter_audit.md`, journal | Documenté |
| Robustesse Q1-R9 : masque maïs 2008 | Le jour même, déclarée avant estimation | 2026-10-11 | 2026-10-11 | Journal | Documenté |
| Audit avant HAL : écarts et corrections | Le jour même | 2026-10-11 et 2026-10-12 | — | Journal | Documenté |
| Diagnostics de puissance et de taille de Q1 | Le jour même, déclarés avant calcul | 2026-10-12 | 2026-10-12 | Journal | Documenté |
| Reproduction depuis les fichiers bruts | Le jour même | 2026-10-12 | 2026-10-12 | Journal ; annexe A | Documenté |
| Mesure de chaleur E-OBS | Le jour même, déclarée avant calcul | 2026-10-12 | 2026-10-12 | Journal | Documenté |
| Relecture simulée et quatre analyses qui en découlent | Le jour même | 2026-10-12 | 2026-10-12 | Journal | Documenté |
| Audit complet et analyses complémentaires (G1-G10) | Le jour même, déclarées avant calcul | 2026-10-12 | 2026-10-12 | Journal (empreinte avant calcul) | Documenté |
| Protocole G11 (température de surface MODIS) | Le jour même, avant réception des données | 2026-10-12 | 2026-10-12 | Journal | Documenté |
| Tests T1-T3 ; non-linéarité et extrêmes (N) ; S1-S4 | Le jour même, déclarés avant calcul | 2026-10-13 | 2026-10-13 | Journal (empreintes avant calcul) | Documenté |
| Spécification figée pour les récoltes futures | Non documentée | 2026-10-13 (`c4321182e691…`) | À venir (chiffres définitifs de 2026, automne 2027 au plus tôt) | `docs/specification_recoltes_futures.md`, journal | Documenté ; calcul prévisionnel |
| Réserve utile et eau d'irrigation (R1, W1, W2) | Le jour même, déclarées avant calcul | 2026-10-13 | 2026-10-13 | Journal | Documenté |
| Projections DRIAS (D1) | Le jour même, déclarées avant calcul | 2026-10-13 (commandes le 13) | 2026-10-14 | Journal ; `data/raw/drias/commandes.csv` ; manifeste | Documenté |
| Trois figures ajoutées à la relecture | Le jour même | 2026-10-14 | 2026-10-14 | Journal | Documenté |
| V1 (taille du CV3) et V2 (signatures d'imputation de la SAA) | Le jour même, après les revues simulées | 2026-10-14 (empreinte `55c1a73c…`) | 2026-10-14 | Journal ; `docs/revues/` | Documenté |
| P1-P4 (chaleur moyenne, statut, sol projeté, récolte 2026) | Le jour même, après les revues simulées | 2026-10-14 (empreinte `d972032e…`) | 2026-10-14 | Journal ; `data/raw/drias_eau/commandes.csv` | Documenté |
| Prévision figée du blé 2026 (RF_B0, GBM_B0) | Non documentée (prévue par la spécification figée du 13) | 2026-10-14 (SHA-256 du fichier consigné) | 2026-10-14 ; comparaison au définitif à venir | `reports/tables/phase7_p4_prevision_ble_2026.csv`, journal | Documenté ; comparaison prévisionnelle |
| Audit des dates | Le jour même | 2026-10-15 | — | Journal | Documenté |

## À venir (prévisionnel)

| Échéance | Activité |
|---|---|
| Dès que possible | Dépôt de `docs/specification_recoltes_futures.md` sur OSF ou Zenodo, pour un horodatage indépendant de l'auteur |
| Printemps 2027 | SAA 2026 provisoire |
| Automne 2027 | SAA 2026 définitive : premier rapport annuel prévu par la spécification figée ; comparaison de la prévision du blé 2026 |
| 2030 ou plus tard | Test sur cinq récoltes nouvelles (spécification figée, § 1 (ii)) |
