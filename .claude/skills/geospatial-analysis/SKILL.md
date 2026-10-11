---
name: geospatial-analysis
description: Conçoit et vérifie des traitements géospatiaux, des jointures spatiales, des rasters et des indicateurs de télédétection comme le NDVI.
---

# Geospatial analysis

## Quand utiliser ce skill
Utilise-le pour les données géoréférencées, images satellitaires, rasters, géométries administratives, jointures spatiales et indicateurs environnementaux.

## Avant de traiter

- Identifie le type de donnée : raster, vecteur, grille, point, polygone ou série temporelle.
- Vérifie le système de coordonnées (CRS), la résolution spatiale, l'étendue, la période et les unités.
- Vérifie les règles de licence et les contraintes de téléchargement.
- Commence par une tuile, une zone et une période de test.
- Vérifie que les métadonnées accompagnent les fichiers et ne sont pas perdues à l'export.

## Traitements

- Utilise GeoPandas/Shapely pour les données vectorielles si adaptés.
- Utilise Rasterio pour lire, masquer, reprojeter et agréger les rasters.
- Utilise xarray lorsque les données ont des dimensions temporelles, spatiales ou spectrales.
- N'ajoute pas une bibliothèque supplémentaire si les outils déjà retenus couvrent le besoin.
- Pour une jointure spatiale, indique le prédicat utilisé, le CRS et la cardinalité attendue.
- Vérifie les géométries invalides et les changements de limites administratives.
- Documente les règles d'agrégation, notamment quand des pixels sont résumés au niveau d'une région ou d'une unité agricole.

## Indicateurs satellitaires

Pour le NDVI, la formule usuelle est `(NIR - RED) / (NIR + RED)`, mais vérifie les bandes et leur correspondance pour le produit précis utilisé.

- Vérifie les facteurs d'échelle, les valeurs NoData et les pixels masqués.
- Traite les nuages, ombres et pixels invalides selon les métadonnées du produit.
- N'interprète pas automatiquement une variation du NDVI comme une variation de rendement agricole.
- Documente la fenêtre temporelle d'agrégation et sa justification agronomique.
- Vérifie les artefacts de bord, les pixels partiellement couverts et la surface valide par unité géographique.
- Distingue les mesures de réflectance, les indicateurs dérivés et les résultats agricoles observés.

## Contrôles de qualité

- CRS compatible avant superposition ou jointure.
- Emprise et résolution cohérentes.
- Nombre de pixels valides et proportion masquée.
- Distribution des valeurs et plages plausibles.
- Géométries valides et absence de doublons inattendus.
- Vérification visuelle sur un petit exemple lorsque possible.
- Test d'une agrégation sur un cas artificiel connu.

## Livrable attendu

Documente les données d'entrée, le produit et les bandes utilisés, le CRS, les étapes de masquage, les transformations, la règle d'agrégation et les contrôles effectués. Si une donnée ne peut pas être traitée avec l'environnement actuel, propose une petite expérience de faisabilité au lieu de lancer un traitement massif.
