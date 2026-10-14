# Revue 4 — revue de littérature systématique ciblée (chenlu-hung/literature-review)

**Objet.** Confronter le chapitre 2 du mémoire et sa bibliographie à une recherche documentée, pour trouver les travaux proches qui manquent et vérifier les citations existantes.

**Adaptation.** Le skill est conçu pour l'apprentissage automatique : cadre PMDB, grille de reproductibilité de type NeurIPS, tableaux de benchmarks. Le cadre a été transposé au sujet. La grille ML et les tableaux de benchmarks ne s'appliquent pas à une littérature d'économétrie agricole et n'ont pas été utilisés. La génération PDF (pandoc) n'a pas été lancée.

**Exécution.**
- Les scripts de recherche et d'agrégation du skill ont été lus, puis exécutés en mode isolé (`python3 -I`), sans email ni élément identifiant du mémoire. Ils n'utilisent que la bibliothèque standard et font de simples requêtes GET.
- Le validateur `verify_citations.py` n'a **pas** été exécuté (règle du projet). La vérification des DOI a été faite par un script écrit pour cette revue, qui interroge Crossref et DataCite.

## 1. Cadre (PMDB transposé)

- **P, problème** : comment la sensibilité des rendements à la chaleur extrême diffère entre cultures irriguées et pluviales ; rôle de l'eau (VPD, humidité du sol) ; inférence en présence de chocs météo communs.
- **M, familles de méthodes** : panels statistiques à effets fixes (degrés-jours) ; modèles de culture ; télédétection (température de surface) ; inférence par grappes, bootstrap et placebo.
- **D, données** : rendements observés séparés irrigué/pluvial (comtés, départements) ; réanalyses météo.
- **B, critères** : l'étude compare-t-elle irrigué et pluvial sur des observations ? Sépare-t-elle la chaleur de l'eau ?

**Période** : 2005-2026. **Inclusion** : articles et prépublications sur des rendements observés ou des mécanismes directement mobilisés par le mémoire. **Exclusion** : génétique et physiologie végétale, essais d'irrigation à la parcelle sans lien avec la chaleur, études de demande en eau.

## 2. Journal de recherche (2026-10-14)

