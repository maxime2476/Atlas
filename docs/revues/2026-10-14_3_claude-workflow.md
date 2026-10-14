# Revue d'excellence : mémoire ATLAS — méthode `/research-excellence` (nemmerel/claude-workflow)

**Date :** 2026-10-14
**Fichier :** `memoire/main.tex` et ses `\input`

**Exécution.**
- Le modèle claude-workflow (règles, hooks, CLAUDE.md, arborescence `papers/`, conventions Stata) **n'a pas été installé** dans ATLAS : il modifierait la configuration du projet et entrerait en conflit avec son CLAUDE.md.
- La revue combinée `/research-excellence` a été appliquée, avec ses quatre agents (économétrie, article, relecture, réplication) tenus par un seul relecteur, et ses deux barèmes.
- `scripts/quality_score.py` (le correcteur automatique du modèle) n'a pas été exécuté.
- Le skill prévoit d'enregistrer le rapport dans `quality_reports/`. Il a été enregistré hors du dépôt.

## Score

| Barème | Score | Seuil |
|---|---|---|
| `quality-gates.md`, article `.tex` (technique) | **90/100** | ≥ 80 pour commiter : PASS ; ≥ 90 pour soumettre : PASS, à la limite |
| `research-excellence`, barème combiné (fond) | **10/100** | FAIL |

**Détail du barème technique :**
- compilation réussie : 0 ;
- aucune citation indéfinie : 0 ;
- aucune `Overfull \hbox` : 0 ;
- aucun fichier de tableau ou de figure manquant : 0 ;
- aucun renvoi cassé : 0 ;
- notation incohérente entre sections : θ a trois sens, −5 ; SIM, SIM2 et SAFRAN alternent, −5.

**Détail du barème de fond :**
- 2 problèmes d'identification majeurs, −30 : ventilation SAA non contrôlée, taille du CV3 non mesurée ;
- 4 problèmes majeurs de rédaction ou de structure, −40 : projections, unité du résultat, littérature manquante, notes des tableaux 12 et 21 ;
- 10 problèmes mineurs, −20.

**Lecture.** Ce barème est additif et sans plancher : il pénalise une revue exhaustive autant qu'un article faible. Le 10/100 dit seulement qu'il reste six problèmes majeurs. Il ne mesure pas la qualité du mémoire. Le barème technique, plus objectif, place le mémoire au seuil de soumission.

## Résultats par agent

| Agent | Problèmes | Critiques | Majeurs | Mineurs |
|---|---|---|---|---|
| Économétrie | 5 | 0 | 3 | 2 |
| Article | 4 | 0 | 2 | 2 |
| Relecture | 6 | 0 | 1 | 5 |
| Réplication | 1 | 0 | 0 | 1 |

## Audit de réplication (agent `replication-auditor`)

**Méthode.** 25 chiffres du texte ont été recalculés directement depuis les tables de résultats (`reports/tables/*.csv`), sans passer par `scripts/26_tables_memoire.py`, puis comparés aux macros de `memoire/tables/numbers.tex`. Tolérance : égalité à l'arrondi affiché.

**Résultat : 25/25 PASS.** Les chiffres vérifiés :
- H1 : β, % par degré-jour, p unilatéral, taille du WCR ;
- l'intervalle à 90 % (bornes basse et haute) et la réplication 2000-2009 ;
- la courbe de spécification : nombre d'estimations, positives, significatives, médiane, et les comptes de la météo par surface ;
- DRIAS : médianes des degrés-jours aux trois niveaux, écarts β × Δ, VPD à +2,7 °C ;
- W1 : p et N ;
- VPD : seul, conjoint, corrélation.

**Arithmétique des projections.** 100(e^{β·Δ} − 1) a été recalculé avec Δ médian et avec les bornes de β : 4,2 / 9,7 / 29,7 %, et un intervalle de 9,4 à 105,9 % à +4 °C, identiques à la table.

