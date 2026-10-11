"""Étape 15 : évaluation chronologique du module prédictif (docs/specification_phase5.md).

Usage : uv run python scripts/15_forecast_cv.py   (~10 min)
Sorties (reports/tables/) :
  phase5_predictions.parquet      toutes les prévisions (date, variante, année test, département, modèle)
  phase5_metriques_annee.csv      RMSE / MAE / skill par modèle et par année test
  phase5_synthese.csv             moyennes, bootstrap par blocs d'années de l'écart de MSE à B1, années gagnées
  phase5_pertes.csv               détection des pertes (rappel, précision)
  phase5_national.csv             erreur sur le rendement national pondéré
  phase5_importance.csv           importance par permutation (RIDGE, GBM, 1er juillet, variante principale)
"""

import time

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from atlas.download import ROOT
from atlas.forecast import SEED, features, run_fold

TAB = ROOT / "reports" / "tables"
MODELS = ["B0", "B1", "L1", "RIDGE", "RF", "GBM"]
TEST_YEARS = range(2016, 2026)


def wmse(e, w):
    return np.average(e ** 2, weights=w)


def main() -> None:
    data = pd.read_parquet(ROOT / "data" / "processed" / "forecast_features.parquet")
    data = data[data["echantillon_principal"]].reset_index(drop=True)
    preds, importances = [], []
    for variant, first in [("principale_2010", 2010), ("longue_1990", 1990)]:
        for date in ["juin", "juillet"]:
            for t in TEST_YEARS:
                t0 = time.perf_counter()
                train = data[(data.annee >= first) & (data.annee < t)]
                test = data[data.annee == t]
                out, obj = run_fold(train, test, date)
                preds.append(out.assign(date=date, variante=variant, annee_test=t, alpha_ridge=obj["alpha"]))
                if variant == "principale_2010" and date == "juillet":
                    y_res = test["log_rendement"].to_numpy() - obj["base_te"]
                    for name in ["ridge", "gbm"]:
                        pi = permutation_importance(obj[name], obj["xte"], y_res, n_repeats=10, random_state=SEED,
                                                    sample_weight=test["surface_ref_ha"].to_numpy(),
                                                    scoring="neg_mean_squared_error")
                        importances.append(pd.DataFrame({"modele": name.upper(), "annee_test": t,
                                                         "variable": features(date),
                                                         "importance": pi.importances_mean}))
                print(f"{variant} {date} {t}: entraînement {train.annee.min()}-{train.annee.max()} "
                      f"({len(train)} obs.), α ridge = {obj['alpha']} ({time.perf_counter() - t0:.0f} s)")
    P = pd.concat(preds, ignore_index=True)
    P.to_parquet(TAB / "phase5_predictions.parquet", index=False)

    # --- Métriques par année test -------------------------------------------------------------
    rows = []
    for (variant, date, t), g in P.groupby(["variante", "date", "annee_test"]):
        w = g["poids"].to_numpy()
        mse_b1 = wmse(g["obs"] - g["B1"], w)
        for m in MODELS:
            e = g["obs"] - g[m]
            e_q = np.exp(g["obs"]) - np.exp(g[m])
            rows.append({"variante": variant, "date": date, "annee_test": t, "modele": m,
                         "mse_log": wmse(e, w), "rmse_log": np.sqrt(wmse(e, w)),
                         "mae_q_ha": np.average(np.abs(e_q), weights=w), "rmse_q_ha": np.sqrt(wmse(e_q, w)),
                         "skill_vs_B1": 1 - wmse(e, w) / mse_b1})
    M = pd.DataFrame(rows)
    M.to_csv(TAB / "phase5_metriques_annee.csv", index=False)

    # --- Synthèse et bootstrap par blocs d'années ------------------------------------------------
    rng = np.random.default_rng(SEED)
    syn = []
    for (variant, date), g in M.groupby(["variante", "date"]):
        piv = g.pivot(index="annee_test", columns="modele", values="mse_log")
        boot_idx = rng.integers(0, len(piv), size=(9999, len(piv)))
        for m in MODELS:
            diff = (piv[m] - piv["B1"]).to_numpy()  # < 0 : le modèle fait mieux que B1
            bd = diff[boot_idx].mean(axis=1)
            gm = g[g.modele == m]
            syn.append({"variante": variant, "date": date, "modele": m,
                        "rmse_log_moyen": np.sqrt(piv[m].mean()), "mae_q_ha_moyenne": gm["mae_q_ha"].mean(),
                        "skill_moyen_vs_B1": 1 - piv[m].mean() / piv["B1"].mean(),
                        "ecart_mse_vs_B1": diff.mean(), "ic95_bas": np.quantile(bd, 0.025),
                        "ic95_haut": np.quantile(bd, 0.975), "annees_meilleur_que_B1": int((diff < 0).sum()),
                        "n_annees": len(diff)})
    S = pd.DataFrame(syn)
    S.to_csv(TAB / "phase5_synthese.csv", index=False)

    # --- Détection des pertes et rendement national -------------------------------------------------
    loss_rows, nat_rows = [], []
    for (variant, date), g in P.groupby(["variante", "date"]):
        lost = (g["obs"] - g["B1"]) < np.log(0.9)
        for m in MODELS[2:]:
            pred_lost = (g[m] - g["B1"]) < np.log(0.95)
            tp = int((lost & pred_lost).sum())
            loss_rows.append({"variante": variant, "date": date, "modele": m, "pertes_observees": int(lost.sum()),
                              "pertes_predites": int(pred_lost.sum()), "vrais_positifs": tp,
                              "rappel": tp / max(int(lost.sum()), 1), "precision": tp / max(int(pred_lost.sum()), 1)})
        for t, gt in g.groupby("annee_test"):
            row = {"variante": variant, "date": date, "annee_test": t,
                   "observe_q_ha": np.average(np.exp(gt["obs"]), weights=gt["poids"])}
            for m in MODELS:
                row[f"{m}_q_ha"] = np.average(np.exp(gt[m]), weights=gt["poids"])
            nat_rows.append(row)
    pd.DataFrame(loss_rows).to_csv(TAB / "phase5_pertes.csv", index=False)
    pd.DataFrame(nat_rows).to_csv(TAB / "phase5_national.csv", index=False)

    imp = pd.concat(importances).groupby(["modele", "variable"], as_index=False)["importance"].mean()
    imp.sort_values(["modele", "importance"], ascending=[True, False]).to_csv(TAB / "phase5_importance.csv", index=False)

    pd.set_option("display.width", 200)
    print("\n== Synthèse (écart de MSE < 0 : meilleur que B1)\n",
          S.round({"rmse_log_moyen": 4, "mae_q_ha_moyenne": 2, "skill_moyen_vs_B1": 3, "ecart_mse_vs_B1": 5,
                   "ic95_bas": 5, "ic95_haut": 5}).to_string(index=False))


if __name__ == "__main__":
    main()
