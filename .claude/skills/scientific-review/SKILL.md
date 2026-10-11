---
name: scientific-review
description: Réalise un audit indépendant de la validité scientifique, des fuites de données, de l'inférence, de la reproductibilité et de la formulation des conclusions.
---

# Scientific review

## Quand utiliser ce skill
Utilise-le avant de valider une phase d'analyse, avant de publier des résultats et avant de finaliser le README ou un rapport.

## Mode de revue

Agis comme un relecteur critique, pas comme un co-auteur cherchant à défendre le résultat. Commence par lire le plan d'analyse et le code concerné. Ne modifie pas le code durant la première passe de revue.

## Checklist scientifique

### Données
- La source et la licence sont-elles documentées ?
- La population analysée correspond-elle à la question ?
- Les exclusions et valeurs manquantes sont-elles transparentes ?
- Les définitions et unités sont-elles cohérentes dans le temps et entre sources ?
- Les jointures ont-elles modifié l'échantillon de façon inattendue ?

### Prédiction
- Y a-t-il une fuite de données directe ou indirecte ?
- Le découpage train/validation/test respecte-t-il la temporalité et la géographie ?
- Les transformations ont-elles été ajustées uniquement sur les données d'entraînement lorsque nécessaire ?
- Les métriques sont-elles adaptées à la cible et comparées à un baseline crédible ?
- Les résultats sont-ils comparés à des modèles plus simples ?
- Les incertitudes et limites de généralisation sont-elles présentées ?

### Économétrie et causalité
- L'estimand et la population cible sont-ils clairs ?
- La spécification découle-t-elle du design de recherche ?
- Les erreurs-types sont-elles adaptées à la structure des données ?
- Les hypothèses d'identification sont-elles discutées et, lorsque possible, examinées ?
- Les contrôles post-traitement ou variables de collision risquent-ils d'introduire un biais ?
- Les effets hétérogènes ont-ils été préspécifiés ou clairement présentés comme exploratoires ?
- Les résultats nuls et les spécifications défavorables sont-ils rapportés honnêtement ?

### Géospatial et temporalité
- Les unités spatiales sont-elles comparables ?
- L'agrégation évite-t-elle les décalages temporels ou spatiaux artificiels ?
- L'autocorrélation spatiale ou temporelle peut-elle rendre l'inférence trop optimiste ?
- Les périodes d'exposition précèdent-elles correctement les résultats étudiés ?

### Reproductibilité
- Les environnements et versions sont-ils documentés ?
- Les scripts repartent-ils des entrées décrites ?
- Les chemins et secrets sont-ils gérés correctement ?
- Les graines aléatoires et les limites de reproductibilité sont-elles documentées ?
- Les tests vérifient-ils les résultats, pas seulement l'exécution ?

## Format de rapport

Classe chaque problème :
- **Bloquant** : empêche de soutenir la conclusion principale.
- **Important** : fragilise l'interprétation ou la reproductibilité.
- **Mineur** : amélioration utile, mais sans impact central.

Pour chaque problème, fournis le fichier ou l'étape concernée, le constat, pourquoi cela importe, une correction concrète et un test de vérification. Distingue les défauts avérés des risques à examiner.

Termine par l'une de ces conclusions :
- validable ;
- validable après corrections importantes ;
- non validable en l'état.

Ne modifie pas les résultats pour les rendre plus convaincants. La bonne conclusion peut être qu'un effet n'est pas établi.
