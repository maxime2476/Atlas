# ATLAS — Spécification économétrique de la phase 4 (pré-spécifiée)

*Rédigée le 2026-10-10, **avant toute estimation** d'un lien entre météo et rendement. Toute modification ultérieure sera consignée dans `docs/decisions.md` avec sa justification. La spécification initiale sera toujours rapportée.*

## 1. Échantillon et variables

- **Données :** `data/processed/panel_ble.parquet`, lignes `echantillon_principal == TRUE`, soit 83 départements × récoltes 2010-2025 = 1 328 observations.
- **Variable expliquée :** `log_rendement`.
- **Poids :** `surface_ref_ha` (surface moyenne 2010-2012, fixe).
- **Effets fixes :** département et année de récolte.

## 2. Modèles principaux

Le seuil de 32 °C a été confirmé par la règle de repli (`docs/decisions.md`).

**M1, chaleur, sans variable d'eau de mai-juin (« effet total » de la chaleur) :**

log Y_dt = α_d + γ_t + β₁ `gdd_0_32_remplissage` + β₂ `dd_32_remplissage` + θ₁ `prec_printemps` + θ₂ `dd_0_automne` + θ₃ `prec_automne` + ε_dt

**M2, chaleur et humidité du sol (« effet partiel ») :** M1 + δ₁ `swi_remplissage` + δ₂ `swi_remplissage`².

**Estimand principal :** β₂, variation du log-rendement par °C·jour supplémentaire au-delà de 32 °C en mai-juin.

- Dans M1, il est identifié par les écarts entre départements une même année.
- Dans M2, il est mesuré à humidité du sol égale. Le SWI étant en partie un médiateur de la chaleur, β₂(M2) est un effet partiel.

**Hypothèses :**

| Hypothèse | Énoncé | Test |
|---|---|---|
| H1 | β₂ < 0 | Unilatéral, rapporté avec l'intervalle à 95 % bilatéral |
| H2 | L'eau a un effet propre | Test joint δ₁ = δ₂ = 0 dans M2 |
| Composé (Ben-Ari et al. 2018) | Pluie de printemps et chaleur d'automne | θ₁ et θ₂, rapportés sans hypothèse directionnelle forte |

**Choix des contrôles :**

- `prec_printemps`, `dd_0_automne` et `prec_automne` sont **antérieurs** à mai-juin : ce ne sont pas des médiateurs de la chaleur de mai-juin.
- `prec_remplissage` est exclu à cause de sa colinéarité avec le SWI (r = 0,63).
- `tmean`, `dd_0` et `gdd_0_32` ne sont jamais combinés (colinéarité mécanique).

## 3. Inférence (les trois méthodes ; ne conclure que sur ce qui résiste aux trois)

1. **Cluster par département** (83 grappes) : dépendance temporelle.
2. **Conley**, rayon de **200 km**, fixé ici. Distances calculées entre centroïdes départementaux (WGS84) avec `fixest::vcov_conley`. Une variante à 300 km est rapportée en robustesse.
3. **Wild cluster bootstrap par année**, version restreinte sous H0 (WCR), poids de Webb (6 points), 9 999 tirages, graine 20261010, pour β₂ et, dans M2, pour δ₁. Avec 16 grappes, c'est le contrôle conservateur.

## 4. Robustesses (toutes rapportées, quel que soit leur résultat)

| Code | Variation | Pourquoi |
|---|---|---|
| R1 | Sans pondération | Estimand différent ; en cas d'écart, hétérogénéité |
| R2 | Sans 84, 30, 48 | Petits départements dominants sans pondération (audit de la phase 3) |
| R3 | Sans 2025 | Année provisoire, 27 % de la variance de `dd_32` |
| R4 | 85 départements (statut 1 et 2) | Filtre de qualité |
| R5 | Seuil de 30 °C (`gdd_0_30`, `dd_30`) | Sensibilité au seuil |
| R6 | Météo pondérée par la surface (pas par le masque blé) | Mesure de l'exposition |
| R7 | + tendances linéaires par région | Confusion avec des évolutions lentes |
| R8 | Panel long 1990-2025, effets fixes département × période (≤ 2009 / ≥ 2010) et année | Puissance (2003) |
| R9 | Conley à 300 km | Rayon |
| R10 | Fenêtre de remplissage élargie à mai-juillet | Phénologie (approximation mensuelle ; le décalage de ±2 semaines prévu en phase 0 exige un recalcul quotidien, **reporté**) |

**Placebo :** M1 + `dd_32_remplissage` de l'année *t*+1 (récoltes 2010-2024). On attend un coefficient nul. Un placebo non significatif ne valide rien à lui seul, et le SWI est persistant.

**Non fait en phase 4, et pourquoi :**

- exclusion des départements de montagne : aucune variable d'altitude n'est construite, test reporté ;
- classes de température (*bins*) : reportées en extension.

## 5. Présentation

- Coefficients avec les trois intervalles ou p-valeurs, N, R² intra (*within*).
- Effet exprimé en % de rendement pour +1 °C·jour et pour l'exposition moyenne de 2019 dans la population.
- Résultats nuls rapportés comme tels.
- Aucune extrapolation au changement climatique.
