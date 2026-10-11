# ATLAS — Spécification de la phase 4 bis (pré-spécifiée)

*Rédigée le 2026-10-11, **avant toute estimation** sur les données de la phase 2 bis. Empreinte SHA-256 consignée dans `docs/decisions.md`. Tout écart ultérieur y sera justifié, et cette version restera rapportée.*

**Règles communes :**

- inférence de référence : **wild cluster bootstrap restreint par année** (WCR, poids de Webb, 9 999 tirages, graine 20261011) ;
- seule cette inférence fonde les conclusions : la phase 4 a montré que le cluster par département et Conley sont fortement surdimensionnés sur ces données. Les deux autres sont rapportées pour information ;
- **taille de chaque test principal vérifiée sur ses propres données** (placebo = champ d'exposition réel à années permutées, R = 300, B = 399). Si la taille empirique dépasse 10 %, la conclusion est signalée comme non fiable ;
- tous les résultats sont rapportés, y compris défavorables.

---

## Q1 : irrigation et chaleur, maïs grain (`data/processed/panel_mais_long.parquet`)

### Échantillon

- 17 départements en statut qualité 1 pour le maïs irrigué, récoltes **2000-2025**.
- **Paires** département-année où les deux modalités sont observées. Le modèle d'écart l'exige ; les modèles en niveau utilisent le même échantillon de paires.
- Poids : `surface_ref_ha` (maïs grain irrigué + non irrigué, moyenne 2010-2012, fixe).
- Météo : masque maïs (RPG `MIS`), fenêtre juillet-août.

### Modèle principal (A1)

ecart_dt = log Y_irrigué − log Y_non irrigué = α_d + γ_t + β · `dd_32_ja` + δ · `swi_ja` + ε_dt

Ce modèle équivaut au modèle empilé entièrement interagi avec les modalités, où β = β_irrigué − β_non irrigué.

### Hypothèse principale (une seule)

- **H1 : β > 0.** Les étés plus chauds creusent l'écart en faveur de l'irrigué, c'est-à-dire que le maïs non irrigué est plus pénalisé.
- Test **unilatéral**, WCR par année (26 grappes), seuil de 5 %.

### Réplication hors échantillon (rapportée, sans être une hypothèse séparée)

- A1 estimé sur **2000-2009 seulement** : ces années n'ont été utilisées par aucune analyse antérieure du projet.
- On rapporte le signe, l'estimation et la p-valeur WCR (10 grappes : peu de puissance, ce qui est assumé).

### Hypothèses secondaires (famille corrigée par Holm, 4 tests)

| Code | Hypothèse | Modèle | Test |
|---|---|---|---|
| H2a | δ < 0 : un sol plus humide réduit l'écart | A1 | Unilatéral, WCR |
| H2b | La chaleur pénalise le maïs non irrigué | log Y_non irrigué = α_d + γ_t + β_N · `dd_32_ja` + δ_N · `swi_ja` | Unilatéral (β_N < 0), WCR |
| H2c | La chaleur pénalise aussi le maïs irrigué | idem pour log Y_irrigué | Unilatéral (β_I < 0), WCR |
| H3 | Les jours de « crise » VigiEau réduisent la protection : coefficient de `dd_32_ja` × `jours_crise_ja` < 0 | A1 + `jours_crise_ja` + interaction, sur **2016-2025** | Unilatéral, WCR ; **lecture descriptive** (les restrictions sont endogènes à la sécheresse) |

### Valorisation (descriptive, conditionnelle à β̂)

**Quintaux associés à la protection** dans le département *d* l'année *t* :

surface irriguée_dt × Y_non irrigué,dt × [exp(β̂ · (`dd_32_ja`_dt − moyenne_d)) − 1]

- Calculée pour **2003, 2019 et 2022**, et agrégée au niveau national pour l'échantillon.
- Valeur en € : prix du maïs, IPPAP maïs (INSEE 010776430) raccordé à Eurostat maïs (`apri_ap_crpouta`, code 01500000) sur 2012-2016, selon la même règle que pour le blé. Si le rapport n'est pas stable (écart maximal ≥ 0,002 €/q par point), la valorisation est abandonnée.
- **Fourchette :** on recalcule avec les bornes de l'intervalle à 90 % de β obtenu par cluster année (CR1) ; ce n'est qu'une indication.
- Formulation : « quintaux **associés** à l'irrigation lors d'un été chaud », jamais « gain causé par l'irrigation ».

### Robustesses de A1 (toutes rapportées)

| Code | Variation |
|---|---|
| Q1-R1 | 38 départements (tous statuts) |
| Q1-R2 | 2010-2025 seulement (comparaison avec la phase 6) |
| Q1-R3 | Météo pondérée par la surface (`_surf`) |
| Q1-R4 | Seuil de 30 °C (`dd_30_ja`) |
| Q1-R5 | Fenêtre juillet seul |
| Q1-R6 | Sans pondération |
| Q1-R7 | Sans 2025 (provisoire) |
| Q1-R8 | Sans 2003 (année dominante de l'exposition) |

---

## Q2 : sensibilité du blé à la chaleur, 1959-2025 (`data/processed/panel_ble_1959.parquet`)

### Échantillon

- 83 départements de l'échantillon principal (statut qualité 1), récoltes **1959-2025**.
- Les observations dont le rendement manque sont retirées : 27, toutes avant 1968.
- Poids : `surface_ref_ha`. Météo : masque blé.

### Modèle principal (B1)

log Y_dt = α_{d,p} + γ_t + β₁ `gdd_0_32_remplissage` + β₂ `dd_32_remplissage` + θ₁ `prec_printemps` + θ₂ `dd_0_automne` + θ₃ `prec_automne` + ε_dt

- Ce sont les mêmes variables que M1 en phase 4.
- *p* désigne la **période de source** : 1959-1988 (numérisation manuelle de Schauberger et al.), 1989-2009 (ancienne base Agreste), 2010-2025 (SAA rétropolée). L'effet fixe département × période absorbe les ruptures de niveau.

### Hypothèses

- **Hypothèse principale (Q2-H1) : β₂ < 0.** Test unilatéral, WCR par année (67 grappes, 5 %).
- **Secondaire (Q2-H2), adaptation :** β₂ diffère-t-il entre 1959-1981, 1982-2003 et 2004-2025, trois périodes de 22 à 23 ans ?
  - Modèle : B1 avec `dd_32_remplissage` en interaction avec la période.
  - Test : Wald joint de l'égalité des trois pentes, WCR joint par année.
  - C'est une question **descriptive** : variétés, dates de semis et irrigation changent en même temps.

### Robustesses de B1

| Code | Variation |
|---|---|
| Q2-R1 | + tendances linéaires par région |
| Q2-R2 | Sans 2025 |
| Q2-R3 | 1968-2025 (panel sans rendement manquant) |
| Q2-R4 | Effets fixes département seuls par période de source, contre un effet fixe département unique |
| Q2-R5 | Seuil de 30 °C |

---

## Ce qui conclurait

- **Q1 :** H1 est établie si p WCR unilatérale < 0,05 **et** si la taille empirique du test est ≤ 10 %. La réplication 2000-2009 est rapportée comme convergente ou non, sans seuil.
- **Q2 :** même règle pour Q2-H1.
- Dans tous les cas, l'interprétation reste **associative** pour l'irrigation et « effet de court terme d'un choc météo » pour la chaleur. Aucune extrapolation au changement climatique.
