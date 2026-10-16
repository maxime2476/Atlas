# Licences of this repository

| Content | Licence |
|---|---|
| Code (`src/`, `scripts/`, `R/`, `tests/`) | MIT (`LICENSE`) |
| Research monograph (`memoire/`) and documentation (`docs/`, `README.md`) | Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/ |
| Result tables (`reports/tables/`) and figures | Derived from the data sources below, which keep their own licences; reuse must credit them. `reports/tables/phase4bis_q1_eobs_departement.csv` and `phase4bis_q1_eobs.csv` are derived from E-OBS, whose data policy restricts use to non-commercial research and education |

Raw data are not redistributed in this repository. `scripts/01_download_raw.py` downloads them and `docs/manifest_raw.csv` lists their URLs, access dates and SHA-256 hashes.

## Data sources: licences and required attribution

Terms for Agreste, INSEE, Eurostat and NASA were checked on the producers' pages on 2026-10-11. Terms for Météo-France, IGN and VigiEau are those recorded when the data were audited and downloaded (`docs/sources.md`, `docs/phase0bis_cadrage.md`). Access dates are those of the manifest.

| Source | Licence (as stated by the producer) | Attribution used | Accessed |
|---|---|---|---|
| Agreste (SSP, French Ministry of Agriculture), *Statistique agricole annuelle* (long series and older series `SAANR_DEVELOPPE_2`) | Free reuse, including commercial, without licence fee, provided the source is cited (legal notice of agreste.agriculture.gouv.fr); Agreste datasets on data.gouv.fr are under Licence Ouverte 2.0 | Source : Agreste, Statistique agricole annuelle | 2026-10-10 and 2026-10-11 |
| Météo-France, SIM2 daily (SAFRAN-ISBA) | Licence Ouverte / Etalab 2.0 | Source : Météo-France, SIM2 quotidienne | 2026-10-10 to 2026-10-11 |
| IGN, ADMIN EXPRESS COG CARTO 2026 | Licence Ouverte / Etalab 2.0 | Source : IGN, ADMIN EXPRESS | 2026-10-10 |
| IGN / ASP, Registre parcellaire graphique (RPG 2.0, 2015-2017; RPG 1.0, 2008) | Licence Ouverte / Etalab 2.0 | Source : IGN, RPG | 2026-10-10 and 2026-10-11 |
| IGN, altimetry service (RGE ALTI) | Licence Ouverte / Etalab 2.0 | Source : IGN, RGE ALTI | 2026-10-10 |
| Ministry of Ecological Transition, VigiEau "Donnée Sécheresse" (data.gouv.fr) | Licence Ouverte / Etalab 2.0 | Source : MTE, VigiEau | 2026-10-11 |
| INSEE, producer price index (IPPAP), BDM series 010776425 and 010776430 | Licence Ouverte / Etalab 2.0 (INSEE legal notice: "Source : Insee", date of update) | Source : Insee | 2026-10-10 and 2026-10-11 |
| Eurostat, `apri_ap_crpouta` | Reuse authorised provided the source is acknowledged; EU content under CC BY 4.0 (Eurostat copyright notice) | Source : Eurostat | 2026-10-10 and 2026-10-11 |
| Schauberger et al. (2021), GFZ Data Services, doi:10.5880/PIK.2021.001 | CC BY 4.0 | Cited as a dataset; **changes:** RAW version, yields converted from t/ha to q/ha, departments matched to INSEE codes | 2026-10-10 |
| NASA LP DAAC, MOD13Q1 v6.1 (Didan 2021, doi:10.5067/MODIS/MOD13Q1.061) and MOD11A2 v6.1 (Wan, Hook & Hulley 2021, doi:10.5067/MODIS/MOD11A2.061), via AppEEARS | NASA-led mission data: Creative Commons Zero (CC0); citation requested (NASA Earthdata data use guidance) | Cited as a dataset | 2026-10-10 to 2026-10-11 |
| NASA LP DAAC, MCD12Q2 v061 (Friedl, Gray & Sulla-Menashe 2022, doi:10.5067/MODIS/MCD12Q2.061) and ECOSTRESS ECO_L2T_LSTE v002 (Hook & Hulley 2022, doi:10.5067/ECOSTRESS/ECO_L2T_LSTE.002), direct download | NASA-led mission data: Creative Commons Zero (CC0); citation requested (NASA Earthdata data use guidance) | Cited as datasets | 2026-10-15 to 2026-10-16 |
| IGN / ASP, RPG 2.0 2022, regions R84 and R44 | Licence Ouverte / Etalab 2.0 | Source : IGN, Registre parcellaire graphique | 2026-10-15 |
| RTE / ODRÉ, national register of electricity production and storage installations (snapshot of 30/06/2026), used only for the wind-capacity check | Licence Ouverte / Etalab 2.0 | Source : RTE, registre national des installations (ODRÉ) | 2026-10-12 |
| ECA&D / Copernicus, E-OBS v33.0e (Tmin, Tmax, 0.1°), used only to check the heat measure | ECA&D/E-OBS data policy: non-commercial research and education only; results to be published in the open literature (policy read on 2026-10-12) | "We acknowledge the E-OBS dataset and the data providers in the ECA&D project (https://www.ecad.eu)." Cornes et al. (2018), doi:10.1029/2017JD028200 | 2026-10-12 |
| INRAE, Réservoir utile des sols de la France métropolitaine (Román Dobarco et al. 2019), Recherche Data Gouv, doi:10.15454/9IRARJ, file `AWCr_mm_0_200.tif` | Licence Ouverte / Etalab 2.0 | Cited as a dataset; **changes:** averaged over grain maize parcels by department | 2026-10-13 |
| OFB / water agencies, BNPE water withdrawals, via the Hub'Eau API "Prélèvements en eau" (usage IRR, 2012-2023) | Licence Ouverte / Etalab 2.0 (Hub'Eau terms: cite the data producer) | Source : BNPE (OFB, agences de l'eau), via Hub'Eau | 2026-10-13 |
| Agreste, Recensement agricole 2020, table RA2020_0052 (irrigated area by crop and department) | Free reuse with citation of the source (as for the SAA) | Source : Agreste, RA 2020 | 2026-10-13 |
| DRIAS (Météo-France, CERFACS, IPSL), EXPLORE2-Climat 2022 bias-corrected with ADAMONT, 17 GCM/RCM simulations (historical, RCP8.5), extracted with the author's personal account | Licence Etalab (DRIAS terms of use) | "Drias, données Météo-France, CERFACS, IPSL" | 2026-10-13 |
| DRIAS-Eau (Météo-France), Explore2 / SIM2 2024, monthly water indicators by warming level (NORSWIAV, July–August, 17 simulations), extracted with the author's personal account | Licence Etalab (terms of use of the DRIAS-Climat and DRIAS-Eau portals, read on 2026-10-14) | "DRIAS-Eau, données Météo-France, Explore2" | 2026-10-14 |
| Agreste, Conjoncture – Infos rapides Grandes cultures n° 2026-131, departmental file (early estimates at 1 October 2026) | Free reuse with citation of the source (as for the SAA) | Source : Agreste, conjoncture grandes cultures | 2026-10-14 |
| Météo-France, SIM2 daily file 2026 (to 1 October 2026) | Licence Ouverte 2.0 | As for SIM2 | 2026-10-14 |

The README diagrams (`docs/figures/pipeline_atlas*.svg`, `regle_decision*.svg`, `frise_projet*.svg`, generated by `scripts/32_diagrammes_readme.py`) follow the "Medallion", "Flowchart" and "Timeline" layouts and style tokens of diagram-design by Cathryn Lavery (MIT licence, https://github.com/cathrynlavery/diagram-design); no file of that project is copied.

Transformations of the data (aggregation, degree-days, panels) are described in `docs/` and in the monograph; they do not alter the meaning of the source data.
