# IGN / ASP — RPG version 2.0, parcelles, millésimes 2015-2017 (masque blé)

- Source : https://data.geopf.fr/telechargement/resource/RPG (Licence Ouverte 2.0)
- Fichiers : `RPG_2-0__SHP_LAMB93_FR-<année>_<année>-01-01.7z` (≈ 2,8 Go chacun), France métropolitaine, Lambert 93.
- Téléchargement : `uv run python scripts/01_download_raw.py --rpg 2015-2017`
- Extraction de la seule couche utile (fichiers dérivés, hors `raw/`, ≈ 4,4 Go par millésime) :

```bash
for y in 2015 2016 2017; do
  mkdir -p data/interim/rpg/$y
  7z e -y data/raw/ign_rpg/RPG_2-0__SHP_LAMB93_FR-${y}_${y}-01-01.7z -odata/interim/rpg/$y "*/PARCELLES_GRAPHIQUES.*" -r
done
```

Outil système requis : `7zip` (paquet Ubuntu 26.04, version 26.00).
