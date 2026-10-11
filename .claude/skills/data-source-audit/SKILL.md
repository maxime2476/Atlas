---
name: data-source-audit
description: Vérifie la faisabilité et la compatibilité de sources de données publiques avant de les intégrer dans un pipeline empirique.
---

# Data source audit

## Quand utiliser ce skill
Utilise-le avant de choisir définitivement le sujet, avant de télécharger un volume important de données et avant de joindre deux sources.

## Procédure d'audit

Pour chaque source, renseigne autant que possible :
1. organisme producteur et nom exact du jeu de données ;
2. URL officielle et documentation technique ;
3. licence, attribution requise et restrictions de redistribution ;
4. méthode d'accès : API, fichiers directs, portail, téléchargement manuel ou authentification ;
5. format, taille approximative, schéma et système de coordonnées si applicable ;
6. couverture temporelle, fréquence, couverture géographique et résolution ;
7. unité d'observation et identifiants disponibles ;
8. délai de publication, révisions et stabilité de la source ;
9. valeurs manquantes connues, limites de mesure et ruptures méthodologiques ;
10. procédure reproductible pour obtenir un échantillon test.

## Compatibilité entre sources

Avant toute jointure, vérifie :
- le niveau géographique et les changements de frontières ;
- la période, le fuseau ou calendrier, la fréquence et la saisonnalité ;
- les unités de mesure, définitions et conversions nécessaires ;
- la cardinalité attendue des clés ;
- les doublons et identifiants manquants ;
- le décalage temporel plausible entre exposition et résultat ;
- le risque de biais de couverture ou de sélection.

N'accepte pas une jointure simplement parce que le code s'exécute. Fournis un tableau de contrôle : lignes avant/après, clés uniques, taux de correspondance, doublons, valeurs manquantes et observations perdues.

## Tests de faisabilité

- Commence par un petit échantillon ou une période limitée.
- Vérifie que les données peuvent réellement être lues et interprétées.
- Ne télécharge pas de gros rasters ou archives avant d'avoir validé le besoin et l'accès.
- Si l'accès exige des identifiants ou une procédure manuelle, indique-le clairement. Ne contourne pas les contrôles d'accès.
- Distingue une source annoncée dans la documentation d'une source dont le téléchargement a effectivement été testé.

## Livrable attendu

Crée ou mets à jour un tableau Markdown ou CSV comprenant :
- source ;
- URL officielle ;
- variables utiles ;
- unité et couverture ;
- format et accès ;
- licence ;
- identifiants ;
- limites ;
- test effectué ;
- statut : validée, à vérifier, bloquée ou écartée ;
- décision et justification.

Termine par une recommandation : quelles sources suffisent pour un prototype minimal et quelles sources sont seulement optionnelles. Ne sélectionne pas les sources en fonction du prestige de l'organisme.
