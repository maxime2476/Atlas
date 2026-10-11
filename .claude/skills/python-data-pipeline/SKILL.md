---
name: python-data-pipeline
description: Construit et vérifie des pipelines de données Python simples, reproductibles et testables, de l'ingestion aux tables d'analyse.
---

# Python data pipeline

## Quand utiliser ce skill
Utilise-le pour les scripts d'ingestion, de nettoyage, de validation, de transformation, d'agrégation et de préparation des données destinées à l'analyse.

## Principes d'architecture

- Privilégie une suite de scripts explicites sous `src/` ou un répertoire de pipeline clairement nommé.
- Garde les étapes lisibles : ingestion, validation, nettoyage, agrégation et export.
- N'ajoute pas de classes ou d'architecture configurable si quelques fonctions simples suffisent.
- Une fonction doit représenter une opération cohérente ou éviter une répétition significative.
- Ne mets pas les données brutes dans le dépôt si elles sont volumineuses ou si la licence ne le permet pas.
- Évite les chemins absolus ; utilise des chemins relatifs robustes.

## À vérifier dans chaque étape

1. Schéma attendu : noms, types et unités des colonnes.
2. Clés : unicité, doublons, valeurs manquantes.
3. Plages plausibles et valeurs impossibles.
4. Nombre de lignes et taux de perte avant/après chaque transformation importante.
5. Types de jointure et cardinalité attendue.
6. Cohérence temporelle et spatiale.
7. Traitement explicite des erreurs d'accès, fichiers incomplets et données manquantes.
8. Sortie déterministe lorsque c'est possible.

## Outils

- Utilise `uv` pour l'environnement Python et maintiens `uv.lock`.
- Privilégie les bibliothèques déjà installées et justifiées par le projet.
- Utilise pandas ou Polars selon la taille et les opérations ; ne migre pas de bibliothèque sans raison.
- Utilise DuckDB si les requêtes SQL simplifient des agrégations ou des jointures sur des fichiers.
- Ajoute pytest pour les transformations critiques.
- Ruff peut servir au linting et au formatage si le projet l'a configuré.

## Tests minimaux

Écris des tests ciblés pour :
- le schéma de sortie ;
- l'unicité des clés lorsque nécessaire ;
- les jointures attendues ;
- les conversions d'unités ;
- les agrégations connues sur un petit jeu de données artificiel ;
- le comportement face à des valeurs manquantes ou des entrées invalides.

N'utilise pas de données réelles sensibles dans les tests. Ne te contente pas de tester que le script s'exécute : vérifie la justesse de ses sorties.

## Comportement

- Inspecte les fichiers existants avant de les modifier.
- Exécute uniquement les tests pertinents et rapporte leur résultat exact.
- Ne prétends pas avoir exécuté les tests si l'environnement ne permet pas de le faire.
- Ne remplace pas silencieusement une source indisponible par une autre.
- Documente les hypothèses de transformation et les limites dans le code ou dans une note associée.
