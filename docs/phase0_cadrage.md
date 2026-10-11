# ATLAS — Phase 0 : cadrage scientifique et faisabilité

*Rédigé le 2026-10-10. Document de travail : les décisions marquées « en attente » ne sont pas validées.*

Convention de statut utilisée dans tout le document :

- **[TESTÉ]** : vérifié par un accès réel pendant la phase 0 (téléchargement d'un échantillon, lecture d'en-tête, requête API).
- **[DOCUMENTÉ]** : lu sur la page ou la notice officielle, sans test d'accès aux données elles-mêmes.
- **[À VÉRIFIER]** : hypothèse plausible, non confirmée.

---

## 1. Questions de recherche candidates

### Contexte bibliographique (à compléter en phase 1)

L'effet de la chaleur sur les rendements céréaliers français au niveau départemental **est déjà étudié**. Une originalité sur ce point seul ne peut donc pas être revendiquée.

- Gammans, Mérel & Ortiz-Bobea (2017), *Environmental Research Letters* 12(5), 054007, DOI 10.1088/1748-9326/aa6b0c. Panel départemental 1950-2014, blé et orge ; la chaleur estivale est le principal facteur et les températures au-delà d'environ 33 °C sont nuisibles. https://doaj.org/article/9697ca7cd50e4c4fa0533ca9ad2ec6e1
- Hawkins et al. (2013), maïs français, influence croissante du stress thermique. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3599478/
- Ben-Ari et al. (2018), *Nature Communications*, DOI 10.1038/s41467-018-04087-x. La perte de 2016 sur le blé n'a pas été anticipée par les systèmes de prévision ; elle s'explique par un événement composé (automne doux puis printemps très humide). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5915531/
- Schlenker & Roberts (2009), *PNAS* 106 : 15594-15598. Effets non linéaires de la température via les degrés-jours au-dessus d'un seuil. https://pmc.ncbi.nlm.nih.gov/articles/PMC2747166
- Ortiz-Bobea et al. (2019), *ERL*. Aux États-Unis, l'humidité du sol est le meilleur prédicteur des variations interannuelles. La chaleur reste le moteur principal des projections. Résumé de presse lu, article non lu : https://news.cornell.edu/node/311456
- Références méthodologiques connues, à relire en phase 1 : Dell, Jones & Olken (2014, *JEL*), « What do we learn from the weather? » ; Hsiang (2016, *Annual Review of Resource Economics*) ; Blanc & Schlenker (2017, *REEP*) sur les modèles de panel climat-agriculture.

Il faut donc chercher une valeur ajoutée vérifiable :

1. séparer stress thermique et stress hydrique du sol, en France, avec l'humidité du sol modélisée par ISBA ;
2. mesurer l'exposition là où la culture est réellement semée, grâce au RPG, plutôt que sur tout le département ;
3. tester si un modèle entraîné sur le passé anticipe les années extrêmes récentes (2016, 2020, 2022, 2024).

Je n'ai pas vérifié que ces trois points sont absents de la littérature : une recherche bibliographique ciblée est prévue en phase 1.

### Comparaison des options

| | **A. Sensibilité des rendements à la chaleur et au déficit hydrique** | **B. L'irrigation comme amortisseur (maïs)** | **C. Prévision des rendements en cours de saison** | **D. Adaptation par l'assolement** |
|---|---|---|---|---|
| Question | Quel est l'effet d'un choc de chaleur (degrés-jours > seuil) et d'un déficit d'humidité du sol pendant les phases critiques sur le rendement départemental du blé tendre, de l'orge, du colza et du maïs ? | L'écart de rendement entre maïs irrigué et non irrigué augmente-t-il lors des étés chauds et secs ? | Avec la météo disponible au 1er juin (blé) ou au 1er août (maïs), peut-on prévoir le rendement départemental mieux qu'une tendance naïve ? | Un choc de sécheresse en *t* réduit-il la surface de maïs en *t+1* au profit du tournesol ou du sorgho ? |
| Intérêt | Base de toute évaluation des dommages climatiques ; les extrêmes récents (2016-2025) sont absents de l'étude 1950-2014 de Gammans et al. Leur présence dans d'autres travaux reste à vérifier. | Valeur économique de l'eau d'irrigation, au cœur des conflits d'usage récents. | Utile à la gestion des marchés et de l'assurance ; 2016 montre les limites des prévisions existantes. | Comportement des exploitants : adaptation de court terme. |
| Mécanismes | Échaudage (chaleur pendant le remplissage du grain), déficit hydrique à la floraison, excès d'eau au printemps. | L'irrigation retire la contrainte hydrique mais pas toute la contrainte thermique ; restrictions d'eau en cas de sécheresse. | Mêmes mécanismes, utilisés pour prévoir et non pour estimer un effet. | Anticipations adaptatives, aversion au risque, contraintes de rotation de la PAC. |
| Hypothèses testables | H1 : effet non linéaire (nul en dessous du seuil, négatif au-dessus). H2 : chaleur et déficit hydrique ont des effets séparés et identifiables. H3 : ces effets sont plus forts pour les cultures de printemps et d'été. | H4 : la dérivée de l'écart irrigué − non irrigué par rapport au déficit hydrique est positive. | H5 : le gain de précision par rapport à une tendance naïve est significatif sur les années test, y compris les années extrêmes. | H6 : sécheresse en *t* → baisse de la part du maïs en *t+1*. |
| Données nécessaires | SAA départementale, SIM quotidienne, RPG (masque de cultures) | SAA (maïs irrigué / non irrigué), SIM | SAA, SIM, éventuellement NDVI | SAA (surfaces) ou RPG, SIM |
| Identification | Les chocs météo sont plausiblement aléatoires conditionnellement aux effets fixes département et année. C'est le design standard de la littérature : on estime l'effet de la météo, pas du climat. | Faible : la composition des surfaces irriguées varie et les restrictions d'eau dépendent elles-mêmes de la sécheresse. L'effet est descriptif et hétérogène, pas causal. | Aucune identification requise : objectif purement prédictif. | Moyenne : prix, réformes de la PAC (2015, 2023) et tendances régionales sont des facteurs de confusion ; effets probablement faibles face au bruit. |
| Faisabilité | **Élevée** (voir § 3) | **Limitée** : statut qualité fragile pour la majorité des départements | **Élevée** pour la météo ; **à risque** pour le NDVI (continuité MODIS) | Moyenne |
| Originalité attendue | Faible à moyenne | Moyenne à élevée (à vérifier) | Moyenne | Moyenne |

