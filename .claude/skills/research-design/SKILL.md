---
name: research-design
description: Cadre une question de recherche empirique, définit les estimands et hypothèses, compare les stratégies descriptives, prédictives et causales, et prépare un plan d'analyse avant le développement.
---

# Research design

## Quand utiliser ce skill
Utilise ce skill au démarrage du projet, lors d'un changement de question scientifique ou avant toute analyse qui pourrait être interprétée causalement.

## Procédure

1. Reformule la question en une phrase précise et falsifiable.
2. Identifie la population, l'unité d'observation, la période, la géographie et la fréquence.
3. Sépare :
   - l'objectif descriptif ;
   - l'objectif prédictif, s'il existe ;
   - l'objectif causal, uniquement si une stratégie d'identification crédible est envisageable.
4. Définis les variables principales, leurs unités et leur rôle : résultat, traitement/exposition, contrôles, identifiants, dimensions temporelles et spatiales.
5. Établis un diagramme causal ou une liste explicite des mécanismes et facteurs de confusion lorsque cela aide à clarifier l'identification.
6. Propose au maximum trois designs plausibles. Pour chacun, expose les hypothèses, les données requises, les menaces à la validité et les contrôles possibles.
7. Recommande le design le plus faisable compte tenu des données réellement accessibles.
8. Établis un plan d'analyse préliminaire : critères d'exclusion, spécification principale, inférence, robustesses et résultats qui invalideraient l'interprétation.
9. Liste les décisions qui restent ouvertes. Ne les présente pas comme des faits établis.

## Règles de rigueur

- Ne confonds jamais prédiction et causalité.
- Ne propose pas un DiD uniquement parce que les données sont un panel. Il faut justifier le traitement, le groupe de comparaison, la date d'événement et les hypothèses.
- Pour une étude événementielle, examine les pré-tendances, les effets anticipés, l'hétérogénéité temporelle et les limites des tests de pré-tendances.
- Pour des données spatiales, explique les risques d'autocorrélation spatiale, de changement d'échelle et d'erreur écologique.
- Si aucune stratégie causale crédible n'est disponible, recommande une analyse descriptive ou prédictive honnête.
- Ne choisis pas une question seulement parce qu'elle permet d'utiliser un modèle sophistiqué.

## Livrable attendu

Produis un court document Markdown avec :
- question de recherche ;
- motivation ;
- hypothèses ;
- unité et période ;
- variables et estimands ;
- sources nécessaires ;
- stratégie empirique ;
- menaces à la validité ;
- critères de réussite ;
- décisions en attente.

Ne commence pas à coder tant que les données minimales et la question ne sont pas suffisamment définies.
