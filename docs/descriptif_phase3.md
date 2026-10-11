# ATLAS — Analyse descriptive du panel blé (phase 3)

*Rédigé le 2026-10-10. Résultats **descriptifs** uniquement : aucune relation entre météo et rendement n'a été estimée.*

**Reproduction :**

```bash
uv run python scripts/09_build_panel.py
uv run python scripts/10_descriptives.py
```

Les tableaux sont dans `reports/tables/` et les figures dans `reports/figures/` (non versionnées).

## 1. Construction et jointures

| Étape | Lignes avant | Lignes après | Appariement |
|---|---|---|---|
| SAA blé tendre d'hiver (métropole) → population (85 départements) | 1 520 | 1 360 | — |
| Jointure de la météo (masque blé), 2010-2025 | 1 360 | 1 360 | 1 360 / 1 360 |
| Panel long : rendements 1990-2009 (Schauberger RAW) + 2010-2025 (SAA) → météo 1990-2025 | 3 060 | 3 060 | 3 060 / 3 060 ; 0 rendement manquant |

**Contrôles** (`tests/test_panel.py`) :

- clé unique et panel équilibré ;
- aucune valeur manquante dans le panel principal ;
- poids fixes ;
- partie 2010-2025 du panel long identique au panel principal ;
- toutes les colonnes documentées dans `docs/dictionnaire_panel.md`.

## 2. Rendements

**Observé.** Rendement national (moyenne pondérée par la surface fixe 2010-2012, 85 départements ; `reports/figures/rendement_national.png`) :

- **2016 : 53,9 q/ha**, le minimum de 1990-2025. L'écart médian au rendement moyen du département est de −18,3 %.
- **2024 : 60,8 q/ha** (−13,4 %), puis 2020 (−6,3 %).
- 2003 : 64,3 q/ha et 2007 : 64,2 q/ha dans la période longue.
- Meilleures années : 2015 (79,7), 2019 (79,4), 2004 (77,9), 1998 (77,5).
- 2025 (provisoire) : 74,2 q/ha.