### Recommandation

**Retenir A comme cœur du projet, C comme module prédictif construit sur le même panel, et B comme analyse d'hétérogénéité exploratoire.** D reste une extension optionnelle.

Justification :

- A est la seule option qui combine des données fiables (statut qualité 1 pour 85 départements sur 87 en blé tendre d'hiver), une stratégie d'identification défendable et un volume suffisant (environ 1 380 département-années pour le blé).
- C réutilise exactement les mêmes variables. Il apporte une composante ML honnête, évaluée hors échantillon et dans le temps, sans prétention causale.
- B est la question la plus intéressante économiquement, mais les données ne permettent pas d'en faire l'axe principal (voir § 3.3).
- La composante géospatiale n'est pas décorative. Agréger la grille SAFRAN au département en pondérant par les surfaces réellement cultivées (RPG) est une question de mesure. Remplacer l'exposition des champs par la moyenne départementale ressemble plutôt à une erreur de Berkson, avec peu d'atténuation attendue. Avec plusieurs régresseurs corrélés, le sens du biais n'est pas garanti. La comparaison des deux pondérations est donc une **analyse de sensibilité**, pas un test d'atténuation.
- Le satellitaire (NDVI) n'est justifié que dans C. Il reste optionnel tant que la continuité de la série n'est pas confirmée.

---

## 2. Audit des sources de données

| Source | Producteur / URL officielle | Variables utiles | Couverture et granularité | Format et accès | Licence | Identifiants | Limites connues | Test effectué | Statut |
|---|---|---|---|---|---|---|---|---|---|
| **SAA, séries longues départementales 2010-2025** | SSP / Agreste. https://agreste.agriculture.gouv.fr/agreste-web/disaron/SAA-SeriesLongues/detail/ | Surface (ha), rendement (q/ha), production (q), par culture ; `STATUT_QUALITE` | 2010-2025 ; 95 départements métropolitains + DROM ; annuel. 2025 provisoire (données arrêtées au 30/03/2026). | Zip de 7,1 Mo contenant 2 xlsx (départemental 11,2 Mo, régional 3,5 Mo) ; une feuille par famille de cultures ; format large (`SURF_2010`… `PROD_2025`). | [À VÉRIFIER] Licence Ouverte attendue pour Agreste, non lue explicitement sur cette page | Libellé « 077 - Seine-et-Marne » (code et nom concaténés) ; culture « 01 - Blé tendre d'hiver… » | Opération de **synthèse multi-sources**, pas une mesure directe. Les rendements sont « plus difficiles à établir » que les surfaces. Le statut qualité ne reflète que la dernière année publiée. Séries **rétropolées 2010-2019** sur le RA 2020. | **[TESTÉ]** Téléchargement (SHA-256 `46e2ea94…0d76f`), lecture des en-têtes, comptages. Le serveur n'envoie pas son certificat intermédiaire (HARICA GEANT TLS RSA 1) : il faut fournir cet intermédiaire, ne pas désactiver TLS. | **Validée** |
| **SAA 2000-2009** (tableaux interactifs) | Agreste. https://agreste.agriculture.gouv.fr/agreste-web/disaron/saa/cda8b080-3e9e-4368-b41d-7a29c1da0be6/search/ | Mêmes variables | 2000-2010 | Interface interactive, pas de fichier direct identifié | idem | idem | **Non rétropolées sur le RA 2020** : rupture méthodologique avec la série 2010-2025, selon la page méthodologique. | [DOCUMENTÉ] | **Écartée** pour l'analyse principale (robustesse éventuelle) |
| **Note de statut qualité de la SAA** | https://agreste.agriculture.gouv.fr/agreste-web/download/methode/S-SAA/Statut_qualité_SAA.pdf | Définition des statuts 1, 2 et 3 | — | PDF | — | — | Statut 2 : à utiliser « dans des totaux ». Statut 3 : extrapolé, « exclusivement pour des totaux ». | **[TESTÉ]** Lue intégralement | Référence |
| **SIM2 quotidienne (SAFRAN-ISBA)** | Météo-France. https://www.data.gouv.fr/datasets/donnees-changement-climatique-sim-quotidienne | `T`, `TINF_H`, `TSUP_H` (°C), `PRELIQ`, `PRENEI` (mm), `ETP` (mm, Penman-Monteith FAO-56), `SWI` (%), `WG_RACINE` (m³/m³), `SSWI_10J`, `HU`, `SSI` | **1958-2026** ; France métropolitaine ; grille de 0,072° (≈ 8 km), **9 892 points** ; quotidien | Un csv.gz par an (≈ 137 Mo compressés pour 2020), séparateur `;`, coordonnées Lambert II étendu en hectomètres, table de correspondance vers lat/lon fournie | **Licence Ouverte 2.0** (API data.gouv : `lov2`) | `LAMBX`, `LAMBY`, `DATE` (AAAAMMJJ) | Réanalyse modélisée : interpolation optimale par massif et tranche d'altitude, réseau de stations variable dans le temps, moins fiable en montagne [À VÉRIFIER dans la littérature]. **Fenêtres différentes selon la variable** : `TINF_H` sur ]18-18 UTC], `TSUP_H` et précipitations sur ]06-06 UTC], `T` sur ]00-00 UTC]. Mise à jour bimensuelle sur les 4 dernières années, donc des révisions sont possibles. | **[TESTÉ]** HEAD (taille), lecture partielle par requête Range (en-tête et premières lignes de 2020), téléchargement de la grille de coordonnées, lecture des deux notices PDF. | **Validée** |
| **RPG (Registre parcellaire graphique)** | IGN / ASP. https://www.data.gouv.fr/datasets/rpg ; téléchargement : https://data.geopf.fr/telechargement/resource/RPG | Parcelles avec culture principale (code), îlots ; tables de référence des cultures | Millésimes annuels (couches WMS 2007-2024 visibles) ; version 2.x des parcelles depuis 2015 ; 3.0 depuis 2024 | Vecteur (GeoPackage ou shapefile par région [À VÉRIFIER]), flux WMS/WFS | **Licence Ouverte 2.0** | Code culture ; pas d'identifiant d'exploitation (version anonymisée) | Ne couvre que les déclarants PAC. Avant 2015, seuls les îlots et leur groupe de cultures majoritaire sont disponibles [À VÉRIFIER]. Fichiers volumineux. Changement de structure en 2024. | [DOCUMENTÉ] via l'API data.gouv ; pas de téléchargement | **À vérifier** (taille, format par région, nomenclature 2010-2014) |
| **ADMIN EXPRESS COG** | IGN. https://www.data.gouv.fr/datasets/admin-express-admin-express-cog-admin-express-cog-carto-admin-express-cog-carto-pe-admin-express-cog-carto-plus-pe | Contours des départements | Métropole + DROM ; éditions annuelles | Shapefile / GeoPackage | **Licence Ouverte 2.0** | Code INSEE du département | Aucune fusion de départements sur 2010-2025 en métropole ; à confirmer avec le COG (Corse 2A/2B, Rhône/Métropole de Lyon pour 69D et 69M). | [DOCUMENTÉ] | **Validée** (à télécharger en phase 1) |
| **Prix agricoles (Eurostat `apri_ap_crpouta`)** | Eurostat. https://ec.europa.eu/eurostat/databrowser/view/apri_ap_crpouta/default/table | Prix de vente annuels (€/100 kg) du blé tendre, de l'orge, du maïs, etc. | **France entière**, 2000-2024 (mise à jour du 15/05/2025) | API JSON | Politique de réutilisation d'Eurostat [À VÉRIFIER le texte exact] | Code produit | National seulement : sert uniquement à valoriser les pertes en euros (descriptif). Absorbé par l'effet fixe année dans les régressions. 2025 absent. | **[TESTÉ]** Requête API, dimensions lues | **Optionnelle** |
| **NDVI MODIS (MOD13Q1 v6.1)** | NASA LP DAAC. https://modis.gsfc.nasa.gov/data/dataprod/mod13.php | NDVI et EVI à 250 m, composites de 16 jours | 2000 à ~2025 | HDF/GeoTIFF ; compte NASA Earthdata (gratuit) ; alternatives AppEEARS ou Google Earth Engine | Données NASA, ouvertes [À VÉRIFIER] | Grille sinusoïdale | **Fin de vie de Terra** : Google Earth Engine affiche une série arrêtée au 2025-09-30 ; un relais VIIRS est en cours (VNP13 v1 retiré, délais différents selon les produits). Les sources consultées se contredisent. | [DOCUMENTÉ] par des sources secondaires ; rien testé | **À vérifier**, optionnelle |
| **RICA (comptabilité des exploitations)** | SSP | Revenus, charges | Données individuelles en accès restreint ; résultats publics agrégés par région ou orientation | — | — | — | Granularité trop grossière pour un panel département-année | Aucun | **Écartée** (justification ci-contre) |
| **Restrictions d'eau (Propluvia / VigiEau)** | Ministère de la Transition écologique | Arrêtés de restriction | [À VÉRIFIER] historique disponible depuis 2012 environ | — | — | — | Endogènes à la sécheresse | Aucun | **À vérifier**, optionnelle pour B |

**Prototype minimal suffisant :** SAA séries longues + SIM2 quotidienne + ADMIN EXPRESS. Le RPG est **fortement recommandé** pour le masque de cultures, mais un prototype peut d'abord pondérer par la surface du département. Prix Eurostat et NDVI sont optionnels.

---

## 3. Évaluation de la faisabilité

### 3.1 Observations exploitables

Comptages **réellement calculés** sur le fichier SAA départemental (métropole, 2010-2025, département-années avec au moins 1 000 ha de la culture et un rendement renseigné) :

| Culture (code SAA) | Département-années | Statut qualité 2025 (départements ≥ 1 000 ha) |
|---|---|---|
| Blé tendre d'hiver (01) | 1 379 | 85 en statut 1, 2 en statut 2 |
| Orge d'hiver et escourgeon (08) | 1 315 | 76 / 6 |
| Orge de printemps (09) | 788 | 45 / 7 |
| Colza d'hiver (29) | 1 109 | 67 / 1 |
| Tournesol (32) | 851 | 53 / 4 |
| Total maïs grain + semence (18) | 1 232 | non calculé |
| Maïs grain irrigué (14) | 620 | 17 en statut 1, 21 en statut 2, 1 en statut 3 |
| Maïs grain non irrigué (15) | 1 167 | statut non renseigné (74 lignes vides) |

Pour un panel départemental, ce volume est raisonnable : environ 86 départements × 16 ans pour le blé. En revanche, **16 années, c'est peu** pour estimer des effets de chaleur extrême, qui sont rares par définition. La puissance statistique dépend du nombre de départements-années réellement exposés au-delà du seuil. Il faudra le calculer en phase 2 avant de fixer la spécification.

### 3.2 Liaison des sources

- **SAA ↔ départements** : clé = code département extrait du libellé (« 077 »). Contrôles à prévoir : 95 départements en métropole (2A/2B), aucun doublon par (département, culture), cardinalité 1:1 avec ADMIN EXPRESS.
- **SIM ↔ départements** : jointure spatiale de 9 892 mailles de 8 km avec les polygones départementaux. Choix à faire : centroïde de la maille ou part de surface de la maille dans le département. Une maille peut chevaucher plusieurs départements ; les mailles côtières sont partielles.
- **Ordre d'agrégation (point critique)** : les variables non linéaires (degrés-jours au-dessus d'un seuil) doivent être calculées **au niveau maille-jour, puis agrégées**. Agréger d'abord la température puis appliquer le seuil sous-estimerait systématiquement l'exposition (inégalité de Jensen).
- **Pondération par les cultures (RPG)** : pondérer chaque maille par la surface de la culture concernée qu'elle contient. Les millésimes 2010-2014 posent un problème de nomenclature [À VÉRIFIER] ; un masque fixe moyen sur 2015-2017 pourrait servir, ce qui suppose que la localisation des cultures est stable.
- **Calendrier** : le blé d'hiver est semé à l'automne *t−1* et récolté en *t*. L'année agricole doit commencer au 1er septembre de *t−1*, donc **SIM doit démarrer en septembre 2009**.

