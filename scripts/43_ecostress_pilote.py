"""Étape 43 : pilote ECOSTRESS (L3) : les parcelles de maïs irriguées sont-elles exposées à une autre chaleur ?

Usage : uv run python scripts/43_ecostress_pilote.py telecharger   # scènes de juillet-août 2022, 11 h-17 h locales
        uv run python scripts/43_ecostress_pilote.py calculer
Entrées : ECOSTRESS L2T LSTE v002 (70 m ; couches LST, cloud, QC) depuis le LP DAAC, jeton EARTHDATA_TOKEN de .env
          (jamais affiché) ; RPG 2022 (R84, R44) extrait dans data/interim/rpg/2022_<région>/ ; météo par maille.
Sorties : data/raw/ecostress/<granule>/*.tif (non modifiés, au manifeste) ; reports/tables/phase7_l3_*.csv.
Décisions déclarées avant calcul : docs/decisions.md, « Pistes d'amélioration (L1-L4, S1-S3) », L3. Pilote descriptif.
"""

import hashlib
import importlib.util
import json
import sys
import urllib.error
import urllib.request

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio
import rasterio
from rasterio.features import rasterize
from sklearn.mixture import GaussianMixture

from atlas.download import ROOT
from atlas.rpg import cell_of

RAW = ROOT / "data" / "raw" / "ecostress"
TAB = ROOT / "reports" / "tables"
DEPS = {"01": "R84", "38": "R84", "67": "R44"}
LAYERS = ["LST", "cloud", "QC"]


def fetch(req, tries: int = 4) -> bytes:
    """Lecture avec reprises : le LP DAAC et le CMR renvoient parfois des erreurs 5xx passagères."""
    import time
    for k in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 or k == tries - 1:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):   # coupure ou délai dépassé : on réessaie
            if k == tries - 1:
                raise
        time.sleep(10 * (k + 1))


def token() -> str:
    env = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
    return env["EARTHDATA_TOKEN"].strip()


def departements() -> gpd.GeoDataFrame:
    dep = gpd.read_parquet(RAW.parent / "ign_admin_express" / "ADMIN-EXPRESS-COG-CARTO_4-0_2026-01-01_departement.parquet")
    return dep.set_geometry("geometrie")[["code_insee", "geometrie"]].rename(columns={"code_insee": "dep_code"})


def granules(dep_code: str) -> list[dict]:
    b = departements().to_crs(4326).query("dep_code == @dep_code").total_bounds
    bbox = ",".join(f"{v:.3f}" for v in b)
    out, page = [], 1
    while True:
        q = ("https://cmr.earthdata.nasa.gov/search/granules.umm_json?short_name=ECO_L2T_LSTE&version=002"
             f"&temporal=2022-07-01T00:00:00Z,2022-08-31T23:59:59Z&bounding_box={bbox}&page_size=500&page_num={page}")
        items = json.loads(fetch(q))["items"]
        out += items
        if len(items) < 500:
            break
        page += 1
    keep = []
    for e in out:
        start = e["umm"]["TemporalExtent"]["RangeDateTime"]["BeginningDateTime"]
        if 9 <= int(start[11:13]) < 15:            # 11 h-17 h, heure d'été (UTC + 2)
            urls = {u["URL"].rsplit("_", 1)[1][:-4]: u["URL"] for u in e["umm"]["RelatedUrls"]
                    if u["URL"].startswith("https") and u["URL"].endswith(".tif")}
            keep.append({"granule": e["umm"]["GranuleUR"], "debut": start, **{k: urls[k] for k in LAYERS}})
    return keep


def telecharger() -> None:
    spec = importlib.util.spec_from_file_location("dl", ROOT / "scripts" / "01_download_raw.py")
    dl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dl)
    tok = token()
    seen, rows, source_of = set(), [], {}
    for dep_code in DEPS:
        for g in granules(dep_code):
            if g["granule"] in seen:
                continue
            seen.add(g["granule"])
            batch = []
            for layer in LAYERS:
                dest = RAW / g["granule"] / g[layer].rsplit("/", 1)[1]
                if dest.exists():                     # reprise : fichier déjà présent, inscrit tel quel
                    data, fresh = dest.read_bytes(), False
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    req = urllib.request.Request(g[layer], headers={"Authorization": f"Bearer {tok}"})
                    data, fresh = fetch(req), True
                    dest.write_bytes(data)
                batch.append({"file": str(dest.relative_to(ROOT)), "url": g[layer], "size_bytes": len(data),
                              "sha256": hashlib.sha256(data).hexdigest(), "downloaded": fresh})
                source_of[batch[-1]["file"]] = "ecostress"
            dl.update_manifest(batch, source_of)      # manifeste à jour après chaque scène
            rows += [r for r in batch if r["downloaded"]]
        print(f"{dep_code} : {len(seen)} granules au total")
    pd.DataFrame(sorted(seen), columns=["granule"]).to_csv(RAW / "granules.csv", index=False)
    print(f"{len(rows)} fichiers téléchargés ({sum(r['size_bytes'] for r in rows) / 1e6:.0f} Mo)")


def parcels(dep_code: str) -> gpd.GeoDataFrame:
    shp = ROOT / "data" / "interim" / "rpg" / f"2022_{DEPS[dep_code]}" / "PARCELLES_GRAPHIQUES.shp"
    p = pyogrio.read_dataframe(shp, columns=["SURF_PARC", "CODE_CULTU"], where="CODE_CULTU = 'MIS'")
    dep = departements().to_crs(p.crs).query("dep_code == @dep_code")
    cent = p.geometry.centroid
    p = p[cent.within(dep.geometry.iloc[0]).to_numpy() & (p.SURF_PARC >= 2)].reset_index(drop=True)
    p["pid"] = np.arange(1, len(p) + 1)
    return p


