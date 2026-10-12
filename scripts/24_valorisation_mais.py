"""Étape 24 : valorisation descriptive de Q1 (phase 4 bis) : quintaux et euros associés à l'irrigation lors des étés chauds.

Usage : uv run python scripts/24_valorisation_mais.py   (après Rscript R/14_q1_maize.R et R/21_q1_revue.R)
Entrées : data/processed/panel_mais_long.parquet ; reports/tables/phase4bis_q1_hypotheses.csv (beta de H1) ;
          reports/tables/phase4bis_q1_revue_intervalles.csv (IC 90 % par inversion du WCR, R/21_q1_revue.R) ;
          data/raw/prix/insee_ippap_mais_010776430.xml ; data/raw/prix/eurostat_apri_ap_crpouta_FR_mais.json
Sortie : reports/tables/phase4bis_q1_valorisation.csv

Formule (docs/specification_phase4bis.md) : pour le département d l'année t,
  q_dt = surface irriguée_dt × Y_non irrigué,dt × [exp(beta × (dd_32_ja_dt − moyenne_d)) − 1]
C'est un ordre de grandeur DESCRIPTIF conditionnel à beta : « quintaux associés à l'irrigation lors d'un été plus
chaud que la moyenne du département », pas un gain causé par l'irrigation.
"""

import json
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

from atlas.download import ROOT

RAW = ROOT / "data" / "raw" / "prix"
TABLES = ROOT / "reports" / "tables"
YEARS = [2003, 2019, 2022]


def maize_price() -> tuple[pd.Series, float, float]:
    root = ET.parse(RAW / "insee_ippap_mais_010776430.xml").getroot()
    ippap = pd.Series({int(o.attrib["TIME_PERIOD"]): float(o.attrib["OBS_VALUE"])
                       for o in root.iter() if o.tag.endswith("Obs")}).sort_index()
    with open(RAW / "eurostat_apri_ap_crpouta_FR_mais.json") as f:
        d = json.load(f)
    idx = {v: int(k) for k, v in d["dimension"]["time"]["category"]["index"].items()}
    eur = pd.Series({idx[int(k)]: v for k, v in d["value"].items()}).sort_index()
    ratio = (eur / ippap).loc[2012:2016]
    spread = ratio.max() - ratio.min()
    # Règle pré-spécifiée : valorisation abandonnée si le rapport n'est pas stable.
    if spread >= 0.002:
        raise SystemExit(f"raccord instable (écart {spread:.4f} €/q par point) : valorisation abandonnée")
    return ratio.mean() * ippap, ratio.mean(), spread


def main() -> None:
    hyp = pd.read_csv(TABLES / "phase4bis_q1_hypotheses.csv")
    h1 = hyp[hyp["hypothese"] == "H1"].iloc[0]
    # Fourchette : bornes de l'intervalle à 90 % obtenu par inversion du WCR (analyse E1, déclarée le 2026-10-12),
    # à la place de l'intervalle CR1 groupé par année, dont la taille n'était pas vérifiée.
    ci = pd.read_csv(TABLES / "phase4bis_q1_revue_intervalles.csv")
    ci = ci[(ci["modele"] == "A1 maïs 2000-2025") & (ci["niveau"] == 0.90)].iloc[0]
    if abs(ci["estimation"] - h1["estimation"]) > 1e-12:
        raise SystemExit("l'intervalle E1 ne porte pas sur le beta de H1")
    betas = {"estimation": h1["estimation"], "ic90_bas": ci["borne_inf"], "ic90_haut": ci["borne_sup"]}

    m = pd.read_parquet(ROOT / "data" / "processed" / "panel_mais_long.parquet")
    m = m[m["echantillon_principal"]]
    irr = m[m.modalite == "irrigue"][["dep_code", "annee", "surface_ha", "dd_32_ja"]]
    non = m[m.modalite == "non_irrigue"][["dep_code", "annee", "rendement_q_ha"]]
    p = irr.merge(non, on=["dep_code", "annee"], how="inner", validate="one_to_one")   # paires, comme en R
    p["ecart_dd32"] = p["dd_32_ja"] - p.groupby("dep_code")["dd_32_ja"].transform("mean")
    price, k, spread = maize_price()
    print(f"prix du maïs : {k:.4f} €/q par point d'IPPAP (raccord 2012-2016, écart max {spread:.4f})")

    rows = []
    for year in YEARS:
        y = p[p.annee == year]
        row = {"annee": year, "departements": len(y), "surface_irriguee_ha": y.surface_ha.sum(),
               "ecart_dd32_moyen_pondere": np.average(y.ecart_dd32, weights=y.surface_ha),
               "prix_eur_q": price.loc[year]}
        for name, b in betas.items():
            q = (y.surface_ha * y.rendement_q_ha * (np.exp(b * y.ecart_dd32) - 1)).sum()
            row[f"quintaux_{name}"] = q
            row[f"millions_eur_{name}"] = q * price.loc[year] / 1e6
        rows.append(row)
    out = pd.DataFrame(rows)
    out["beta"] = betas["estimation"]
    out.to_csv(TABLES / "phase4bis_q1_valorisation.csv", index=False)
    print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
