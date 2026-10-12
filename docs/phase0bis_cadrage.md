# ATLAS — Phase 0 bis : recentrage sur le maïs et l'irrigation, et série longue du blé

*Rédigé le 2026-10-11. Cadrage et audit de faisabilité uniquement : **aucune estimation**. Les décisions marquées « à valider » attendent l'accord de l'utilisateur.*

## 1. Pourquoi recentrer

Les phases 4 à 6 ont montré trois choses :

- **Blé (2010-2025) :** l'information effective tient en 3 ou 4 années. L'association avec la chaleur extrême (≈ −1,5 % par °C·jour) n'est pas distinguable de zéro avec une inférence de taille correcte.
- **Maïs non irrigué (exploratoire) :** la chaleur de juillet-août est nettement associée au rendement : −5,9 % par °C·jour, p WCR = 0,002, taille du test vérifiée.
- **Exposition :** pour le maïs en juillet-août, elle est deux fois plus variable et mieux répartie entre les années (N_eff de 6,9 contre 4,1).

Le signal économiquement intéressant (la valeur de l'irrigation par fortes chaleurs) se trouve donc du côté du maïs. Pour le blé, la seule voie vers plus de puissance est d'allonger la période.

## 2. Questions proposées

### Q1 (principale) : combien l'irrigation protège-t-elle le maïs grain des étés chauds et secs en France ?

- **Estimand :** l'écart de log-rendement entre maïs irrigué et non irrigué, et sa variation avec la chaleur extrême (degrés-jours > 32 °C) et l'humidité du sol de juillet-août, à département et année donnés.
- **Traduction économique :** quintaux, puis euros, « protégés » par hectare irrigué pour un été donné (2003, 2019, 2022…), au prix IPPAP du maïs.
- **Mécanisme :** l'irrigation lève la contrainte hydrique, mais pas toute la contrainte thermique. C'est ce que montrent les données américaines (Schauberger et al. 2017 ; Li & Troy 2018) et indiennes (Zaveri & Lobell 2019).
- **Hypothèses :**
  - H1 : la pente « chaleur → rendement » est plus forte pour le non irrigué ;
  - H2 : l'écart augmente avec la chaleur et diminue avec l'humidité du sol ;
  - H3 (descriptive) : les étés de restrictions de niveau « crise » (VigiEau) réduisent l'écart, l'irrigation y étant restreinte.
- **Nature :** **associative** ; l'irrigation n'est pas assignée au hasard (§ 5).

### Q2 (secondaire) : la sensibilité du blé à la chaleur sur 1959-2025

- **Objet :** même design que la phase 4, sur environ 66 récoltes, avec la série Schauberger RAW (1959-2009) et la SAA (2010-2025).
- **Objectif :** gagner en puissance (davantage d'années extrêmes : 1976, 2003…) et pouvoir tester une **évolution de la sensibilité** au cours du temps (adaptation ?), sans extrapoler au changement climatique.

### Option écartée pour l'instant

L'extension européenne (régions NUTS 2), la plus puissante mais aussi la plus coûteuse : 2 à 3 semaines de travail, et un compte Copernicus pour ERA5-Land.

## 3. Positionnement bibliographique (vérifié sur OpenAlex ; textes à lire en phase 1 bis)

| Référence | Apport | Ce qui manque pour la France |
|---|---|---|
| Hawkins et al. (2013), *Global Change Biology*, DOI 10.1111/gcb.12069 | Maïs français depuis 1960 ; effet des jours > 32 °C ; rôle de l'irrigation **déduit** de la baisse de la sensibilité à la pluie | Pas de comparaison directe entre irrigué et non irrigué |
| van der Velde et al. (2010), EPIC, canicule de 2003 | L'irrigation réduit les pertes de 2003 (modèle de culture) | Pas d'estimation statistique en panel |
| Schauberger et al. (2017), *Nat. Commun.* 8 : 13931 | États-Unis : chaque jour > 30 °C coûte jusqu'à 6 % au maïs non irrigué, et peu à l'irrigué | Hors France |
| Li & Troy (2018), *ERL*, DOI 10.1088/1748-9326/aac4b1 | Comtés américains, rendements irrigués et non irrigués séparés | Hors France |
| Zaveri & Lobell (2019), *Nat. Commun.*, DOI 10.1038/s41467-019-12183-9 | Inde : le blé irrigué a environ ¼ de la sensibilité à la chaleur | Hors France, autre culture |
| Tack, Barkley & Hendricks (2017), *ERL* 12 : 114027 | Kansas, essais : l'irrigation compense la perte due à la chaleur | Échelle d'essais |

**Contribution potentielle (à confirmer par une recherche complémentaire) :** à notre connaissance, aucune estimation en panel ne compare **directement** maïs irrigué et non irrigué en France en lien avec la chaleur et l'humidité du sol. ATLAS apporterait une **application française** de designs établis, avec une **valorisation économique** et un regard sur les **restrictions d'eau**. Ce n'est pas une nouveauté méthodologique.

## 4. Audit des sources (tests réalisés le 2026-10-11)

| Source | Utilité | Test effectué | Constat | Statut |
|---|---|---|---|---|
| SAA, codes 14 et 15 (maïs irrigué / non irrigué), 2010-2025 | Q1 | Déjà exploitée (phase 6) | 38 départements avec ≥ 1 000 ha de chaque ; **seuls 17 en statut qualité 1** ; Jura 2016 et 2018 inexploitables | **Validée**, fragile |
| SAA « anciennes séries » 2000-2020, tableau « Cultures développées » (`SAANR_DEVELOPPE_2`) | Q1 : allonger l'irrigué / non irrigué | Exploration dans Chromium sans interface (Playwright), puis téléchargement direct du ZIP (8,8 Mo, un CSV par année) | **Le partage « maïs grain irrigué / non irrigué » existe** (surface, production, rendement), avec 60 à 65 départements chaque année de 2000 à 2009. Sur 2010-2020, comparé aux séries rétropolées : 671 paires, 94-95 % identiques à ±0,5 q/ha, écart médian 0, corrélation 0,98 (irrigué) et 0,99 (non irrigué). Pas de statut qualité par département | **Validée** : panel maïs 2000-2025 possible |
| RPG 2015-2017, code `MIS` | Masque maïs (Q1) | Table de référence lue ; masque construit en phase 2 bis et comparé à la SAA | **Correction (phase 2 bis)** : `MIS` correspond au **maïs grain** (corrélation départementale de 0,993 avec la SAA grain, 0,04 avec le maïs fourrage ; ratio 1,03-1,08). L'ensilage porte un autre code. Ne distingue pas irrigué et non irrigué | **Validée** |
| SIM 2009-2025 (déjà téléchargé) | Q1 : juillet-août | — | Disponible | **Validée** |
| VigiEau, « Donnée Sécheresse » (MTE), https://www.data.gouv.fr/datasets/donnee-secheresse-vigieau | Q1 / H3 : restrictions d'eau | Arrêtés 2012-2024, arrêtés en cours et arrêtés-cadres téléchargés (21 Mo, au manifeste) | Arrêtés annuels **2012-2024**, avec dates, département, zones d'alerte et **niveau de gravité** (vigilance → crise). Cartes des zones de 2013 à 2025 (lourdes). Licence Ouverte 2.0 | **Validée** (niveau département × jour) |
| IPPAP maïs (INSEE BDM) | Valorisation (Q1) | Série trouvée et téléchargée (idbank 010776430, 1970-2025) | Raccord au prix absolu à faire (Eurostat maïs jusqu'en 2016) | **Validée** |
| Schauberger RAW, blé d'hiver | Q2 | Couverture calculée | 82 départements de la population dès 1950-1965, 85 dès 1970 ; compatibilité avec la SAA déjà validée (2010-2018) | **Validée** |
| SIM 1958-1988 | Q2 | Téléchargés ; couverture contrôlée année par année | 1958 commence le 1er août 1958 (début de la réanalyse), donc septembre 1958 et la récolte 1959 sont couverts. 1959-1988 complets (9 892 mailles, 365 ou 366 jours) | **Validée** |
| Masque blé RPG 2015-2017 | Q2 | — | Appliqué à 1959 : anachronique. Robustesse sans masque (surface) indispensable | **Validée** avec limite |

## 5. Faisabilité et menaces

**Q1, maïs et irrigation :**

- **Taille :** 270 observations (17 départements en statut 1, 2010-2025), ou 606 (38 départements, tous statuts). Ce sont des comptages après retrait des valeurs manquantes, et non des produits (17 × 16 = 272 ; 38 × 16 = 608). C'est petit mais informatif : la taille du WCR est vérifiée et N_eff = 6,9.
- **Sélection et composition :**
  - le partage irrigué / non irrigué de la SAA est en partie **construit** (statut 2 ou 3 pour 21 départements sur 38) ;
  - les surfaces irriguées changent d'une année à l'autre, et l'on irrigue d'abord les meilleures terres ou les exploitations les mieux équipées.

  L'écart mélange donc l'effet de l'eau et des différences de sol et de conduite. Les effets fixes département absorbent la partie permanente, **pas** les changements de composition.
- **Restrictions (H3) :** elles sont **endogènes** à la sécheresse. Elles ne servent qu'en description ou en hétérogénéité, jamais comme « traitement ».
- **Mesure :**
  - masque `MIS` : maïs grain (vérifié en phase 2 bis), mais sans distinction irrigué / non irrigué ;
  - météo de juillet-août non différenciée entre parcelles irriguées et non irriguées, qui sont souvent dans des secteurs différents d'un même département.
- **Inférence :** WCR par année, la leçon des phases 4 et 6, avec une taille à revérifier pour chaque spécification. 12 tests au moins : correction pour tests multiples (Holm) **à pré-spécifier**.

**Q2, blé 1959-2025 :**

- ruptures de série : SAA rétropolée à partir de 2010, contre l'ancienne Agreste et la numérisation manuelle avant 1989 (Schauberger), d'où un effet fixe département × période ;
- tendance non linéaire (plafonnement depuis le milieu des années 1990), d'où des tendances flexibles (splines ou rupture) **pré-spécifiées** ;
- changements de variétés et de dates de semis sur 66 ans : la sensibilité n'est probablement pas constante. C'est une **question** (adaptation), mais aussi une source de mauvaise spécification ;
- la taille du WCR avec environ 66 grappes année est à revérifier par simulation.

## 6. Protocole préliminaire (à figer dans une spécification avant estimation)

**Q1 :**

1. Masque maïs `MIS` (RPG 2015-2017) → météo de juillet-août pondérée par le maïs.
2. Modèles « empilés » : log Y_{d,t,k} pour *k* ∈ {irrigué, non irrigué}, avec effets fixes département × modalité et année × modalité, et des pentes chaleur et SWI propres à chaque modalité. Le test de H1 porte sur la différence des pentes.
3. Modèle de l'écart (phase 6) en complément.
4. **Valorisation :** l'écart prédit par la chaleur d'un été donné, multiplié par la surface irriguée et par le prix IPPAP du maïs, avec une incertitude par bootstrap. Ce sont des « quintaux associés », non causaux.
5. **H3 :** nombre de jours en restriction « crise » en juillet-août, par département (VigiEau, 2012-2025), en interaction descriptive avec l'écart.
6. **Robustesses :** tous statuts ou statut 1 ; seuils 30 et 32 °C ; fenêtre juillet ou juillet-août ; pondération par le masque ou par la surface ; Holm.

**Q2 :**

1. SIM 1958-2025 → fenêtres du blé (mêmes définitions qu'en phase 4).
2. M1 sur 1959-2025, avec effets fixes département × période et année.
3. Interaction chaleur × décennie (adaptation), à pré-spécifier.
4. WCR par année et simulation de taille.

## 7. Risques

| Risque | Probabilité | Parade |
|---|---|---|
| L'écart irrigué / non irrigué reflète la méthode d'estimation de la SAA plutôt que l'agronomie | Moyenne | Restreindre au statut 1 ; comparer avec les tous statuts ; transparence |
| 17 départements, c'est trop peu pour des interactions | Moyenne | Peu de paramètres, fixés à l'avance ; pas de recherche de spécification |
| Masque `MIS` ~~biaisé par l'ensilage~~ : risque levé en phase 2 bis (`MIS` = maïs grain) | — | Robustesse par la surface conservée |
| Ruptures de la série blé 1959-2025 | Élevée | Effet fixe département × période ; tendances flexibles ; robustesse 1990-2025 |
| Tests multiples | Élevée | Correction de Holm pré-spécifiée ; hypothèse principale unique par question |

## 8. Plan proposé et décisions à valider

| Étape | Contenu | Validation |
|---|---|---|
| **1 bis** | Lire les textes (Hawkins 2013, Li & Troy 2018, Zaveri & Lobell 2019) ; télécharger SIM 1958-1988, VigiEau 2012-2024 et l'IPPAP maïs ; vérifier SIM 1958 et l'existence de l'irrigué / non irrigué de la SAA 2000-2009 (accès manuel) | Manifeste, empreintes, tests de schéma |
| **2 bis** | Masque maïs `MIS` ; météo de juillet-août pondérée par le maïs ; restrictions VigiEau par département et par jour ; fenêtres du blé sur 1959-2025 | Tests unitaires et contrôles de jointure |
| **3 bis** | **Spécification écrite et empreinte consignée avant estimation** (Q1 et Q2), dont la correction de Holm | `decisions.md` |
| **4 bis** | Estimations (R) et simulations de taille | Revue par `econometrics-reviewer` |
| **5 bis** | Valorisation et mise à jour du README | Revue par `scientific-review` |

**Décisions à valider :**

1. Q1 (maïs et irrigation) comme question principale, Q2 (blé 1959-2025) comme question secondaire.
2. Échantillon principal Q1 : les 17 départements en statut 1, les 38 tous statuts en robustesse. Ou l'inverse, pour gagner en taille au prix de la qualité.
3. Téléchargements : environ 4,2 Go de SIM (1958-1988) et quelques Mo de VigiEau et d'IPPAP.
4. Accès manuel aux tableaux SAA 2000-2009 (par vous, dans un navigateur), si l'on veut allonger l'irrigué / non irrigué.

## 9. Décisions prises (2026-10-11)

1. Q1 (maïs et irrigation) en question principale, Q2 (blé 1959-2025) en question secondaire : **validé par l'utilisateur**.
2. Échantillon principal Q1 : la recommandation est retenue. On garde le statut qualité 1 pour le maïs irrigué (17 départements, statut de 2025) ; les 38 départements tous statuts servent de robustesse.

   **Fait nouveau :** les anciennes séries SAA permettent d'allonger le panel maïs à **2000-2025**. Le statut qualité n'existant pas avant 2010, on applique le statut 2025 sur toute la période. C'est une limite à documenter. Effectifs à recalculer en phase 2 bis.
3. Téléchargements réalisés : SIM 1958-1988 (≈ 4,2 Go), VigiEau 2012-2024, IPPAP maïs, SAA anciennes séries.
4. Vérification de la SAA 2000-2009 faite par Claude avec Playwright, à la demande de l'utilisateur.
   - Chromium sans interface a été installé dans le cache de l'utilisateur, et ses bibliothèques manquantes extraites localement depuis les paquets Ubuntu (`apt-get download`), **sans `sudo`**.
   - La vérification TLS n'a pas été désactivée : Chromium complète lui-même la chaîne de certificats d'Agreste.
   - Navigation en lecture seule ; le fichier a ensuite été téléchargé par `scripts/01_download_raw.py --saa-ancienne`.
