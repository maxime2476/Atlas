# ATLAS — Notes méthodologiques (phase 1)

*Rédigées le 2026-10-10. Ces notes **précèdent** tout calcul d'exposition : aucun degré-jour n'a encore été codé.*

---

## 1. Fenêtres, unités et convention de date de `TINF_H` et `TSUP_H`

### Ce que dit la documentation officielle

Source : notice `sim-quotidienne-parametres-20260331.pdf`, lue intégralement.

| Variable | Définition | Fenêtre | Unité |
|---|---|---|---|
| `TINF_H` | Température minimale des 24 températures horaires | ]18 UTC − 18 UTC] | °C, au 1/10 |
| `TSUP_H` | Température maximale des 24 températures horaires | ]06 UTC − 06 UTC] | °C, au 1/10 |
| `T` | Température moyenne quotidienne | ]00 UTC − 00 UTC] | °C, au 1/10 |

La notice **ne précise pas** si la fenêtre ]06 UTC − 06 UTC] associée à la date J commence le jour J ou la veille. La même incertitude vaut pour ]18 − 18 UTC]. La page de documentation Confluence de Météo-France ne le précise pas non plus (consultée le 2026-10-10).

### Vérification empirique

Script `scripts/02_check_sim.py`, fichier 2009, 9 892 mailles × 365 jours.

On corrèle les variations journalières ΔX(J) avec ΔT(J + k). On utilise `T`, dont la fenêtre ]00-00 UTC] est sans ambiguïté, comme référence. Raisonner sur les différences neutralise la persistance de la température.

| | k = −1 | k = 0 | k = +1 |
|---|---|---|---|
| Δ`TINF_H`(J) avec Δ`T`(J+k) | 0,384 | **0,584** | −0,231 |
| Δ`TSUP_H`(J) avec Δ`T`(J+k) | −0,150 | **0,817** | 0,084 |

**Interprétation :**

- `TSUP_H`(J) suit surtout la température du jour civil J. Sa fenêtre est donc ]06 UTC J, 06 UTC J+1], et contient l'après-midi de J.
- `TINF_H`(J) suit aussi le jour J, avec une corrélation résiduelle avec J−1 cohérente avec une fenêtre ]18 UTC J−1, 18 UTC J]. Celle-ci contient la nuit et le matin de J.
- Avec la convention inverse, on aurait attendu un maximum à k = −1 pour `TSUP_H` et à k = +1 pour `TINF_H`.
- Contrôle de cohérence (qui ne départage **pas** les conventions, car deux fenêtres de 24 h décalées de 12 h se chevauchent toujours) : sur tout le fichier 2009, aucune ligne n'a `TINF_H > TSUP_H`.
- Limite du test : une seule année, toutes saisons confondues.

