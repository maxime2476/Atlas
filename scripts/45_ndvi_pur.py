"""Étape 45 : NDVI des parcelles de blé (S2) : pixels de 250 m couverts au moins à moitié par du blé tendre d'hiver.

Usage : uv run python scripts/45_ndvi_pur.py
Entrées : composites NDVI MOD13Q1 déjà téléchargés (data/raw/nasa_appeears) ; parcelles BTH du RPG 2015-2017 ;
          départements (ADMIN EXPRESS) ; forecast_features.parquet ; ndvi_features.parquet (NDVI actuel, phase 6).
Sorties : data/processed/ndvi_pur_dep_composite.parquet ; reports/tables/phase7_s2_ndvi_pur.csv.
Décisions déclarées avant calcul : docs/decisions.md, « Pistes d'amélioration (L1-L4, S1-S3) », S2. Exploratoire :
années test 2016-2025 déjà vues. Deux familles de modèles sont rapportées sans choix : celles de la phase 6 (corrections
de B1, `run_fold`) et les corrections de B0 (comme `b0_corrected` de l'étape 28).
"""

import importlib.util
import re
from datetime import date, timedelta

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio
import rasterio
from rasterio.features import rasterize
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

from atlas import forecast as fc
from atlas.download import ROOT

RAW = ROOT / "data" / "raw" / "nasa_appeears"
PROC = ROOT / "data" / "processed"
TAB = ROOT / "reports" / "tables"
PAT = re.compile(r"_250m_16_days_NDVI_doy(\d{4})(\d{3})\d*_aid\d+\.tif$")
SUB = 4                                      # sous-grille 4 × 4 pour la part de blé de chaque pixel
spec = importlib.util.spec_from_file_location("p19", ROOT / "scripts" / "19_forecast_ndvi.py")
p19 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p19)


def wheat_share(transform, width, height) -> np.ndarray:
    """Part moyenne 2015-2017 de chaque pixel NDVI couverte par des parcelles BTH."""
    fine = rasterio.Affine(transform.a / SUB, transform.b, transform.c, transform.d, transform.e / SUB, transform.f)
    acc = np.zeros((height, width), dtype=np.float32)
    for year in [2015, 2016, 2017]:
        p = pyogrio.read_dataframe(ROOT / "data" / "interim" / "rpg" / str(year) / "PARCELLES_GRAPHIQUES.shp",
                                   columns=["CODE_CULTU"], where="CODE_CULTU = 'BTH'").to_crs(4326)
        r = rasterize(((g, 1) for g in p.geometry), out_shape=(height * SUB, width * SUB), transform=fine,
                      fill=0, dtype="uint8")
        acc += r.reshape(height, SUB, width, SUB).mean(axis=(1, 3))
        print(f"RPG {year} : {len(p):,} parcelles BTH rasterisées")
    return acc / 3