### 3.3 Pourquoi B ne peut pas être l'axe principal

- Le statut qualité du maïs irrigué est 2 ou 3 pour 22 départements sur 39. Selon le producteur, ces chiffres sont à utiliser « dans des totaux ».
- En ne gardant que le statut 1, il reste environ 17 départements. De plus, le statut ne décrit que la dernière année et non toute la série.
- Avec un seuil de 1 000 ha pour chaque modalité, sans filtre de statut : 605 département-années et 41 départements. L'écart médian irrigué − non irrigué est de 31 q/ha (valeur calculée, descriptive).
- Le partage irrigué / non irrigué est en partie une **construction statistique** de la SAA. Une corrélation entre l'écart et la sécheresse pourrait refléter la méthode d'estimation des services régionaux plutôt que l'agronomie.

### 3.4 Biais et menaces

| Menace | Mécanisme | Contrôle prévu |
|---|---|---|
| Erreur de mesure du rendement | Rendements SAA estimés par synthèse, parfois lissés vers des a priori d'experts → atténuation probable | Restreindre au statut 1 ; comparer départemental et régional ; reconnaître la limite |
| Erreur de mesure de l'exposition | Météo moyenne du département ≠ météo des champs | Pondération RPG vs pondération par surface ; sensibilité |
| Sélection | La surface de l'année dépend elle-même de la météo (automne humide de 2019 → moins de blé semé pour 2020) | Population et poids définis sur une **surface fixe** (moyenne 2010-2012), jamais sur la surface de l'année. *Erratum (phase 3) : 2010-2012 appartient à la période d'estimation (ses trois premières années), et non à une période extérieure ; voir `docs/dictionnaire_panel.md`.* |
| Mauvais contrôles | Surface et irrigation sont elles-mêmes des réponses à la météo | Les exclure de la spécification principale |
| Confusion temporelle | Progrès génétique, prix, PAC | Effets fixes année (chocs nationaux) ; tendances spécifiques par département ou région en robustesse. Avec 16 ans, ces tendances peuvent absorber du signal. |
| Autocorrélation spatiale et temporelle | Chocs météo corrélés entre départements voisins ; persistance dans le temps | Triplet d'inférence décrit au § 5 ; ne conclure que sur ce qui résiste aux trois méthodes |
| Médiation par l'humidité du sol | La chaleur assèche le sol : le SWI est en partie un médiateur | Rapporter chaleur seule, puis chaleur + SWI, la seconde étant appelée « effet partiel » |
| Phénologie | Un printemps chaud avance les stades : l'erreur sur les fenêtres calendaires est corrélée au choc | Robustesse à ± 2 semaines ; limite reconnue explicitement |
| Adaptation | Les exploitants ajustent dates de semis et variétés | Interprétation stricte : effet de court terme d'un **choc météo**, **pas** effet du changement climatique |
| Erreur écologique | Relation départementale ≠ relation à la parcelle | Ne pas transposer à l'exploitation |
| Recherche de spécification | Nombreux seuils, fenêtres et cultures | Spécification principale **pré-spécifiée** (pas « pré-enregistrée » : *S*, f(SWI) et le rayon de Conley restent à fixer avant estimation) ; les autres choix sont présentés comme analyses de sensibilité |
| Fuite de données (ML) | Seuils et fenêtres choisis sur tout l'échantillon ; chocs d'une même année corrélés dans l'espace | Sélection à l'intérieur des plis ; validation **par année**, jamais par découpage aléatoire |

