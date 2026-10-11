# `wcr` — bootstrap par période et vérification de la taille des tests

Module R autonome (un seul fichier, `wcr.R` ; dépendance : `fixest`). Il sert à tester un coefficient de modèle à effets fixes quand les chocs sont **communs à toutes les unités une même période** : météo, prix ou politique nationale.

## Le problème

Dans ces panels, l'exposition et le résidu sont corrélés entre unités une même période, et les effets fixes de période n'en retirent que la moyenne. Les erreurs-types usuelles supposent à tort l'indépendance entre unités. Cela vaut pour le cluster par unité, et seulement en partie pour Conley. Elles rejettent alors l'hypothèse nulle bien plus souvent que le niveau annoncé.

**Exemple simulé** (`exemple.R`) : 40 régions × 25 années, vrai effet nul, 300 panels.

| Inférence | Rejets à tort au seuil de 5 % |
|---|---|
| Cluster par région | 19,7 % |
| Cluster par année (CR1) | 5,0 % |
| **Wild cluster bootstrap restreint par année (WCR)** | **4,0 %** |

**Sur les données réelles d'ATLAS** (rendements départementaux, `docs/resultats_phase4.md` et `docs/resultats_phase4bis.md`) :

- le cluster par département rejette à tort dans 16 à 56 % des cas ;
- Conley à 200 km, dans 16 à 39 % ;
- le WCR par année, dans 3,7 à 4,3 %.

Avec peu de périodes (une dizaine ou moins), le CR1 par période devient lui aussi peu fiable. Le WCR avec poids de Webb est alors recommandé (Cameron, Gelbach & Miller 2008 ; Webb 2023).

## Fonctions

| Fonction | Rôle | Retour |
|---|---|---|
| `wcr_pvalue(data, y, x, z, fe, cluster, weights, B, seed)` | Test de β_x = 0 | `t`, `p` (bilatérale), `p_left` (H1 : β < 0), `p_right` (H1 : β > 0), `G`, `B` |
| `wcr_wald_pvalue(data, y, xs, z, fe, cluster, weights, B, seed)` | Test joint de plusieurs coefficients | `wald`, `p`, `G`, `B` |
| `placebo_size(data, x, unit, period, tests, R, alpha, seed)` | Taille empirique de **vos** tests sur **vos** données : l'exposition `x` est remplacée par le champ réel d'une autre période (dérangement) | Taux de rejet à tort par test, nombre de permutations distinctes |

**Arguments :**

- `z` : autres régresseurs (`character(0)` s'il n'y en a pas) ;
- `fe` : noms des effets fixes ;
- `weights` : nom d'une colonne de poids (une colonne de 1 pour des MCO non pondérés).

**Exemple minimal :**

```r
library(fixest)
source("R/wcr/wcr.R")
df$poids <- 1
b <- wcr_pvalue(df, y = "log_rendement", x = "chaleur", z = c("pluie"),
                fe = c("departement", "annee"), cluster = "annee", weights = "poids")
b$p          # p bilatérale ; b$p_left / b$p_right pour un test unilatéral

tests <- list(
  cluster_dep = function(s) coeftable(feols(log_rendement ~ x_placebo + pluie | departement + annee, s),
                                      vcov = ~departement)["x_placebo", "Pr(>|t|)"],
  wcr_annee  = function(s) wcr_pvalue(s, "log_rendement", "x_placebo", "pluie",
                                      c("departement", "annee"), "annee", "poids", B = 399)$p
)
placebo_size(df, x = "chaleur", unit = "departement", period = "annee", tests = tests, R = 300)
```

## Méthode (résumé)

1. **Frisch-Waugh-Lovell :** on retire les effets fixes (`fixest::demean`, pondéré), puis on projette sur `z`.
2. **Tirages :** sous H0, chaque résidu restreint est multiplié par un poids de Webb tiré par grappe. Les poids prennent six valeurs : ±√(3/2), ±1, ±√(1/2).
3. **Re-projection :** à chaque tirage, la variable simulée est re-projetée sur les effets fixes et sur `z`. Sans cette étape, la taille est faussée ; elle était de 8,7 % au lieu de 6,6 % dans une version antérieure du projet.
4. **Comparaison :** on compare la statistique t observée (erreurs-types par grappe, sans facteur de petit échantillon puisqu'il se simplifie) à celle des tirages.

**Validation :**

- la statistique t observée est comparée à celle de `fixest` ;
- la taille est vérifiée par simulation, dans `exemple.R` et sur chaque jeu de données du projet.

Il n'y a pas de suite de tests unitaires R.

## Limites

- `placebo_size` garde y fixe et ne permute que les périodes de x : avec T périodes, les placebos sont peu nombreux et non indépendants. C'est un diagnostic indicatif.
- **Graine :** `wcr_pvalue` appelle `set.seed(seed)`. Dans une boucle de simulation, il faut tirer les permutations avant les tests (comme `placebo_size`) ou passer une graine différente à chaque tour (comme `R/14_q1_maize.R`). Sinon, les tirages se répètent.
- Le test porte sur un coefficient à la fois, ou sur un test joint, avec des grappes à une seule dimension.
- Le temps de calcul est proportionnel à n × B.

## Références

- Cameron, A. C., Gelbach, J. B. & Miller, D. L. (2008). Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics* 90(3), 414-427.
- Webb, M. D. (2023). Reworking wild bootstrap-based inference for clustered errors. *Canadian Journal of Economics* 56(3), 839-858. DOI 10.1111/caje.12661.