**Nombres écrits à la main.** 317 nombres repérés hors macros dans les chapitres. Ce sont des constantes du design (17, 26, 83, 300, 9 999, seuils, fenêtres), des largeurs de colonnes LaTeX, des chiffres historiques du journal (8,7 % → 6,6 %, 18 et non 27, 1,1 % d'imputations NDVI, erreur Monte-Carlo de 0,002) ou des chiffres externes cités (1 410 m³/ha, 0,20-0,28 €/m³, 1,4 kg/m³, 45 %). **Aucun résultat du projet n'est écrit à la main**, comme l'annonce l'annexe A.

**Chiffre non vérifiable.** [MINOR] La phrase « 2003, 2019, 2022 were also dry » (§ 10.1) n'est appuyée par aucun chiffre. Un renvoi vers le SWI de ces années (déjà calculé dans les panels) la rendrait vérifiable.

**Code.** La concordance entre la théorie et le code a été vérifiée pour A1 par `scripts/39_figures_complements.py`, qui affirme que la pente des résidus FWL égale β à 10⁻¹⁰ près. Le code R n'a pas été réexécuté.

## Problèmes critiques

Aucun. L'identification n'est pas invalide pour l'objet revendiqué, une association descriptive.

## Problèmes majeurs

1. **[Économétrie] La ventilation irrigué/pluvial de la SAA n'est pas contrôlée sur les données** (§ 10.2, dernier paragraphe). C'est la principale limite de la variable expliquée, et elle n'est traitée qu'en mots. Correction : chercher les signatures d'imputation (rapports constants, multiples fixes, sauts en 2010, arrondis selon le mode).
2. **[Économétrie] Le jackknife CV3 n'a pas de taille mesurée** (tableau 11), alors que c'est le seul test valide qui ne rejette pas. Correction : appliquer le placebo des années avec `placebo_size`, ce qui demande de déclarer d'abord l'analyse.
3. **[Économétrie] Projections** (§ 10.3) : la pente est identifiée en coupe et appliquée à un réchauffement commun, à SWI constant. Correction : écrire ces deux limites et retirer le sens net donné à l'erreur.
4. **[Article] L'unité du résultat principal** (« 1.6 % wider gap ») est ambiguë face à « median gap 38 % ». Correction : définir le rapport Y_I/Y_R dès le résumé.
5. **[Article] La littérature la plus proche manque** : Luan et al. (2021, ERL) et Rigden et al. (2020, *Nature Food*).
6. **[Relecture] Tableaux 12 et 21.** Le tableau 12 n'a pas de note. Le tableau 21 donne des noms de variables du code en français et des codes de départements sans noms.

## Problèmes mineurs

7. **[Économétrie] La borne basse de la valeur par m³ est fragile.** Le minimum (0,17 €/m³) vient du Puy-de-Dôme, où la règle de plausibilité a exclu **6 des 12 années**, et sa dose médiane (2 948 m³/ha) touche presque le plafond de 3 000. Correction : signaler dans le § 7.10 que la fourchette repose, à son bas, sur un département à moitié exclu, ou donner la fourchette sans lui (0,42 à 0,96 €/m³ d'après la table W2).
8. **[Économétrie]** Les tests et le nombre de côtés ne sont pas indiqués pour plusieurs p ajoutés : dose (p = 0,039, WCR bilatéral), VPD des volumes (p = 0,114, unilatéral), composition (CR1 par année).
9. **[Article]** « in log points » doit devenir « in log terms » (§ 10.3) ; le renvoi « Figure 1 » doit devenir « Table 5 » (introduction).
10. **[Article]** Les verbes causaux « resists », « helps » et « The mechanism… is » (§§ 7.7 et 10.1) sont à adoucir.
11. **[Relecture]** Notation : θ a trois sens, T deux sens, les poids manquent dans l'éq. (7).
12. **[Relecture]** Nom des sources et des mesures : SIM / SIM2 / SAFRAN, « department-area » / « department-wide ».
13. **[Relecture]** Les tableaux 5, 11, 13 et 16 n'ont pas de notes.
14. **[Relecture]** Les annexes B et D, et les tableaux 19, 21 et 22, ne sont jamais cités par un renvoi.
15. **[Relecture]** Carte sans échelle ; figure 7 sans attribution DRIAS dans sa légende.
16. **[Réplication]** La phrase « 2003, 2019 and 2022 were also dry » n'est appuyée par aucun chiffre.

## Points positifs

- **La chaîne de nombres est exemplaire** : 25 recalculs sur 25 concordent, aucun résultat n'est écrit à la main, et le script s'arrête si les empreintes des spécifications changent.
- **Inférence** : la taille de chaque test principal est mesurée sur les données. Le résultat contraire (CV3) est rapporté au lieu d'être tu.
- **Transparence** : la part exploratoire, les écarts au plan (annexe C) et les résultats nuls sur le blé et la prévision sont rapportés intégralement.

## Recommandation

Le mémoire franchit le seuil technique de soumission. Trois actions sont prioritaires :
1. contrôler la ventilation SAA sur les données ;
2. mesurer la taille du CV3 (à déclarer d'abord) ;
3. corriger le § 10.3 (projections) et l'unité du résultat.
