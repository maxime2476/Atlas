# ATLAS — Spécification du module prédictif (phase 5), pré-spécifiée

*Rédigée le 2026-10-10, **avant tout calcul de prévision**. L'empreinte SHA-256 sera consignée dans `docs/decisions.md`. Les modifications ultérieures y seront justifiées, et la version initiale sera rapportée.*

## 1. Question et cible

**Question :** la météo connue à la date de prévision améliore-t-elle, hors échantillon et dans l'ordre chronologique, la prévision du rendement départemental du blé tendre d'hiver par rapport à des références naïves ?

**Cadre :**

- objectif **prédictif** uniquement, sans aucune interprétation causale des importances de variables ;
- échantillon : 83 départements de l'échantillon principal ; cible : `log_rendement` ; erreurs aussi rapportées en q/ha.

## 2. Dates de prévision et variables disponibles

| Date | Météo utilisée | Fenêtres |
|---|---|---|
| **1er juin** de *t* | jusqu'au 31 mai | automne (sept.-nov. *t*−1), hiver (déc.-févr.), printemps (mars-avril), **mai** |
| **1er juillet** de *t* | jusqu'au 30 juin | automne, hiver, printemps, **mai-juin** |

**Variables par fenêtre** (masque blé) : `gdd_0_32`, `dd_32`, `hot_30`, `prec`, `etp`, `swi`, `swi_dry`, `tmin`, `tmax`. Cela donne 9 × 4 = 36 variables. Elles sont **fixées ici**, sans sélection sur les données.

**Jamais utilisés :**

- surfaces et production de l'année ;
- rendements de l'année *t* ;
- RPG de l'année *t* : le masque blé est fixe (2015-2017), une information future pour les années de test antérieures à 2018, à signaler ;
- effets fixes année.

## 3. Schéma de validation

- **Origine glissante :** pour chaque année test *t* = 2016, …, 2025, l'entraînement porte sur 2010…*t*−1 (de 6 à 15 années).
- **Tout est estimé dans le pli d'entraînement :** moyennes départementales, tendance commune, standardisation et hyperparamètres.
- **Variante (robustesse) :** entraînement sur 1990…*t*−1 avec le panel long (Schauberger RAW avant 2010), mêmes années test.
- **Fuites connues et non corrigeables, à rapporter :**
  - séries SAA rétropolées sur le RA 2020 (calées en 2022) ;
  - SIM est une réanalyse révisée ;
  - 2025 est provisoire.

## 4. Modèles

**Références :**

- **B0** : moyenne du log-rendement du département sur les années d'entraînement.
- **B1** : effet fixe département + tendance linéaire commune, par MCO sur l'entraînement, pondérés par `surface_ref_ha`.

**Modèles météo.** Ils prédisent le **résidu de B1** à partir des 36 variables météo. Les variables sont centrées par département sur l'entraînement, puis standardisées. La prévision vaut B1 + résidu prédit.

| Code | Modèle | Réglages |
|---|---|---|
| **L1** | MCO sur les variables de la spécification M1 de la phase 4, à la date de prévision | Juin : `gdd_0_32_mai`, `dd_32_mai`, `prec_printemps`, `dd_0_automne`, `prec_automne`. Juillet : version `remplissage` |
| **RIDGE** | Ridge sur les 36 variables | α choisi dans {0,1 ; 1 ; 10 ; 100 ; 1 000} par validation croisée **interne** par année (*leave-one-year-out* à l'intérieur des années d'entraînement) |
| **RF** | Forêt aléatoire | 500 arbres, `min_samples_leaf` = 10, `max_features` = 1/3 ; graine 20261010 ; pas de réglage |
| **GBM** | `HistGradientBoostingRegressor` | `max_depth` = 3, `learning_rate` = 0,05, `max_iter` = 200, `min_samples_leaf` = 20 ; graine 20261010 ; pas de réglage |

## 5. Métriques et comparaison

- **Par année test et en moyenne :**
  - RMSE et MAE du log-rendement et du rendement (q/ha), pondérés par `surface_ref_ha` ;
  - *skill score* par rapport à B1 : 1 − MSE / MSE(B1).
- **Erreur de production nationale :** rendement national pondéré prévu contre observé, par année.
- **Détection des pertes :** une année-département est « en perte » si le rendement observé est inférieur de plus de 10 % à la prévision de B1. On rapporte le rappel et la précision des modèles, la perte étant prédite si la prévision est inférieure de plus de 5 % à B1.
- **Incertitude :** intervalle à 95 % de l'écart de MSE entre un modèle et B1, par **bootstrap par blocs d'années test** (10 blocs, 9 999 tirages, graine 20261010). On rapporte aussi le nombre d'années test où le modèle bat B1.
- **Ce qui conclurait à un gain de la météo :** un *skill score* moyen positif **et** un intervalle de l'écart de MSE excluant 0. Sinon, on conclut à l'absence de gain démontré.

## 6. Importances de variables

L'importance par permutation est calculée sur les années test, pour RIDGE et GBM, à la date du 1er juillet. Elle est présentée comme une **contribution prédictive**, et non comme un effet.