### 3.5 Limites de l'approche causale

Le design A identifie l'effet d'une **variation météorologique interannuelle** sur le rendement, sous l'hypothèse que la météo, conditionnellement aux effets fixes département et année, n'est pas corrélée aux autres déterminants du rendement. Cette hypothèse est classique et défendable.

Elle ne permet **pas** d'affirmer :

- l'effet du changement climatique de long terme, à cause de l'adaptation ;
- un effet de l'irrigation : en B, l'irrigation n'est pas assignée aléatoirement ;
- un effet sur les revenus des exploitations : il n'existe pas de données de revenu au niveau département-année.

Un DiD ou une étude événementielle n'est **pas** proposé : aucun traitement discret avec une date et un groupe de comparaison crédibles n'a été identifié.

### 3.6 Faisabilité d'une validation prédictive

- L'effet fixe année ne peut pas être estimé pour une année test. Le modèle de prévision est donc **un modèle distinct**, réestimé sans effet fixe année (effet fixe département + tendance + météo). Il ne réutilise **pas** le β du modèle à effets fixes bidimensionnels. Ce β est identifié seulement par les écarts entre départements une même année, et la composante nationale des années extrêmes est absorbée par l'effet fixe année.
- Avec une origine glissante commençant en 2016 (entraînement sur 2010-2015, soit 6 ans seulement), 2016 est testée, mais sur un modèle très peu entraîné. Des tendances propres à chaque département seraient alors du surajustement : tendance commune ou régionale uniquement.
- Le test n'est **pas un vrai test en temps réel**. La rétropolation 2010-2019 sur le RA 2020 et les révisions de SIM font entrer dans les années d'entraînement de l'information postérieure. Il faut le dire.

