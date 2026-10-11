# ATLAS — Revue bibliographique ciblée (phase 1, étape A)

*Rédigée le 2026-10-10. La revue n'est pas exhaustive : elle porte sur les travaux les plus proches de la question d'ATLAS.*

## Niveau de lecture

Chaque référence porte l'un des niveaux suivants :

- **[TEXTE]** : texte original lu (PDF en accès ouvert, extrait localement avec `pypdf`).
- **[RÉSUMÉ]** : seul le résumé officiel a été lu (via OpenAlex, HAL ou le site de l'éditeur). Le texte complet n'était pas accessible automatiquement : paywall Elsevier, ou défi anti-robot Anubis sur HAL, que je n'ai pas contourné.
- **[SECONDAIRE]** : ni le texte ni le résumé n'ont été lus ; l'information provient d'un moteur de recherche ou d'une page de présentation. À confirmer.

Les chiffres cités sont ceux des auteurs. Ils n'ont pas été recalculés.

---

## 1. Effets de la température et des précipitations sur les rendements céréaliers français

### Gammans, Mérel & Ortiz-Bobea (2017) [TEXTE]

« Negative impacts of climate change on cereal yields: statistical evidence from France ». *Environmental Research Letters* 12 : 054007. DOI 10.1088/1748-9326/aa6b0c. Licence CC-BY 3.0.

- **Question :** effet de la distribution des températures et des précipitations sur les rendements du blé et de l'orge ; projections climatiques.
- **Données :** rendements départementaux 1950-2015, collectés par les auteurs dans les publications du ministère ; 1956 est exclue (hiver exceptionnel).
  - Météo : E-OBS v14, grille de 0,25° (≈ 25 km).
  - Agrégation au département pondérée par la surface **agricole** CORINE (moyenne 1996, 2000 et 2006), sans distinguer les cultures.
- **Méthode :**
  - Exposition à chaque intervalle de 1 °C, calculée par une courbe en double sinus entre la Tmin et la Tmax de jours consécutifs.
  - log(rendement) expliqué par un effet fixe département, une **tendance quadratique par région** (et non des effets fixes année), une fonction en escalier (pas de 2 °C) ou un polynôme de la température, et la précipitation cumulée et son carré.
  - Saisons fixes : mars-juillet, automne et hiver pour les cultures d'hiver.
  - Erreurs-types corrigées de la corrélation spatiale (voisins jusqu'au 3e degré).
- **Résultats :**
  - Tous les rendements diminuent quand les températures du printemps-été augmentent.
  - Les cultures d'hiver sont sensibles au froid extrême après le semis.
  - Projections en RCP 8.5, fin de siècle : −21,0 % pour le blé d'hiver, −17,3 % pour l'orge d'hiver, −33,6 % pour l'orge de printemps.
  - Une température flexible améliore la prévision hors échantillon par rapport à la température moyenne. Elle est évaluée par des réplications aléatoires, et non par une validation chronologique.
- **Limites signalées par les auteurs :**
  - « There is little exposure to temperatures above 34 °C in our data ».
  - Effet de court terme seulement.
  - Les anomalies de température peuvent servir de proxy à des épisodes secs non captés par la précipitation saisonnière, d'où cette phrase : « *Additional information on historical soil moisture levels throughout the growing season would be needed to fully allay this concern* ».

**Pertinence pour ATLAS : très élevée.** C'est la référence à étendre. Les auteurs identifient eux-mêmes l'absence d'humidité du sol comme une limite.

### Mérel & Gammans (2021) [SECONDAIRE]

« Climate Econometrics: Can the Panel Approach Account for Long-Run Adaptation? ». *American Journal of Agricultural Economics* 103(4) : 1207-1238. DOI 10.1111/ajae.12200.

- Ils montrent sous quelles conditions un panel non linéaire à effets fixes approche la réponse de long terme.
- D'après les résumés consultés, ils trouvent des indices d'adaptation de long terme pour les rendements aux États-Unis et en France.
- **Pertinence :** utile pour interpréter correctement le β d'ATLAS (effet de court terme vs long terme). À lire en phase 4.

### Ceglar, Toreti, Lecerf, van der Velde & Dentener (2016) [RÉSUMÉ]

« Impact of meteorological drivers on regional inter-annual crop yield variability in France ». *Agricultural and Forest Meteorology* 216 : 58-67. DOI 10.1016/j.agrformet.2015.10.004 (mis en ligne en 2015).

- **Question :** quelle variable météo mensuelle explique la variabilité interannuelle des rendements de blé d'hiver et de maïs grain dans 92 départements ?
- **Méthode :** régression PLS sur la température, la précipitation et le rayonnement mensuels de la saison de croissance.
- **Résultats :**
  - Pour le blé, la température domine dans l'Est, la pluie dans le Nord, le Nord-Ouest et le Sud-Est.
  - L'irrigation masque le signal de la pluie pour le maïs les années sèches.
- **Limites :** pas d'humidité du sol ; estimation département par département, sans inférence de panel ; période et source météo non lues.
- **Pertinence :** montre une forte hétérogénéité régionale, ce qui justifie une analyse d'hétérogénéité.

### Ben-Ari, Boé, Ciais, Lecerf, van der Velde & Makowski (2018) [TEXTE]

« Causes and implications of the unforeseen 2016 extreme yield loss in the breadbasket of France ». *Nature Communications* 9 : 1627. DOI 10.1038/s41467-018-04087-x.

- **Question :** pourquoi la perte de 2016 sur le blé n'a-t-elle pas été anticipée ?
- **Données :**
  - Rendements officiels de 27 départements du bassin céréalier, récoltes 1959-2016.
  - Détrendage par loess ; perte « sévère » < −10 %, perte « extrême » < −15 %.
  - Météo SAFRAN (8 km), quotidienne, agrégée en valeurs mensuelles puis sur le territoire de chaque département.
  - **Aucun masque de cultures** : « initial tests showed no difference in climate between the entire territory of administrative units and their cropland-covered fraction ».
- **Méthode :** régressions logistiques binomiales de l'occurrence de pertes ; sous-ensemble de variables choisi par BIC.
- **Résultats :**
  - En 2016, les rendements ont été inférieurs de 17 à 45 % aux valeurs attendues.
  - Les variables retenues sont les jours de vernalisation de décembre, la pluie de novembre, la pluie de printemps et la Tmin de juin, avec des interactions.
  - Avec un modèle entraîné sans 2016, la cote de perte extrême en 2016 est 35 fois plus élevée qu'attendu.
- **Limites (lecture d'ATLAS, pas des auteurs) :**
  - Le texte indique que le sous-ensemble de covariables a été choisi « relying on the extreme climate events characterizing the 2015–2016 growing season ».
  - Le test « hors échantillon » exclut donc 2016 de l'ajustement, mais pas du choix des variables. Ce n'est pas un test de prévision au sens strict.
- **Pertinence : élevée.**
  - Mécanisme composé à intégrer : automne doux + printemps humide.
  - Pour ATLAS, le choix des variables doit être fait à l'intérieur des plis de validation.
  - Leur constat relativise le bénéfice attendu d'un masque de cultures, au moins dans le bassin céréalier.

### Nóia Júnior, Martre, Deswarte, Cohan, van der Velde, Webber, Ewert, Ruane, Ben-Ari & Asseng (2025) [TEXTE]

« Past and future wheat yield losses in France's breadbasket ». *Field Crops Research* 322 : 109703. DOI 10.1016/j.fcr.2024.109703. Licence CC-BY 4.0. PDF fourni par l'utilisateur (version HAL).

- **Question :** quelles sont les causes, climatiques et sanitaires, des pertes de rendement passées et futures du blé dans le bassin céréalier ?
- **Données :**
  - Rendements départementaux Agreste 1980-2019, agrégés en **5 zones agroclimatiques homogènes** du bassin céréalier.
  - Météo issue de **8 stations** (Tmin, Tmax, rayonnement, pluie), et non d'une grille.
  - Stades phénologiques simulés par le modèle de culture CHN (Arvalis) pour une seule variété.
- **Variables :** 11 indices, dont 9 climatiques et 2 de maladies (fusariose de l'épi, maladies foliaires).
  - La chaleur est le nombre de jours avec Tmax > 30 °C, le 90e percentile.
  - Sécheresse et excès d'eau proviennent d'un bilan **pluie − ETo** (Hargreaves) cumulé autour de la floraison et pendant le remplissage, **sans modèle d'humidité du sol**.
  - **Les seuils sont des percentiles calculés sur 1980-2021**, période qui inclut les années évaluées.
- **Détrendage :** pente linéaire estimée **sur toute la série 1980-2019** pour chaque département.
- **Modèle :** forêt aléatoire (`randomForest` sous R, 500 arbres, `mtry` = 3).
- **Validation :**
  - En retirant une station à la fois : rRMSEp 0,48 t/ha, soit 5 %, r² = 0,59, NSE = 0,48.
  - En retirant une année à la fois (annexe) : rRMSEp 8 %.
  - En entraînement, r² = 0,98, ce qui signale un fort surajustement de la forêt.
  - **Aucune validation chronologique** (passé → futur).
- **Résultats :**
  - Le modèle explique environ 59 % de la variabilité historique.
  - En fin de siècle, une année de rendement extrêmement bas surviendrait tous les 10 ans au lieu de tous les 20 ans.
  - Les pertes liées aux canicules doubleraient.
  - La fusariose représenterait 20 % des pertes attendues.
  - Résultats sensibles à la date de floraison (fin mai - début juin).
- **Limites pour la prévision (lecture d'ATLAS) :** la tendance et les seuils utilisent l'information des années testées. Le score « une année retirée » n'est donc pas une performance de prévision au sens strict.
- **Pertinence : très élevée.** C'est le concurrent le plus direct. ATLAS s'en distingue :
  - par la grille SIM au lieu de 8 stations ;
  - par une humidité du sol modélisée (ISBA) au lieu de pluie − ETo ;
  - par une couverture de la France entière (85 départements) ;
  - par un panel économétrique explicatif à effets fixes ;
  - par une validation chronologique avec tendance et seuils estimés dans les plis.

  ATLAS **n'inclut pas** de modèle de maladies : c'est une limite à reconnaître, la fusariose étant un mécanisme important de 2016.

### Urruty, Guyomard, Tailliez-Lefebvre & Huyghe (2017) [RÉSUMÉ]

*Field Crops Research*, DOI 10.1016/j.fcr.2017.07.018.

- Échelle de l'exploitation (réseau Ecophyto) : robustesse du rendement du blé face aux conditions défavorables selon le système de culture.
- **Pertinence : faible** pour ATLAS (autre échelle), mais elle illustre l'hétérogénéité des pratiques cachée par l'agrégat départemental.

---

## 2. Prévision agrométéorologique du blé au niveau départemental

### Gouache, Bouchon, Jouanneau & Le Bris (2015) [TEXTE]

« Agrometeorological analysis and prediction of wheat yield at the departmental level in France ». *Agricultural and Forest Meteorology* 209-210 : 1-10. DOI 10.1016/j.agrformet.2015.04.027. PDF fourni par l'utilisateur.

- **Question :** outil de prévision opérationnel (Arvalis) du rendement départemental du blé d'hiver.
- **Données :**
  - Rendements Agreste 1986-2010.
  - Le résumé annonce « 23 departments », la section 2.1 en compte 22 (18 en blé tendre, 4 en blé dur), qui couvrent 43 % de la surface de blé tendre.
  - **Une station météo par département**, choisie par un expert, avec une « situation représentative » (réserve utile, date de semis, variété).
- **Variables :**
  - Plus de 250 indicateurs calculés par phase phénologique (modèle AFRC-Wheat modifié) et par un bilan hydrique (Choisnel) : stress thermique, sécheresse, excès d'eau, gel, quotient photothermique.
  - **Tendance bilinéaire** avec rupture (plafonnement des rendements depuis le milieu des années 1990, d'après Brisson et al. 2010).
- **Méthode :**
  - Sélection pas à pas (*stepwise*) ; variables retenues si elles sont choisies dans plus de 90 % des rééchantillonnages, par bootstrap ou par retrait d'une année.
  - Modèles linéaires de 5 à 7 variables.
- **Validation :**
  - (1) Retrait d'une année à la fois, **sans refaire la sélection** : RMSEP de 2,5 à 4,1 q/ha, environ deux fois mieux que la moyenne des 25 ans.
  - (2) **Années nouvelles 2011-2014**, non utilisées : RMSEP de **6,4, 11,7, 7,4 et 9,2 q/ha**. L'erreur médiane est environ deux fois celle de la validation croisée, avec des erreurs extrêmes jusqu'à 24,3 q/ha. 2012 est surestimée.
- **Prévision en cours de saison :** les données météo manquantes sont complétées par une distribution fréquentielle sur 20 ans. Les prévisions deviennent possibles environ 20 jours après l'épiaison.
- **Limites signalées :**
  - Modèles hors de leur domaine d'apprentissage en 2011-2014, d'où la recommandation d'outils signalant l'extrapolation.
  - Les variables étant choisies sur toutes les années, la validation par retrait d'une année est optimiste.
- **Pertinence : très élevée** pour le module prédictif. C'est la **preuve la plus directe, en France**, qu'une validation sur années futures dégrade fortement la performance par rapport à une validation croisée. Cela justifie le protocole chronologique d'ATLAS et la comparaison à une référence naïve.

### Paudel et al. (2021) [RÉSUMÉ]

« Machine learning for large-scale crop yield forecasting ». *Agricultural Systems* 187 : 103016. DOI 10.1016/j.agsy.2020.103016.

- Référence ML conçue pour le système européen MCYFS ; régions de France, d'Allemagne et des Pays-Bas.
- Accent explicite sur l'**absence de fuite d'information** et sur la comparaison à une référence naïve (tendance linéaire ou moyenne d'entraînement).
- Prévisions de début de saison comparables au MCYFS pour le blé tendre en France.
- **Pertinence :** modèle méthodologique pour le module C (références naïves, fuites liées aux tendances).

---

## 3. Déficit hydrique du sol

### Ortiz-Bobea, Wang, Carrillo & Ault (2019) [RÉSUMÉ ; PDF téléchargé, lecture détaillée à faire]

« Unpacking the climatic drivers of US agricultural yields ». *Environmental Research Letters* 14 : 064003. DOI 10.1088/1748-9326/ab1e75.

- Comtés américains, 1981-2017, six cultures.
- Humidité du sol d'un modèle de surface et météo fine ; sensibilités intra-saisonnières flexibles à l'humidité du sol et à la température.
- Le stress hydrique joue un rôle important dans les rendements historiques, mais la chaleur directe reste le principal facteur des projections.
- **Pertinence : très élevée.** C'est exactement le design que Gammans et al. (2017) n'ont pas pu appliquer à la France faute d'humidité du sol. SIM (ISBA) fournit cette variable.

### Lischeid, Webber, Sommer, Nendel & Ewert (2022) [RÉSUMÉ]

*Agricultural and Forest Meteorology* 312 : 108698. DOI 10.1016/j.agrformet.2021.108698.

- Allemagne, 351 districts, 40 ans, ML (forêts aléatoires et SVM).
- L'humidité du sol est « clearly proved less relevant compared to meteorological drivers ».
- Plusieurs jeux de prédicteurs donnent des performances équivalentes : l'interprétation demande un jugement d'expert.
- **Pertinence :** un résultat contraire à Ortiz-Bobea et al. Un résultat nul sur le SWI en France serait donc plausible et publiable honnêtement.

### Laurent, Ullmann & Castel (2025) [RÉSUMÉ]

*Agricultural and Forest Meteorology*, DOI 10.1016/j.agrformet.2025.110493.

- Indice de stress hydrique du blé calculé sur chaque point de grille SIM, 1960-2021.
- Hausse du risque de sécheresse après les réchauffements abrupts de 1987/1988 et 2014/2015.
- **Ce n'est pas une étude des rendements**, mais elle montre que SIM permet de construire un indicateur de stress hydrique propre au blé (eau extractible relative < 40 %).

### Le Roux et al. (2024) [RÉSUMÉ]

*Scientific Reports* 14 : 8184. DOI 10.1038/s41598-024-58826-w.

- Indicateurs agroclimatiques combinés à un modèle phénologique du blé français.
- La précocité des stades permet d'éviter une partie du déficit hydrique dans le futur proche.
- **Pertinence :** confirme la limite des fenêtres calendaires fixes (§ 3.4 du cadrage).

---

## 4. Mesure de l'exposition (géospatial, surfaces cultivées)

### Schlenker & Roberts (2009) [RÉSUMÉ]

*PNAS* 106 : 15594-15598. DOI 10.1073/pnas.0906865106.

- Comtés américains ; distribution complète des températures dans la journée et sur la saison.
- Seuils d'environ 29 °C (maïs), 30 °C (soja) et 32 °C (coton) ; la pente est beaucoup plus forte au-dessus du seuil.
- La même relation est obtenue en séries temporelles et en coupe.
- **Pertinence :** fondement du choix degrés-jours de croissance (GDD) / degrés-jours extrêmes (EDD).

### Hogan & Schlenker (2024) [RÉSUMÉ]

*Nature Communications* 15 : 4638. DOI 10.1038/s41467-024-48388-w.

- Avec ERA5-Land et GMFD, la relation non linéaire est bien retrouvée.
- « Correctly capturing the effect of daily extremes has a larger effect than the choice of weather data ».
- D'après une source secondaire, l'étude pondère les mailles par la surface cultivée et construit les extrêmes au niveau de la maille avant d'agréger.
- **Pertinence :** confirme l'ordre d'agrégation prévu (maille-jour, puis département). Le choix du jeu de données compte moins que le traitement des extrêmes.

### Synthèse sur le masque de cultures

| Étude | Pondération de la météo |
|---|---|
| Gammans et al. (2017) | Surface agricole CORINE, fixe |
| Ben-Ari et al. (2018) | Aucun masque, « aucune différence » constatée dans le bassin céréalier |
| Schlenker & Roberts (2009) | Masque de cultures satellitaire |

**Conséquence pour ATLAS :** la pondération par le RPG n'est **pas une contribution défendable** en soi. Elle reste un raffinement et un test de sensibilité.

Point nouveau relevé dans la méthodologie SAA : les terres sont rattachées au département du **siège de l'exploitation**, pas à celui de la parcelle. Le RPG localise les parcelles ; les deux ne coïncident donc pas exactement près des limites départementales.

---

## 5. Validation chronologique des modèles de prévision agricole

| Référence | Constat principal | Niveau |
|---|---|---|
| Morales & Villalobos (2023), *Frontiers in Plant Science*, DOI 10.3389/fpls.2023.1128388 | Avec une partition ordonnée dans le temps, même la forêt aléatoire (RMSE 35-38 %) n'a qu'un **avantage limité** sur une référence sensée (moyenne de l'exploitation, 42 %) | [RÉSUMÉ] |
| Paudel et al. (2021) | Les tendances calculées sur toute la série font fuiter de l'information ; comparaison obligatoire aux références naïves | [RÉSUMÉ] |
| Prépublication arXiv 2512.15140 (Allemagne, NUTS-3) | Performances très dégradées sur des années indépendantes par rapport à un découpage spatial ; des SHAP « crédibles » peuvent provenir de modèles peu fiables temporellement | [SECONDAIRE] |
| Étude tchèque (2026, *ScienceDirect* S2666154326000323) | Le découpage aléatoire surestime la qualité ; le découpage temporel la fait chuter | [SECONDAIRE] |

**Conséquence pour ATLAS :** la validation glissante par origine, déjà prévue, est la bonne. Il faut s'attendre à un gain modeste, voire nul, sur la référence naïve, et le présenter comme un résultat.

---

## 6. Source de données complémentaire repérée

**Schauberger, Kato, Kato, Watanabe & Ciais (2022)** [TEXTE, partiel]. « French crop yield, area and production data for ten staple crops from 1900 to 2018 at county resolution ». *Scientific Data* 9 : 38. DOI 10.1038/s41597-022-01145-4. Données sous **CC-BY 4.0**.

- Surfaces, productions et rendements par département, 1900-2018, dix cultures dont le blé tendre.
- Avant 1989, données numérisées à la main ; de 1989 à 2018, extraites de la base Agreste.
- **Intérêt pour ATLAS :** allonger la période à environ 1990-2025 augmenterait fortement le nombre d'années exposées à la chaleur extrême, qui est le principal risque de puissance identifié en phase 0.
- **Problème :** les années antérieures à 2010 ne sont pas recalées sur le RA 2020 (rupture de série). Voir la décision 1 ci-dessous.

---

## 7. Comparaison : littérature existante et contribution potentielle d'ATLAS

| Dimension | État de la littérature | Ce qu'ATLAS peut apporter | Solidité |
|---|---|---|---|
| Effet de la chaleur sur le blé français | Établi : Gammans 2017 (1950-2015), Ceglar 2016, Nóia Júnior 2025 | Rien de nouveau sur le principe | — |
| **Séparer stress thermique et stress hydrique du sol** | Fait aux États-Unis (Ortiz-Bobea 2019). Pour la France, identifié comme manquant par Gammans 2017. Aucune étude en panel départemental avec l'humidité du sol ISBA trouvée dans cette revue non exhaustive. | Panel départemental avec SWI ou eau du sol (SIM) et chaleur, avec rapport explicite de l'effet total et de l'effet partiel | **Moyenne à bonne.** Principal apport défendable, sous réserve d'une recherche complémentaire dans HAL et Google Scholar sur « SIM / SWI / rendement » |
| **Années récentes 2016-2025** | Les études lues s'arrêtent en 2015-2019 | Inclut 2016, 2020, 2022 et 2024 ; séries SAA recalées sur le RA 2020 | **Bonne**, mais il s'agit d'une mise à jour, pas d'une idée nouvelle |
| **Prévision chronologique sans fuite** | Gouache 2015 (retrait d'une année à la fois, puis test sur 2011-2014 : erreur environ doublée) ; Ben-Ari 2018 (sélection informée par 2016) ; Nóia Júnior 2025 (retrait d'une station ou d'une année ; tendance et seuils calculés sur toute la période ; aucune validation chronologique) ; mises en garde méthodologiques (Paudel, Morales) | Évaluation glissante stricte, références naïves, résultats par année test, comparaison économétrie / ML | **Moyenne.** Valeur surtout méthodologique |
| Masque de cultures par le RPG | CORINE ou aucun masque ; « aucune différence » selon Ben-Ari | Test de sensibilité seulement | **Faible** : n'est plus revendiqué comme contribution |
| Irrigation (maïs) | Hawkins 2013, Ceglar 2016 (irrigation et signal de la pluie) | Exploratoire, données fragiles | Faible |

### Conclusion sur l'originalité

ATLAS **n'est pas inédit** sur sa question générale. Sa contribution défendable est une **extension ciblée** de Gammans et al. (2017) :

1. elle introduit l'humidité du sol modélisée (ISBA) pour séparer la chaleur et l'eau ;
2. elle couvre les extrêmes récents ;
3. elle s'accompagne d'une évaluation prédictive chronologique sans fuite.

Pour un projet de portfolio de niveau M2, c'est défendable si c'est présenté ainsi, et non comme une découverte.

### Recentrage proposé

Pas de changement de sujet. Trois ajustements :

1. La **contribution principale** devient la décomposition entre chaleur et stress hydrique du sol. Le masque RPG passe au rang de robustesse.
2. ~~Lire Nóia Júnior et al. (2025) et Gouache et al. (2015) en texte complet.~~ **Fait** (PDF fournis par l'utilisateur, 2026-10-10). Ces lectures **renforcent** la contribution prédictive : aucune des deux études ne réalise de validation chronologique sans fuite, et Gouache et al. montrent que l'erreur double sur des années futures.
3. **Décision à prendre :** faut-il allonger la période vers ~1990 avec les données Schauberger (CC-BY 4.0) pour gagner de la puissance sur la chaleur extrême ?
   - Spécification principale sur 2010-2025 (séries homogènes).
   - Robustesse sur ~1990-2025, avec un effet fixe département × période pour absorber la rupture de 2010.

## 8. Lectures restant à faire

- Texte complet de Mérel & Gammans (2021).
- Recherche complémentaire sur HAL et theses.fr : « SAFRAN-ISBA rendement département », « indice d'humidité des sols rendement blé ».
- Hawkins et al. (2013) sur le maïs français (pour l'exploratoire B).

## 9. Références ajoutées pour la phase 0 bis et le mémoire : niveau de lecture (2026-10-11)

Résumés officiels lus via OpenAlex, notices vérifiées dans Crossref. Les affirmations du mémoire se limitent à ce que disent ces résumés.

| Référence | Niveau | Ce que dit le résumé (et ce que le mémoire en retient) |
|---|---|---|
| Hawkins et al. (2013), *Global Change Biology* | [RÉSUMÉ] | Maïs français : l'importance de la pluie a baissé depuis les années 1960, « likely due to increased irrigation » ; baisse significative par jour > 32 °C |
| Schauberger et al. (2017), *Nat. Commun.* | [RÉSUMÉ] | États-Unis : chaque jour > 30 °C réduit le maïs et le soja jusqu'à 6 % en pluvial ; déclins faibles en zones irriguées |
| Li & Troy (2018), *ERL* | [RÉSUMÉ] | Rendements de comté pluviaux et irrigués aux États-Unis ; le bénéfice de l'irrigation dépend du climat de la saison. **Ne dit pas** que la chaleur pénalise davantage le maïs pluvial |
| Zaveri & Lobell (2019), *Nat. Commun.* | [RÉSUMÉ] | Inde : le blé irrigué a environ un quart de la sensibilité à la chaleur du blé pluvial |
| Tack, Barkley & Hendricks (2017), *ERL* | [RÉSUMÉ] | Kansas, essais : l'irrigation « completely offsets » la perte due au réchauffement « in our sample » |
| van der Velde, Wriedt & Bouraoui (2010), *AEE* | [TITRE] | Pas de résumé disponible : seul le titre est utilisé (estimation de l'irrigation et de son effet sur le maïs en 2003) |
| van der Velde, Tubiello, Vrieling & Bouraoui (2012), *Climatic Change* | [RÉSUMÉ] | Modèle EPIC à 10 km évalué contre les anomalies régionales de 2003 et 2007 |
| Mérel & Gammans (2021), *AJAE* | [RÉSUMÉ] (était [SECONDAIRE]) | Conditions sous lesquelles le panel non linéaire approche la réponse de long terme ; indices d'adaptation de long terme aux États-Unis et en France |
| Cameron, Gelbach & Miller (2008), *REStat* | [RÉSUMÉ] | Sur-rejet avec peu de grappes (5 à 30) ; bootstrap-t en grappes |
| Webb (2023), *Canadian Journal of Economics* | [RÉSUMÉ] | Poids à 6 points qui améliorent la fiabilité avec peu de grappes |
| MacKinnon & Webb (2017), *JAE* | [RÉSUMÉ] | Bootstrap en grappes et tailles de grappes inégales ; simulations de « placebo laws » |
| Bertrand, Duflo & Mullainathan (2004), *QJE* | [RÉSUMÉ] | Lois placebo : effets « significatifs » à 5 % pour jusqu'à 45 % d'entre elles |
| Conley (1999), *Journal of Econometrics* | [TITRE] | Pas de résumé disponible : cité pour la méthode d'erreurs-types à dépendance spatiale, d'usage courant |
| Baskerville & Emin (1969), *Ecology* | [RÉSUMÉ] | Accumulation de chaleur estimée par une courbe sinusoïdale entre Tmin et Tmax |
