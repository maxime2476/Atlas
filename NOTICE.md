# Licences of this repository

| Content | Licence |
|---|---|
| Code (`src/`, `scripts/`, `R/`, `tests/`) | MIT (`LICENSE`) |
| Research monograph (`memoire/`) and documentation (`docs/`, `README.md`) | Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/ |
| Result tables (`reports/tables/`) and figures | Derived from public data sources that keep their own licences; reuse must credit them |

Licences of the data sources (details in `docs/sources.md`):

- Licence Ouverte / Etalab 2.0: Météo-France (SIM2), IGN (ADMIN EXPRESS, RPG, altimetry), Ministry of Ecological Transition (VigiEau); presumed for Agreste (SAA);
- CC BY 4.0: Schauberger et al. (2022), GFZ Data Services;
- NASA data policy: MODIS MOD13Q1 (LP DAAC);
- INSEE and Eurostat price series: terms of reuse to be confirmed.

Raw data are not redistributed in this repository; `scripts/01_download_raw.py` downloads them and `docs/manifest_raw.csv` lists their SHA-256 hashes.
