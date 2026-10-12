"""Étape 34 : déficit de pression de vapeur (VPD) de juillet-août, masque maïs, 2000-2025 (test N3).

Usage : uv run python scripts/34_vpd.py
Entrées : data/raw/meteofrance_sim/QUOT_SIM2_<année>.csv.gz (TSUP_H, T, HU) ; data/processed/weights_cell_dep_maize.parquet
Sortie : data/processed/vpd_dep_ja.parquet (dep_code, annee, vpd_ja en kPa)

Définition déclarée avant calcul (docs/decisions.md, « Tests 4 et 5 ») : par maille et par jour,
VPD = es(TSUP_H) − HU/100 × es(T), avec es(T) = 0,6108 exp(17,27 T / (T + 237,3)) en kPa (Tetens) :
pression de vapeur saturante au maximum de l'après-midi, moins la pression de vapeur réelle estimée à partir
de l'humidité relative et de la température moyennes du jour. Moyenne des jours de juillet-août par maille,
puis moyenne pondérée par le masque maïs (comme les degrés-jours ; Lobell et al. 2013).
"""

import duckdb
import numpy as np
import pandas as pd

from atlas.download import ROOT
from atlas.spatial import weighted_mean

RAW = ROOT / "data" / "raw" / "meteofrance_sim"
PROC = ROOT / "data" / "processed"


def es(t):
    """Pression de vapeur saturante (kPa), formule de Tetens, t en °C."""
    return 0.6108 * np.exp(17.27 * t / (t + 237.3))


def main() -> None:
    weights = pd.read_parquet(PROC / "weights_cell_dep_maize.parquet")
    con = duckdb.connect()
    parts = []
    for year in range(2000, 2026):
        d = con.execute(f"""SELECT LAMBX, LAMBY, TSUP_H, T, HU FROM read_csv('{RAW / f"QUOT_SIM2_{year}.csv.gz"}',
                            delim=';', header=true)
                            WHERE DATE BETWEEN {year}0701 AND {year}0831""").df()
        n_days = d.groupby(["LAMBX", "LAMBY"]).size()
        if n_days.min() != 62:
            raise RuntimeError(f"{year} : jours manquants en juillet-août pour certaines mailles")
        d["vpd"] = es(d["TSUP_H"]) - d["HU"] / 100 * es(d["T"])   # d["T"], pas d.T (transposée)
        cell = d.groupby(["LAMBX", "LAMBY"], as_index=False).vpd.mean().rename(columns={"vpd": "vpd_ja"})
        parts.append(cell.assign(annee=year))
        print(f"{year} : VPD médian {cell.vpd_ja.median():.2f} kPa")
    cell_year = pd.concat(parts, ignore_index=True)
    out = weighted_mean(cell_year, weights, ["vpd_ja"], "w_maize", ["annee"])
    out = out.sort_values(["dep_code", "annee"]).reset_index(drop=True)
    if out.vpd_ja.isna().any() or (out.vpd_ja <= 0).any():
        raise RuntimeError("VPD départemental manquant ou non positif")
    out.to_parquet(PROC / "vpd_dep_ja.parquet", index=False)
    print(f"{out.dep_code.nunique()} départements × {out.annee.nunique()} années")


if __name__ == "__main__":
    main()
