# ATLAS — Phase 0 ter : audit des sources pour consolider Q1

*2026-10-11. Audit uniquement : aucun téléchargement en masse dans `data/raw/`. Les échantillons sont restés dans le scratchpad de la session, puis ont été supprimés.*

**Objectif** (après la phase 4 bis) :

- **Étape 1 :** déterminer si la dépendance de Q1 à la mesure de la chaleur vient d'un masque maïs anachronique (2015-2017 appliqué à 2000-2009) ;
- **Étape 2 :** vérifier s'il est possible d'exprimer le résultat par m³ d'eau d'irrigation.

## 1. Tableau d'audit

| Source | URL / accès | Variables utiles | Couverture | Licence | Test effectué | Statut |
|---|---|---|---|---|---|---|
| IGN / ASP, RPG version 1.0 (îlots anonymes) | `https://data.geopf.fr/telechargement/resource/RPG`, archives `RPG_1-0__SHP_LAMB93_R<région>_<année>-01-01.7z` | Géométrie de l'îlot, `CODE_CULTU` = **groupe de cultures majoritaire** de l'îlot (02 = « maïs grain et ensilage ») | 2007-2014 ; 13 régions métropolitaines (découpage 2016) × 8 ans ; ≈ 10,8 Go en tout, 260-280 Mo par région et par an | Licence Ouverte 2.0 (comme le RPG 2.0) | Liste des 139 paquets ; téléchargement et lecture de Nouvelle-Aquitaine 2008 et Auvergne-Rhône-Alpes 2008 ; masque comparé au masque MIS 2015-2017 | **Validée**, avec deux limites : îlot entier attribué au groupe majoritaire, et ensilage inclus |
| BNPE via l'API Hub'Eau « Prélèvements en eau » | `https://hubeau.eaufrance.fr/api/v1/prelevements/chroniques(.csv)?code_departement=..&code_usage=IRR` | Volume annuel prélevé (m³) par ouvrage, usage, commune, mode d'obtention (mesuré, estimé, forfaitaire), producteur (agence de l'eau) | Irrigation : 821 352 lignes pour la France ; 2008-2024 selon les agences ; pagination de 20 000 lignes | Licence Ouverte (données publiques Eaufrance, **à vérifier**) | Requêtes sur les Landes, le Bas-Rhin, le Loiret et l'Isère | **Validée avec réserves fortes** (§ 3) |

## 2. Étape 1 : le masque d'époque change-t-il l'exposition ?

**Méthode :** même règle que le masque 2015-2017 (îlots du groupe 02, rattachés à une maille SIM et à un département par leur centroïde), sur 2008.

**Comparaison des masques, Auvergne-Rhône-Alpes** (`dd_32` de juillet-août, °C·jour) :

| Département | Corrélation des poids par maille (2008 / 2015-2017) | 2003, masque 2008 | 2003, masque 2015-2017 | 2003, pondération surfacique (R3) |
|---|---|---|---|---|
| 01 Ain (échantillon principal) | 0,99 | 15,5 | 15,7 | 11,7 |
| 03 Allier (principal) | 0,96 | 21,0 | 21,0 | 20,2 |
| 26 Drôme (principal) | 0,96 | 20,4 | 20,7 | 12,7 |
| 38 Isère (principal) | 0,94 | 17,1 | 17,8 | 9,3 |
| 63 Puy-de-Dôme (principal) | 0,97 | 16,9 | 18,5 | 8,1 |
| 69 Rhône (principal) | 0,85 | 16,6 | 19,5 | 15,3 |

- **Nouvelle-Aquitaine :** même constat. Les écarts entre masques ne dépassent pas 0,3 °C·jour en 2003, sauf dans la Creuse, qui a peu de maïs.
- **Surfaces :** les îlots du groupe 02 dépassent la surface SAA en maïs grain de 2008 de 20 à 50 %, parce que l'ensilage est inclus et que les îlots sont attribués en entier.

**Résultat observé :**

- un masque de 2008 donne **presque la même exposition** que le masque 2015-2017 ;
- les écarts restent faibles là où il y a de l'ensilage dans les reliefs (Rhône, Puy-de-Dôme : 1,5 à 3 °C·jour en 2003) ;
- le masque d'époque reste **très loin** de la pondération surfacique, dont les écarts atteignent 8 à 10 °C·jour en 2003.

**Interprétation :**