**Carte 2016** (`cartes_rendement_exposition.png`) : la perte est concentrée dans le Bassin parisien et le Centre (jusqu'à environ −49 %). Le Sud-Est et une partie du Sud-Ouest sont proches de la normale, voire au-dessus.

**Décomposition de la variance du log-rendement :**

| Panel | Effets fixes département | Effets fixes année | Résiduelle | Écart-type résiduel |
|---|---|---|---|---|
| 2010-2025 | 73,9 % | 9,3 % | **16,8 %** | 0,100 |
| 1990-2025 | 76,6 % | 8,6 % | **14,7 %** | 0,093 |

**Interprétation (prudente) :**

- L'essentiel de la variance est un écart permanent entre départements, absorbé par les effets fixes.
- La variation utile pour identifier un effet météo, celle qui reste après les deux effets fixes, ne représente qu'environ 15-17 % de la variance totale, soit un écart-type de 10 % du rendement.
- Les deux années de pertes les plus fortes, 2016 et 2024, ne sont **pas** des années de chaleur extrême, d'après la phase 2 et Ben-Ari et al. (2018) pour 2016. Si l'excès d'eau au printemps et l'automne doux jouent un rôle, un modèle centré sur la chaleur ne « verra » pas ces années. C'est une hypothèse à tester en phase 4, pas une conclusion.

## 3. Variables météo (masque blé, 2010-2025)

| Variable | Moyenne | Écart-type | Max | Écart-type résiduel* | Part résiduelle de la variance* |
|---|---|---|---|---|---|
| `dd_32_remplissage` (°C·jour) | 0,36 | 0,82 | 8,89 | 0,54 | 43,8 % |
| `gdd_0_32_remplissage` (°C·jour) | 999,7 | 101,8 | 1 351 | 22,5 | 4,9 % |
| `swi_remplissage` | 0,58 | 0,16 | 1,03 | 0,075 | 21,3 % |
| `swi_dry_remplissage` (jours) | 12,8 | 15,9 | 60,5 | 8,6 | 29,1 % |
| `prec_remplissage` (mm) | 150,8 | 57,5 | 397 | 33,7 | 34,2 % |
| `prec_printemps` (mm) | 121,6 | 53,1 | 359 | 29,5 | 30,9 % |
| `etp_remplissage` (mm) | 216,6 | 32,6 | 342 | 11,9 | 13,4 % |
| `dd_0_automne` (°C·jour) | 1 145,7 | 135,6 | 1 545 | 25,3 | 3,5 % |
| `prec_automne` (mm) | 236,3 | 88,0 | 736 | 51,3 | 34,0 % |
| `tmin_hiver` (°C) | 2,43 | 1,82 | 7,14 | 0,35 | 3,6 % |

\* Après effets fixes département et année : c'est la variation qui identifiera les coefficients en phase 4.

**Observé :**

- Les variables de **température moyenne ou cumulée** (`gdd_0_32_*`, `dd_0_automne`, `tmin_hiver`) gardent **moins de 5 %** de leur variance après effets fixes. Leur variation est surtout géographique et nationale : leurs coefficients seront peu précis.
- Les variables d'eau et la chaleur extrême gardent 20 à 44 % de leur variance.

## 4. Colinéarité entre chaleur et eau (hypothèse H2)

Corrélations des résidus, après effets fixes département et année :

| Paire | r |
|---|---|
| `dd_32_remplissage` × `swi_remplissage` | −0,05 |
| `dd_32_remplissage` × `swi_dry_remplissage` | +0,11 |
| `dd_32_remplissage` × `prec_remplissage` | −0,16 |
| `dd_32_remplissage` × `etp_remplissage` | +0,14 |
| `dd_32_remplissage` × `gdd_0_32_remplissage` | +0,18 |
| `swi_remplissage` × `prec_printemps` | +0,51 |
| `swi_remplissage` × `prec_remplissage` | +0,63 |

Une régression du résidu de `dd_32_remplissage` sur les résidus de SWI, de pluie et d'ETP donne un R² de **0,036** : 96 % de la variation résiduelle de la chaleur extrême est indépendante des variables d'eau (`reports/figures/residus_chaleur_swi.png`).

**Interprétation :**

- À l'échelle département × année et en mai-juin, chaleur extrême et humidité du sol sont **peu colinéaires** une fois les effets fixes retirés. Séparer leurs effets (H2) n'est donc pas empêché par la colinéarité.
- La faible corrélation peut aussi refléter la rareté de l'exposition au-delà de 32 °C : la plupart des résidus valent presque zéro.
- Le SWI et la pluie sont, eux, nettement corrélés (0,5 à 0,6). Il faudra éviter de les inclure tous les deux sans justification.

## 5. Points d'audit

Audit indépendant par l'agent `data-auditor` (lecture seule, 2026-10-10). **Aucun point bloquant.** Points importants, vérifiés de nouveau puis traités :

| Constat | Vérification | Traitement |
|---|---|---|
| **Filtre statut qualité 1 omis**, alors qu'il est prévu par le protocole de la phase 0 | Statut 2 : Belfort (90) et Essonne (91), 0,74 % du poids | Colonne `echantillon_principal` (83 départements) ; 90 et 91 en robustesse ; exposition inchangée |
| **Deux petits départements dominent l'exposition sans pondération** | Sans poids, Vaucluse (84) = 16,6 % et Gard (30) = 11,7 % de la variance résiduelle de `dd_32_remplissage` ; environ 1 600 ha chacun ; ratio RPG/SAA du 84 = 0,74 | Spécification principale pondérée ; robustesses non pondérée et sans 84, 30, 48 (`decisions.md`) |
| **N_eff pondéré non documenté** | Pondéré : 4,75 (3,20 sans 2025) | Consigné dans `decisions.md` ; la règle, non pondérée, est inchangée |
| **Rendements arrondis** | 86,6 % d'entiers en 2010-2025 ; 25 départements n'ont que des entiers ; 95,6 % avant 2010 ; aucune série constante, aucune répétition anormale (au plus 3) | Documenté dans le dictionnaire : erreur d'au plus ±0,5 q/ha sur la variable expliquée, donc une perte de puissance sans biais |
| **Écarts entre documentation et données** | Le cadrage parlait d'une surface « hors période d'estimation » ; 10 et non 11 départements exclus ; type de `production_q` ; maximum de `dd_32` selon la pondération | Erratum dans `phase0_cadrage.md` ; dictionnaire et `notes_exposition.md` corrigés |

**Points mineurs confirmés :**

- aucune rupture visible entre 2009 et 2010 (moyenne nationale continue ; médiane de |Δlog| : 0,082 en 2010, contre 0,095 les autres années) ;
- production dérivée du rendement (ratio entre 0,9993 et 1,0007) ;
- `gdd_0_32`, `dd_0` et `tmean` sont mécaniquement colinéaires (r ≥ 0,998).

**Tests ajoutés :** échantillon principal, identité production = surface × rendement, cohérence des indicateurs de chaleur (`tests/test_panel.py`).

**Reste ouvert :**

- version définitive SAA 2025 (novembre 2026) ;
- licence SAA, présumée ;
- mécanisme « évolution nationale appliquée aux petites régions » de la SAA (84, 48, 73), non testé directement ;
- identification des 4 paires Schauberger / SAA manquantes sur 2010-2018 : années 2014 et 2015 (manquantes dans la version RAW), sans effet sur le panel long, qui utilise la SAA à partir de 2010.
