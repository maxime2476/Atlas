"""Étape 44 : fenêtre phénologique du maïs (L4) : date du pic de végétation (MODIS MCD12Q2) et chaleur autour du pic.

Usage : uv run python scripts/44_phenologie_mais.py telecharger
        uv run --with pyhdf==0.11.6 python scripts/44_phenologie_mais.py construire
(pyhdf, lecteur HDF4, n'est pas une dépendance du projet : il n'est utilisé que pour lire MCD12Q2.)
Entrées : MCD12Q2 v061, tuile h18v04, 2001-2025, depuis le LP DAAC (jeton EARTHDATA_TOKEN de .env, jamais affiché) ;
          parcelles de maïs du RPG 2015-2017 (data/interim/rpg/<année>/) ; SIM2 quotidien ; poids du masque maïs.
Sortie : data/processed/phenologie_mais.parquet (département × année : date du pic, fenêtre, chaleur et SWI de la fenêtre).
Décisions déclarées avant calcul : docs/decisions.md, « Pistes d'amélioration (L1-L4, S1-S3) », L4, et sa précision.
"""

import hashlib
import importlib.util
import json
import sys
import time
import urllib.error
import urllib.request

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio
from pyproj import Transformer

from atlas.download import ROOT
from atlas.spatial import weighted_mean
from atlas.weather import daily_indicators, read_year

RAW = ROOT / "data" / "raw" / "nasa_mcd12q2"
PROC = ROOT / "data" / "processed"
SIM = ROOT / "data" / "raw" / "meteofrance_sim"
YEARS = range(2001, 2026)
DEP17 = ["01", "03", "18", "26", "28", "36", "37", "38", "39", "41", "45", "58", "63", "67", "68", "69", "89"]
# Grille sinusoïdale MODIS : tuile h18v04, 2 400 × 2 400 pixels de 500 m.
SINU = "+proj=sinu +R=6371007.181 +nadgrids=@null +wktext +units=m +no_defs"
TILE = 1111950.5197665
ULX, ULY = -20015109.355798 + 18 * TILE, 10007554.677899 - 4 * TILE
PIX = TILE / 2400
BEFORE, AFTER = 20, 40                       # fenêtre [pic − 20 j, pic + 40 j], 61 jours comme juillet-août


def token() -> str:
    env = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
    return env["EARTHDATA_TOKEN"].strip()


def fetch(req, tries: int = 4) -> bytes:
    for k in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 or k == tries - 1:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):   # coupure ou délai dépassé : on réessaie
            if k == tries - 1:
                raise
        time.sleep(15 * (k + 1))


def telecharger() -> None:
    spec = importlib.util.spec_from_file_location("dl", ROOT / "scripts" / "01_download_raw.py")
    dl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dl)
    q = ("https://cmr.earthdata.nasa.gov/search/granules.json?short_name=MCD12Q2&version=061"
         "&temporal=2001-01-01T00:00:00Z,2025-12-31T23:59:59Z&bounding_box=1.0,45.5,7.5,48.5&page_size=100")
    entries = json.loads(fetch(q))["feed"]["entry"]
    entries = [e for e in entries if ".h18v04." in e["title"]]
    # Une année peut exister en plusieurs traitements (2025 : deux) : on garde le plus récent (date dans le nom).
    latest = {}
    for e in entries:
        year = e["title"].split(".")[1][1:5]
        if year not in latest or e["title"] > latest[year]["title"]:
            latest[year] = e
    entries = list(latest.values())
    assert len(entries) == len(YEARS), f"{len(entries)} granules au lieu de {len(YEARS)}"
    tok = token()
    RAW.mkdir(parents=True, exist_ok=True)
    for e in sorted(entries, key=lambda e: e["time_start"]):
        url = [l["href"] for l in e["links"] if l["href"].startswith("https") and l["href"].endswith(".hdf")][0]
        dest = RAW / url.rsplit("/", 1)[1]
        fresh = not dest.exists()
        if fresh:
            dest.write_bytes(fetch(urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})))
        data = dest.read_bytes()
        row = {"file": str(dest.relative_to(ROOT)), "url": url, "size_bytes": len(data),
               "sha256": hashlib.sha256(data).hexdigest(), "downloaded": fresh}
        dl.update_manifest([row], {row["file"]: "nasa_mcd12q2"})
        print(f"{dest.name} : {len(data) / 1e6:.0f} Mo")


def maize_pixels() -> pd.DataFrame:
    """Surface moyenne de maïs (RPG 2015-2017, centroïdes) par pixel MODIS de 500 m et par département."""
    dep = gpd.read_parquet(ROOT / "data" / "raw" / "ign_admin_express" /
                           "ADMIN-EXPRESS-COG-CARTO_4-0_2026-01-01_departement.parquet").set_geometry("geometrie")
    dep = dep[dep.code_insee.isin(DEP17)][["code_insee", "geometrie"]].rename(columns={"code_insee": "dep_code"})
    parts = []
    for year in [2015, 2016, 2017]:
        p = pyogrio.read_dataframe(ROOT / "data" / "interim" / "rpg" / str(year) / "PARCELLES_GRAPHIQUES.shp",
                                   columns=["SURF_PARC", "CODE_CULTU"], where="CODE_CULTU = 'MIS'")
        c = gpd.GeoDataFrame({"surf_ha": p.SURF_PARC.to_numpy()}, geometry=p.geometry.centroid, crs=p.crs)
        c = gpd.sjoin(c, dep.to_crs(c.crs), how="inner", predicate="within")
        x, y = Transformer.from_crs(c.crs, SINU, always_xy=True).transform(c.geometry.x.to_numpy(), c.geometry.y.to_numpy())
        col, row = np.floor((x - ULX) / PIX).astype(int), np.floor((ULY - y) / PIX).astype(int)
        ok = (col >= 0) & (col < 2400) & (row >= 0) & (row < 2400)
        parts.append(pd.DataFrame({"dep_code": c.dep_code.to_numpy()[ok], "row": row[ok], "col": col[ok],
                                   "surf_ha": c.surf_ha.to_numpy()[ok]}))
        print(f"RPG {year} : {ok.sum():,} parcelles de maïs dans la tuile ({(~ok).sum()} hors tuile)")
    a = pd.concat(parts).groupby(["dep_code", "row", "col"], as_index=False).surf_ha.sum()
    a["surf_ha"] /= 3
    return a


