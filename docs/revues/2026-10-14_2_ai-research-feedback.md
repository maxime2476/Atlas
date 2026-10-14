# Rapport de pré-soumission — méthode `review-paper` (claesbackman/AI-research-feedback)

**Article** : *Summer Heat, Irrigation and Crop Yields in France: Pre-specified Estimates and the Empirical Size of Tests in Panels with Common Shocks*
**Auteur** : Maxime Gourguechon
**Date** : 2026-10-14
**Niveau d'exigence** : revue de champ de premier plan (`top-field`, aucune revue cible donnée)

**Exécution.**
- Le skill prévoit 8 agents en parallèle. Les 8 rôles ont été tenus ici l'un après l'autre par un seul relecteur, sans sous-agents, donc sans indépendance réelle entre eux.
- Fichiers lus : `memoire/main.tex` et ses `\input` (chapitres 00 à 11, annexes A à G, `tables/*.tex`). Les figures ont été vues sur le PDF compilé.
- Les rapports de revue précédents ont été ignorés, comme le demande le skill.
- Le skill prévoit d'enregistrer le rapport dans `memoire/reviews/`. Il a été enregistré **hors du dépôt**, pour ne pas y ajouter de fichiers sans accord.

---

## Appréciation d'ensemble

Le mémoire compare, dans un même département et une même année, les rendements de maïs irrigué et pluvial publiés par la SAA, et relie leur écart à la chaleur extrême. Il mesure la taille réelle de chaque test sur ses propres données.

- **Pour l'avocat**, la contribution est significative pour une revue de champ, du fait de la combinaison données, design et inférence.
- **Pour le sceptique**, elle est incrémentale : c'est un résultat connu à l'étranger, transposé à la France, et l'estimation la plus forte repose sur un seul été.

Le point le plus critique, à l'échelle du design entier, est que la ventilation irrigué/pluvial de la SAA n'est pas documentée. L'écart pourrait refléter une méthode d'estimation. Le mémoire le dit, mais n'a fait aucun contrôle sur les données (Action 1).

**Contribution** : significative (avocat) / incrémentale (sceptique). Le désaccord porte sur un point : l'écart intra-département observé et l'inférence dont la taille est contrôlée constituent-ils un apport en soi, ou une application soignée ?

**Recommandation préliminaire** : *Revise before sending to referees*.

---

## 1. Contribution centrale

### Le plaidoyer (agent 7)

**Contribution revendiquée.** Première estimation, pour la France, fondée sur des rendements irrigués et pluviaux *observés* dans le même département et la même année, de la manière dont l'avantage de l'irrigation varie avec la chaleur extrême. S'y ajoute la démonstration, sur trois panels, que les erreurs-types usuelles rejettent à tort une hypothèse vraie dans 16 à 56 % des cas.