| Source | Requête | Résultats |
|---|---|---|
| OpenAlex | irrigated rainfed crop yield extreme heat sensitivity | 60 |
| OpenAlex | irrigation heat stress maize yield statistical panel | 60 |
| OpenAlex | vapor pressure deficit maize yield extreme degree days | 60 |
| OpenAlex | maize yield climate irrigation France | 60 |
| OpenAlex | standard errors spatial correlation weather crop yield panel inference | 60 |
| Crossref | les mêmes 5 requêtes | 5 × 40 |
| Semantic Scholar | les mêmes 5 requêtes | 0, 0, 0, 40, 0 (limite de débit de l'API sans clé : couverture incomplète) |
| Recherche web (revue 1) | 5 requêtes | Luan et al. 2021, Rigden et al. 2020, Pinto et Mieno 2026 |

Fichiers bruts : `sources/*.json`. Agrégation : `all_j.json` et `all.md`.

## 3. Flux de sélection (adapté de PRISMA)

```
Identifiés : n = 540   (OpenAlex 300 | Crossref 200 | Semantic Scholar 40)
   │ dédoublonnage (DOI, puis titre normalisé)
   ▼
Après dédoublonnage : n = 472
   │ tri sur titres, filtre de mots-clés puis lecture
   ▼
Titres retenus : n = 97
   │ tri sur résumés (récupérés depuis l'API OpenAlex)
   ▼
Pertinents : n = 22, dont 9 déjà cités dans le mémoire
   │
   ▼
Ajouts recommandés : n = 13  (dont 1, Rigden et al. 2020, trouvé seulement par la recherche web de la revue 1)
```

Ce qui a été exclu sur titre : surtout la génétique du maïs, les essais d'irrigation déficitaire en Chine ou en Iran, et les outils statistiques génériques renvoyés par Crossref sur la requête 5. Cette requête a peu rendu : la littérature sur l'inférence en présence de chocs communs est mal indexée par mots-clés.

**Déjà cités et retrouvés** (signe que la recherche couvre bien le champ) : Zaveri et Lobell 2019, Tack et al. 2017, Siebert et al. 2017, Li et Troy 2018, Zhu et Burney 2022, Hawkins et al. 2013, van der Velde et al. 2010 et 2012, Lobell et al. 2013.

## 4. Synthèse thématique : ce qui manque

### Thème A — Rendements irrigués et pluviaux observés : le design du mémoire existe aux États-Unis

C'est le manque le plus important. Le tableau 1 du mémoire dit « Direct evidence abroad », mais il ne cite pour ce design que Li et Troy (2018) et Schauberger et al. (2017).

- **Troy, Kipgen et Pal (2015)**, *ERL* 10:054013, doi:10.1088/1748-9326/10/5/054013. Rendements de comtés américains, irrigués et pluviaux, face aux extrêmes climatiques et à leur calendrier, sur quatre cultures. C'est le premier travail de ce type et le plus cité de la sélection (332 citations).
- **Luan, Bommarco, Scaini et Vico (2021)**, *ERL* 16(6), doi:10.1088/1748-9326/abfc76. Comtés américains 1970-2010, maïs et soja irrigués et pluviaux. Les rendements pluviaux sont les plus faibles par temps chaud et sec, et l'irrigation modifie la réponse à la chaleur et à la sécheresse combinées.
- **Hunter, Mueller, Lombardozzi et Mueller (2026)**, « Irrigated crop yields reveal distinct influences of heat and moisture », doi:10.25675/3.027152, **prépublication non évaluée**. D'après son résumé : « Using paired rainfed and irrigated yield observations across the US, we are able to control for the effects of water availability and independently evaluate the influence of temperature on yields ». C'est la logique exacte du mémoire, utilisée pour séparer chaleur et eau. **C'est le comparateur le plus proche.** Il faut le lire en entier et positionner le mémoire par rapport à lui. Son résultat sur la chaleur prise isolément est directement lié au constat VPD du § 7.7.
- **Pinto et Mieno (2026)**, AgEcon Search, doi:10.22004/ag.econ.404420, document de travail. Indemnités d'assurance récolte 2011-2023, converties en pertes de rendement. Les exploitations irriguées sont nettement moins sensibles à la chaleur, avec un effet résiduel indiscernable de zéro.
- **Snyder et al. (2021)**, *ERL*, doi:10.1088/1748-9326/ac15ce. Chocs de rendement liés à la météo, maïs, soja et blé, irrigués et pluviaux, États-Unis.

**Conséquence pour le mémoire.** La contribution doit être formulée comme une **première application française**. Les apports propres sont l'écart intra-département et intra-année, la mesure sur les parcelles et l'inférence dont la taille est contrôlée. Il ne faut pas laisser entendre que la comparaison irrigué/pluvial observée serait nouvelle en soi. Le texte actuel (« None of these studies compares observed irrigated and rainfed yields within the same department and year ») reste exact, mais seulement grâce à la précision « within the same department and year ». Il faut l'assumer explicitement face à ces travaux.

### Thème B — Chaleur ou eau : la lecture « VPD » a une littérature dédiée

- **Carter, Melkonian, Riha et Shaw (2016)**, *ERL* 11:094012, doi:10.1088/1748-9326/11/9/094012. Le maïs irrigué sert à séparer le stress thermique du stress hydrique. D'après le résumé, les pertes corrélées à la chaleur et au VPD « likely reflect underlying soil moisture limitations ». C'est l'argument du § 7.7, avec le maïs irrigué comme témoin.
- **Rigden et al. (2020)**, *Nature Food* 1:127-133. Combiner la demande évaporative et l'humidité du sol prédit mieux les rendements. Une projection fondée sur la seule demande indiquerait environ le double des dommages. C'est directement pertinent pour le § 10.3.
- **Kimm et al. (2020)**, *Agric. For. Meteorol.*, doi:10.1016/j.agrformet.2020.107930. Le VPD domine l'humidité du sol dans la régulation stomatique du maïs et du soja de la Corn Belt.
- **Webber et al. (2018)**, *Nature Communications*, doi:10.1038/s41467-018-06525-2. Ensemble de modèles de culture sur l'Europe : la sécheresse compte plus que la chaleur pour le maïs grain, et le mélange irrigué/pluvial est modélisé. C'est le repère européen manquant.

**Conséquence.** Le § 7.7 cite Lobell et al. (2013) seuls. Les quatre références ci-dessus donnent au constat VPD une portée plus large et montrent qu'il est attendu plutôt que fortuit. Carter et al. (2016) est le plus utile, car il utilise lui aussi l'irrigué comme contrôle de l'eau.

### Thème C — Menaces de composition et d'adaptation : la littérature d'économie agricole

- **Cui (2020)**, *JAERE*, doi:10.1086/709859. Le rapport entre surfaces récoltées et semées chute au-delà de 35 °C (comtés américains). C'est la référence de base pour la menace « abandon ou ensilage » du § 10.2. Le mémoire discute cette menace sans source.
- **Bareille et Chakir (2023)**, *AJAE*, doi:10.1111/ajae.12420. Modèle structurel qui sépare les effets agronomiques de la météo des effets d'adaptation des agriculteurs. Les auteurs travaillent sur la France. C'est la référence pour le paragraphe « Irrigation itself responds to the summer », qui mélange justement agronomie et comportement.

### Thème D — France

- **Ceglar, Zampieri, González-Reviriego, Ciais et al. (2020)**, *ERL*, doi:10.1088/1748-9326/aba1be. Impact variable dans le temps du climat sur le maïs et le blé en France depuis 1900. Le mémoire cite Ceglar et al. (2016), pas cette étude, qui est pertinente pour le § 8.2 (une sensibilité du blé qui change ou non dans le temps).
- **Raghuram et Coffel (2026)**, *ERL*, doi:10.1088/1748-9326/ae7c89. Aux États-Unis, la sensibilité du maïs à la chaleur a augmenté d'environ 20 % entre 1960 et 2019. C'est un repère pour la question de stabilité du § 8.2 et pour l'extrapolation du § 10.3.

### Thème E — Inférence

Aucun manque significatif n'a été trouvé : Cameron et al. (2008), MacKinnon et Webb (2017), MacKinnon et al. (2023), Webb (2023), Bertrand et al. (2004) et Conley (1999) couvrent le champ. La recherche par mots-clés est peu efficace sur ce thème, ce qui est une limite de cette revue.

## 5. Vérification des citations existantes

Script écrit pour cette revue (Crossref, puis DataCite pour les DOI absents de Crossref) appliqué aux 46 entrées de `memoire/references.bib` :

| Statut | N | Détail |
|---|---|---|
| PASS (DOI résolu, année et premier auteur concordants) | 40 + 3 DataCite | Schauberger et al. 2021 (GFZ), Didan 2021 et Wan et al. 2021 (LP DAAC) : DOI DataCite, absents de Crossref mais résolus |
| WARN | 3 | Hawkins et al. (2013 dans la bibliographie, 2012 chez Crossref), van der Velde et al. (2012 contre 2011), MacKinnon et Webb (2017 contre 2016). La bibliographie retient l'année du numéro et Crossref la mise en ligne, ce qui est cohérent. Rien à corriger. |
| Sans DOI | 3 | DRAAF Occitanie 2017, Agreste Occitanie 2026, DRIAS 2022 : rapports et portail, sans DOI attendu |

**Aucune citation fabriquée ou introuvable.** Un point de fond reste ouvert : la caractérisation de **Lischeid et al. (2022)** (« soil moisture less relevant than meteorological drivers »). Le DOI est correct, mais le contenu n'a pas pu être confirmé par la recherche. L'auteur doit vérifier la phrase sur le texte.

Deux entrées de la bibliographie (`urruty2017`, `laurent2025`) ne sont citées nulle part. biblatex ne les imprime pas, ce qui est sans conséquence.

## 6. Limites de cette revue

- Semantic Scholar n'a quasiment rien renvoyé (limite de débit), et les citations « influentes » ne sont donc pas disponibles.
- Le tri s'est fait sur titres et résumés seulement : aucun texte intégral n'a été lu, y compris pour Hunter et al. (2026), dont seul le résumé est connu.
- Le thème inférence est mal couvert par la recherche par mots-clés.
- La date de fin de recherche est le 2026-10-14.

## 7. Recommandations pour le chapitre 2

1. **§ 2.2** : ajouter Troy et al. (2015), Luan et al. (2021), Hunter et al. (2026, prépublication) et Pinto et Mieno (2026, document de travail), et formuler la différence avec le mémoire en une phrase (écart intra-département et intra-année, France, mesure sur les parcelles, taille des tests).
2. **§ 2.1, rôle de l'eau** : ajouter Carter et al. (2016), Rigden et al. (2020) et Webber et al. (2018) ; citer Rigden et al. dans les limites des projections (§ 10.3).
3. **§ 10.2** : citer Cui (2020) pour la menace de l'abandon ou de l'ensilage, et Bareille et Chakir (2023) pour l'adaptation des irrigants.
4. **§ 8.2** : citer Ceglar et al. (2020) et Raghuram et Coffel (2026).
5. **Tableau 1** : remplacer « Direct evidence abroad » par « Direct evidence abroad from county yields reported by irrigation status (US) ; indirect for France ».
6. Vérifier sur le texte la phrase sur Lischeid et al. (2022).

Chaque ajout doit être vérifié sur le texte intégral avant d'être cité. Les résumés ci-dessus sont repris des notices OpenAlex ou de la recherche web, pas d'une lecture complète.