def calculer() -> None:
    gr = pd.read_csv(RAW / "granules.csv").granule.tolist()
    m = pd.read_parquet(ROOT / "data" / "interim" / "weather_cell_month.parquet")
    ja = (m[m.month.isin([7, 8]) & m.year.isin([2003, 2022])].groupby(["LAMBX", "LAMBY", "year"]).dd_32.sum()
          .unstack("year").rename(columns={2003: "dd_32_ja_2003", 2022: "dd_32_ja_2022"}).reset_index())
    long = pd.read_parquet(ROOT / "data" / "processed" / "panel_mais_long.parquet")
    saa = long[long.annee == 2022].pivot_table(index="dep_code", columns="modalite", values="surface_ha")
    res, parc_rows = [], []
    for dep_code in DEPS:
        p = parcels(dep_code)
        sums, counts = np.zeros(len(p) + 1), np.zeros(len(p) + 1)
        n_scenes = 0
        for g in gr:
            files = {lay: next((RAW / g).glob(f"*_{lay}.tif"), None) for lay in LAYERS}
            if any(v is None for v in files.values()):
                continue
            with rasterio.open(files["LST"]) as src:
                lst = src.read(1).astype(float)
                crs, tr, shape = src.crs, src.transform, src.shape
            with rasterio.open(files["cloud"]) as src:
                cloud = src.read(1)
            with rasterio.open(files["QC"]) as src:
                qc = src.read(1)
            pp = p.to_crs(crs)
            lab = rasterize(zip(pp.geometry, pp.pid), out_shape=shape, transform=tr, fill=0, dtype="int32")
            ok = (lab > 0) & np.isfinite(lst) & (lst > 250) & (cloud == 0) & ((qc & 0b11) <= 1)
            if ok.sum() < 300:
                continue
            mean = np.bincount(lab[ok], weights=lst[ok], minlength=len(p) + 1) / np.maximum(
                np.bincount(lab[ok], minlength=len(p) + 1), 1)
            npx = np.bincount(lab[ok], minlength=len(p) + 1)
            seen = npx >= 3                                   # au moins 3 pixels de 70 m dans la parcelle
            seen[0] = False
            if seen.sum() < 30:
                continue
            anom = mean - np.median(mean[seen])
            sums[seen] += anom[seen]
            counts[seen] += 1
            n_scenes += 1
        p["anomalie_lst"] = np.where(counts[1:] >= 3, sums[1:] / np.maximum(counts[1:], 1), np.nan)
        p["scenes"] = counts[1:]
        q = p.dropna(subset=["anomalie_lst"]).copy()
        gm = GaussianMixture(2, random_state=20261020).fit(q[["anomalie_lst"]])
        cool = int(np.argmin(gm.means_.ravel()))
        q["irrigue_proxy"] = gm.predict(q[["anomalie_lst"]]) == cool
        # Maille SIM2 du centroïde (même règle que les masques), puis chaleur de juillet-août 2003 et 2022.
        c = q.geometry.centroid.to_crs(27572)
        q["LAMBX"], q["LAMBY"] = cell_of(c.x.to_numpy(), c.y.to_numpy())
        q = q.merge(ja, on=["LAMBX", "LAMBY"], how="left", validate="many_to_one")
        w = q.SURF_PARC
        grp = {k: q[q.irrigue_proxy == k] for k in (True, False)}
        def wavg(g, col):
            return np.average(g[col], weights=g.SURF_PARC)
        res.append({
            "dep_code": dep_code, "scenes_utilisees": n_scenes, "parcelles": len(p), "parcelles_classees": len(q),
            "part_surface_irriguee_proxy": grp[True].SURF_PARC.sum() / w.sum(),
            "part_surface_irriguee_saa_2022": saa.loc[dep_code, "irrigue"] / saa.loc[dep_code].sum(),
            "ecart_lst_moyen_irrigue": wavg(grp[True], "anomalie_lst"), "ecart_lst_moyen_pluvial": wavg(grp[False], "anomalie_lst"),
            "dd_32_ja_2003_irrigue": wavg(grp[True], "dd_32_ja_2003"), "dd_32_ja_2003_pluvial": wavg(grp[False], "dd_32_ja_2003"),
            "dd_32_ja_2022_irrigue": wavg(grp[True], "dd_32_ja_2022"), "dd_32_ja_2022_pluvial": wavg(grp[False], "dd_32_ja_2022"),
        })
        parc_rows.append(q[["pid", "SURF_PARC", "anomalie_lst", "scenes", "irrigue_proxy", "LAMBX", "LAMBY"]]
                         .assign(dep_code=dep_code))
        print(f"{dep_code} : {n_scenes} scènes, {len(q)} parcelles classées")
    out = pd.DataFrame(res)
    out["diff_dd_2003"] = out.dd_32_ja_2003_irrigue - out.dd_32_ja_2003_pluvial
    out["diff_dd_2022"] = out.dd_32_ja_2022_irrigue - out.dd_32_ja_2022_pluvial
    out["lecture"] = np.where(out.diff_dd_2003.abs() < 1, "même chaleur non contredite", "chaleur différente")
    out.to_csv(TAB / "phase7_l3_ecostress.csv", index=False)
    pd.concat(parc_rows).to_csv(TAB / "phase7_l3_parcelles.csv", index=False)
    print(out.round(3).T.to_string())


if __name__ == "__main__":
    {"telecharger": telecharger, "calculer": calculer}[sys.argv[1]]()