- **L'âge du masque n'explique pas la divergence entre les deux mesures.** La divergence vient de la géographie intra-départementale. Dans les départements de relief (Drôme, Isère, Jura, Puy-de-Dôme, Ain), le maïs est cultivé dans les plaines chaudes (vallées du Rhône et de l'Isère, Limagne, Bresse). La pondération surfacique y mélange ces plaines avec des montagnes sans maïs, et sous-estime fortement la chaleur subie par la culture.
- Deux éléments jouent en faveur du masque maïs :
  - la spécification de la phase 4 bis avait désigné **avant estimation** le masque maïs comme mesure principale, et la pondération surfacique comme robustesse (R3) ;
  - l'argument agronomique (mesurer la chaleur là où pousse la culture) est fort.
- Cette lecture reste une **explication proposée après coup**, pas un test. Elle n'explique pas pourquoi la pondération surfacique donne un coefficient *plus fort* sur 2010-2025.

**Conséquence pour l'étape 1 :** construire un masque 2007-2009 complet coûterait environ 4 Go. D'après cet audit, ce masque ne changerait que marginalement l'exposition. Je recommande donc une **version allégée** :

- masque 2008 pour les seules 4 régions de l'échantillon principal (Auvergne-Rhône-Alpes, Grand Est, Centre-Val de Loire, Bourgogne-Franche-Comté), soit environ 1,1 Go ;
- réestimation de A1, déclarée comme robustesse supplémentaire **non pré-spécifiée en phase 4 bis**.

## 3. Étape 2 : BNPE, l'eau d'irrigation est-elle mesurable ?

**Volumes d'irrigation annuels en millions de m³ (Mm³) :**

| | 2012 | 2015 | 2019 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|
| 67 Bas-Rhin (agence Rhin-Meuse) | 17,6 | 37,7 | 31,2 | 9,2 | 42,1 | 37,9 |
| 45 Loiret (agences Loire-Bretagne et Seine-Normandie) | 38,1 | 83,2 | 74,1 | 44,2 | 79,6 | 41,8 |
| 38 Isère (agence Rhône-Méditerranée-Corse) | 76,6 | 66,5 | 78,8 | 37,9 | 93,3 | 66,9 |

- **Signal plausible :** volumes bas en 2021 (été humide) et élevés en 2015, 2019 et 2022.
- **Mesure :** 90 à 99 % des volumes sont mesurés, contre 0,5 à 9 % estimés ou forfaitaires.

**Réserves :**

1. **Couverture hétérogène selon l'agence.** Rhin-Meuse et Rhône-Méditerranée-Corse couvrent 2012-2023 dans l'API ; Adour-Garonne, Loire-Bretagne et Seine-Normandie couvrent 2008-2024. La période commune est **2012-2023**, soit 12 étés.
2. **Ruptures de déclaration :** en Isère, le nombre d'ouvrages tombe de 1 452 à 312 en 2014, puis remonte à 866. Dans les Landes, il passe de 1 645 en 2012 à 721 en 2024. Une partie de ces variations reflète la collecte, pas les prélèvements.
3. **Toutes cultures confondues :** le volume n'est pas attribué au maïs. Le maïs domine l'irrigation en Alsace et dans le Sud-Ouest, mais pas dans le Loiret (blé, semences, légumes).
4. **Volume annuel, pas estival ;** BNPE alimentée par les redevances des agences, donc non exhaustive (petits préleveurs).
5. **Endogénéité :** on irrigue davantage pendant les étés chauds. Un ratio « € associés par m³ » serait descriptif, jamais une productivité marginale de l'eau.

**Conséquence pour l'étape 2 :** un ratio par m³ est faisable, mais seulement :

- en **descriptif** ;
- sur 2012-2023 ;
- dans des départements où le maïs domine l'irrigation : il faudra le vérifier, par exemple avec le recensement agricole 2020 (surface irriguée par culture), source **non auditée ici** ;
- avec un contrôle des ruptures de déclaration.

Pour l'échantillon principal, cela laisse surtout le Haut-Rhin et le Bas-Rhin (environ 32 % du poids). L'intérêt est réel, mais la portée serait limitée.

## 4. Recommandation

1. **Étape 1 allégée (recommandée, peu coûteuse) :**
   - masque 2008 pour les 4 régions, réestimation de A1 ;
   - documentation de la géographie intra-départementale comme cause de la divergence entre mesures (carte ou tableau descriptif des départements de relief).

   Résultat attendu : Q1 devient défendable sur ce point. L'explication restera rédigée comme a posteriori.
2. **Étape 2 :** à faire seulement si un ratio par m³ restreint à quelques départements vous intéresse. Il faut d'abord auditer le recensement agricole 2020 (part du maïs dans l'irrigation).
3. Dans tous les cas, la conclusion de Q1 reste une **association**.

---

*Errata du 2026-10-12 (audit avant publication) :*
- *Volume du masque 2008 : les quatre archives régionales téléchargées font 81 à 284 Mo, soit ≈ 0,63 Go au total, et non « environ 1,1 Go » (§ 2) ni « 260-280 Mo par région » pour toutes (§ 1).*
- *Licence du RPG 1.0 : vérifiée le 2026-10-12 sur la fiche data.gouv « RPG » (Licence Ouverte 2.0), qui liste les ressources RPG 1.0 2008 ; la mention « comme le RPG 2.0 » du § 1 était une présomption.*
