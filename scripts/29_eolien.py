"""Étape 29 : puissance éolienne terrestre raccordée cumulée par département et par année (analyse G10, v1.2).

Usage : uv run python scripts/29_eolien.py   (après 01_download_raw.py --eolien)
Entrées :
  data/raw/rte_registre/registre_installations_2026-06-30.csv   registre national RTE / ODRÉ (Licence Ouverte 2.0)
  data/raw/agreste_saa/...zip, feuille TER                       SAU du département (ligne 33), 2010-2012
Sortie : data/processed/eolien_dep_annee.parquet (dep_code, annee, mw_cumul, sau_ref_ha, mw_par_10kha_sau ; 2000-2025)

Le registre est un instantané des installations EN SERVICE au 30/06/2026 : une éolienne démantelée avant
cette date n'y figure pas, et un parc renouvelé (repowering) peut porter une date de mise en service récente.
La puissance des premières années est donc mesurée avec erreur (sous-estimée). Déclaration : docs/decisions.md
(« Analyses complémentaires (v1.2) »), avant calcul.
"""

import pandas as pd

from atlas.download import ROOT
from atlas.saa import dep_code_from_label, read_sheet_wide

RAW = ROOT / "data" / "raw"
YEARS = range(2000, 2026)
SAA_ZIP = RAW / "agreste_saa" / "SAA-SeriesLongues-2010-2025_DonneesProvisoires-DepartementalesRegionales.zip"


def sau_reference() -> pd.Series:
    """SAU du département (ligne 33 de la feuille TER), moyenne 2010-2012, en ha."""
    ter = read_sheet_wide(SAA_ZIP, "TER")
    ter = ter[ter.LIB_SAA.str.startswith("33 - ")]
    ter = ter.assign(dep_code=ter.LIB_DEP.map(dep_code_from_label))
    ter = ter[~ter.dep_code.str.startswith("97")]
    if ter.dep_code.duplicated().any():
        raise RuntimeError("SAU : plusieurs lignes 33 pour un département")
    surf = ter.set_index("dep_code")[["SURF_2010", "SURF_2011", "SURF_2012"]].apply(pd.to_numeric, errors="raise")
    return surf.mean(axis=1)


def main() -> None:
    reg = pd.read_csv(RAW / "rte_registre" / "registre_installations_2026-06-30.csv", sep=";", dtype=str,
                      encoding="utf-8-sig")
    wind = reg[(reg.filiere == "Eolien") & (reg.technologie == "Terrestre")].copy()
    wind["mw"] = pd.to_numeric(wind["puismaxinstallee"], errors="raise") / 1000
    wind["annee_mes"] = pd.to_datetime(wind["datemiseenservice_date"], errors="coerce").dt.year
    n0 = len(wind)
    wind = wind.dropna(subset=["annee_mes", "codedepartement"])
    print(f"éolien terrestre : {n0} installations, {n0 - len(wind)} sans date ou département retirées ; "
          f"{wind.mw.sum():.0f} MW au 30/06/2026")

    by_year = wind.groupby(["codedepartement", "annee_mes"])["mw"].sum().rename("mw").reset_index()
    sau = sau_reference()
    grid = pd.MultiIndex.from_product([sau.index, YEARS], names=["dep_code", "annee"]).to_frame(index=False)
    rows = []
    for dep, year in grid.itertuples(index=False):
        d = by_year[(by_year.codedepartement == dep) & (by_year.annee_mes <= year)]
        rows.append((dep, year, d.mw.sum()))
    out = pd.DataFrame(rows, columns=["dep_code", "annee", "mw_cumul"])  # au 31 décembre de l'année
    out["sau_ref_ha"] = out.dep_code.map(sau)
    out["mw_par_10kha_sau"] = out.mw_cumul / out.sau_ref_ha * 1e4
    if out.sau_ref_ha.isna().any() or out.duplicated(["dep_code", "annee"]).any():
        raise RuntimeError("SAU manquante ou doublon dans le panel éolien")
    out.to_parquet(ROOT / "data" / "processed" / "eolien_dep_annee.parquet", index=False)
    print(f"{out.dep_code.nunique()} départements × {out.annee.nunique()} années ; "
          f"MW cumulés fin 2025 : {out[out.annee == 2025].mw_cumul.sum():.0f}")


if __name__ == "__main__":
    main()