**Règle retenue (déduite, non documentée officiellement) :** pour le jour civil J, Tmin(J) = `TINF_H`(J) (minimum du matin de J) et Tmax(J) = `TSUP_H`(J) (maximum de l'après-midi de J). C'est l'appariement standard des méthodes sinusoïdales.

**Réplication sur 2022** (même script, `--year 2022`) : Δ`TINF_H` → 0,396 / **0,593** / −0,200 ; Δ`TSUP_H` → −0,082 / **0,799** / 0,121 (k = −1 / 0 / +1). La conclusion est identique.

Reste possible : demander confirmation à Météo-France (la documentation est muette sur ce point).

### Unités

- Températures en °C au 1/10, confirmé par les valeurs observées (`TSUP_H` max 2009 = 40,6 °C).
- **`SWI` : écart à la notice.** La notice indique « % », mais les valeurs vont de −0,035 à 2,075. C'est un indice sans dimension, environ 0 au point de flétrissement et 1 à la capacité au champ. Cette lecture est conforme à la définition usuelle du Soil Wetness Index de Météo-France, mais **elle reste à confirmer**. Tout seuil devra s'exprimer sur cette échelle.

---

## 2. Calcul de l'exposition thermique à partir de Tmin et Tmax quotidiennes

Le fichier quotidien ne fournit pas les températures horaires de SAFRAN. L'exposition au-delà d'un seuil (degrés-jours extrêmes, EDD) doit donc être **approximée** à partir de Tmin et Tmax.

| Méthode | Principe | Référence | Avantages | Limites |
|---|---|---|---|---|
| **Sinus simple** | Un sinus entre Tmin(J) et Tmax(J) sur 24 h ; on intègre la partie au-dessus du seuil | Baskerville & Emin (1969), *Ecology* 50 : 514-517, DOI 10.2307/1933912 (référence vérifiée sur Crossref) | Formule fermée, simple à tester | Cycle symétrique ; ignore la nuit suivante |
| **Double sinus** | Un demi-sinus de Tmin(J) à Tmax(J) (matin → après-midi), un autre de Tmax(J) à Tmin(J+1) (après-midi → matin suivant) | Utilisée par Gammans et al. (2017) : « fitting a double-sine curve between the minimum and maximum temperatures of consecutive days » [texte lu] | Comparabilité directe avec la référence française | Formule un peu plus longue ; demande Tmin(J+1) |
| **Jours avec Tmax > seuil** | Simple comptage | — | Très lisible, robuste | Ne mesure pas l'intensité |

**Proposition :**

- **double sinus en spécification principale** (comparabilité avec Gammans et al.) ;
- comptage des jours avec Tmax > *T\** en robustesse.

Les deux sont calculés **au niveau maille-jour, puis agrégés** au département (phase 0, § 3.2 ; Hogan & Schlenker 2024).

**Limites à reconnaître :**

1. Le cycle diurne réel n'est pas sinusoïdal (montée rapide le matin, descente lente le soir).
2. Tmin et Tmax proviennent de fenêtres décalées (§ 1). L'appariement est inféré.
3. Une réanalyse interpolée à 8 km **lisse probablement les extrêmes locaux** : l'EDD sera vraisemblablement sous-estimé par rapport aux stations. C'est une hypothèse plausible, non vérifiée ici.
4. Il s'agit de la température de l'air à 2 m, pas de celle du couvert végétal.
5. Gammans et al. notent « little exposure to temperatures above 34 °C » sur 1950-2015. L'exposition au-delà de 32 °C doit être **comptée avant toute régression** (règle de repli, phase 0, § 5).

**Tests unitaires prévus en phase 2**, sur des cas calculés à la main :

- Tmax ≤ seuil → EDD = 0 ;
- Tmin ≥ seuil → EDD = moyenne − seuil ;
- cas symétrique Tmin = 20, Tmax = 36, seuil = 28 → valeur analytique ;
- monotonie par rapport à Tmax ;
- GDD + EDD cohérents avec la moyenne quand aucune borne n'est active.

---

## 3. Disponibilité et compatibilité des millésimes RPG

Sources lues : « RPG — Suivi des évolutions » (révision de septembre 2026), descriptifs de contenu v1.0 et v2.1, inventaire du flux `https://data.geopf.fr/telechargement/resource/RPG` (349 entrées).

| Millésimes | Version | Unité | Information culture | Livraison |
|---|---|---|---|---|
| 2007-2014 | 1.0 | **Îlot** (groupe de parcelles contiguës d'un même exploitant) | **Groupe de cultures majoritaire** uniquement ; « 01 BLÉ TENDRE » ne distingue pas hiver et printemps | Shapefile **par région** |
| 2015-2020 | 2.0 | **Parcelle** | Code culture détaillé (`BTH` = blé tendre d'hiver, `BTP` = de printemps) ; de nouveaux codes apparaissent en 2017, 2018, 2019 et 2020 | Shapefile par région ou France ; GeoPackage à partir de 2019 |
| 2021-2023 | 2.0 / 2.1 / 2.2 | Parcelle | Idem ; pas de continuité de `ID_PARCEL` avant et après 2022 | GeoPackage national : **4,2 Go en `.7z`** (2021) |
| 2024-2025 | 3.0 / 4.0 | Parcelle | Offre éclatée en 8 ou 9 sous-produits | GeoPackage national : **≈ 11 Go en `.7z` (3 parties)** (2025) |

**Conséquences :**

- Une pondération **propre à chaque année et à la culture** (blé tendre d'hiver) n'est **pas possible de façon homogène** sur 2010-2025 : rupture d'unité et de nomenclature en 2015.
- Une pondération annuelle serait de toute façon **indésirable** : la surface semée de l'année dépend de la météo d'automne (phase 0, § 3.4), et les poids doivent être fixes.
- **Proposition :**
  - spécification principale avec un **masque fixe** de parcelles `BTH`, moyenne 2015-2017 (premiers millésimes parcellaires) ;
  - robustesse 1 : masque fixe v1.0 2010-2012 (îlots du groupe 01, sur la même période que la définition de la population) ;
  - robustesse 2 : aucun masque (moyenne sur la surface du département), comme Ben-Ari et al. (2018).
- **Promesse à ne pas faire :** « pondération par les parcelles cultivées de chaque année sur toute la période ».
- **Technique :** les archives `.7z` demandent l'outil système `7zip` (décision du 2026-10-10, installation par l'utilisateur en attente, voir `docs/decisions.md`). Les shapefiles régionaux 2015-2017 sont probablement plus légers ; à vérifier en phase 2 avant tout téléchargement.

---

## 4. Information disponible à la date de prévision (module prédictif)

Règle générale : une variable n'est utilisable pour prévoir la récolte de l'année *t* à la date *D* que si elle est connue à *D*.

| Information | Connue au 1er juin *t* ? | Commentaire |
|---|---|---|
| Météo SIM jusqu'au 31 mai *t* | Oui | Troncature des séries à `DATE` ≤ 31 mai. La fenêtre de `TSUP_H`(31 mai) s'achève le 1er juin à 06 UTC, avant la prévision. |
| Météo SIM après le 31 mai *t* | **Non** | Exclue des variables de la prévision au 1er juin (incluse dans celle au 1er juillet, jusqu'au 30 juin) |
| Version de SIM | **Différente** | Les fichiers actuels sont une réanalyse révisée ; en temps réel, on aurait disposé d'une version provisoire. Fuite d'information légère, non corrigeable, **à signaler** |
| Rendements SAA ≤ *t*−1 | Partiellement | En juin *t*, seule la version **provisoire** de *t*−1 était publiée. Les séries actuelles sont de plus rétropolées sur le RA 2020 (calées en 2022). Fuite légère, **à signaler** |
| Surface de blé de l'année *t* (SAA) | **Non** | Publiée au printemps *t*+1 ; exclue des variables (et c'est un mauvais contrôle) |
| RPG de l'année *t* | **Non** | Déclarations PAC au printemps *t*, diffusion en *t*+1 ; le masque fixe 2015-2017 évite le problème… sauf pour les prévisions des années ≤ 2017, où le masque utilise une **information future**. À signaler, ou remplacer par le masque v1.0 2010-2012 pour ces années. |
| Tendance, effets fixes département | Oui, **si estimés sur les seules années d'entraînement** | À recalculer dans chaque pli |
| Seuils, fenêtres, sélection de variables | Oui, **s'ils sont fixés ex ante ou dans les plis** | Leçon de Ben-Ari et al. (2018) : leur sélection était informée par 2016 |

---

## 5. Engagement sur les spécifications

Les seuils (*T\** = 32 °C, repli à 30 °C), les fenêtres (phase 0, § 5), la population (85 départements, surface moyenne 2010-2012 ≥ 1 000 ha, comptée en phase 1) et la spécification principale sont **fixés avant toute estimation**.

Toute modification ultérieure doit :

1. être consignée avec sa date et sa justification dans un journal des décisions ;
2. reposer sur un motif extérieur aux résultats d'estimation (exposition insuffisante, erreur de données, etc.) ;
3. laisser la spécification initiale rapportée à côté de la nouvelle.

Aucun seuil, fenêtre ou spécification ne sera modifié pour améliorer la significativité statistique.
