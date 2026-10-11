"""Tests du module prédictif : absence de fuite et justesse des références."""

import numpy as np
import pandas as pd
import pytest

from atlas.download import ROOT
from atlas.forecast import DATES, center_by_dep, features, fit_b1, run_fold

FEAT = ROOT / "data" / "processed" / "forecast_features.parquet"


def test_june_features_exclude_june_weather():
    assert all("remplissage" not in f for f in features("juin"))
    assert any(f.endswith("_mai") for f in features("juin"))
    assert all(f.split("_")[-1] in DATES["juillet"] for f in features("juillet"))


def test_b1_recovers_department_effects_and_trend():
    rows = [{"dep_code": d, "annee": t, "surface_ref_ha": 1.0,
             "log_rendement": base + 0.01 * (t - 2010)} for d, base in [("A", 4.0), ("B", 4.3)]
            for t in range(2010, 2020)]
    df = pd.DataFrame(rows)
    pred = fit_b1(df)(pd.DataFrame({"dep_code": ["A", "B"], "annee": [2020, 2020]}))
    assert np.allclose(pred, [4.10, 4.40])


def test_centering_uses_training_means_only():
    train = pd.DataFrame({"dep_code": ["A", "A"], "x": [1.0, 3.0]})
    test = pd.DataFrame({"dep_code": ["A"], "x": [100.0]})
    xtr, xte = center_by_dep(train, test, ["x"])
    assert np.allclose(xtr.ravel(), [-1, 1]) and np.allclose(xte.ravel(), [98])


@pytest.fixture(scope="module")
def data():
    if not FEAT.exists():
        pytest.skip("exécuter scripts/14_forecast_features.py")
    d = pd.read_parquet(FEAT)
    return d[d["echantillon_principal"] & (d["annee"] >= 2010)].reset_index(drop=True)


def test_test_year_outcome_does_not_affect_predictions(data):
    """Changer les rendements de l'année test ne doit modifier AUCUNE prévision (pas de fuite)."""
    train, test = data[data.annee < 2018], data[data.annee == 2018]
    p1, _ = run_fold(train, test, "juillet")
    test2 = test.assign(log_rendement=test["log_rendement"] + 5.0)
    p2, _ = run_fold(train, test2, "juillet")
    cols = ["B0", "B1", "L1", "RIDGE", "RF", "GBM"]
    assert np.allclose(p1[cols].to_numpy(), p2[cols].to_numpy())


def test_future_weather_does_not_affect_june_forecast(data):
    """Au 1er juin, modifier la météo de juin (fenêtre remplissage) ne change pas la prévision."""
    train, test = data[data.annee < 2018], data[data.annee == 2018]
    p1, _ = run_fold(train, test, "juin")
    test2 = test.copy()
    for c in [c for c in test.columns if c.endswith("_remplissage")]:
        test2[c] = test2[c] * 3 + 10
    p2, _ = run_fold(train, test2, "juin")
    assert np.allclose(p1[["L1", "RIDGE", "RF", "GBM"]].to_numpy(), p2[["L1", "RIDGE", "RF", "GBM"]].to_numpy())
