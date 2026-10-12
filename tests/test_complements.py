"""Tests des analyses complémentaires v1.2 (scripts/28_complements_python.py, scripts/29_eolien.py)."""

import importlib.util

import numpy as np
import pandas as pd
import pytest

from atlas.download import ROOT

spec = importlib.util.spec_from_file_location("compl", ROOT / "scripts" / "28_complements_python.py")
compl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compl)
PROC = ROOT / "data" / "processed"


def test_two_way_residuals_remove_department_and_year_means():
    # y = effet département + effet année + bruit : les résidus ne doivent garder que le bruit (centré).
    rng = np.random.default_rng(0)
    df = pd.DataFrame([(d, t) for d in "abcd" for t in range(2000, 2006)], columns=["dep_code", "annee"])
    noise = rng.normal(size=len(df))
    df["y"] = df.dep_code.map({"a": 1, "b": 2, "c": 3, "d": 4}) + (df.annee - 2000) * 0.5 + noise
    r = compl.two_way_residuals(df, ["y"], np.ones(len(df)))
    assert np.allclose(r.groupby(df.dep_code).y.mean(), 0, atol=1e-10)
    assert np.allclose(r.groupby(df.annee).y.mean(), 0, atol=1e-10)


def test_conformal_coverage_on_exchangeable_errors():
    # Erreurs i.i.d. : la couverture d'un intervalle à 90 % doit être proche de 90 %.
    rng = np.random.default_rng(1)
    years = range(2010, 2026)
    p = pd.DataFrame([(t, d) for t in years for d in range(200)], columns=["annee", "dep"])
    p["obs"] = rng.normal(size=len(p))
    for m in ["B0", "B1", "L1", "RIDGE", "RF", "GBM"]:
        p[m] = 0.0
    p["poids"], p["date"], p["variante"] = 1.0, "juin", "test"
    out = compl.conformal(p, level=0.90, start=2012)
    assert out.couverture_moyenne.between(0.87, 0.93).all()


@pytest.mark.skipif(not (PROC / "eolien_dep_annee.parquet").exists(), reason="panel éolien absent")
def test_wind_panel_keys_and_cumulative():
    w = pd.read_parquet(PROC / "eolien_dep_annee.parquet")
    assert not w.duplicated(["dep_code", "annee"]).any()
    assert w.annee.min() == 2000 and w.annee.max() == 2025
    assert len(w) == w.dep_code.nunique() * 26
    assert (w.mw_cumul >= 0).all() and w.sau_ref_ha.gt(0).all()
    # Puissance cumulée : jamais décroissante dans un département.
    assert (w.sort_values(["dep_code", "annee"]).groupby("dep_code").mw_cumul.diff().dropna() >= -1e-9).all()


@pytest.mark.skipif(not (PROC / "phase7_covariables_dep.parquet").exists(), reason="covariables absentes")
def test_covariates_and_fodder():
    cov = pd.read_parquet(PROC / "phase7_covariables_dep.parquet")
    assert len(cov) == 38 and cov.dep_code.is_unique
    assert cov.part_irriguee.between(0, 1).all() and cov.relief.sum() == 6
    fod = pd.read_parquet(PROC / "phase7_fourrage.parquet")
    assert not fod.duplicated(["dep_code", "annee"]).any()
    assert fod.annee.between(2010, 2025).all()
    assert fod.part_fourrage_non_irr.dropna().between(0, 1).all()