def peaks(pix: pd.DataFrame) -> pd.DataFrame:
    from pyhdf.SD import SD
    rows = []
    for year in YEARS:
        f = SD(str(sorted(RAW.glob(f"MCD12Q2.A{year}001.h18v04.061.*.hdf"))[-1]))
        peak, qa = f.select("Peak").get(), f.select("QA_Overall").get()
        pk = peak[pix.row.to_numpy(), pix.col.to_numpy(), :].astype(float)
        q = qa[pix.row.to_numpy(), pix.col.to_numpy(), :]
        pk[(pk >= 32767) | (q > 1)] = np.nan
        # Mois et jour de l'année du pic, pour chacun des deux cycles (NaT si absent ou de mauvaise qualité).
        dts = [pd.to_datetime("1970-01-01") + pd.to_timedelta(pk[:, k], unit="D") for k in range(2)]
        month = np.column_stack([d.month.to_numpy(dtype=float, na_value=np.nan) for d in dts])
        doys = np.column_stack([d.dayofyear.to_numpy(dtype=float, na_value=np.nan) for d in dts])
        inwin = (month >= 6) & (month <= 9)
        one = inwin.sum(axis=1) == 1                       # exactement un cycle dont le pic tombe en juin-septembre
        doy = np.where(one, doys[np.arange(len(pk)), np.argmax(inwin, axis=1)], np.nan)
        d = pix.assign(doy=doy)
        for dep_code, g in d.groupby("dep_code"):
            v = g.doy.notna()
            rows.append({"dep_code": dep_code, "annee": year, "pic_doy": np.average(g.doy[v], weights=g.surf_ha[v]) if v.any() else np.nan,
                         "part_valide": g.surf_ha[v].sum() / g.surf_ha.sum()})
    out = pd.DataFrame(rows)
    out.loc[out.part_valide < 0.5, "pic_doy"] = np.nan    # pas de date si moins de la moitié du maïs est datée
    return out


def construire() -> None:
    pix = maize_pixels()
    pk = peaks(pix)
    w = pd.read_parquet(PROC / "weights_cell_dep_maize.parquet")
    w = w[w.dep_code.isin(DEP17)]
    cells = w[["LAMBX", "LAMBY"]].drop_duplicates()
    out = []
    for year in YEARS:
        t0 = time.perf_counter()
        nxt = SIM / f"QUOT_SIM2_{year + 1}.csv.gz"
        df = read_year(SIM / f"QUOT_SIM2_{year}.csv.gz", nxt if nxt.exists() else None).merge(cells, on=["LAMBX", "LAMBY"])
        di = daily_indicators(df)[["LAMBX", "LAMBY", "date", "dd_32", "swi"]]
        dep_day = weighted_mean(di, w, ["dd_32", "swi"], "w_maize", ["date"])
        dep_day["doy"] = dep_day.date.dt.dayofyear
        dep_day["month"] = dep_day.date.dt.month
        for dep_code, g in dep_day.groupby("dep_code"):
            p = pk[(pk.dep_code == dep_code) & (pk.annee == year)].pic_doy.iloc[0]
            ja = g[g.month.isin([7, 8])]
            row = {"dep_code": dep_code, "annee": year, "pic_doy": p, "dd_32_ja_quotidien": ja.dd_32.sum()}
            if np.isfinite(p):
                win = g[(g.doy >= round(p) - BEFORE) & (g.doy <= round(p) + AFTER)]
                assert len(win) == BEFORE + AFTER + 1
                row.update({"debut_doy": round(p) - BEFORE, "fin_doy": round(p) + AFTER,
                            "dd_32_ph": win.dd_32.sum(), "swi_ph": win.swi.mean()})
            out.append(row)
        print(f"{year} : {time.perf_counter() - t0:.0f} s")
    res = pd.DataFrame(out).merge(pk[["dep_code", "annee", "part_valide"]], on=["dep_code", "annee"])
    # Contrôle : la somme quotidienne de juillet-août redonne la chaleur mensuelle du panel (même masque, même formule).
    panel = pd.read_parquet(PROC / "panel_mais_long.parquet").drop_duplicates(["dep_code", "annee"])
    chk = res.merge(panel[["dep_code", "annee", "dd_32_ja"]], on=["dep_code", "annee"])
    assert np.allclose(chk.dd_32_ja_quotidien, chk.dd_32_ja, atol=1e-6), "chaleur quotidienne ≠ chaleur mensuelle"
    res.to_parquet(PROC / "phenologie_mais.parquet", index=False)
    print(res.describe().round(2).to_string())


if __name__ == "__main__":
    {"telecharger": telecharger, "construire": construire}[sys.argv[1]]()
