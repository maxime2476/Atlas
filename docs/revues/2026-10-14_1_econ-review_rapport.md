# Revue 1 — méthode `econ-review` (hanlulong/econ-paper-review-skill)

- Objet : `memoire/main.pdf` (61 pages), état du 2026-10-14 après les corrections de la relecture précédente.
- Mode : `full`. Pas de revue d'adéquation à une revue scientifique (option non demandée).
- Exécution : la méthode du skill a été suivie à la main. Son environnement géré, ses validateurs et son finaliseur (`finalize_review.py`) **n'ont pas été exécutés** (règle du projet sur les skills tiers). Le paquet signé (PDF de revue, registres JSON) n'existe donc pas. Ce rapport en tient lieu.
- Code et données : lus sans être exécutés. Une seule vérification a été faite sur les tables : le tableau 12, où deux coefficients égaux sont une coïncidence réelle (0,010418 et 0,010444).
- Recherche de littérature : 5 requêtes web, sans le titre ni les phrases du mémoire.

## Ce que le mémoire établit (digest de reconstruction)

**Question.** L'avantage de rendement du maïs grain irrigué sur le maïs pluvial s'élargit-il les étés très chauds ?

**Objet estimé.** La pente β de ln Y_I − ln Y_R sur les degrés-jours au-dessus de 32 °C en juillet-août :
- mesurés sur le masque des parcelles de maïs ;
- avec des effets fixes département et année, et le SWI comme contrôle ;
- pondérés par la surface 2010-2012 ;
- sur 17 départements (statut de qualité 1) et 435 couples département-année, 2000-2025.

**Inférence.** Bootstrap sauvage restreint (WCR) par année. La taille du test est mesurée par un placebo qui permute les années.

**Statut.** Association descriptive, pré-spécifiée après une exploration de 2010-2025. La réplication sur 2000-2009 est faible. Le résultat est sensible à la mesure de la chaleur et aux six départements à relief, et il passe par le VPD quand celui-ci entre dans le modèle.

**Hypothèses maintenues :**
- aucune composition des surfaces (irrigué / pluvial / ensilage) ne varie avec la chaleur à l'intérieur d'un département ;
- la ventilation irrigué / pluvial de la SAA ne dépend pas de la météo de l'année.

Ce qui fonctionne et doit être préservé :
- la mesure de la taille des tests sur les données elles-mêmes ;
- l'annonce honnête de la part exploratoire (62 %) ;
- la courbe de spécification ;
- le recensement complet des écarts (annexe C) ;
- la séparation stricte entre association et effet causal.

Aucune des remarques ci-dessous ne remet en cause ces points.

## Littérature la plus proche et différences essentielles

- **Luan, Bommarco, Scaini et Vico (2021)**, *Environmental Research Letters* 16(6), doi:10.1088/1748-9326/abfc76.
  - L'étude utilise les rendements de comtés américains publiés séparément pour l'irrigué et le pluvial (maïs et soja, 1970-2010). Elle montre que les rendements pluviaux sont les plus faibles par temps chaud et sec, et que l'irrigation atténue les deux stress.
  - C'est le comparateur le plus direct du design du mémoire, qui ne le cite pas. Li et Troy (2018) sont cités, mais seulement pour l'Ouest américain.
  - La différence qui subsiste : la France, l'écart intra-département et intra-année, la mesure sur les parcelles et l'inférence dont la taille est contrôlée.
- **Rigden, Mueller, Holbrook, Pillai et Huybers (2020)**, *Nature Food* 1(2), 127-133.
  - Les rendements de maïs américains sont mieux prédits par la combinaison de la demande évaporative et de l'humidité du sol que par la température et la précipitation.
  - Surtout, une projection fondée sur la seule demande atmosphérique indiquerait environ **deux fois** les dommages.
  - Ce papier appuie la lecture « VPD » du § 7.7 et pèse directement sur les projections du § 10.3 (voir le constat 1).
- **Pour la France**, aucune estimation statistique fondée sur des rendements irrigués et pluviaux observés n'a été trouvée. La recherche n'a renvoyé que van der Velde et al. (2010, 2012) et Hawkins et al. (2013), déjà cités. La phrase « I am not aware of… » reste défendable, mais seulement dans les limites de cette recherche.

---

## Constats de fond, par gravité

### 1. [Majeur] Les projections appliquent une pente identifiée en coupe à un réchauffement commun, à humidité du sol constante

