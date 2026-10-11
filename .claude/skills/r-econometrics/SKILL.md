---
name: r-econometrics
description: Prépare, estime et vérifie des modèles économétriques en R, avec une attention particulière aux panels, effets fixes, DiD et à l'inférence.
---

# R econometrics

## Quand utiliser ce skill
Utilise-le lorsqu'une analyse nécessite une estimation économétrique en R, une inférence statistique explicite ou des résultats tabulaires reproductibles.

## Avant l'estimation

- Décris la question, l'estimand, l'unité d'observation et l'échantillon.
- Vérifie les définitions, unités, valeurs manquantes et règles d'exclusion.
- Identifie la structure des données : coupe transversale, série temporelle, panel ou données hiérarchiques.
- Vérifie que la spécification correspond au design de recherche et non à une préférence logicielle.
- Indique les hypothèses d'identification et ce qui pourrait les invalider.

## Implémentation

- Utilise `fixest` pour les modèles de panel, effets fixes ou DiD lorsque cela convient.
- Utilise `data.table` si ses opérations rendent le traitement plus clair ou plus efficace.
- Utilise `ggplot2` pour les graphiques statistiques.
- Utilise `broom` ou les outils de `fixest` pour exporter proprement les résultats.
- Maintiens un environnement reproductible avec `renv` si le code R devient une partie importante du projet.
- Garde le code accessible : formules explicites, noms de variables compréhensibles, commentaires sur les choix méthodologiques.

## Inférence et robustesse

Pour chaque estimation, indique :
- la variable dépendante et les variables explicatives ;
- les effets fixes inclus ;
- le niveau de regroupement des erreurs-types et sa justification ;
- le nombre d'observations et d'unités ;
- le coefficient ou estimand, son erreur-type, son intervalle de confiance et sa valeur p lorsque pertinente ;
- la spécification exacte et les exclusions ;
- les hypothèses nécessaires à l'interprétation.

Pour un DiD ou une étude événementielle, examine la définition du traitement, le calendrier, les groupes de comparaison, les pré-tendances, les effets anticipés, l'hétérogénéité des effets et les méthodes adaptées au calendrier de traitement. N'interprète pas l'absence de significativité d'un test de pré-tendances comme une preuve que l'hypothèse est vraie.

## Python et R

- Utilise des fichiers Parquet ou CSV documentés pour les échanges.
- Vérifie les unités, l'ordre des catégories, les clés, le nombre de lignes et l'échantillon entre les langages.
- N'essaie pas de forcer deux estimations à être identiques si les méthodes ou échantillons diffèrent.
- Si les résultats diffèrent, identifie d'abord les différences de données, de spécification, de valeurs manquantes et d'inférence.

## Livrable attendu

Fournis le script R, une sortie de résultats reproductible et une courte note méthodologique. Ne crée pas de tableaux de coefficients fictifs. Si R ou les paquets requis ne sont pas disponibles, indique la commande nécessaire et attends l'autorisation avant toute installation système.
