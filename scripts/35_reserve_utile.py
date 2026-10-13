"""Étape 35 : réserve utile (RU) des sols sous les parcelles de maïs grain, par département (analyse R1).

Usage : uv run python scripts/35_reserve_utile.py   (après scripts/01_download_raw.py --ru)
Entrées : data/raw/inrae_ru/AWCr_mm_0_200.tif (RU 0-200 cm en mm, 90 m, Lambert 93 ; INRAE, doi:10.15454/9IRARJ) ;
          data/interim/rpg/<2015-2017>/PARCELLES_GRAPHIQUES.shp (parcelles MIS) ; ADMIN EXPRESS (départements)
Sortie : data/processed/ru_dep_mais.parquet : dep_code, ru_mm, ru_ecart_type_mm, pixels_mais, part_sans_donnee

Règle déclarée avant calcul (docs/decisions.md, « Réserve utile des sols et eau d'irrigation ») : moyenne des pixels
dont le centre tombe dans une parcelle MIS, chaque millésime 2015, 2016 et 2017 comptant une fois (un pixel en maïs
les trois années pèse 3) ; département du pixel par ADMIN EXPRESS rastérisé sur la même grille ; pixels sans donnée
exclus, leur part rapportée.
"""

import time

import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize

from atlas.download import ROOT
from atlas.rpg import wheat_parcels
from atlas.spatial import departements

RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROC = ROOT / "data" / "processed"
YEARS = [2015, 2016, 2017]


def main() -> None:
    with rasterio.open(RAW / "inrae_ru" / "AWCr_mm_0_200.tif") as r:
        ru = r.read(1)
        transform, crs, nodata = r.transform, r.crs, r.nodata
    valid = np.isfinite(ru) & (ru != nodata) & (ru >= 0)
    print(f"RU : {ru.shape}, {crs}, pixels valides {valid.mean():.1%}, médiane {np.median(ru[valid]):.0f} mm")

    # Nombre de millésimes où le centre du pixel est dans une parcelle de maïs grain (0 à 3).
    n_maize = np.zeros(ru.shape, dtype=np.uint8)
    for year in YEARS:
        t0 = time.perf_counter()
        parcels = wheat_parcels(INTERIM / "rpg" / str(year) / "PARCELLES_GRAPHIQUES.shp", crop_code="MIS")
        if parcels.crs != crs:
            parcels = parcels.to_crs(crs)
        n_maize += rasterize(((g, 1) for g in parcels.geometry), out_shape=ru.shape, transform=transform,
                             fill=0, dtype="uint8")
        # Contrôle : surface des pixels retenus (0,81 ha chacun) contre la surface déclarée au RPG.
        print(f"{year} : {len(parcels):,} parcelles, {parcels.SURF_PARC.sum() / 1e6:.3f} Mha au RPG ; "
              f"pixels cumulés {(n_maize > 0).sum():,} ({time.perf_counter() - t0:.0f} s)")
    pixel_ha = abs(transform.a * transform.e) / 1e4

    dep = departements(RAW / "ign_admin_express" / "ADMIN-EXPRESS-COG-CARTO_4-0_2026-01-01_departement.parquet")
    dep = dep.to_crs(crs).reset_index(drop=True)
    dep_id = rasterize(((g, i) for i, g in enumerate(dep.geometry)), out_shape=ru.shape, transform=transform,
                       fill=-1, dtype="int16")

    m = n_maize > 0
    d = pd.DataFrame({"dep": dep_id[m], "w": n_maize[m].astype(float), "ru": np.where(valid[m], ru[m], np.nan)})
    print(f"pixels de maïs hors département : {(d.dep < 0).sum():,} ; "
          f"surface maïs moyenne 2015-2017 rastérisée : {d.w.sum() * pixel_ha / 3 / 1e6:.3f} Mha")
    d = d[d.dep >= 0]
    rows = []
    for k, g in d.groupby("dep"):
        ok = g.ru.notna()
        mean = np.average(g.ru[ok], weights=g.w[ok]) if ok.any() else np.nan
        sd = np.sqrt(np.average((g.ru[ok] - mean) ** 2, weights=g.w[ok])) if ok.any() else np.nan
        rows.append({"dep_code": dep.dep_code[k], "ru_mm": mean, "ru_ecart_type_mm": sd, "pixels_mais": len(g),
                     "part_sans_donnee": 1 - g.w[ok].sum() / g.w.sum()})
    out = pd.DataFrame(rows).sort_values("dep_code").reset_index(drop=True)
    if out.dep_code.duplicated().any():
        raise RuntimeError("département dupliqué")
    out.to_parquet(PROC / "ru_dep_mais.parquet", index=False)
    print(f"{len(out)} départements ; part sans donnée max {out.part_sans_donnee.max():.2%}")
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
