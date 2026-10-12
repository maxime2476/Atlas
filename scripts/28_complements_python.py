"""Étape 28 : analyses complémentaires v1.2 côté Python (préparation des variables, G2, G8, G12).

Usage : uv run python scripts/28_complements_python.py preparer     (avant R/22_q1_complements.R)
        uv run python scripts/28_complements_python.py prevision    (G12, indépendant)
Déclaration : docs/decisions.md (« Analyses complémentaires (v1.2) »), avant calcul. Exploratoire.

Sorties :
  data/processed/phase7_covariables_dep.parquet   un département par ligne (38 départements de la population maïs) :
      part_irriguee (maïs grain irrigué / total, surfaces 2010-2012), alt_masque_m, alt_surface_m, ecart_alt_m
      (surface − masque), relief (6 départements du tableau 5), lat_centroide
  data/processed/phase7_fourrage.parquet          département × année 2010-2025 : surfaces de maïs fourrage et de maïs
      grain non irrigués, part_fourrage_non_irr = fourrage / (fourrage + grain)
  data/processed/phase7_dml_residus.parquet       G8 : résidus du DML (Y et dd_32_ja), pour l'inférence WCR en R
  reports/tables/phase7_prevision_conforme.csv, phase7_prevision_vs_B0.csv   G12
"""

import argparse

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge

from atlas import forecast as fc
from atlas.download import ROOT
from atlas.saa import read_sheet_wide, to_long

PROC = ROOT / "data" / "processed"
TAB = ROOT / "reports" / "tables"
SAA_ZIP = ROOT / "data" / "raw" / "agreste_saa" / "SAA-SeriesLongues-2010-2025_DonneesProvisoires-DepartementalesRegionales.zip"
RELIEF = ["01", "26", "38", "39", "63", "69"]
SEED = 20261012


def maize_pairs() -> pd.DataFrame:
    """Paires irrigué / non irrigué de l'échantillon principal (même construction que R/14)."""
    m = pd.read_parquet(PROC / "panel_mais_long.parquet")
    m = m[m.echantillon_principal]
    irr = m[m.modalite == "irrigue"]
    non = m[m.modalite == "non_irrigue"][["dep_code", "annee", "log_rendement"]].rename(
        columns={"log_rendement": "log_non_irrigue"})
    d = irr.merge(non, on=["dep_code", "annee"], how="inner", validate="one_to_one")
    d["ecart_log"] = d.log_rendement - d.log_non_irrigue
    if len(d) != 435:
        raise RuntimeError(f"{len(d)} paires au lieu de 435")
    return d


def covariates() -> pd.DataFrame:
    m = pd.read_parquet(PROC / "panel_mais_long.parquet")
    ref = (m[m.annee.between(2010, 2012)].groupby(["dep_code", "modalite"]).surface_ha.mean().unstack())
    out = pd.DataFrame({"part_irriguee": ref.irrigue / (ref.irrigue + ref.non_irrigue)})
    alt = pd.read_parquet(PROC / "cell_altitude.parquet")
    for wfile, wcol, col in [("weights_cell_dep_maize", "w_maize", "alt_masque_m"),
                             ("weights_cell_dep_area", "w_area", "alt_surface_m")]:
        w = pd.read_parquet(PROC / f"{wfile}.parquet").merge(alt, on=["LAMBX", "LAMBY"]).dropna(subset=["altitude_moy_m"])
        out[col] = w.groupby("dep_code").apply(lambda d: (d[wcol] * d.altitude_moy_m).sum() / d[wcol].sum())
    out["ecart_alt_m"] = out.alt_surface_m - out.alt_masque_m
    out = out.reset_index()
    out["relief"] = out.dep_code.isin(RELIEF)
    out = out.merge(m[["dep_code", "lat_centroide"]].drop_duplicates(), on="dep_code", how="left", validate="one_to_one")
    if out.isna().any().any() or len(out) != 38:
        raise RuntimeError("covariables départementales incomplètes")
    return out