**Texte concerné.**
- § 10.3 : « Multiplying the median change by β̂ gives a gap between irrigated and rainfed maize larger by about 4 %, 10 % and 30 % ».
- § 7.10 : « a slope that is identified from differences between departments within a year; in the regression, the national part of each summer is absorbed by the year effects. A simple check suggests it overstates the 2003 figure by about 17 % ».

**Problème.** Le mémoire signale lui-même, pour la valorisation, que β est identifié par les écarts entre départements au sein d'une année, alors que la projection applique β à un déplacement *national* de la chaleur. La même raison vaut pour les projections, et c'est même leur cas typique : tout le réchauffement y est commun. Or le § 10.3 n'en parle pas.

S'y ajoute un second point. β est mesuré « à humidité du sol donnée », mais la projection ne fait varier que les degrés-jours. Le terme δ·ΔSWI est absent, alors que les sols seront probablement plus secs (δ̂ = −0,35). Il manque donc un canal, dans un sens qui élargit l'écart. Rigden et al. (2020) montrent qu'ignorer l'humidité du sol dans une projection peut doubler les dommages estimés. Le signe de l'erreur nette est donc inconnu, alors que le texte conclut « more likely too high than too low ».

**Pourquoi c'est important.** Les +4 / +10 / +30 % sont les seuls chiffres du mémoire tournés vers l'avenir. Le lecteur les retiendra.