---

## 4. Question de recherche recommandée

**Question principale (explicative).** En France métropolitaine, de 2010 à 2025, quel est l'effet des chocs de chaleur et de déficit hydrique du sol pendant les phases critiques de croissance sur le rendement départemental du blé tendre d'hiver ?

**Question prédictive (séparée, avec un modèle différent).** Un modèle fondé sur la météo de la saison, entraîné uniquement sur les années passées, prévoit-il les rendements départementaux, y compris pendant les années de pertes nationales, mieux qu'une tendance naïve ?

**Questions secondaires.**

1. Les effets diffèrent-ils entre cultures d'hiver (blé, orge d'hiver, colza) et cultures de printemps ou d'été (orge de printemps, maïs, tournesol) ?
2. Pondérer l'exposition par la localisation réelle des cultures (RPG) modifie-t-il les coefficients estimés ? Il s'agit d'une analyse de sensibilité de mesure.
3. *(Exploratoire, descriptif)* Dans les départements en statut qualité 1, l'écart maïs irrigué − non irrigué augmente-t-il avec le déficit hydrique estival ?
4. *(Descriptif)* À quelle valeur nationale de production perdue, aux prix Eurostat, correspondent les chocs estimés pour 2016 et les autres années extrêmes ?

**Estimand principal.** Variation moyenne du log-rendement associée à un degré-jour supplémentaire au-dessus du seuil *T\** pendant la fenêtre de remplissage du grain. Elle est identifiée **uniquement par les écarts entre départements une même année**, la composante nationale étant absorbée par l'effet fixe année. Deux versions sont rapportées :

- un effet de la chaleur seule ;
- un effet partiel, à humidité du sol donnée. Le SWI est en partie un médiateur de la chaleur.