def fodder() -> pd.DataFrame:
    fou = to_long(read_sheet_wide(SAA_ZIP, "FOU"))
    cop = pd.read_parquet(ROOT / "data" / "interim" / "saa_cop_departements_long.parquet")
    f = fou[fou.culture_code == "05"][["dep_code", "annee", "surface_ha"]].rename(columns={"surface_ha": "fourrage_non_irr_ha"})
    g = cop[cop.culture_code == "15"][["dep_code", "annee", "surface_ha"]].rename(columns={"surface_ha": "grain_non_irr_ha"})
    out = f.merge(g, on=["dep_code", "annee"], how="inner", validate="one_to_one")
    out["part_fourrage_non_irr"] = out.fourrage_non_irr_ha / (out.fourrage_non_irr_ha + out.grain_non_irr_ha)
    return out


def two_way_residuals(df: pd.DataFrame, cols: list[str], w: np.ndarray) -> pd.DataFrame:
    """Résidus de MCO pondérés de chaque colonne sur les indicatrices département et année."""
    X = pd.get_dummies(df[["dep_code", "annee"]].astype(str), drop_first=True, dtype=float)
    X.insert(0, "const", 1.0)
    sw = np.sqrt(w)[:, None]
    Y = df[cols].to_numpy(float)
    coef = np.linalg.lstsq(X.to_numpy() * sw, Y * sw, rcond=None)[0]
    return pd.DataFrame(Y - X.to_numpy() @ coef, columns=cols, index=df.index)


def dml(d: pd.DataFrame) -> None:
    """G8 : modèle partiellement linéaire, nuisances par forêt aléatoire, validation croisée par blocs d'années."""
    controls = ["swi_ja", "prec_ja", "etp_ja", "gdd_0_32_ja"]
    w = d.surface_ref_ha.to_numpy(float)
    r = two_way_residuals(d, ["ecart_log", "dd_32_ja"] + controls, w)
    years = np.sort(d.annee.unique())
    folds = {y: k % 5 for k, y in enumerate(np.random.default_rng(SEED).permutation(years))}
    fold = d.annee.map(folds).to_numpy()
    res = pd.DataFrame(index=d.index, columns=["y_res", "d_res"], dtype=float)
    for k in range(5):
        tr, te = fold != k, fold == k
        for target, name in [("ecart_log", "y_res"), ("dd_32_ja", "d_res")]:
            rf = RandomForestRegressor(n_estimators=500, min_samples_leaf=5, random_state=SEED, n_jobs=-1)
            rf.fit(r.loc[tr, controls], r.loc[tr, target], sample_weight=w[tr])
            res.loc[te, name] = r.loc[te, target] - rf.predict(r.loc[te, controls])
    beta = np.sum(w * res.d_res * res.y_res) / np.sum(w * res.d_res ** 2)
    out = d[["dep_code", "annee", "surface_ref_ha"]].assign(y_res=res.y_res, d_res=res.d_res)
    out.to_parquet(PROC / "phase7_dml_residus.parquet", index=False)
    print(f"G8 DML : beta = {beta:.4f} (A1 : 0,0158) ; inférence WCR dans R/22")


def prepare() -> None:
    cov = covariates()
    cov.to_parquet(PROC / "phase7_covariables_dep.parquet", index=False)
    print(cov[cov.dep_code.isin(maize_pairs().dep_code)].round(3).to_string(index=False))
    fod = fodder()
    fod.to_parquet(PROC / "phase7_fourrage.parquet", index=False)
    print(f"fourrage : {len(fod)} département-années ; part médiane du fourrage dans le maïs non irrigué : "
          f"{fod.part_fourrage_non_irr.median():.2f}")
    dml(maize_pairs())


# --- G12 : prévision -------------------------------------------------------------------------------
def conformal(pred: pd.DataFrame, level: float = 0.90, start: int = 2018) -> pd.DataFrame:
    """Couverture d'intervalles conformes à origine glissante : quantile des |résidus| des années test passées."""
    rows = []
    for (date, variant), p in pred.groupby(["date", "variante"]):
        for model in ["B0", "B1", "L1", "RIDGE", "RF", "GBM"]:
            covered, width = [], []
            for t in range(start, 2026):
                past = p[p.annee < t]
                q = np.quantile(np.abs(past.obs - past[model]), level)
                cur = p[p.annee == t]
                covered.append(np.average(np.abs(cur.obs - cur[model]) <= q, weights=cur.poids))
                width.append(2 * q)
            rows.append({"date": date, "variante": variant, "modele": model, "niveau": level,
                         "annees_test": f"{start}-2025", "couverture_moyenne": np.mean(covered),
                         "couverture_min_annee": np.min(covered), "largeur_moyenne_log": np.mean(width)})
    return pd.DataFrame(rows)