**Suggestions.**
1. Ajouter au § 10.3 la phrase de la valorisation : le réchauffement projeté est commun à tous les départements, alors que β est identifié par les écarts entre départements.
2. Écrire que la projection laisse le SWI inchangé (DRIAS fournit l'humidité du sol par d'autres produits, non téléchargés ici) et que ce choix joue en sens inverse.
3. Remplacer « more likely too high than too low » par « of unknown net direction ».
4. Option plus forte : ne garder que la comparaison des chaleurs (l'été médian à +4 °C est plus chaud que 2003) et supprimer les pourcentages d'écart. Le message principal du paragraphe tient sans eux.

**Résolu quand** le § 10.3 mentionne les deux limites et ne donne plus de sens net à l'erreur.

### 2. [Majeur] Le jackknife CV3 contredit le test de référence, et sa taille n'a pas été mesurée

**Texte concerné.**
- Tableau 11 : « Cluster jackknife by year (CV3), t with 25 d.f. — 0.074 — not measured ».
- § 7.3 : « the result is not significant under every reasonable inference ».

**Problème.** Le mémoire a pour fil conducteur de mesurer la taille de chaque test sur les données. Mais le seul test valide qui contredit H1 n'a pas été soumis à ce contrôle. Avec une année qui pèse 41 % de la variance utile, le CV3 peut être très conservateur, avec une taille bien inférieure à 5 %. Si c'est le cas, son p = 0,074 renseigne sur la puissance, pas sur la validité. S'il est au contraire correctement calibré, le désaccord est réel.

**Pourquoi c'est important.** C'est l'une des trois réserves du résumé, et le mesurer coûte peu : la fonction `placebo_size` du module `wcr` accepte une liste de tests.

**Suggestions.** Déclarer puis mesurer la taille et la puissance du CV3 avec le placebo habituel (300 répétitions), et lire le résultat selon une règle fixée d'avance :
- si la taille est inférieure à 2 %, écrire que le CV3 est conservateur sur ces données ;
- si elle est proche de 5 %, garder la réserve telle quelle.

**Résolu quand** le tableau 11 donne une taille pour le CV3.

### 3. [Majeur] L'unité du résultat principal est ambiguë

**Texte concerné.**
- Résumé : « each degree-day is associated with a 1.6 % wider gap ».
- § 7.1 : « The median gap is 38 % ».

**Problème.** L'écart est un log-ratio, et 1,6 % est la variation relative du rapport Y_I/Y_R : un écart médian de 38 % passe à environ 40 %, soit +2,2 points. Rapprochée de « gap 38 % », la formule « 1.6 % wider gap » peut aussi se lire comme +1,6 point de pourcentage ou comme +1,6 % de 38 %. La note du tableau 10 définit l'unité (100(e^β − 1)), mais ni le résumé ni l'introduction ne le font.

**Suggestions.** Écrire une fois, dans le résumé et dans l'introduction : « raises the ratio of irrigated to rainfed yield by 1.6 % per degree-day (at the median, an advantage of 38 % becomes about 40 %) ». Ces chiffres sont à générer par macro, pas à calculer à la main.

**Résolu quand** l'unité est définie à la première occurrence.

### 4. [Majeur] Le comparateur international le plus proche manque

**Texte concerné.** § 2.2 et tableau 1 : « Direct evidence abroad; indirect evidence for France ».

**Problème.** Luan et al. (2021) utilisent exactement le même type de données (rendements publiés séparément pour l'irrigué et le pluvial) et trouvent le même schéma chaud-et-sec. Sans eux, le lecteur ne peut pas situer la contribution. Rigden et al. (2020) manquent aussi : ils soutiennent la lecture par le VPD et posent une limite aux projections.

**Suggestions.**
- Ajouter les deux références au § 2.2 et au § 2.1 (rôle de l'eau).
- Dans le tableau 1, préciser que la preuve directe à l'étranger inclut des données publiées séparément, et que la différence tient à l'échelle intra-département et à l'inférence.

**Résolu quand** les deux références sont citées avec la différence exacte.

### 5. [Mineur] Le rapport « 2.6 fois plus sensible » et la part de « 38 % » sont donnés sans incertitude

**Texte concerné.**
- § 7.2 : « Rainfed maize is about 2.6 times more sensitive to heat ».
- § 10.1 : « irrigated maize keeps about 38 % of the heat sensitivity ».

**Problème.** Ce sont des rapports de deux coefficients. L'intervalle de β va de 0,55 à 4,5 %, donc celui du rapport est certainement large. Le mot « about » ne le dit pas.

**Suggestions.** Calculer un intervalle par bootstrap par année (les tirages existent déjà), ou écrire « several times » et renvoyer aux deux coefficients.

### 6. [Mineur] Les inférences des vérifications ajoutées ne sont pas toujours nommées

**Texte concerné.**
- § 7.10 : « the dose rises (74 m³/ha per degree-day, p = 0.039) », sans test ni nombre de côtés (dans `scripts/26_tables_memoire.py:692`, c'est un WCR bilatéral).
- § G.2 : « p = 0.58, clustered by year ».
- § 7.7 : `p = 0.114` pour le VPD des volumes.

**Problème.** Le mémoire fait de l'inférence son argument central. Le lecteur doit donc savoir, pour chaque p, de quel test il vient et de combien de côtés.

**Suggestions.** Indiquer le test et les côtés à chaque p du § 7.7, du § 7.10 et de l'annexe G. Option : un tableau en annexe qui liste chaque vérification ajoutée avec sa règle de lecture déclarée, son inférence et son résultat. Le tableau 20 le fait en partie, mais sans les résultats.

### 7. [Mineur] Mauvaise unité dans la nouvelle phrase des projections

**Texte concerné.** § 10.3 : « (0.202 against 0.172 in log points) ».

**Problème.** 0,202 et 0,172 sont des différences de log, c'est-à-dire 20,2 et 17,2 points de log. Le § 7.10 écrit correctement « in log terms ».

**Suggestion.** Remplacer « in log points » par « in log terms ».

### 8. [Mineur] Un renvoi de l'introduction pointe vers la carte

**Texte concerné.** Introduction : « understates the heat … by 4.0 to 10.3 degree-days (Figure 1) ».

**Problème.** La figure 1 situe les départements, mais les écarts de chaleur sont dans le tableau 5.

**Suggestion.** Écrire « (Table 5; Figure 1 shows where they lie) ».

### 9. [Mineur] Le nombre de vérifications ajoutées appelle une lecture prudente des vérifications significatives

**Texte concerné.** Tableau 20, dernière ligne (plus de 30 vérifications ajoutées après audit) ; le résumé s'appuie sur la réplication sur l'ensilage et sur la courbe de spécification.

**Problème.** Chaque vérification a été déclarée avant d'être calculée, et la plupart sont présentées comme exploratoires. Mais le résumé met en avant celles qui soutiennent le résultat. La courbe de spécification ne couvre que les choix de mesure, pas cette famille de vérifications.

**Suggestion.** Une phrase dans le § 7.11 : « of the N checks added later, k support the association, m are uninformative, and the VPD and upland checks qualify it ». Les comptes sont à générer depuis le journal des décisions.

---

## Synthèse éditoriale

**Diagnostic.** Le cœur empirique est solide et honnête. Ce qui reste à corriger tient à deux endroits :
- **l'extrapolation des projections** (constat 1) ;
- **l'asymétrie du contrôle de taille** : il manque la taille du CV3 (constat 2).

Les constats 3 et 4 améliorent la lisibilité et le positionnement sans toucher aux résultats.

**Posture.** Révision mineure à modérée pour un mémoire de M2. Seul le constat 2 demande un nouveau calcul, et il faut d'abord le déclarer.