def main() -> None:
    files = sorted(f for f in RAW.rglob("*.tif") if PAT.search(f.name))
    with rasterio.open(files[0]) as r0:
        transform, width, height = r0.transform, r0.width, r0.height
    share = wheat_share(transform, width, height)
    dep = gpd.read_parquet(ROOT / "data" / "raw" / "ign_admin_express" /
                           "ADMIN-EXPRESS-COG-CARTO_4-0_2026-01-01_departement.parquet").set_geometry("geometrie").to_crs(4326)
    dep = dep[dep.code_insee.str.len() == 2].reset_index(drop=True)
    dep_id = rasterize(((g, i + 1) for i, g in enumerate(dep.geometry)), out_shape=(height, width), transform=transform,
                       fill=0, dtype="int32")
    pure = (share >= 0.5) & (dep_id > 0)
    code, w = dep_id[pure], share[pure]
    n_dep = len(dep) + 1
    w_total = np.bincount(code, weights=w, minlength=n_dep)
    print(f"pixels purs (≥ 50 % de blé) : {pure.sum():,}")
    out = []
    for f in files:
        year, doy = map(int, PAT.search(f.name).groups())
        with rasterio.open(f) as rn, rasterio.open(f.with_name(f.name.replace("_NDVI_", "_pixel_reliability_"))) as rr:
            assert (rn.transform, rn.width, rn.height) == (transform, width, height)
            ndvi, rel = rn.read(1)[pure], rr.read(1)[pure]
        ok = (ndvi != -3000) & np.isin(rel, [0, 1])
        wv = np.bincount(code[ok], weights=w[ok], minlength=n_dep)
        s = np.bincount(code[ok], weights=w[ok] * ndvi[ok] * 1e-4, minlength=n_dep)
        val = np.where(wv >= 0.5 * w_total, s / np.maximum(wv, 1e-12), np.nan)   # même règle des 50 % que l'étape 18
        start = date(year, 1, 1) + timedelta(days=doy - 1)
        out.append(pd.DataFrame({"dep_code": dep.code_insee.to_numpy(), "ndvi": val[1:], "poids_pur": w_total[1:],
                                 "annee": year, "doy": doy, "debut": pd.Timestamp(start),
                                 "fin": pd.Timestamp(start + timedelta(days=15))}))
    comp = pd.concat(out, ignore_index=True)
    comp.to_parquet(PROC / "ndvi_pur_dep_composite.parquet", index=False)

    # Variables NDVI comme en phase 6 (composites terminés avant la date de prévision).
    parts = []
    for name, (mo, da) in p19.DATES.items():
        cut = pd.to_datetime(dict(year=comp["annee"], month=mo, day=da))
        ok = comp[comp["fin"] < cut].copy()
        ok["mois"] = ok["debut"].dt.month
        piv = ok[ok["mois"].between(4, 6)].pivot_table(index=["dep_code", "annee"], columns="mois", values="ndvi")
        piv.columns = [f"ndvi_{ {4: 'avril', 5: 'mai', 6: 'juin'}[c] }" for c in piv.columns]
        piv["ndvi_max"] = ok.groupby(["dep_code", "annee"])["ndvi"].max()
        piv.columns = [f"{c}_{name}" for c in piv.columns]
        parts.append(piv)
    nd_pur = pd.concat(parts, axis=1).reset_index()
    nd_old = pd.read_parquet(PROC / "ndvi_features.parquet")
    data = pd.read_parquet(PROC / "forecast_features.parquet")
    data = data[data.echantillon_principal & (data.annee >= 2010)]
    rows = []
    for label, nd in [("ndvi_actuel", nd_old), ("ndvi_pur", nd_pur)]:
        dd = data.merge(nd, on=["dep_code", "annee"], how="left")
        for dt in p19.DATES:
            cols = [c for c in nd.columns if c.endswith("_" + dt) and nd[c].notna().any()]
            for t in range(2016, 2026):
                train, test = dd[dd.annee < t], dd[dd.annee == t]
                train, test = p19.impute_by_train_dep_mean(train, test, cols)
                y, wt = test.log_rendement.to_numpy(), test.surface_ref_ha.to_numpy()
                # (a) modèles de la phase 6 : corrections de B1 (run_fold), avec NDVI.
                o, _ = fc.run_fold(train, test, dt, extra=cols)
                for m in [c for c in o.columns if c in ("B0", "RIDGE", "RF", "GBM")]:
                    rows.append({"ndvi": label, "date": dt, "annee": t, "famille": "phase 6 (B1)", "modele": m,
                                 "mse": np.average((o["obs"].to_numpy() - o[m].to_numpy()) ** 2, weights=o["poids"].to_numpy())})
                # (b) corrections de B0 (comme b0_corrected), variables météo + NDVI.
                xcols = fc.features(dt) + cols
                b0_tr = train.groupby("dep_code").log_rendement.transform("mean").to_numpy()
                b0_te = fc.predict_b0(train, test)
                resid, w = train.log_rendement.to_numpy() - b0_tr, train.surface_ref_ha.to_numpy()
                xtr, xte = fc.center_by_dep(train, test, xcols)
                xtr, xte = fc.standardize(xtr, xte)
                preds = {"B0": b0_te,
                         "RF_B0": b0_te + RandomForestRegressor(n_estimators=500, min_samples_leaf=10, max_features=1 / 3,
                                                                random_state=fc.SEED, n_jobs=-1).fit(xtr, resid, sample_weight=w).predict(xte),
                         "GBM_B0": b0_te + HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=200,
                                                                         min_samples_leaf=20, early_stopping=False,
                                                                         random_state=fc.SEED).fit(xtr, resid, sample_weight=w).predict(xte)}
                for m, pr in preds.items():
                    rows.append({"ndvi": label, "date": dt, "annee": t, "famille": "corrections de B0", "modele": m,
                                 "mse": np.average((y - pr) ** 2, weights=wt)})
        print(f"{label} terminé")
    M = pd.DataFrame(rows)
    rng = np.random.default_rng(fc.SEED)
    syn = []
    for (fam, dt, m), g in M.groupby(["famille", "date", "modele"]):
        piv = g.pivot(index="annee", columns="ndvi", values="mse")
        diff = (piv.ndvi_pur - piv.ndvi_actuel).to_numpy()
        boot = diff[rng.integers(0, len(diff), size=(9999, len(diff)))].mean(axis=1)
        syn.append({"famille": fam, "date": dt, "modele": m, "mse_ndvi_actuel": piv.ndvi_actuel.mean(),
                    "mse_ndvi_pur": piv.ndvi_pur.mean(), "gain_pur_pct": 100 * (1 - piv.ndvi_pur.mean() / piv.ndvi_actuel.mean()),
                    "ic95_bas": np.quantile(boot, 0.025), "ic95_haut": np.quantile(boot, 0.975),
                    "annees_mieux_avec_pur": int((diff < 0).sum())})
    S = pd.DataFrame(syn)
    S.to_csv(TAB / "phase7_s2_ndvi_pur.csv", index=False)
    print(S.round(5).to_string(index=False))


if __name__ == "__main__":
    main()