Formulation cible pour le rapport : « À année donnée, les départements ayant connu davantage de degrés-jours au-dessus de *T\** pendant le remplissage du grain ont enregistré des rendements plus faibles de X % par degré-jour. Il s'agit d'un effet de court terme d'un choc météo, identifié sur peu d'années d'exposition, et non d'un effet du changement climatique. »

---

## 5. Protocole empirique préliminaire

### Unité, période, population

- Unité : département × année × culture.
- Période : récoltes 2010 à 2025 ; météo à partir de septembre 2009.
- Population : départements métropolitains dont la **surface moyenne 2010-2012** de la culture est d'au moins *S* ha (*S* = 1 000 ha proposé, en attente). Elle est fixée une fois pour toutes, pour que la sélection ne dépende pas de la météo de l'année. Les poids de régression utilisent la même surface fixe. Exclusion des DROM, car la grille SIM ne couvre que la métropole.
- Filtre statut qualité 1 : il est quasi neutre pour le blé (85 départements sur 87). Le statut ne décrit que la dernière année publiée : ce n'est pas une garantie de qualité sur toute la série.
- 2025 provisoire inclus mais signalé, avec une robustesse sans 2025.
- **Étape préalable obligatoire (phase 2), avant toute régression sur les rendements** : compter, par année, les départements exposés au-delà de *T\**. Calculer la variance de l'EDD résiduelle après effets fixes, et l'effet minimal détectable.
- **Règle de repli écrite à l'avance** : si l'exposition au-delà de 32 °C est concentrée sur moins d'environ 4 années, la spécification principale passe à un seuil de 30 °C (ou à des classes de température). Ce changement est signalé comme tel dans le rapport.
- Appariement Tmin / Tmax : `TINF_H` (]18-18 UTC]) et `TSUP_H` (]06-06 UTC]) sont associées à la même `DATE`. La règle exacte sera écrite et testée en phase 2.

### Variables

| Rôle | Variable | Construction | Unité |
|---|---|---|---|
| Résultat | log(rendement) | `REND_t` de la SAA | log(q/ha) |
| Exposition thermique | Degrés-jours de croissance (GDD) entre 0 °C et *T\**, et degrés-jours extrêmes (EDD) au-dessus de *T\** | À partir de `TINF_H` et `TSUP_H`, au niveau maille-jour, en approximation sinusoïdale ou trapézoïdale intra-journalière, puis agrégation départementale | °C·jour |
| Exposition hydrique | Indice d'humidité du sol moyen (`SWI`) ou nombre de jours sous un seuil, par fenêtre | Maille-jour, puis agrégation | % ou jours |
| Pluie excessive | Cumul de `PRELIQ` au printemps (mécanisme de 2016) | idem | mm |
| Fenêtres (blé, proposition) | Automne (sept-nov *t−1*), hiver, printemps (mars-avril), remplissage du grain (mai-juin) | Calendaires et fixes ; décalages en robustesse | — |
| Effets fixes | Département ; année | — | — |
| Hétérogénéité (B) | Écart de rendement irrigué − non irrigué | SAA codes 14 et 15 | q/ha |

Seuil *T\** : la littérature indique environ 29 à 33 °C selon la culture (Schlenker & Roberts ; Gammans et al.). Proposition : **fixer *T\** = 32 °C pour le blé avant estimation**, puis tester une grille de seuils en sensibilité, présentée comme telle.

### Modèles de référence

1. Moyenne du département avec tendance linéaire (prédictif naïf).
2. Panel à effets fixes : log(Y_dt) = α_d + γ_t + β₁·GDD_dt + β₂·EDD_dt + f(SWI_dt) + θ·Pluie_dt + ε_dt, estimé avec `fixest`.

### Méthodes économétriques