def b0_corrected() -> pd.DataFrame:
    """Modèles prédisant le résidu de B0 (moyenne du département) au lieu de B1 ; mêmes réglages que fc.run_fold.

    Variante principale (entraînement depuis 2010), années test 2016-2025, déjà vues : exploratoire.
    """
    feat = pd.read_parquet(PROC / "forecast_features.parquet")
    feat = feat[feat.echantillon_principal].reset_index(drop=True)
    rows = []
    for date in ["juin", "juillet"]:
        cols = fc.features(date)
        for t in range(2016, 2026):
            train, test = feat[(feat.annee >= 2010) & (feat.annee < t)], feat[feat.annee == t]
            b0_tr = train.groupby("dep_code").log_rendement.transform("mean").to_numpy()
            b0_te = fc.predict_b0(train, test)
            resid, w = train.log_rendement.to_numpy() - b0_tr, train.surface_ref_ha.to_numpy()
            xtr, xte = fc.center_by_dep(train, test, cols)
            xtr, xte = fc.standardize(xtr, xte)
            alpha = fc.choose_ridge_alpha(xtr, resid, w, train.annee.to_numpy())
            preds = {
                "B0": b0_te,
                "RIDGE_B0": b0_te + Ridge(alpha=alpha).fit(xtr, resid, sample_weight=w).predict(xte),
                "RF_B0": b0_te + RandomForestRegressor(n_estimators=500, min_samples_leaf=10, max_features=1 / 3,
                                                       random_state=fc.SEED, n_jobs=-1)
                .fit(xtr, resid, sample_weight=w).predict(xte),
                "GBM_B0": b0_te + HistGradientBoostingRegressor(max_depth=3, learning_rate=0.05, max_iter=200,
                                                                min_samples_leaf=20, early_stopping=False,
                                                                random_state=fc.SEED)
                .fit(xtr, resid, sample_weight=w).predict(xte),
            }
            y, wt = test.log_rendement.to_numpy(), test.surface_ref_ha.to_numpy()
            for model, pr in preds.items():
                rows.append({"date": date, "annee": t, "modele": model, "mse": np.average((y - pr) ** 2, weights=wt)})
    m = pd.DataFrame(rows)
    rng = np.random.default_rng(SEED)
    out = []
    for date, g in m.groupby("date"):
        piv = g.pivot(index="annee", columns="modele", values="mse")
        boot_idx = rng.integers(0, len(piv), size=(9999, len(piv)))   # blocs d'années, comme en phase 5
        for model in ["RIDGE_B0", "RF_B0", "GBM_B0"]:
            diff = (piv[model] - piv["B0"]).to_numpy()
            bd = diff[boot_idx].mean(axis=1)
            out.append({"date": date, "modele": model, "skill_vs_B0": 1 - piv[model].mean() / piv["B0"].mean(),
                        "ecart_mse_vs_B0": diff.mean(), "ic95_bas": np.quantile(bd, 0.025),
                        "ic95_haut": np.quantile(bd, 0.975), "annees_meilleur_que_B0": int((diff < 0).sum())})
    return pd.DataFrame(out)


def forecasting() -> None:
    pred = pd.read_parquet(TAB / "phase5_predictions.parquet")
    conf = conformal(pred)
    conf.to_csv(TAB / "phase7_prevision_conforme.csv", index=False)
    print(conf.round(3).to_string(index=False))
    vs = b0_corrected()
    vs.to_csv(TAB / "phase7_prevision_vs_B0.csv", index=False)
    print(vs.round(4).to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("etape", choices=["preparer", "prevision"])
    {"preparer": prepare, "prevision": forecasting}[ap.parse_args().etape]()