**Types de contribution :** cadre nouveau, données nouvellement assemblées (raccordement de deux éditions de la SAA), réponse méthodologique à un vieux problème (l'inférence en présence de chocs communs).

**À retenir en une ligne :** « Irrigated maize loses about 1 % per hot degree-day, rainfed about 2.5 %; and with weather shocks you must size your tests. »

**Apport par rapport aux travaux les plus proches cités :**
1. *van der Velde et al. (2010)* simulent l'été 2003 avec un modèle de culture. Le mémoire, lui, utilise des rendements observés sur 26 récoltes et des écarts intra-département.
2. *Schauberger et al. (2017)* et *Zaveri et Lobell (2019)* montrent, aux États-Unis et en Inde, une sensibilité plus faible des cultures irriguées. Le mémoire apporte la même direction en France, avec une estimation de l'écart *dans* une même unité et une même année. L'écart retire les chocs communs aux deux modes.
3. *Bertrand et al. (2004)* utilisent des lois placebo. Le mémoire transpose ce placebo aux champs météo réels et en fait une règle de décision publiée avec un module de code.

**Le plaidoyer le plus fort.** Le design en écart est bien choisi : il neutralise ce qui rend l'étude du blé impuissante, et la démonstration en est faite dans le mémoire même (blé : p = 0,374 ; maïs : p = 0,007). La leçon d'inférence est générale et reproductible. Le résultat qui porte la contribution est H1 : il est établi selon la règle, et sa taille est de 3,7 %.

**Note provisoire : Significant**, pour une revue de champ appliquée.

### Le réquisitoire (agent 8)

**La contribution attaquée.**
- Que l'irrigation réduise la sensibilité à la chaleur est un acquis à l'étranger, d'après les papiers que l'auteur cite lui-même.
- Le mémoire le confirme en France, avec un intervalle à 90 % qui couvre un facteur 8 (0,55 à 4,5 %).
- L'été 2003 porte 41 % de la variance utile, et la décennie de réplication se résume à un test sur un été (N_eff = 1,5).
- La leçon d'inférence est reconnue comme « not new » par l'auteur lui-même (conclusion).

**Ce qui est promis et ce qui est livré.**
- L'introduction : « Knowing how the yield advantage … varies with summer heat is a first step towards valuing that water ». Mais la valeur par m³ (0,55 €) est descriptive, porte sur six départements, et sa pente en été chaud n'est pas mesurable.
- « It measures heat where the maize grows » : ce choix porte le résultat sur 2000-2009, alors que la justification par le relief a été trouvée après coup.
- Le résultat change peu les a priori. Sa partie la plus intéressante, le VPD plutôt que la chaleur, reste non séparable.

**Ce qu'il faudrait :**
1. Recentrer la contribution sur le **design en écart et l'inférence dont la taille est contrôlée**, plutôt que sur un « effet de l'irrigation ».
2. Produire un contrôle sur données de la ventilation SAA (Action 1).
3. Relier le VPD à la littérature *demande évaporative × humidité du sol* (Rigden et al. 2020, Luan et al. 2021). Ces deux références ne sont pas dans la bibliographie [UNVERIFIED pour l'agent ; vérifiées par la revue 1].

**Note provisoire : Incremental.**

### Synthèse

Les deux lectures s'accordent sur trois points :
- le design en écart est le bon ;
- l'inférence est exemplaire ;
- la magnitude est imprécise et repose sur 2003.

Le désaccord tient à la façon de présenter la contribution : une découverte sur l'irrigation, ou une méthode et une mesure appliquées avec soin à un cas où l'on peut enfin les tester. L'introduction doit gagner sur ce point. La note reste partagée : *Significant (avocat) / Incremental (sceptique)*.

Le changement qui renforcerait le plus la contribution : recentrer l'introduction sur le design et l'inférence dont la taille est contrôlée, en présentant la magnitude comme secondaire.

*La nouveauté vis-à-vis de la littérature non citée n'a pas été vérifiée par ce skill. La revue 1 l'a fait partiellement.*

---

## 2. Évaluation de l'arbitre (agent 6)

### Identification et crédibilité

**La variation exploitée.** L'écart de chaleur entre départements la même année, une fois retirées les moyennes du département et de l'année. Elle vient surtout de 2003 et de six départements à relief.

**Exogénéité.** La météo est exogène, mais pas l'écart. Les menaces sont bien listées au § 10.2 :
- composition des surfaces (ensilage) ;
- réponse des irrigants ;
- différences de terres ;
- méthode de la SAA.

**Ce qui est fait.** Les tests de calendrier (été suivant, juin, septembre), la composition et la réplication sur l'ensilage répondent bien aux trois premières menaces.

**Ce qui manque.** La quatrième menace, la ventilation irrigué/pluvial produite par les services régionaux, n'est traitée qu'en limite. Un sceptique en séminaire dirait : « si les services régionaux imputent le rendement pluvial à partir d'un jugement d'expert sur la sécheresse, votre β mesure leur jugement ».

**Statut.** Le résultat est correctement présenté comme une association.

**Pour convaincre un public exigeant :**
- un contrôle sur données de la ventilation SAA ;
- la taille du CV3 ;
- une mesure de la chaleur séparée pour l'irrigué et le pluvial (infaisable avec le RPG actuel, ce qui est reconnu).

### Analyses requises et suggérées

**Requises :**
1. [CRITICAL] **Contrôle de la ventilation SAA sur les données.**
   - Chercher les signatures d'imputation : rapports Y_I/Y_R identiques d'une année à l'autre dans un même département, rendements pluviaux égaux à un multiple fixe du rendement total, sauts de l'écart au changement d'édition en 2010, fréquence des arrondis selon le mode.
   - Pourquoi : c'est la seule menace classée par l'auteur comme « main untested limitation of the outcome variable ».
   - Effet d'un résultat favorable : l'absence de signature rend moins probable l'hypothèse d'un écart construit.
2. [CRITICAL] **Taille du jackknife CV3** avec le placebo des années (voir la revue 1, constat 2).
   - Pourquoi : c'est le seul test valide qui ne rejette pas, et sa calibration est inconnue.
   - Effet d'un résultat favorable : si le CV3 est très conservateur, la réserve du résumé tombe ou s'atténue.

**Suggérées :**
1. [MAJOR] **Chaleur moyenne SAFRAN et E-OBS** comme mesure unique, avec la variable instrumentale déjà estimée. Cela réduirait l'erreur de mesure sans choisir une source. Faisable.
2. [MAJOR] **Ventilation 2003 / autres années** dans la courbe de spécification : un panneau d'indicateurs sous la courbe, comme chez Simonsohn et al. (2020), pour voir quels choix déplacent l'estimation. Faisable.
3. [MAJOR] **Réplication sur la récolte 2026** avec la spécification gelée. Elle est déjà prévue. C'est la seule preuve nouvelle possible, qui dépend du calendrier.
4. [MAJOR] **Projection avec l'humidité du sol.** Si DRIAS ou Explore2 fournissent un indicateur d'humidité du sol, ajouter δ·ΔSWI (voir la revue 1, constat 1). Faisabilité à vérifier.
5. [MAJOR] **Hétérogénéité dans les 38 départements**, en interaction avec le statut de qualité, pour savoir si les données de moindre qualité donnent une pente différente (2,2 % contre 1,6 %). Faisable.

### Positionnement dans la littérature

- La couverture est bonne pour la chaleur, l'inférence et la prévision.
- Il manque, pour le maïs irrigué/pluvial, Luan et al. (2021, ERL), et pour la demande évaporative, Rigden et al. (2020, *Nature Food*). Ces deux références ont été vérifiées dans la revue 1.
- Lischeid et al. (2022) est cité pour la thèse « soil moisture less relevant than meteorological drivers ». Ce résumé n'a pas pu être confirmé par la recherche : l'auteur doit le vérifier.
- Ortiz-Bobea et al. (2019) est correctement résumé : humidité du sol pour l'historique, chaleur pour les projections.

### Revue cible et recommandation

Cibles réalistes :
- *European Review of Agricultural Economics* ;
- *American Journal of Agricultural Economics*, qui a publié Mérel et Gammans (2021) ;
- *Environmental Research Letters* ;
- pour la partie méthode, une note dans *Economics Letters* ou dans *Journal of Applied Econometrics* (replication section).

**Recommandation : Revise before sending to referees.** Pour atteindre le niveau requis : les deux analyses requises et une introduction resserrée (une quinzaine de pages au total en moins).

### Questions à l'auteur

1. How are irrigated and rainfed grain-maize yields produced in the SAA at the department level, and is "irrigated" land actually irrigated in the year or merely equipped? What does the data look like for patterns typical of imputation?
2. The cluster jackknife gives p = 0.074. What is its empirical size on your placebo? If it is close to 5 %, why should the reader privilege the wild bootstrap?
3. Your estimate on 2000–2009 rests on one summer (N_eff = 1.5). In what sense is this a replication rather than a re-reading of 2003?
4. Six upland departments carry the significance, and the heat measure matters most there. Can you show the result for the eleven lowland departments with a common, pre-declared alternative measure of heat?
5. If the association is carried by the vapour pressure deficit, should the headline be stated in kPa rather than in degree-days, and do the projections then still hold?
6. The 38-department estimate is larger (2.2 %). Is the quality-status selection pushing the estimate down, and what would that imply for the South-West?

---

## 3. Affirmations non étayées et intégrité de l'identification (agent 3)

### Langage causal excessif
1. [MINOR] **§ 10.1** : « the safest reading of the main result is that irrigated maize *resists* hot, dry summers better ». Le verbe « resists » attribue une capacité au maïs irrigué. Remplacer par « that the advantage of irrigated maize is larger in hot, dry summers ».
2. [MINOR] **§ 10.1** : « Whether irrigation *helps* by supplying water or also by cooling the canopy cannot be told apart ». La phrase présuppose un effet causal. Écrire : « Whether the association reflects water supply or also canopy cooling… ».
3. [MINOR] **§ 7.7** : « The mechanism behind the gap is that irrigated fields receive water that rainfed fields do not ». Le mécanisme est affirmé comme un fait. Écrire : « The presumed mechanism… ».

### Généralisation
4. [MAJOR] **§ 10.3, projections** : on extrapole hors du support et on applique une pente identifiée en coupe à un réchauffement commun (revue 1, constat 1).
5. [MINOR] **Conclusion** : « standard errors … can reject a true null in a large share of cases ». Le constat est limité aux trois panels, ce que le texte dit ensuite. Garder ce lien dans la même phrase.

### Réserves manquantes
6. [MAJOR] **Valeur par m³ (§ 7.10)** : la dose suppose que le maïs reçoit autant d'eau par hectare que les autres cultures irriguées. Cette hypothèse est dite, mais son sens n'est pas discuté : le maïs est souvent plus irrigué que les céréales à paille, ce qui gonflerait la dose et abaisserait la valeur par m³. Ajouter une phrase sur le sens probable de ce biais.
7. [MINOR] **Affirmation de priorité** : « I am not aware of a statistical estimate built on observed irrigated and rainfed yields » (pour la France). L'affirmation est nuancée et la recherche de la revue 1 la soutient, mais l'auteur doit la confirmer avant publication.

### Significativité statistique et économique
8. [MINOR] La valorisation de 2003 (49 M€) est donnée sans ordre de grandeur de comparaison, par exemple la valeur totale du maïs grain des 17 départements cette année-là. Le lecteur ne peut pas juger si c'est beaucoup.

---

## 4. Cohérence interne et renvois (agent 2)

**Vérifications sans écart :** les chiffres du résumé, de l'introduction, de la conclusion et des tableaux 8, 10, 11 et 12 concordent (macros générées). Les points vérifiés : 1,6 %, p = 0,007, 3,7 %, 62 %, 76/68, 16-56 %, 28 départements, p = 0,074, 0,55-4,5 %.

### Incohérences
1. [MINOR] **Introduction ↔ tableau 5** : « by 4.0 to 10.3 degree-days (Figure 1) ». Les écarts figurent dans le tableau 5, pas dans la figure 1.
2. [MINOR] **§ 10.3** : « 0.202 against 0.172 in log points ». C'est faux : il s'agit de différences de log (le § 7.10 écrit « in log terms »).
3. [MINOR] **§ 7.10** : la pente de la dose (p = 0,039) n'indique ni le test ni le nombre de côtés.
4. [MINOR] **§ 7.1** : « all but 4 … (it is lower in 1) » laisse au lecteur le soin de déduire qu'il y a 3 égalités.

### Dérive terminologique
5. [MINOR] **SIM2 / SIM / SAFRAN / SAFRAN–ISBA** désignent la même source : « 5.9 % with SIM » (§ 7.6), « SIM is a reanalysis » (§ 9.1), « the SAFRAN measure » (§ 7.6). Fixer une règle : SIM2 pour le produit, SAFRAN pour la grille.
6. [MINOR] **« department-area weather » / « department-wide weather » / « Department area »** désignent la même mesure. Choisir un nom et s'y tenir.
7. [MINOR] **« soil moisture » / « soil wetness » / « SWI »** : l'estimand dit « holding soil moisture fixed » alors que la variable est un indice. Écrire « soil wetness (SWI) » partout où la variable est en jeu.

### Citations
8. [MINOR] **Lischeid et al. (2022)** : le résumé de leur résultat reste à vérifier par l'auteur (voir la section 2).

---

## 5. Mathématiques et notation (agent 4)

1. [MINOR] **Éq. (7)** : β̂ − β = Σx̃ε / Σx̃². L'estimation est pondérée, mais les poids w_d n'apparaissent pas. Écrire Σ w x̃ ε / Σ w x̃², ou préciser « with weights absorbed in x̃ and ε ».
2. [MINOR] **Le symbole θ a trois sens** : l'angle de l'éq. (1), le coefficient des jours de crise dans l'éq. (5) et les coefficients θ₁ à θ₃ des contrôles du blé dans l'éq. (6). Renommer le coefficient de l'éq. (5), par exemple en κ.
3. [MINOR] **Le symbole T a deux sens** : la température (§ 4.1) et le nombre d'années dans « 1/(T − 1) » (§ 6.4). Écrire « 1/(N_years − 1) ».
4. [MINOR] **Unités** : « % per DD » est défini comme 100(e^β̂ − 1), mais la figure 2 indique « 1.58 log points per degree-day ». Les deux sont justes, à condition de signaler une fois la différence.
5. Les éq. (1) et (2) sont correctes ; l'équivalence entre l'éq. (4) et le modèle empilé tient, avec les mêmes poids dans les deux modes.

---

## 6. Tableaux, figures et documentation (agent 5)

### Tableaux sans notes ou aux notes incomplètes
1. [MAJOR] **Tableau 12 (robustesse du maïs)** : aucune note.
   - Il manque : la définition de « p boot. one-sided », la pondération, les effets fixes, le contrôle SWI, le nombre de tirages, et le fait que « Without 2003 » perd 17 observations.
   - Correction : copier la note du tableau 10.
2. [MAJOR] **Tableau 21 (blé, annexe D)** :
   - noms de variables du code en français (`dd_32_remplissage`, `dd_32_mjj`, `dd_32_m2s`, `dd_32_p2s`) dans un tableau en anglais ;
   - « Without 84, 30, 48 » donne des codes sans noms de départements.
   - Correction : des libellés en anglais (« DD>32, May–June », « May–July », « shifted −2 weeks ») et les noms des départements.
3. [MINOR] **Tableau 16** : le tiret « — » de la colonne bilatérale des vérifications de robustesse n'est pas expliqué.
4. [MINOR] **Tableaux 5, 11, 13** : sans notes. Pour le tableau 5, préciser les poids des altitudes et le sens du signe de « Area − mask ». Pour le tableau 11, définir CV3 et la randomisation. Pour le tableau 13, rappeler les poids et les effets fixes.

### Figures
5. [MINOR] **Figure 4 (courbe de spécification)** : il manque le panneau d'indicateurs qui montre, pour chaque estimation, les choix retenus. Sans lui, la figure ne dit pas *quels* choix déplacent l'estimation, ce que le texte affirme pourtant (la météo par surface).
6. [MINOR] **Figure 2** : pas de bande d'incertitude. C'est acceptable pour un nuage de résidus, mais on peut ajouter dans la légende l'intervalle à 90 % de β.
7. [MINOR] **Figure 1 (carte)** : pas d'échelle. La source des contours (IGN ADMIN EXPRESS) n'est pas dans la légende.
8. [MINOR] **Figure 7** : la légende ne mentionne pas la licence ni l'attribution « Drias, données Météo-France, CERFACS, IPSL ». Elles sont dans la ligne Sources du tableau 2, mais une figure peut circuler seule.

### Renvois
9. [MINOR] **Tableaux jamais appelés par un renvoi** : 19 (dictionnaire), 21 et 22 (robustesse complète). Les annexes B (variables) et D (robustesse complète) ne sont jamais citées par un renvoi (`\cref`), seulement nommées dans le plan ; l'annexe F l'est bien depuis le § 4.1. Ajouter un renvoi vers l'annexe B au § 3 et vers l'annexe D au § 7.5 et au § 8.1.

---

## 7. Orthographe, grammaire et style (agent 1)

Aucun mot de remplissage (« interestingly », « importantly », « notably », « clearly », « obviously ») n'a été trouvé dans les sources.

1. [MINOR] **Pourcentages** : « 1.6 % » avec une espace fine, conformément à STYLE.md. C'est cohérent dans tout le texte.
2. [MINOR] **§ 10.3** : « Two features of the estimate push in the same direction » est ambigu (revue 1, remarque de rédaction 1).
3. [MINOR] **Chiffres en lettres** : « 17 departments », « 26 harvests », mais « six departments » et « five clusters ». La règle (chiffres en lettres sous 10) est appliquée. RAS.
4. [MINOR] **Cohérence de la première personne** : « I » est utilisé partout. RAS.

---

## Actions prioritaires

**CRITICAL**
1. Recentrer la contribution (synthèse en « Incremental » par le sceptique) : l'introduction doit présenter d'abord le design en écart et l'inférence dont la taille est contrôlée, la magnitude venant ensuite.
2. Contrôler la ventilation irrigué/pluvial de la SAA sur les données (signatures d'imputation).
3. Mesurer la taille du jackknife CV3.

**MAJOR**
4. Projections : ajouter la limite de la pente identifiée en coupe et du SWI tenu fixe (§ 10.3).
5. Note complète pour le tableau 12.
6. Tableau 21 : libellés en anglais et noms de départements.
7. Valeur par m³ : discuter le sens du biais de l'hypothèse « même dose pour toutes les cultures ».
8. Citer Luan et al. (2021) et Rigden et al. (2020).
9. Suggestions de l'arbitre : moyenne SAFRAN/E-OBS, panneau d'indicateurs, hétérogénéité selon le statut de qualité.

**MINOR**
10. « in log points » → « in log terms » (§ 10.3).
11. Renvoi de l'introduction : Figure 1 → Table 5.
12. Uniformiser SIM2/SAFRAN, « department-area », « soil wetness ».
13. Renommer le θ de l'éq. (5) ; mettre les poids dans l'éq. (7) ; remplacer T dans « 1/(T−1) ».
14. Ajouter des notes aux tableaux 5, 11, 13 et 16.
15. Ajouter un renvoi vers les tableaux 19, 21 et 22 et vers les annexes B et D.
16. Verbes « resists », « helps », « the mechanism is » (§ 7.7, § 10.1).
17. Comparer la valorisation de 2003 à la valeur totale de la production.
18. Vérifier le résumé de Lischeid et al. (2022).
19. Échelle et source sur la carte ; attribution DRIAS sur la figure 7.

**Nombre de points par catégorie** : CRITICAL 3, MAJOR 6, MINOR 10. Les points listés dans les sections détaillées sont plus nombreux, car certains ont été regroupés ici. Aucun fichier de tableau ou de figure n'a été exclu comme non référencé.
