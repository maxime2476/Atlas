# Données ATLAS

Seuls ces fichiers README sont versionnés. Prérequis : `uv sync`, `Rscript -e 'renv::restore()'`, R ≥ 4.5, l'outil système `7z` (archives RPG), un compte NASA Earthdata pour le NDVI (voir `README.md`, § 7).

Les fichiers sources sont révisés par leurs producteurs (SAA provisoire 2025, SIM récents, VigiEau) : une reproduction **bit à bit**, contrôlée par `docs/manifest_raw.csv`, n'est garantie qu'avec les fichiers téléchargés les 10 et 11 octobre 2026. Les données se retrouvent ainsi :

```bash
# 1. Téléchargements (~18 Go ; RPG 2008 et NDVI plus bas, ~5,6 Go)
uv run python scripts/01_download_raw.py --sim-years 1958-2025 --rpg 2015-2017 --schauberger --prix --saa-ancienne --vigieau
# extraction des couches RPG : voir data/raw/ign_rpg/README.md (≈ 13 Go, à supprimer après l'étape 07)
uv run python scripts/02_check_sim.py --all-years                 # contrôles SIM (1958 partiel : attendu)
uv run python scripts/03_build_saa_long.py                        # -> data/interim/
# 2. Météo, masques, fenêtres, panels
uv run python scripts/04_build_spatial_weights.py                 # poids maille -> département (~15 s)
uv run python scripts/05_build_weather_monthly.py                 # indicateurs météo mensuels 1958-2025 (~20 min)
uv run python scripts/07_build_wheat_mask.py                      # masque blé RPG + météo pondérée (~1,5 min)
uv run python scripts/07_build_wheat_mask.py --culture MIS        # masque maïs grain RPG (~1,5 min)
uv run python scripts/06_exposure_check.py --weights wheat        # fenêtres + règle de repli (référence)
uv run python scripts/06_exposure_check.py --weights area
uv run python scripts/06_exposure_check.py --weights wheat --first-year 1990
uv run python scripts/06_exposure_check.py --weights wheat --first-year 1959
uv run python scripts/08_check_schauberger.py                     # compatibilité Schauberger / SAA
uv run python scripts/09_build_panel.py                           # panels blé (2010, 1990 et 1959-2025)
uv run python scripts/10_descriptives.py                          # tableaux et figures descriptifs
uv run python scripts/11_extra_windows.py                         # fenêtre mai-juillet (R10)
uv run python scripts/12_build_semimonthly.py                     # demi-mois et classes de température (R11, R12, R14, ~5 min)
uv run python scripts/13_cell_altitude.py                         # altitude des mailles via le service IGN (R13, ~3 min)
uv run python scripts/23_vigieau_indicators.py                    # restrictions d'eau juillet-août 2012-2025
uv run python scripts/22_build_panel_mais.py                      # panel maïs irrigué / non irrigué 2000-2025
# 3. Économétrie (R, renv ; depuis la racine)
Rscript R/10_fe_models.R && Rscript R/11_robustness.R && Rscript R/12_diagnostics.R   # blé 2010-2025 (phase 4)
# 4. Prévision
uv run python scripts/14_forecast_features.py                     # variables de prévision (1er juin, 1er juillet)
uv run python scripts/15_forecast_cv.py                           # évaluation chronologique (~10 min)
# 5. Phase 6 (exploratoire)
uv run python scripts/16_phase6_build.py                          # prix, pertes valorisées, panel maïs 2010-2025
Rscript R/13_maize_gap.R                                          # maïs irrigué / non irrigué (exploratoire)
# NDVI : APPEEARS_TOKEN dans .env (voir .env.example), puis :
uv run python scripts/17_ndvi_appeears.py soumettre --annees 2010-2025   # puis « statut », puis « telecharger --tache <id> »
#   (exécution réelle : 2 commandes, test 2022 puis 2010-2021,2023-2025 ; 18_ndvi_aggregate lit TOUS les
#    dossiers de data/raw/nasa_appeears/ : ne pas télécharger deux fois la même année, sinon il s'arrête)
uv run python scripts/18_ndvi_aggregate.py                        # NDVI par département (~15 min)
uv run python scripts/19_forecast_ndvi.py                         # apport du NDVI à la prévision (~30 min)
# 6. Phase 4 bis (pré-spécifiée : docs/specification_phase4bis.md)
Rscript R/14_q1_maize.R                                           # Q1 maïs 2000-2025 (~1 min)
Rscript R/21_q1_revue.R                                           # analyses E1-E4 de la relecture (~15 min ; avant 24)
uv run python scripts/24_valorisation_mais.py                     # valorisation descriptive de Q1
Rscript R/15_q2_wheat.R                                           # Q2 blé 1959-2025 (~3 min)
Rscript R/16_q1_exploratoire.R                                    # diagnostics exploratoires de Q1
uv run python scripts/01_download_raw.py --rpg1 2008              # phase 0 ter : îlots RPG 2008, 4 régions (~0,6 Go)
uv run python scripts/25_build_maize_mask_2008.py                 # masque maïs 2008 + météo (Q1-R9)
Rscript R/17_q1_mask2008.R                                        # robustesse Q1-R9
Rscript R/18_residual_autocorr.R                                  # diagnostic : autocorrélation des résidus
Rscript R/19_q1_power_size.R                                      # diagnostics D1-D2 : puissance de H1, taille de la réplication
uv run python scripts/01_download_raw.py --eobs                    # E-OBS Tmin/Tmax 0,1°, 1995-2025 (~4 Go)
uv run python scripts/27_eobs_heat.py                             # degrés-jours > 32 °C de juillet-août avec E-OBS
Rscript R/20_q1_eobs.R                                            # vérification Q1-E (source de température)
uv run python scripts/01_download_raw.py --eolien                  # registre RTE des installations (~45 Mo)
uv run python scripts/29_eolien.py                                # puissance éolienne par département et année
uv run python scripts/28_complements_python.py preparer           # covariables, fourrage, DML (G8)
Rscript R/22_q1_complements.R                                     # analyses complémentaires G1-G10 (~5 min)
uv run python scripts/28_complements_python.py prevision          # prévision : intervalles conformes, modèles sur B0 (~5 min)
Rscript R/wcr/exemple.R                                           # exemple simulé du module wcr (Monte-Carlo)
# 7. Figures, mémoire et tests
uv run python scripts/20_figures_rapport.py                       # figures du README (PNG) et du mémoire (PDF)
uv run python scripts/32_diagrammes_readme.py                   # diagrammes du README (chaîne de données, règle de décision, frise ; SVG)
uv run python scripts/26_tables_memoire.py                        # chiffres et tableaux du mémoire (memoire/tables/)
(cd memoire && latexmk -pdf main.tex)                             # compilation du mémoire
uv run pytest
```

| Dossier | Contenu | Règle |
|---|---|---|
| `raw/` | Fichiers tels que téléchargés | Jamais modifiés ; empreintes dans `docs/manifest_raw.csv` |
| `interim/` | Transformations intermédiaires (ex. SAA au format long) | Toujours régénérables depuis `raw/` |
| `processed/` | Poids spatiaux, météo département × mois et × récolte ; panel (phase 3) | Régénérables |

Provenance, licences, révisions : `docs/sources.md`.
