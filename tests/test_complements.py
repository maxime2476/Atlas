"""Tests des analyses complémentaires (scripts/28_complements_python.py, scripts/29_eolien.py)."""

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


@pytest.mark.skipif(not (PROC / "panel_fourrage.parquet").exists(), reason="panel fourrage absent")
def test_fodder_panel():
    fo = pd.read_parquet(PROC / "panel_fourrage.parquet")
    assert not fo.duplicated(["dep_code", "annee"]).any()
    assert fo.annee.between(2010, 2025).all() and fo.dep_code.nunique() == 28
    assert (fo.irrigue > 0).all() and (fo.non_irrigue > 0).all()
    assert np.allclose(fo.ecart_log, np.log(fo.irrigue) - np.log(fo.non_irrigue))
    assert fo[["dd_32_ja", "swi_ja", "surface_ref_ha"]].notna().all().all() and (fo.dd_32_ja >= 0).all()


def test_tetens_saturation_pressure():
    # Valeurs de référence de la formule de Tetens : 0,6108 kPa à 0 °C, environ 3,17 kPa à 25 °C.
    spec = importlib.util.spec_from_file_location("vpd", ROOT / "scripts" / "34_vpd.py")
    vpd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vpd)
    assert np.isclose(vpd.es(0.0), 0.6108) and np.isclose(vpd.es(25.0), 3.168, atol=0.002)


@pytest.mark.skipif(not (PROC / "vpd_dep_ja.parquet").exists(), reason="VPD absent")
def test_vpd_panel():
    v = pd.read_parquet(PROC / "vpd_dep_ja.parquet")
    assert not v.duplicated(["dep_code", "annee"]).any() and v.annee.between(2000, 2025).all()
    assert v.vpd_ja.between(0.1, 5).all()      # kPa, ordre de grandeur estival


@pytest.mark.skipif(not (PROC / "vpd_dep_ja_fourrage.parquet").exists(), reason="VPD fourrage absent")
def test_vpd_fodder_panel():
    v = pd.read_parquet(PROC / "vpd_dep_ja_fourrage.parquet")
    assert not v.duplicated(["dep_code", "annee"]).any() and v.vpd_ja.between(0.1, 5).all()


DEP17 = ["01", "03", "18", "26", "28", "36", "37", "38", "39", "41", "45", "58", "63", "67", "68", "69", "89"]


@pytest.mark.skipif(not (PROC / "ru_dep_mais.parquet").exists(), reason="RU absente")
def test_ru_panel():
    ru = pd.read_parquet(PROC / "ru_dep_mais.parquet")
    assert not ru.dep_code.duplicated().any() and set(DEP17) <= set(ru.dep_code)
    assert ru.ru_mm.between(0, 300).all()                    # mm sur 0-200 cm
    assert (ru.part_sans_donnee < 0.01).all() and (ru.pixels_mais > 0).all()


@pytest.mark.skipif(not (PROC / "bnpe_irr_dep_annee.parquet").exists(), reason="BNPE absente")
def test_bnpe_panel_matches_raw_total():
    v = pd.read_parquet(PROC / "bnpe_irr_dep_annee.parquet")
    assert sorted(v.dep_code.unique()) == DEP17 and len(v) == 17 * 12
    assert not v.duplicated(["dep_code", "annee"]).any() and (v.volume_m3 > 0).all()
    raw = pd.concat(pd.read_csv(f, sep=";", usecols=["volume"]) for f in (ROOT / "data" / "raw" / "hubeau_bnpe").glob("*.csv"))
    assert np.isclose(v.volume_m3.sum(), raw.volume.sum())   # l'agrégation ne perd ni ne double aucun volume


@pytest.mark.skipif(not (PROC / "ra_irrigation_dep.parquet").exists(), reason="RA2020 absent")
def test_ra2020_shares():
    ra = pd.read_parquet(PROC / "ra_irrigation_dep.parquet")
    assert set(ra.annee_ra) == {2010, 2020} and not ra.duplicated(["dep_code", "annee_ra"]).any()
    assert ra.part_mais_grain_irrigue.dropna().between(0, 1).all()
    r68 = ra[(ra.dep_code == "68") & (ra.annee_ra == 2020)].iloc[0]   # valeurs lues dans le fichier brut
    assert r68.mais_grain_irrigue_ha == 30584 and r68.sau_irriguee_ha == 41994


@pytest.mark.skipif(not (ROOT / "reports" / "tables" / "phase7_w2_departement_annee.csv").exists(), reason="W2 absent")
def test_water_value_identities():
    w = pd.read_csv(ROOT / "reports" / "tables" / "phase7_w2_departement_annee.csv", dtype={"dep_code": str})
    assert sorted(w.dep_code.unique()) == ["01", "03", "18", "63", "67", "68"]
    assert np.allclose(w.dose_m3_ha, w.volume_m3 * w.part_2020 / w.surface_ha)
    ok = w.plausible
    assert (ok == w.dose_m3_ha.between(500, 3000)).all() and w.eur_par_m3[~ok].isna().all()
    assert np.allclose(w.eur_par_m3[ok], w.kg_par_m3[ok] / 100 * w.prix_eur_q[ok])


def _drias():
    spec = importlib.util.spec_from_file_location("drias", ROOT / "scripts" / "38_drias_indicateurs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pressure_and_vapour_pressure():
    d = _drias()
    assert np.isclose(d.pressure_kpa(0.0), 101.3) and np.isclose(d.pressure_kpa(1000.0), 90.0, atol=0.1)   # FAO-56
    # q = 0,622 e / (p − 0,378 e) inversée : e retrouvé à partir de q
    e, p = 1.8, 98.0
    q = 0.622 * e / (p - 0.378 * e)
    assert np.isclose(d.vapour_pressure(q, p), e)


@pytest.mark.skipif(not (PROC / "drias_dep_annee.parquet").exists(), reason="DRIAS absent")
def test_drias_panel():
    v = pd.read_parquet(PROC / "drias_dep_annee.parquet")
    assert v.modele.nunique() == 17 and sorted(v.dep_code.unique()) == DEP17
    assert not v.duplicated(["modele", "periode", "dep_code", "annee"]).any()
    assert v[["dd_32_ja", "vpd_ja"]].notna().all().all() and (v.dd_32_ja >= 0).all() and v.vpd_ja.between(0.1, 6).all()
    hist = v[v.periode == "historique"]
    assert hist.annee.between(1976, 2005).all() and len(hist) == 17 * 17 * 30
    syn = pd.read_csv(ROOT / "reports" / "tables" / "phase7_d1_synthese.csv")
    assert list(syn.horizon) == ["1976-2005", "France +2.0", "France +2.7", "France +4.0"]
    assert syn.dd_32_ja_mediane.is_monotonic_increasing