- MCO à effets fixes bidimensionnels, avec trois méthodes d'inférence complémentaires. On ne conclut que sur ce qui reste significatif avec les trois :
  1. cluster par département, pour la dépendance temporelle ;
  2. Conley pour la dépendance spatiale, avec un rayon **fixé avant estimation**. Vérifier dans la documentation de `fixest` ce que `vcov_conley` fait en panel ;
  3. wild cluster bootstrap par année avec poids de Webb, comme contrôle conservateur. Il se dégrade si la variation de l'EDD est concentrée sur peu d'années (MacKinnon & Webb).

  Écartés : cluster bidimensionnel (16 années, ce n'est pas fiable) ; cluster région × année seul (les canicules couvrent plusieurs régions).
- Pondérée par une surface fixe vs non pondérée : une MCO pondérée à deux effets fixes ne donne pas un « effet moyen par hectare ». Un écart entre les deux est lu comme un signe d'hétérogénéité des effets (Solon, Haider & Wooldridge 2015, référence à vérifier).
- Hétérogénéité par culture et par région, avec un modèle empilé et interactions.
- Pas de DiD, pas de variables instrumentales : aucun instrument ni traitement crédible n'a été identifié.

### Modèles ML à comparer (module C)

- Ridge ou Lasso sur l'ensemble des variables météo par fenêtre.
- Forêt aléatoire.
- Gradient boosting (`HistGradientBoostingRegressor` de scikit-learn, pour éviter une dépendance supplémentaire).
- Tous comparés au modèle naïf et au modèle linéaire à effets fixes (sans effet fixe année).

### Validation et métriques

- **Dates de prévision fixées** (blé) : au 1er juin, avec la météo disponible jusqu'au 31 mai, ce qui ne couvre que le début du remplissage ; et au 1er juillet, en fin de remplissage, peu avant la récolte. Les variables sont tronquées à la date de prévision.
- **Validation chronologique par origine glissante** : entraînement sur 2010…*t−1*, test sur *t*, pour *t* = 2016 à 2025, soit 10 années test. Les premières années sont testées sur des modèles entraînés sur très peu d'années.
- **Validation par blocs d'années (leave-one-year-out)** en complément : elle utilise le futur, elle n'est donc pas un substitut.
- Validation par blocs spatiaux (régions) en analyse secondaire. Le choc de l'année test étant présent à l'entraînement, elle est présentée comme de l'**interpolation spatiale**, pas de la prévision.
- Métriques : RMSE et MAE sur le rendement et sur l'écart à la tendance ; *skill score* relatif au modèle naïf ; rappel et précision pour la détection des pertes de plus de 10 %. Les résultats sont rapportés **année par année**, pas seulement en moyenne : avec 9 années test, l'incertitude est grande.
- Toute sélection d'hyperparamètres, de seuils ou de fenêtres se fait à l'intérieur des plis d'entraînement.
- Importances de variables (SHAP ou permutation) : interprétées comme **associations prédictives**, jamais comme effets.

### Analyses de robustesse

Prioritaires : échantillon et poids fixés hors période ; seuil *T\** et classes de température ; tendances par région ; sans 2025 ; sans les départements de montagne. Autres : fenêtres décalées de ± 2 semaines ; pondération RPG vs surface ; seuil de surface *S* ; échantillon équilibré ; exclusion de 2025 ; tendances par région ; statut qualité 1 vs tous statuts ; données régionales SAA au lieu des départementales ; type d'erreurs-types ; exclusion des départements de montagne.

### Résultats qui invalideraient l'interprétation

- Coefficients météo très sensibles à l'ajout de tendances, ce qui suggère une confusion avec des évolutions lentes.
- Effet de la météo de l'année *t+1* sur le rendement *t* (test placebo) significativement non nul. Attention : le SWI est persistant, et un placebo non significatif ne valide rien à lui seul.
- Effets de signe agronomiquement implausible, par exemple une chaleur extrême bénéfique au blé.

### Limites à reconnaître dans le rapport final

Rendements synthétiques de la SAA ; courte période ; réanalyse modélisée plutôt qu'observations ; effet de la météo ≠ effet du climat ; niveau départemental, sans conclusion pour les exploitations ; pas de revenus ; irrigation non aléatoire.

---

## 6. Risques scientifiques et techniques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Effets de la chaleur extrême imprécis (exposition au-delà de 32 °C probablement concentrée sur 2 à 4 années ; non calculé) | **Élevée** | Élevé | Comptage et effet minimal détectable en phase 2 ; règle de repli écrite (§ 5) ; empiler les cultures ; rapporter honnêtement des intervalles larges |
| Résultat déjà publié sous une forme proche | Moyenne | Moyen | Recherche bibliographique ciblée en début de phase 1 ; recentrer sur les extrêmes récents ou la prévision si nécessaire |
| Rétropolation 2010-2019 qui lisse les rendements | Inconnue | Élevé | Lire la méthodologie complète (PDF de 37 pages, non lu faute d'outil d'extraction) ; comparer avec les données régionales |
| Volume de SIM (≈ 2,2 Go compressés pour 2009-2025) | Faible | Moyen | Lecture directe des csv.gz par DuckDB, filtrée et agrégée, sans décompression complète |
| Taille du RPG (vecteur national, plusieurs Go) | Moyenne | Moyen | Traitement région par région ; ne conserver qu'une grille agrégée de surfaces par maille |
| Certificat TLS incomplet d'Agreste | Certaine | Faible | Fournir l'intermédiaire HARICA au script de téléchargement ; ne jamais désactiver la vérification |
| Discontinuité du NDVI MODIS | Élevée | Faible (optionnel) | Ne pas en faire une dépendance du projet |
| Environnement absent (pas de `uv`, R ni DuckDB) | Certaine | Moyen | Installation à valider (§ 8) |

---

## 7. Architecture cible minimale

```text
Atlas/
├── CLAUDE.md, .claude/          # configuration existante (inchangée)
├── README.md                    # rédigé progressivement
├── pyproject.toml, uv.lock      # environnement Python
├── renv.lock                    # environnement R (à partir de la phase économétrique)
├── docs/
│   ├── phase0_cadrage.md        # ce document
│   └── sources.md               # provenance : URL, dates d'accès, SHA-256, licences
├── data/                        # ignoré par Git sauf les README
│   ├── raw/<source>/            # fichiers téléchargés, jamais modifiés
│   ├── interim/                 # Parquet intermédiaires (ex. météo maille-jour filtrée)
│   └── processed/               # panel département-année-culture (Parquet + dictionnaire)
├── src/atlas/                   # quelques modules Python : download.py, saa.py, weather.py, spatial.py
├── scripts/                     # étapes numérotées et lisibles : 01_download.py, 02_build_saa.py,
│                                #   03_weather_aggregate.py (appelle des requêtes DuckDB), 04_build_panel.py,
│                                #   20_forecast_cv.py
├── R/                           # 10_fe_models.R, 11_robustness.R
├── tests/                       # pytest : schémas, clés, plages, cardinalités, degrés-jours
└── reports/                     # figures et tables générées (figures ignorées par Git)
```

Rôle de chaque technologie :

- **Python** : téléchargement, lecture des xlsx SAA, géospatial (jointure grille-département, masque RPG), ML, tests.
- **DuckDB**, via le paquet Python, sans installation système : agrégation de la SIM quotidienne directement depuis les csv.gz (environ 9 900 mailles × 365 jours × 17 ans ≈ 61 millions de lignes). C'est le seul endroit où il simplifie réellement le travail.
- **R** : économétrie (`fixest` pour les effets fixes et les erreurs-types de Conley ; `modelsummary` pour les tables). Pas de duplication avec Python : l'économétrie est en R, la prédiction en Python.
- **Interface entre les langages** : un unique fichier Parquet `data/processed/panel.parquet`, accompagné d'un dictionnaire de variables (nom, unité, construction).

Dépendances Python envisagées, à valider : `pandas`, `pyarrow`, `duckdb`, `openpyxl`, `geopandas`, `shapely`, `pyproj`, `scikit-learn`, `matplotlib`, `pytest`.
Dépendances R envisagées : `fixest`, `arrow`, `modelsummary`, `ggplot2`.

Volontairement non retenus : orchestrateur (Snakemake, Airflow), base de données serveur, conteneurs, API. Si l'enchaînement des scripts devient pénible, un `Makefile` de quelques lignes suffira.

---

## 8. Plan de travail par étapes

| Phase | Contenu | Critères de validation |
|---|---|---|
| **1. Environnement, bibliographie, ingestion brute** | Installer `uv` (et R plus tard) ; initialiser Git ; recherche bibliographique ciblée ; scripts de téléchargement SAA, ADMIN EXPRESS, SIM (sept. 2009-2025) ; fichier `docs/sources.md` | Fichiers bruts présents avec SHA-256 ; aucun fichier brut versionné ; tests de schéma SAA (colonnes, 95 départements, unicité département × culture) ; note bibliographique sur l'originalité |
| **2. Exposition climatique (géospatial)** | Jointure grille SIM ↔ départements ; GDD/EDD maille-jour ; fenêtres ; agrégation DuckDB ; masque RPG | Tests unitaires des degrés-jours sur des cas calculés à la main ; contrôle de cardinalité de la jointure spatiale (chaque maille affectée, poids sommant à 1) ; comparaison avec des valeurs climatologiques publiées ; nombre de département-années exposés au-delà de *T\** |
| **3. Panel et analyse descriptive** | Construction du panel ; statistiques descriptives ; cartes ; audit (agent `data-auditor`) | Tableau de contrôle des jointures (lignes avant/après, taux de correspondance, valeurs manquantes) ; dictionnaire des variables |
| **4. Économétrie (R)** | Spécification principale, puis robustesses et placebo | Revue par l'agent `econometrics-reviewer` ; spécification principale conforme à ce document |
| **5. Prédiction (Python)** | Validation glissante, références naïves, modèles ML | Revue de fuite de données (skill `scientific-review`) ; résultats par année test |
| **6. Extensions** | Hétérogénéité irrigué / non irrigué ; valorisation en euros ; NDVI si l'accès est validé | Chaque extension est présentée comme exploratoire |
| **7. Rapport et README** | Résultats, y compris nuls ; limites | Relecture `scientific-review` et `code-reviewer` |

---

## 9. Décisions en attente de validation

1. Direction : A en cœur, C en module prédictif, B en exploratoire (D écarté pour l'instant).
2. Culture principale : blé tendre d'hiver ; extension aux autres cultures en secondaire.
3. Période 2010-2025, avec 2025 provisoire inclus et signalé.
4. Population fixée sur la surface moyenne 2010-2012 ≥ *S* = 1 000 ha ; filtre statut qualité 1 (quasi neutre pour le blé).
5. *T\** = 32 °C fixé ex ante pour le blé, avec la règle de repli à 30 °C du § 5 si l'exposition est trop concentrée.
6. Installation de `uv` (utilisateur, sans sudo) en phase 1, puis R (installation système, `sudo apt`) en phase 4.
7. Création du dépôt Git en début de phase 1.
8. NDVI : laissé optionnel, à réexaminer en phase 6.

---

## 10. Revue indépendante

Le protocole a été relu par l'agent `econometrics-reviewer` le 2026-10-10. Trois points bloquants ont été signalés et intégrés :

- sélection et poids fondés sur la surface de l'année, alors que cette surface dépend de la météo ;
- confusion entre le β à effets fixes bidimensionnels et la prévision des années nationales extrêmes ;
- inférence fragile sur un EDD concentré sur peu d'années.

Les points importants ont aussi été intégrés : triplet d'inférence, SWI comme médiateur, interprétation de la pondération, dates de prévision, test qui n'est pas en temps réel, blocs spatiaux = interpolation. Une revue `scientific-review` complète interviendra avant la conclusion des phases 4 et 5.
