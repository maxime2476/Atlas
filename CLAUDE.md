# ATLAS — Instructions pour Claude Code

## 1. Mission du projet

ATLAS est un projet individuel de recherche appliquée à l'intersection de l'économétrie, de la Data Science, du Machine Learning et de l'analyse géospatiale. L'objectif est de construire une chaîne reproductible allant de sources publiques documentées à des résultats descriptifs, prédictifs et, uniquement si le plan d'identification le permet, causaux.

Le sujet précis, la zone géographique, la période, l'unité d'observation et les sources ne sont pas encore considérés comme validés. Ils doivent être décidés pendant la phase 0 après un audit de faisabilité.

## 2. Règle de travail : une phase à la fois

- Respecte le plan de phases défini dans la conversation ou dans la documentation du dépôt.
- Ne passe pas à la phase suivante sans demande explicite de l'utilisateur.
- Avant de coder, reformule brièvement l'objectif de la phase, les fichiers concernés et les critères de réussite.
- Si une décision scientifique ou une donnée essentielle manque, signale-la et propose une décision argumentée au lieu de l'inventer.
- À la fin d'une phase, indique les fichiers créés/modifiés, les commandes exécutées, les tests et contrôles effectués, les résultats observés et les limites restantes.

## 3. Niveau et style de code attendus

Le code doit être celui d'un étudiant de Master 2 en économétrie appliquée qui maîtrise les outils et cherche à produire un travail sérieux, pas celui d'une équipe de plateforme senior.

- Privilégie un code clair, explicite, lisible et facile à expliquer en entretien.
- Utilise des fonctions lorsqu'elles évitent une vraie répétition ou isolent une opération cohérente, mais ne transforme pas chaque ligne en fonction.
- Une répétition raisonnable est acceptable si elle rend le déroulement plus compréhensible.
- Évite les architectures génériques, les abstractions prématurées, les classes sans besoin clair, les systèmes de plugins maison et les couches de configuration inutiles.
- N'ajoute pas de microservices, Kubernetes, orchestration complexe ou framework d'agents sans besoin démontré.
- Commente le raisonnement et les choix non évidents, pas chaque instruction triviale.
- N'introduis pas de dépendance uniquement parce qu'elle est populaire ou impressionnante.
- Ne prétends jamais que le code a été exécuté si tu ne l'as pas exécuté.

## 4. Rigueur scientifique

Distingue systématiquement trois types de résultats :

1. **Descriptif** : décrit les données et les associations observées.
2. **Prédictif** : évalue la capacité de généralisation à des observations non utilisées pour l'entraînement.
3. **Causal** : nécessite une stratégie d'identification explicite et des hypothèses défendables.

Ne présente jamais une corrélation, une importance de variable, une performance prédictive ou un coefficient de régression comme un effet causal sans justification.

Avant tout modèle, documente :
- la question et l'estimand visés ;
- l'unité d'observation, la période et la population étudiée ;
- la construction des variables et leurs unités ;
- les critères d'inclusion et d'exclusion ;
- les valeurs manquantes, les doublons et les changements de définition ;
- les risques de biais, de fuite de données et de sélection ;
- les limites de couverture et de mesure.

Pour toute conclusion importante, distingue le résultat observé de son interprétation. Ne fabrique jamais de résultats, de citations, de références, de métadonnées ou de valeurs de performance. Si un résultat n'a pas été calculé, écris qu'il reste à calculer.

## 5. Sources et données

- Audite les sources avant de construire le pipeline.
- Vérifie l'existence réelle des données, les formats, la couverture temporelle et géographique, la fréquence, la licence, les conditions d'accès et la stabilité des identifiants.
- Ne suppose pas que deux jeux de données sont compatibles parce qu'ils concernent le même sujet.
- Établis la compatibilité des unités spatiales et temporelles avant toute jointure.
- Conserve les données brutes téléchargées sans les modifier. Les transformations doivent produire des fichiers distincts.
- Ne versionne pas de gros fichiers bruts, de secrets ou de données dont la licence interdit la redistribution.
- Documente les URL, dates d'accès, versions, licences et procédures de téléchargement lorsque c'est possible.
- Si les données ne peuvent pas être téléchargées automatiquement, documente une procédure manuelle reproductible et les limites.

## 6. Choix technologiques

Utilise chaque technologie pour une responsabilité identifiable :
- **Python** : ingestion, nettoyage, traitement de données, géospatial, Machine Learning, automatisation et éventuellement API.
- **R** : économétrie appliquée, modèles de panel, inférence et visualisations statistiques lorsque cela est pertinent.
- **SQL/DuckDB** : exploration et agrégation de données tabulaires volumineuses lorsque cela simplifie réellement le travail.

Le choix final dépendra des sources et de la question scientifique. N'impose pas artificiellement toutes les technologies à chaque phase. Évite de dupliquer le même travail dans Python et R sans raison méthodologique.

Utilise `uv` et `uv.lock` pour Python. Utilise `renv` et `renv.lock` si un environnement R reproductible devient nécessaire. Les interfaces entre langages doivent rester simples, de préférence Parquet ou CSV avec schéma et unités documentés.

## 7. Qualité et reproductibilité

- Ajoute des tests pour les transformations importantes, les schémas, les clés, les plages de valeurs et les agrégations.
- Contrôle explicitement les cardinalités des jointures et les changements du nombre de lignes.
- Sépare les données brutes, intermédiaires et finales.
- Fixe les graines aléatoires quand cela est pertinent et documente les sources de non-déterminisme.
- Évite les chemins absolus propres à une machine.
- N'ajoute pas de test qui ne teste qu'un détail d'implémentation sans valeur scientifique ou technique.
- Pour les modèles prédictifs, utilise une validation cohérente avec la structure temporelle et/ou spatiale des données. Ne fais pas de découpage aléatoire naïf si cela provoque une fuite entre observations proches.
- Pour l'économétrie, vérifie les spécifications, les erreurs-types, les échantillons et la sensibilité des résultats.

## 8. Sécurité et opérations

- Ne révèle, n'imprime et ne committe jamais de clés API, jetons ou identifiants.
- N'exécute pas de commande destructive, de suppression massive, de réinitialisation Git ou d'installation système sans accord explicite.
- Inspecte les scripts téléchargés avant de les exécuter.
- N'utilise pas de mode de contournement global des permissions.
- N'écrase pas un fichier de l'utilisateur sans avoir inspecté son contenu et expliqué la modification.
- Préfère des modifications ciblées et vérifiables.

## 9. Documentation

Le README final doit permettre à un recruteur ou à un chercheur de comprendre :
- la question de recherche et son intérêt ;
- les données et leurs licences ;
- l'architecture et le flux des données ;
- les choix méthodologiques et les hypothèses ;
- comment installer et reproduire les analyses ;
- les résultats réellement obtenus, y compris les résultats nuls ou inattendus ;
- les limites et les pistes d'amélioration.

Ne présente pas le projet comme plus robuste ou plus causal qu'il ne l'est. La transparence méthodologique fait partie du livrable.

## 10. Mode d'interaction

Sois direct et précis. Si plusieurs options sont possibles, compare brièvement leurs avantages, limites et coûts, puis recommande une option. N'écris pas un long plan théorique lorsque l'utilisateur demande une action limitée. Ne génère pas tout le projet en une seule réponse : attends les validations entre phases.
