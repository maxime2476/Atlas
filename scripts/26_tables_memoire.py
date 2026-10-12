"""Étape 26 : chiffres et tableaux du mémoire (LaTeX), générés à partir de reports/tables/.

Usage : uv run python scripts/26_tables_memoire.py
Sorties : memoire/tables/numbers.tex (macros \\newcommand utilisées dans le texte) et memoire/tables/*.tex.
Règle : aucun chiffre de résultat n'est saisi à la main dans le mémoire ; le texte n'utilise que ces macros.
"""

import math

import pandas as pd

from atlas.download import ROOT

TAB = ROOT / "reports" / "tables"
OUT = ROOT / "memoire" / "tables"


def pv(p: float) -> str:
    """p-valeur pour le texte : trois décimales, ou « <0.001 »."""
    return "<0.001" if p < 0.0005 else f"{p:.3f}"


def pct(x: float, digits: int = 1) -> str:
    return f"{x:.{digits}f}"


def data_numbers(n: dict) -> None:
    """Chiffres de description des données (chapitre 3), recalculés depuis les fichiers du projet."""
    proc = ROOT / "data" / "processed"
    saa = pd.read_parquet(ROOT / "data" / "interim" / "saa_cop_departements_long.parquet")

    # Panel maïs : population, échantillon principal, retraits, paires.
    m = pd.read_parquet(proc / "panel_mais_long.parquet")
    n_dep, n_years = m.dep_code.nunique(), m.annee.nunique()
    n["MaizeDeps"], n["MaizeYears"] = str(n_dep), str(n_years)
    n["MaizeMainDeps"] = str(m.loc[m.echantillon_principal, "dep_code"].nunique())
    n["MaizeRemoved"] = str(n_dep * n_years * 2 - len(m))           # rendements manquants ou nuls retirés
    pairs = m.pivot_table(index=["dep_code", "annee"], columns="modalite", values="log_rendement").dropna()
    n["MaizePairs"] = str(len(pairs))
    main_deps = set(m.loc[m.echantillon_principal, "dep_code"])
    n["MaizeMainPairs"] = str(int(pairs.index.get_level_values(0).isin(main_deps).sum()))

    # Raccord des deux versions de la SAA (2010-2020), maïs irrigué et non irrigué.
    import importlib.util
    spec = importlib.util.spec_from_file_location("pm", ROOT / "scripts" / "22_build_panel_mais.py")
    pm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pm)
    import io
    import zipfile
    z = zipfile.ZipFile(ROOT / "data" / "raw" / "agreste_saa_ancienne" / "FDS_DEVELOPPE_2.zip")
    parts = []
    for y in range(2010, 2021):
        d = pd.read_csv(io.BytesIO(z.read(f"FDS_DEVELOPPE_{y}.csv")), sep=";", dtype=str)
        parts.append(d[d.N306_LIB.isin(pm.MOD) & (d.N027_LIB == "Rendement") & (d.DEP != "...")])
    old = pd.concat(parts)
    old = old.assign(annee=old.ANNREF.astype(int), modalite=old.N306_LIB.map(pm.MOD),
                     old=pd.to_numeric(old.VALEUR, errors="coerce"))[["DEP", "annee", "modalite", "old"]]
    new = pm.new_series(saa)
    j = old.merge(new.rename(columns={"dep_code": "DEP"}), on=["DEP", "annee", "modalite"]).dropna(subset=["old", "rendement_q_ha"])
    j = j[(j.old > 0) & (j.rendement_q_ha > 0)]
    diff = (j.old - j.rendement_q_ha).abs()
    n["SpliceN"] = f"{len(j):,}"
    n["SpliceShare"] = f"{100 * (diff <= 0.5).mean():.0f}"
    n["SpliceMedian"] = f"{(j.old - j.rendement_q_ha).median():.1f}"
    n["SpliceCorrIrr"] = f"{j[j.modalite == 'irrigue'][['old', 'rendement_q_ha']].corr().iloc[0, 1]:.2f}"
    n["SpliceCorrRain"] = f"{j[j.modalite == 'non_irrigue'][['old', 'rendement_q_ha']].corr().iloc[0, 1]:.2f}"

    # Masque maïs RPG (MIS) contre la SAA : code 18 (total maïs grain et maïs semence, 16 + 17 ; la semence en fait environ 4 %
    # en 2015-2017) et maïs fourrage (feuille FOU, code 06).
    from atlas.saa import read_sheet_wide, to_long
    area = pd.read_parquet(proc / "maize_area_cell_dep_rpg.parquet").groupby(["dep_code", "millesime"])["surf_ha"].sum()
    grain = saa[(saa.culture_code == "18") & saa.metropole & saa.annee.between(2015, 2017)].set_index(["dep_code", "annee"])["surface_ha"]
    fou = to_long(read_sheet_wide(ROOT / "data" / "raw" / "agreste_saa" /
                                  "SAA-SeriesLongues-2010-2025_DonneesProvisoires-DepartementalesRegionales.zip", "FOU"))
    fodder = fou[(fou.culture_code == "06") & fou.metropole & fou.annee.between(2015, 2017)].set_index(["dep_code", "annee"])["surface_ha"]
    for s in (grain, fodder):
        s.index.names = area.index.names
    c = pd.concat([area.rename("rpg"), grain.rename("grain"), fodder.rename("fodder")], axis=1).fillna(0)
    c = c[c.rpg > 2000]
    n["MaskCorrGrain"] = f"{c[['rpg', 'grain']].corr().iloc[0, 1]:.3f}"
    n["MaskCorrFodder"] = f"{c[['rpg', 'fodder']].corr().iloc[0, 1]:.2f}"

    # Blé : panels 2010-2025 et 1959-2025.
    w = pd.read_parquet(proc / "panel_ble.parquet")
    n["WheatDeps"], n["WheatMainDeps"] = str(w.dep_code.nunique()), str(w.loc[w.echantillon_principal, "dep_code"].nunique())
    n["WheatMainObs"] = f"{int(w.echantillon_principal.sum()):,}"
    n["WheatIntegerShare"] = f"{100 * (w.rendement_q_ha.round(6) % 1 == 0).mean():.1f}"   # rendements entiers en q/ha
    w59 = pd.read_parquet(proc / "panel_ble_1959.parquet")
    main59 = w59[w59.echantillon_principal]
    n["WheatLongMissing"] = str(int(main59.rendement_q_ha.isna().sum()))
    n["WheatLongMissingLast"] = str(int(main59.loc[main59.rendement_q_ha.isna(), "annee"].max()))
    # 1976 contre les autres années avant 2000 : moyenne simple des départements de Q2, degrés-jours > 32 °C en mai-juin.
    heat = main59[main59.log_rendement.notna()].groupby("annee").dd_32_remplissage.mean()
    n["HeatSeventySix"] = f"{heat.loc[1976]:.2f}"
    n["HeatPreTwoThousandOtherMax"] = f"{heat[(heat.index < 2000) & (heat.index != 1976)].max():.2f}"

    allw = pd.read_parquet(ROOT / "data" / "interim" / "weather_cell_month.parquet", columns=["swi"])["swi"]
    n["SwiMin"], n["SwiMax"] = f"{allw.min():.2f}", f"{allw.max():.2f}"

    grid = pd.read_csv(ROOT / "data" / "raw" / "meteofrance_sim" / "coordonnees_grille_safran_lambert-2-etendu.csv", sep=";")
    n["SimCells"] = f"{len(grid):,}"
    n["SimCellsFrance"] = f"{pd.read_parquet(proc / 'weights_cell_dep_area.parquet')[['LAMBX', 'LAMBY']].drop_duplicates().shape[0]:,}"

    # VigiEau : part des arrêtés sans niveau de gravité.
    v = pd.read_parquet(proc / "vigieau_dep_ete.parquet").groupby("annee")["part_arretes_sans_niveau"].first() * 100
    n["VigiMissEarlyMin"], n["VigiMissEarlyMax"] = f"{v.loc[2012:2015].min():.0f}", f"{v.loc[2012:2015].max():.0f}"
    n["VigiMissMidMin"], n["VigiMissMidMax"] = f"{v.loc[2016:2022].min():.0f}", f"{v.loc[2016:2022].max():.0f}"


def exposure_numbers(n: dict) -> None:
    """Chiffres et tableau du chapitre 4 (mesure de l'exposition)."""
    import importlib.util
    proc = ROOT / "data" / "processed"
    spec = importlib.util.spec_from_file_location("expo", ROOT / "scripts" / "06_exposure_check.py")
    expo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expo)

    # Convention de date de SIM : corrélation des variations journalières avec T(J + k), fichier 2009.
    sim = pd.read_csv(ROOT / "data" / "raw" / "meteofrance_sim" / "QUOT_SIM2_2009.csv.gz", sep=";",
                      usecols=["LAMBX", "LAMBY", "DATE", "T", "TINF_H", "TSUP_H"]).sort_values(["LAMBX", "LAMBY", "DATE"])
    g = sim.groupby(["LAMBX", "LAMBY"])
    d = sim[["T", "TINF_H", "TSUP_H"]] - g[["T", "TINF_H", "TSUP_H"]].shift(1)
    for var, name in [("TINF_H", "Tinf"), ("TSUP_H", "Tsup")]:
        for k, lab in [(-1, "Lag"), (0, "Same"), (1, "Lead")]:
            dt = d["T"].groupby([sim.LAMBX, sim.LAMBY]).shift(-k)
            n[f"Conv{name}{lab}"] = f"{d[var].corr(dt):.2f}"

    # Nombre effectif d'années informatives (règle de la phase 2).
    saa = pd.read_parquet(ROOT / "data" / "interim" / "saa_cop_departements_long.parquet")
    pop = expo.wheat_population(saa)
    for first, key in [(2010, "NeffWheat"), (1959, "NeffWheatLong")]:
        suffix = "" if first == 2010 else f"_{first}"
        h = pd.read_parquet(proc / f"weather_dep_harvest_wheat{suffix}.parquet")
        _, ne = expo.exposure_table(h[h.dep_code.isin(pop)].copy(), "dd_32_remplissage")
        n[key] = f"{ne:.1f}"
        if first == 2010:   # règle de repli à la limite : sans 2025 (année provisoire)
            _, ne25 = expo.exposure_table(h[h.dep_code.isin(pop) & (h.annee != 2025)].copy(), "dd_32_remplissage")
            n["NeffWheatNoTwentyFive"] = f"{ne25:.2f}"
            n["NeffWheatExact"] = f"{ne:.2f}"
    m = pd.read_parquet(proc / "panel_mais_long.parquet")
    m = m[m.echantillon_principal & (m.modalite == "non_irrigue")]
    pairs = pd.read_parquet(proc / "panel_mais_long.parquet").pivot_table(index=["dep_code", "annee"], columns="modalite",
                                                                          values="log_rendement").dropna().index
    m = m.set_index(["dep_code", "annee"]).loc[lambda x: x.index.isin(pairs)].reset_index()
    # exposure_table retire les effets fixes par twoway_residuals, exact pour un panel équilibré ; ici 435 paires
    # pour 17 × 26 = 442 cases : N_eff est une approximation.
    by_year, ne = expo.exposure_table(m, "dd_32_ja")
    n["NeffMaize"] = f"{ne:.1f}"
    n["NeffMaizeShareTwoThousandThree"] = f"{100 * by_year.loc[2003, 'part_variance']:.0f}"

    # Tableau : chaleur de 2003 selon la mesure, départements de l'échantillon principal.
    mes = pd.read_csv(TAB / "phase4bis_q1_mesures_departement.csv", dtype={"dep_code": str})
    names = saa.drop_duplicates("dep_code").set_index("dep_code")["dep_libelle"]
    mes["name"] = mes.dep_code.map(names).str.replace(r"^\d+\w?\s*-\s*", "", regex=True)
    # Altitude moyenne des mailles (service IGN), pondérée par le masque maïs ou par la surface du département.
    alt = pd.read_parquet(proc / "cell_altitude.parquet")
    for wfile, wcol, col in [("weights_cell_dep_maize", "w_maize", "alt_maize"), ("weights_cell_dep_area", "w_area", "alt_area")]:
        w = pd.read_parquet(proc / f"{wfile}.parquet").merge(alt, on=["LAMBX", "LAMBY"]).dropna(subset=["altitude_moy_m"])
        mes[col] = mes.dep_code.map(w.groupby("dep_code").apply(lambda d: (d[wcol] * d.altitude_moy_m).sum() / d[wcol].sum()))
    n["ReliefAltCorr"] = f"{mes.ecart_surface_moins_masque_2003.corr(mes.alt_area - mes.alt_maize):.2f}"
    big = mes[mes.ecart_surface_moins_masque_2003 < -3]
    n["ReliefAltDiffMin"] = f"{(big.alt_area - big.alt_maize).min():.0f}"
    n["ReliefAltDiffMax"] = f"{(big.alt_area - big.alt_maize).max():.0f}"
    words = {4: "four", 5: "five", 6: "six", 7: "seven"}
    n["ReliefCount"] = words.get(len(big), str(len(big)))                          # écart > 3 °C·jour
    large = mes[mes.ecart_surface_moins_masque_2003 < -5]
    n["ReliefCountLarge"] = words.get(len(large), str(len(large)))                 # écart > 5 °C·jour
    n["ReliefGapSmallMin"] = f"{-big.ecart_surface_moins_masque_2003.max():.0f}"
    # Seul désaccord notable entre les deux masques maïs (2015-2017 contre 2008), été 2003 : le Rhône.
    rh = mes.set_index("dep_code").loc["69"]
    n["ReliefRhoneMaskGap"] = f"{rh.masque_2015_2017_2003 - rh.masque_2008_2003:.1f}"
    n["ReliefYonneGap"] = f"{mes.set_index('dep_code').loc['89', 'ecart_surface_moins_masque_2003']:.1f}"
    mes = mes.sort_values("ecart_surface_moins_masque_2003")
    rows = [f"{r.name} ({r.dep_code}) & {r.masque_2015_2017_2003:.1f} & {r.masque_2008_2003:.1f} & "
            f"{r.ponderation_surfacique_2003:.1f} & ${r.ecart_surface_moins_masque_2003:+.1f}$ & "
            f"{r.alt_maize:.0f} & {r.alt_area:.0f} \\\\"
            for r in mes.itertuples()]
    (OUT / "relief.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (reports/tables/phase4bis_q1_mesures_departement.csv)\n"
        "\\begin{tabular}{lrrrrrr}\n\\toprule\n"
        " & \\multicolumn{4}{c}{Degree-days $>32\\,^{\\circ}$C, July--August 2003} & \\multicolumn{2}{c}{Mean altitude (m)} \\\\\n"
        "\\cmidrule(lr){2-5}\\cmidrule(lr){6-7}\n"
        "Department & Mask 2015--17 & Mask 2008 & Dept.\\ area & Area $-$ mask & Maize mask & Dept.\\ area \\\\\n\\midrule\n"
        + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")


def spec_hashes(n: dict) -> None:
    """Empreintes SHA-256 des spécifications pré-enregistrées, vérifiées contre docs/decisions.md."""
    import hashlib
    journal = (ROOT / "docs" / "decisions.md").read_text()
    for phase, key in [("4", "Four"), ("5", "Five"), ("6", "Six"), ("4bis", "FourBis")]:
        h = hashlib.sha256((ROOT / "docs" / f"specification_phase{phase}.md").read_bytes()).hexdigest()
        if h not in journal:
            raise SystemExit(f"specification_phase{phase}.md ne correspond plus à l'empreinte consignée")
        n[f"Spec{key}Hash"] = h[:12]


def inference_tables(n: dict) -> None:
    """Tableaux du chapitre 6 : taille des tests sur chaque jeu de données, puissance (blé 2010-2025)."""
    lab = {"cluster_dep": "cluster_dep", "conley_200": "conley_200", "wcr_annee": "wcr_annee"}
    rows = []
    # Les libellés (nombre de départements, années) décrivent le plan de chaque échantillon et sont écrits à la
    # main, comme le dit l'annexe A ; les tailles viennent des CSV.
    sim = pd.read_csv(TAB / "phase4_simulation_inference.csv")
    s4 = sim[sim.beta_vrai == 0].set_index("inference")["taux_rejet_5pct"]
    rows.append(("Wheat, May--June heat, 83 depts, 2010--2025 (two-sided)", 16, int(sim.R.iloc[0]), s4))
    q2 = pd.read_csv(TAB / "phase4bis_q2_taille.csv").set_index("inference")
    rows.append(("Wheat, May--June heat, 83 depts, 1959--2025 (one-sided)", 67, int(q2.R.iloc[0]), q2["taille_5pct"]))
    m6 = pd.read_csv(TAB / "phase6_mais_taille.csv")
    m6r = m6[m6.variable_expliquee == "log_non_irrigue"].set_index("inference")
    rows.append(("Rainfed maize, 17 depts, 2010--2025 (two-sided; phase 6, dept.-area weather)", 16, int(m6r.R.iloc[0]), m6r["taille_5pct"]))
    m6g = m6[m6.variable_expliquee == "ecart_log"].set_index("inference")
    rows.append(("Maize gap, 17 depts, 2010--2025 (two-sided; phase 6, dept.-area weather)", 16, int(m6g.R.iloc[0]), m6g["taille_5pct"]))
    q1 = pd.read_csv(TAB / "phase4bis_q1_taille.csv").set_index("inference")
    rows.append(("Maize gap, 17 depts, 2000--2025 (one-sided)", 26, int(q1.R.iloc[0]), q1["taille_5pct"]))
    body = "\n".join(f"{name} & {G} & {R} & {100 * s['cluster_dep']:.1f} & {100 * s['conley_200']:.1f} & "
                      f"\\textbf{{{100 * s['wcr_annee']:.1f}}} \\\\" for name, G, R, s in rows)
    (OUT / "sizes.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py\n\\begin{tabular}{>{\\raggedright}p{5.6cm}rrrrr}\n\\toprule\n"
        "Data set and test & Years & $R$ & \\shortstack{Cluster\\\\dept.} & \\shortstack{Conley\\\\200 km} & "
        "\\shortstack{Bootstrap\\\\by year} \\\\\n\\midrule\n"
        + body + "\n\\bottomrule\n\\end{tabular}\n")
    allrows = pd.DataFrame({name: s for name, _, _, s in rows}).T * 100
    n["SizeDepMin"], n["SizeDepMax"] = f"{allrows.cluster_dep.min():.0f}", f"{allrows.cluster_dep.max():.0f}"
    n["SizeConleyMin"], n["SizeConleyMax"] = f"{allrows.conley_200.min():.0f}", f"{allrows.conley_200.max():.0f}"
    w = allrows.wcr_annee.sort_values()
    n["SizeWcrMin"], n["SizeWcrMaxButOne"], n["SizeWcrMax"] = f"{w.iloc[0]:.1f}", f"{w.iloc[-2]:.1f}", f"{w.iloc[-1]:.1f}"
    # Puissance (blé 2010-2025) : taux de rejet quand un vrai effet est ajouté.
    prow = []
    for b, s in sim.groupby("beta_vrai", sort=False):
        s = s.set_index("inference")["taux_rejet_5pct"]
        label = "0 (size)" if b == 0 else f"${100 * b:.1f}\\,\\%$ per degree-day"
        prow.append(f"{label} & {100 * s['cluster_dep']:.1f} & {100 * s['conley_200']:.1f} & {100 * s['wcr_annee']:.1f} \\\\")
    (OUT / "power.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4_simulation_inference.csv)\n\\begin{tabular}{lrrr}\n\\toprule\n"
        "True effect added & Cluster dept. & Conley 200 km & Bootstrap by year \\\\\n\\midrule\n"
        + "\n".join(prow) + "\n\\bottomrule\n\\end{tabular}\n")
    n["WheatPowerWCRDouble"] = f"{100 * sim[sim.beta_vrai.round(3) == -0.03].set_index('inference').loc['wcr_annee', 'taux_rejet_5pct']:.0f}"
    n["SimR"] = str(int(sim.R.iloc[0]))
    ex = pd.read_csv(TAB / "wcr_exemple_montecarlo.csv").set_index("inference")["taille_5pct"] * 100
    n["ExRegion"], n["ExCrOne"], n["ExWcr"] = (f"{ex[k]:.1f}" for k in ["cluster_region", "cluster_annee_cr1", "wcr_annee"])


def maize_tables(n: dict) -> None:
    """Tableaux et chiffres du chapitre 7 (résultats maïs, phase 4 bis)."""
    proc = ROOT / "data" / "processed"
    h = pd.read_csv(TAB / "phase4bis_q1_hypotheses.csv").set_index("hypothese")
    names = {"H1": "H1: gap, heat ($\\beta > 0$)", "réplication": "Replication 2000--2009: gap, heat",
             "H2a": "H2a: gap, soil moisture ($\\delta < 0$)", "H2b": "H2b: rainfed yield, heat ($< 0$)",
             "H2c": "H2c: irrigated yield, heat ($< 0$)", "H3": "H3: gap, heat $\\times$ crisis days ($< 0$)"}
    rows = []
    for k, label in names.items():
        r = h.loc[k]
        eff = "" if k in ("H2a", "H3") else f"${r.effet_pct_par_unite:+.2f}$"
        holm = "---" if pd.isna(r.p_holm) else pv(r.p_holm)
        rows.append(f"{label} & ${r.estimation:+.4f}$ & {eff} & {pv(r.p_unilaterale)} & {holm} & {pv(r.p_cluster_dep)} & "
                    f"{int(r.n)} & {r.annees.replace('-', '--')} \\\\")
    (OUT / "maize_hyp.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4bis_q1_hypotheses.csv)\n"
        "\\begin{tabular}{>{\\raggedright}p{4.6cm}rrrrrrr}\n\\toprule\n"
        "Hypothesis & Estimate & \\% per DD & \\shortstack{$p$ boot.\\\\one-sided} & \\shortstack{$p$\\\\Holm} & "
        "\\shortstack{$p$ clust.\\\\dept.} & $n$ & Years \\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
    n["QoneSwi"] = f"{h.loc['H2a', 'estimation']:.2f}"
    n["QoneHthreeEst"] = f"{h.loc['H3', 'estimation']:.4f}"
    n["QoneHthreeN"] = str(int(h.loc["H3", "n"]))
    n["QoneHthreePright"] = pv(1 - h.loc["H3", "p_unilaterale"])

    rob = pd.read_csv(TAB / "phase4bis_q1_robustesse.csv")
    rob = pd.concat([rob, pd.read_csv(TAB / "phase4bis_q1_r9_masque2008.csv")], ignore_index=True)
    en = {"A1": "Main specification", "Q1-R1": "38 departments (all quality statuses)", "Q1-R2": "2010--2025 only",
          "Q1-R3": "Weather weighted by department area", "Q1-R4": "Threshold 30\\,$^{\\circ}$C", "Q1-R5": "July only",
          "Q1-R6": "Unweighted", "Q1-R7": "Without 2025 (provisional)", "Q1-R8": "Without 2003",
          "Q1-R9": "2008 maize mask (added later)"}
    rrows = [f"{en[r.specification.split(' ', 1)[0]]} & ${r.estimation:+.4f}$ & ${r.effet_pct_par_unite:+.2f}$ & "
             f"{pv(r.p_wcb_annee_unilateral_droite)} & {int(r.n)} & "
             f"{int(r.n_departements) if pd.notna(r.n_departements) else n['MaizeMainDeps']} \\\\" for r in rob.itertuples()]
    (OUT / "maize_rob.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4bis_q1_robustesse.csv, phase4bis_q1_r9_masque2008.csv)\n"
        "\\begin{tabular}{lrrrrr}\n\\toprule\n"
        "Specification & $\\hat\\beta$ & \\% per DD & $p$ boot.\\ one-sided & $n$ & Depts \\\\\n\\midrule\n"
        + "\n".join(rrows) + "\n\\bottomrule\n\\end{tabular}\n")
    sig = (rob.p_wcb_annee_unilateral_droite < 0.05).sum()
    n["QoneRobN"], n["QoneRobSig"], n["QoneRobPos"] = str(len(rob)), str(int(sig)), str(int((rob.estimation > 0).sum()))
    r2 = rob[rob.specification.str.startswith("Q1-R2")].iloc[0]
    n["QoneRecentPct"] = pct(r2.effet_pct_par_unite)
    n["QoneAllDepsPct"] = pct(rob[rob.specification.str.startswith("Q1-R1")].iloc[0].effet_pct_par_unite)

    ex = pd.read_csv(TAB / "phase4bis_q1_exploratoire.csv")
    b = ex[ex.analyse.str.startswith("beta")].pivot_table(index="periode", columns="mesure", values="estimation")
    order = ["2000-2025", "2000-2009", "2010-2025", "sans 2003", "2000-2009 sans 2003"]
    lab = {"2000-2025": "2000--2025", "2000-2009": "2000--2009", "2010-2025": "2010--2025", "sans 2003": "Without 2003",
           "2000-2009 sans 2003": "2000--2009 without 2003"}
    mrows = [f"{lab[p]} & ${b.loc[p, 'masque maïs']:+.4f}$ & ${b.loc[p, 'pondération surfacique']:+.4f}$ \\\\" for p in order]
    (OUT / "maize_measure.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4bis_q1_exploratoire.csv)\n"
        "\\begin{tabular}{lrr}\n\\toprule\nPeriod & Maize mask & Department area \\\\\n\\midrule\n"
        + "\n".join(mrows) + "\n\\bottomrule\n\\end{tabular}\n")
    n["AreaEarly"], n["MaskEarly"] = f"{b.loc['2000-2009', 'pondération surfacique']:.4f}", f"{b.loc['2000-2009', 'masque maïs']:.4f}"
    n["AreaRecent"], n["MaskRecent"] = f"{b.loc['2010-2025', 'pondération surfacique']:.4f}", f"{b.loc['2010-2025', 'masque maïs']:.4f}"
    comp = ex[ex.analyse.str.startswith("part")].iloc[0]
    n["CompEst"], n["CompP"] = f"{comp.estimation:.4f}", f"{comp.p_cluster_annee:.2f}"

    val = pd.read_csv(TAB / "phase4bis_q1_valorisation.csv")
    vrows = [f"{int(r.annee)} & {r.ecart_dd32_moyen_pondere:+.1f} & {r.surface_irriguee_ha / 1e3:.0f} & "
             f"{r.quintaux_estimation / 1e6:.2f} & {r.prix_eur_q:.1f} & {r.millions_eur_estimation:.0f} & "
             f"{r.millions_eur_ic90_bas:.0f}--{r.millions_eur_ic90_haut:.0f} \\\\" for r in val.itertuples()]
    (OUT / "valuation.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4bis_q1_valorisation.csv)\n"
        "\\begin{tabular}{lrrrrrr}\n\\toprule\n"
        "Summer & \\shortstack{Heat vs.\\\\normal (DD)} & \\shortstack{Irrigated\\\\area (kha)} & \\shortstack{Quintals\\\\(millions)} & "
        "\\shortstack{Price\\\\(EUR/q)} & \\shortstack{Value\\\\(M EUR)} & \\shortstack{90\\,\\% range\\\\(M EUR)} \\\\\n\\midrule\n"
        + "\n".join(vrows).replace("+", "$+$") + "\n\\bottomrule\n\\end{tabular}\n")

    # Variante de la valorisation : facteur appliqué au rendement irrigué, Y_I (1 - exp(-beta * écart)), été 2003.
    import numpy as np
    beta = h.loc["H1", "estimation"]
    mm = pd.read_parquet(proc / "panel_mais_long.parquet")
    mm = mm[mm.echantillon_principal]
    irr = mm[mm.modalite == "irrigue"][["dep_code", "annee", "surface_ha", "rendement_q_ha", "dd_32_ja"]]
    non = mm[mm.modalite == "non_irrigue"][["dep_code", "annee", "rendement_q_ha"]]
    pp = irr.merge(non, on=["dep_code", "annee"], suffixes=("_irr", "_non"))
    pp["d"] = pp.dd_32_ja - pp.groupby("dep_code").dd_32_ja.transform("mean")
    y3 = pp[pp.annee == 2003]
    q_non = (y3.surface_ha * y3.rendement_q_ha_non * (np.exp(beta * y3.d) - 1)).sum()
    q_irr = (y3.surface_ha * y3.rendement_q_ha_irr * (1 - np.exp(-beta * y3.d))).sum()
    n["ValAltPct"] = f"{100 * (q_irr / q_non - 1):.0f}"
    if abs(q_non / 1e6 - pd.read_csv(TAB / "phase4bis_q1_valorisation.csv").set_index("annee").loc[2003, "quintaux_estimation"] / 1e6) > 1e-6:
        raise SystemExit("valorisation 2003 non reproduite")

    ac = pd.read_csv(TAB / "diag_autocorr_residus.csv").set_index("modele")["rho_ar1"]
    n["ArMaize"], n["ArWheat"] = f"{ac.filter(like='maïs').iloc[0]:.2f}", f"{ac.filter(like='blé').iloc[0]:.2f}"
    ww = mm.pivot_table(index=["dep_code", "annee"], columns="modalite", values="log_rendement").dropna()
    ww["gap"] = ww.irrigue - ww.non_irrigue
    ww = ww.join(mm[mm.modalite == "irrigue"].set_index(["dep_code", "annee"])[["dd_32_ja", "surface_ref_ha"]])
    ww["gap_dev"] = ww.gap - ww.groupby(level=0).gap.transform("mean")
    ww["heat_dev"] = ww.dd_32_ja - ww.groupby(level=0).dd_32_ja.transform("mean")
    w3 = ww.xs(2003, level=1)
    n["GapObsTwoThousandThree"] = f"{np.average(w3.gap_dev, weights=w3.surface_ref_ha):.3f}"
    n["GapPredTwoThousandThree"] = f"{beta * np.average(w3.heat_dev, weights=w3.surface_ref_ha):.3f}"
    # Surestimation de la formule linéaire en 2003 (écart prédit / écart observé - 1), citée au §7.7.
    obs3, pred3 = np.average(w3.gap_dev, weights=w3.surface_ref_ha), beta * np.average(w3.heat_dev, weights=w3.surface_ref_ha)
    n["ValOverPct"] = f"{100 * (pred3 / obs3 - 1):.0f}"

    # Validité externe : part de la surface de la population couverte par l'échantillon principal.
    dd = pd.read_parquet(proc / "panel_mais_long.parquet").drop_duplicates("dep_code")
    n["MainShareArea"] = f"{100 * dd[dd.echantillon_principal].surface_ref_ha.sum() / dd.surface_ref_ha.sum():.0f}"
    n["IrrShareOfRainfedSens"] = f"{100 * h.loc['H2c', 'estimation'] / h.loc['H2b', 'estimation']:.0f}"

    # Description : rendements moyens et écart médian, échantillon principal (paires).
    m = pd.read_parquet(proc / "panel_mais_long.parquet")
    m = m[m.echantillon_principal]
    w = m.pivot_table(index=["dep_code", "annee"], columns="modalite", values="rendement_q_ha").dropna()
    n["YieldIrr"], n["YieldRain"] = f"{w.irrigue.mean():.0f}", f"{w.non_irrigue.mean():.0f}"
    n["GapMedianPct"] = f"{100 * ((w.irrigue / w.non_irrigue).median() - 1):.0f}"
    n["GapNotAboveCount"] = str(int((w.irrigue <= w.non_irrigue).sum()))     # paires où l'irrigué ne dépasse pas
    n["GapBelowCount"] = str(int((w.irrigue < w.non_irrigue).sum()))
    # Part des paires de l'échantillon principal issues des années exploratoires (2010-2025, phase 6).
    years = w.index.get_level_values(1)
    n["ExploPairs"], n["ExploSharePct"] = str(int((years >= 2010).sum())), f"{100 * (years >= 2010).mean():.0f}"


def wheat_tables(n: dict) -> None:
    """Tableaux et chiffres du chapitre 8 (blé, phases 4 et 4 bis)."""
    p4 = pd.read_csv(TAB / "phase4_principal.csv")
    rows = []
    for spec in ["M1", "M2"]:
        r = p4[(p4.specification == spec) & (p4.terme == "dd_32_remplissage")].iloc[0]
        rows.append(f"{spec} & ${r.estimation:+.4f}$ & ${r.effet_pct_par_unite:+.2f}$ & {pv(r.p_cluster_dep)} & "
                    f"{pv(r.p_conley)} & {pv(r.p_wcb_annee)} & {pv(r.p_wcb_annee_unilateral_gauche)} & {int(r.n)} \\\\")
    (OUT / "wheat_short.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4_principal.csv)\n\\begin{tabular}{lrrrrrrr}\n\\toprule\n"
        "Model & $\\hat\\beta_2$ & \\% per DD & \\shortstack{$p$ clust.\\\\dept.} & \\shortstack{$p$\\\\Conley} & "
        "\\shortstack{$p$ boot.\\\\two-sided} & \\shortstack{$p$ boot.\\\\one-sided} & $n$ \\\\\n\\midrule\n"
        + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
    h2 = pd.read_csv(TAB / "phase4_h2.csv")
    n["WheatHtwoPwcr"] = f"{h2[h2.test.str.contains('WCR')].p.iloc[0]:.2f}"
    n["WheatHtwoPdep"] = pv(h2[h2.test.str.contains("cluster d|cluster dép", regex=True)].p.iloc[0])
    rob = pd.read_csv(TAB / "phase4_robustesse.csv")
    pre = rob[rob.specification.str.match(r"R([1-8]|10) ")]       # R9 (Conley 300 km) ne change pas le coefficient
    # Ajoutées après les premières estimations : R11 à R14. R14 (classes de température) n'a pas de coefficient
    # dd_32 comparable ; elle est exclue du décompte, et le texte le dit (08_wheat.tex).
    added = rob[rob.specification.str.match(r"R1[1-3] ")]
    n["WheatRobPreTot"], n["WheatRobPreNeg"] = str(len(pre)), str(int((pre.estimation < 0).sum()))
    n["WheatRobAddTot"], n["WheatRobAddNeg"] = str(len(added)), str(int((added.estimation < 0).sum()))
    b_r3 = rob[rob.specification.str.startswith("R3 ")].estimation.iloc[0]   # R3 : sans 2025
    n["WheatNoTwentyFivePct"] = pct(-100 * (math.exp(b_r3) - 1))
    loyo = pd.read_csv(TAB / "phase4_loyo.csv")
    n["LoyoNeg"], n["LoyoTot"] = str(int((loyo.estimation < 0).sum())), str(len(loyo))

    q2 = pd.read_csv(TAB / "phase4bis_q2_hypotheses.csv")
    lrows = []
    for r in q2.itertuples():
        label = "All years, 1959--2025 (M3)" if r.periode == "1959-2025" else f"Slope {r.periode.replace('-', '--')}"
        lrows.append(f"{label} & ${r.estimation:+.4f}$ & ${r.effet_pct_par_unite:+.2f}$ & {pv(r.p_wcb_annee)} & "
                     f"{pv(r.p_wcb_annee_unilateral_gauche)} \\\\")
    q2r = pd.read_csv(TAB / "phase4bis_q2_robustesse.csv")
    en = {"B1": "Main (M3)", "Q2-R1": "+ regional linear trends", "Q2-R2": "Without 2025 (provisional)",
          "Q2-R3": "1968--2025 (no missing yields)", "Q2-R4": "Single department effect", "Q2-R5": "Threshold 30\\,$^{\\circ}$C"}
    # Robustesses : seule la p unilatérale (règle de décision) est rapportée ; colonne bilatérale vide.
    rrows = [f"{en[r.specification.split(' ', 1)[0]]} & ${r.estimation:+.4f}$ & ${r.effet_pct_par_unite:+.2f}$ & --- & "
             f"{pv(r.p_wcb_annee_unilateral_gauche)} \\\\" for r in q2r.itertuples()]
    (OUT / "wheat_long.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4bis_q2_hypotheses.csv, phase4bis_q2_robustesse.csv)\n"
        "\\begin{tabular}{lrrrr}\n\\toprule\n& $\\hat\\beta_2$ & \\% per DD & $p$ boot.\\ two-sided & $p$ boot.\\ one-sided \\\\\n"
        "\\midrule\n\\multicolumn{5}{l}{\\emph{Heat slope, M3, and slopes by sub-period}} \\\\\n" + "\n".join(lrows)
        + "\n\\midrule\n\\multicolumn{5}{l}{\\emph{Robustness of the main slope}} \\\\\n" + "\n".join(rrows)
        + "\n\\bottomrule\n\\end{tabular}\n")
    rq = q2r[q2r.specification.str.startswith("Q2-")]                # robustesses seules (sans la ligne B1)
    n["QtwoRobNeg"], n["QtwoRobTot"] = str(int((rq.estimation < 0).sum())), str(len(rq))
    n["QtwoRobSig"] = str(int((rq.p_wcb_annee_unilateral_gauche < 0.05).sum()))
    r2 = rq[rq.specification.str.startswith("Q2-R2")].iloc[0]
    n["QtwoNoTwentyFiveP"], n["QtwoNoTwentyFivePtwo"] = pv(r2.p_wcb_annee_unilateral_gauche), pv(r2.p_wcb_annee)
    sl = q2[q2.periode != "1959-2025"].set_index("periode")["effet_pct_par_unite"]
    n["SlopeA"], n["SlopeB"], n["SlopeC"] = (pct(-sl[k]) for k in ["1959-1981", "1982-2003", "2004-2025"])


def forecast_tables(n: dict) -> None:
    """Tableaux et chiffres du chapitre 9 (prévision, phases 5 et 6)."""
    f = pd.read_csv(TAB / "phase5_synthese_vs_B0.csv")
    model = {"B1": "B1 (trend)", "L1": "OLS (M1 variables)", "RIDGE": "Ridge", "RF": "Random forest", "GBM": "Gradient boosting"}
    var = {"principale_2010": "Train from 2010", "longue_1990": "Train from 1990"}
    date = {"juin": "1 June", "juillet": "1 July"}
    rows = []
    for v in ["principale_2010", "longue_1990"]:
        rows.append(f"\\multicolumn{{5}}{{l}}{{\\emph{{{var[v]}}}}} \\\\")
        for d in ["juin", "juillet"]:
            for mname in ["B1", "L1", "RIDGE", "RF", "GBM"]:
                r = f[(f.variante == v) & (f.date == d) & (f.modele == mname)].iloc[0]
                excl = (r.ic95_bas > 0) or (r.ic95_haut < 0)
                rows.append(f"{date[d]} & {model[mname]} & ${100 * r.skill_moyen_vs_B0:+.0f}$ & "
                            f"[${1000 * r.ic95_bas:+.1f}$, ${1000 * r.ic95_haut:+.1f}$]{'$^*$' if excl else ''} & "
                            f"{int(r.annees_meilleur_que_B0)}/10 \\\\")
    (OUT / "forecast.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase5_synthese_vs_B0.csv)\n\\begin{tabular}{llrrr}\n\\toprule\n"
        "Date & Model & \\shortstack{Skill vs.\\\\B0 (\\%)} & \\shortstack{95\\,\\% interval of MSE\\\\difference ($\\times 10^3$)} & "
        "\\shortstack{Years better\\\\than B0} \\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
    b1 = pd.read_csv(TAB / "phase5_synthese.csv")
    rf = b1[(b1.variante == "principale_2010") & (b1.modele == "RF") & (b1.date == "juillet")].iloc[0]
    n["RfVsBoneSkill"] = f"{100 * rf.skill_moyen_vs_B1:.0f}"
    b0 = b1[(b1.variante == "principale_2010") & (b1.modele == "B0") & (b1.date == "juillet")].iloc[0]
    n["BzeroBeatsBone"] = str(int(b0.annees_meilleur_que_B1))
    nd = pd.read_csv(TAB / "phase6_ndvi_synthese.csv")
    nrows = []
    for d in ["juin", "juillet"]:
        for mname in ["RIDGE", "RF", "GBM"]:
            g = nd[(nd.date == d) & (nd.modele == mname)].set_index("comparaison")
            same, vs0 = g.loc["vs_meme_modele_sans_ndvi"], g.loc["vs_B0"]
            excl = (same.ic95_bas > 0) or (same.ic95_haut < 0)   # même convention que forecast.tex
            nrows.append(f"{date[d]} & {model[mname]} & ${100 * same.skill:+.1f}$ & "
                         f"[${1000 * same.ic95_bas:+.2f}$, ${1000 * same.ic95_haut:+.2f}$]{'$^*$' if excl else ''} & "
                         f"${100 * vs0.skill:+.0f}$ \\\\")
    (OUT / "ndvi.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase6_ndvi_synthese.csv)\n\\begin{tabular}{llrrr}\n\\toprule\n"
        "Date & Model & \\shortstack{Gain from NDVI vs.\\\\same model (\\%)} & \\shortstack{95\\,\\% interval of MSE\\\\difference ($\\times 10^3$)} & "
        "\\shortstack{Skill vs.\\\\B0 (\\%)} \\\\\n\\midrule\n" + "\n".join(nrows) + "\n\\bottomrule\n\\end{tabular}\n")
    s = nd[nd.comparaison == "vs_meme_modele_sans_ndvi"]
    n["NdviGainMin"], n["NdviGainMax"] = f"{100 * s.skill.min():.1f}", f"{100 * s.skill.max():.1f}"
    n["NdviSig"], n["NdviTot"] = str(int((s.ic95_haut < 0).sum())), str(len(s))
    n["NdviBeatsBzero"] = str(int((nd[nd.comparaison == "vs_B0"].skill > 0).sum()))


def appendix_tables(n: dict) -> None:
    """Annexes : versions des environnements, nombre de tests, validation des degrés-jours, robustesses complètes."""
    import json
    import re
    import subprocess

    import numpy as np

    from atlas.degree_days import double_sine, single_sine

    # Versions (fichiers de verrouillage).
    lock = json.loads((ROOT / "renv.lock").read_text())
    n["VerR"], n["VerFixest"] = lock["R"]["Version"], lock["Packages"]["fixest"]["Version"]
    n["VerRepoDate"] = re.search(r"(\d{4}-\d{2}-\d{2})", lock["R"]["Repositories"][0]["URL"]).group(1)
    uvlock = (ROOT / "uv.lock").read_text()
    for pkg, key in [("pandas", "VerPandas"), ("scikit-learn", "VerSklearn"), ("duckdb", "VerDuckdb"), ("geopandas", "VerGeopandas")]:
        n[key] = re.search(rf'name = "{pkg}"\nversion = "([^"]+)"', uvlock).group(1)
    n["VerUvDate"] = re.search(r'exclude-newer = "(\d{4}-\d{2}-\d{2})', (ROOT / "pyproject.toml").read_text()).group(1)
    out = subprocess.run(["uv", "run", "pytest", "--collect-only", "-q"], cwd=ROOT, capture_output=True, text=True).stdout
    n["TestCount"] = re.search(r"(\d+) tests? collected", out).group(1)
    # Les contrôles d'empreinte (un test par fichier brut) gonflent le total : on les compte à part.
    n["TestIntegrity"] = str(out.count("test_manifest.py::test_raw_file_matches_manifest"))
    n["TestLogic"] = str(int(n["TestCount"]) - int(n["TestIntegrity"]))
    n["ManifestFiles"] = f"{len(pd.read_csv(ROOT / 'docs' / 'manifest_raw.csv')):,}"

    # Degrés-jours : formule fermée contre intégration numérique sur une grille aléatoire de cas.
    rng = np.random.default_rng(20261010)
    tmin = rng.uniform(-10, 30, 500)
    tmax = tmin + rng.uniform(0.5, 20, 500)
    b = rng.uniform(0, 40, 500)
    t = np.linspace(0, 2 * np.pi, 100_000, endpoint=False)
    num = np.array([np.maximum((lo + hi) / 2 + (hi - lo) / 2 * np.sin(t) - th, 0).mean() for lo, hi, th in zip(tmin, tmax, b)])
    n["DdCases"] = str(len(b))
    err = np.abs(single_sine(tmin, tmax, b) - num).max()
    exp = int(np.floor(np.log10(err)))
    n["DdMaxErr"] = f"{err / 10 ** exp:.1f} \\times 10^{{{exp}}}"      # à utiliser en mode mathématique
    n["DdDoubleSame"] = "yes" if np.allclose(double_sine(tmin, tmax, tmin, b), single_sine(tmin, tmax, b)) else "no"

    # Robustesses complètes, blé 2010-2025 (phase 4), avec les trois inférences.
    en4 = {"M1": "M1 (reference)", "R1": "Unweighted", "R2": "Without 84, 30, 48", "R3": "Without 2025",
           "R4": "85 departments (status 1 and 2)", "R5": "Threshold 30\\,$^{\\circ}$C", "R6": "Department-area weather",
           "R7": "+ regional linear trends", "R8": "Long panel 1990--2025", "R9": "Conley 300 km",
           "R10": "Window May--July", "R11": "Window shifted $-2$ weeks", "R12": "Window shifted $+2$ weeks",
           "R13": "Without mountain departments", "R14": "Temperature bins"}
    rob = pd.read_csv(TAB / "phase4_robustesse.csv")

    def fmt(x):
        return "---" if pd.isna(x) else pv(x)
    rows = []
    for r in rob.itertuples():
        code = r.specification.split(" ", 1)[0]
        label = en4.get(code, r.specification)
        term = r.terme.replace("_", "\\_")
        rows.append(f"{code if code.startswith('R') else ''} & {label} & \\texttt{{{term}}} & ${r.estimation:+.4f}$ & "
                    f"{fmt(r.p_cluster_dep)} & {fmt(r.p_conley)} & {fmt(r.p_wcb_annee)} \\\\")
    (OUT / "rob_wheat_full.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py (phase4_robustesse.csv)\n\\begin{tabular}{llllrrr}\n\\toprule\n"
        "& Variant & Term & $\\hat\\beta$ & $p$ clust.\\ dept. & $p$ Conley & $p$ boot.\\ (two-sided) \\\\\n\\midrule\n"
        + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

    # Robustesses complètes, maïs (phase 4 bis), avec les trois inférences.
    mr = pd.concat([pd.read_csv(TAB / "phase4bis_q1_robustesse.csv"), pd.read_csv(TAB / "phase4bis_q1_r9_masque2008.csv")])
    enm = {"A1": "Main", "Q1-R1": "38 departments", "Q1-R2": "2010--2025", "Q1-R3": "Department-area weather",
           "Q1-R4": "Threshold 30\\,$^{\\circ}$C", "Q1-R5": "July only", "Q1-R6": "Unweighted", "Q1-R7": "Without 2025",
           "Q1-R8": "Without 2003", "Q1-R9": "2008 mask (blocks)"}
    mrows = [f"{enm[r.specification.split(' ', 1)[0]]} & ${r.estimation:+.4f}$ & {fmt(r.p_cluster_dep)} & {fmt(r.p_conley)} & "
             f"{fmt(r.p_wcb_annee)} & {fmt(r.p_wcb_annee_unilateral_droite)} \\\\" for r in mr.itertuples()]
    (OUT / "rob_maize_full.tex").write_text(
        "% GÉNÉRÉ par scripts/26_tables_memoire.py\n\\begin{tabular}{lrrrrr}\n\\toprule\n"
        "Variant & $\\hat\\beta$ & $p$ clust.\\ dept. & $p$ Conley & $p$ boot.\\ two-sided & $p$ boot.\\ one-sided \\\\\n\\midrule\n"
        + "\n".join(mrows) + "\n\\bottomrule\n\\end{tabular}\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    n = {}

    # --- Q1, maïs (phase 4 bis) -----------------------------------------------------
    h = pd.read_csv(TAB / "phase4bis_q1_hypotheses.csv").set_index("hypothese")
    n["QoneBeta"] = f"{h.loc['H1', 'estimation']:.4f}"
    n["QonePct"] = pct(h.loc["H1", "effet_pct_par_unite"])
    n["QoneP"] = pv(h.loc["H1", "p_unilaterale"])
    n["QoneN"] = str(int(h.loc["H1", "n"]))
    n["QoneReplPct"] = pct(h.loc["réplication", "effet_pct_par_unite"])
    n["QoneReplP"] = pv(h.loc["réplication", "p_unilaterale"])
    # Diagnostics D1 (puissance de H1) et D2 (taille et puissance de la réplication), déclarés avant calcul.
    pw = pd.read_csv(TAB / "phase4bis_q1_puissance.csv")
    def rate(diag, beta):
        return pw[pw.diagnostic.str.startswith(diag) & (pw.beta_vrai.round(3) == beta)].taux_rejet_5pct.iloc[0]
    n["PowerCheckSize"] = f"{100 * rate('D1', 0):.1f}"
    n["PowerHalf"], n["PowerFull"] = f"{100 * rate('D1', 0.008):.0f}", f"{100 * rate('D1', 0.016):.0f}"
    n["ReplSize"], n["ReplPower"] = f"{100 * rate('D2', 0):.1f}", f"{100 * rate('D2', 0.011):.0f}"
    # Analyses E1-E4 issues de la relecture simulée (R/21_q1_revue.R), déclarées avant calcul.
    ci = pd.read_csv(TAB / "phase4bis_q1_revue_intervalles.csv")
    def bound(model, level, side):
        b = ci[ci.modele.str.startswith(model) & (ci.niveau == level)][side].iloc[0]
        return 100 * (math.exp(b) - 1)
    n["CiNinetyLow"], n["CiNinetyHigh"] = pct(bound("A1", 0.90, "borne_inf"), 2), pct(bound("A1", 0.90, "borne_sup"), 1)
    n["CiNinetyFiveLow"], n["CiNinetyFiveHigh"] = pct(bound("A1", 0.95, "borne_inf"), 2), pct(bound("A1", 0.95, "borne_sup"), 1)
    # L'intervalle du blé doit porter sur le beta de M1 (phase 4, 83 départements), pas sur celui de R4.
    m1_est = pd.read_csv(TAB / "phase4_principal.csv").query("specification == 'M1' and terme == 'dd_32_remplissage'")
    if abs(ci[ci.modele.str.startswith("M1")].estimation.iloc[0] - m1_est.estimation.iloc[0]) > 1e-12:
        raise SystemExit("l'intervalle E1 du blé ne porte pas sur le beta de M1")
    n["WheatCiLow"], n["WheatCiHigh"] = pct(bound("M1", 0.95, "borne_inf")), pct(bound("M1", 0.95, "borne_sup"))
    dep = pd.read_csv(TAB / "phase4bis_q1_revue_departements.csv")
    loo, relief = dep[dep.n_departements == 16], dep[dep.n_departements == 11].iloc[0]
    n["LooMinPct"], n["LooMaxPct"] = pct(100 * (math.exp(loo.estimation.min()) - 1)), pct(100 * (math.exp(loo.estimation.max()) - 1))
    n["LooSig"] = str(int((loo.p_wcb_annee_unilateral_droite < 0.05).sum()))
    n["NoReliefPct"], n["NoReliefP"] = pct(relief.effet_pct_par_unite), pv(relief.p_wcb_annee_unilateral_droite)
    hum = pd.read_csv(TAB / "phase4bis_q1_revue_humidite.csv")
    n["NoSwiPct"], n["NoSwiP"] = pct(hum.effet_pct_par_unite.iloc[0]), pv(hum.p_wcb_annee_unilateral_droite.iloc[0])
    n["PetPct"], n["PetP"] = pct(hum.effet_pct_par_unite.iloc[1]), pv(hum.p_wcb_annee_unilateral_droite.iloc[1])
    n["CorrPet"] = f"{hum.correlation_intra_dd32_bilan.iloc[0]:.2f}"
    dec = pd.read_csv(TAB / "phase4bis_q1_revue_decennies.csv")
    n["DecDiff"], n["DecDiffP"] = f"{dec.estimation.iloc[0]:.4f}", f"{dec.p_wcb_annee.iloc[0]:.2f}"
    n["DecDiffNoThree"], n["DecDiffNoThreeP"] = f"{dec.estimation.iloc[1]:.4f}", f"{dec.p_wcb_annee.iloc[1]:.2f}"
    # Vérification Q1-E : chaleur recalculée avec E-OBS, déclarée avant calcul, hors du tableau des robustesses.
    qe = pd.read_csv(TAB / "phase4bis_q1_eobs.csv").iloc[0]
    n["EobsPct"], n["EobsP"] = pct(qe["effet_pct_par_unite"]), pv(qe["p_wcb_annee_unilateral_droite"])
    n["EobsCorr"] = f"{qe['correlation_eobs_sim']:.2f}"
    # Analyses complémentaires (R/22, scripts/28-29), déclarées avant calcul, exploratoires.
    it = pd.read_csv(TAB / "phase7_interactions.csv")
    n["RelInter"], n["RelInterP"] = f"{it.estimation.iloc[0]:.4f}", pv(it.p_wcb_annee.iloc[0])
    n["IrrInterP"] = pv(it.p_wcb_annee.iloc[2])
    ens = pd.read_csv(TAB / "phase7_ensilage.csv").iloc[0]
    n["SilageShare"], n["SilageP"] = pct(100 * ens.moyenne_part, 0), pv(ens.p_wcb_annee_unilateral_droite)
    inf = pd.read_csv(TAB / "phase7_inferences.csv").set_index("specification")
    n["DmlBeta"] = f"{inf.loc[inf.index.str.startswith('G8')].estimation.iloc[0]:.4f}"
    n["DmlP"] = pv(inf.loc[inf.index.str.startswith("G8")].p_wcb_annee_unilateral_droite.iloc[0])
    n["CvThreeP"] = pv(inf.loc[inf.index.str.startswith("G9a")].p_unilateral_droite.iloc[0])
    n["RiP"] = pv(inf.loc[inf.index.str.startswith("G9b")].p_unilateral_droite.iloc[0])
    sz = pd.read_csv(TAB / "phase7_tailles.csv").set_index("diagnostic").taux * 100
    n["WithinYearSize"] = pct(sz[sz.index.str.startswith("G3a")].iloc[0])
    n["HtwobSize"] = pct(sz[sz.index.str.contains("H2b")].iloc[0])
    n["HtwocSize"] = pct(sz[sz.index.str.contains("H2c")].iloc[0])
    n["ConleyFixedPct"] = pct(sz[sz.index.str.startswith("G9c")].iloc[0], 0)
    lv = pd.read_csv(TAB / "phase7_levier_annees.csv")
    l03 = lv[lv.annee == 2003].set_index("periode")
    n["LevThree"], n["LevThreeEarly"] = pct(100 * l03.loc["2000-2025", "part_sxx"], 0), pct(100 * l03.loc["2000-2009", "part_sxx"], 0)
    n["NeffLevAll"], n["NeffLevEarly"] = pct(l03.loc["2000-2025", "n_eff_periode"]), pct(l03.loc["2000-2009", "n_eff_periode"])
    g6 = pd.read_csv(TAB / "phase7_pentes_departements.csv")
    n["EbTau"], n["EbQp"] = f"{g6.tau.iloc[0]:.4f}", pv(g6.p_Q.iloc[0])
    n["EbMin"], n["EbMax"] = f"{g6.pente_retrecie.min():.3f}", f"{g6.pente_retrecie.max():.3f}"
    n["EbCorIrr"], n["EbCorAlt"] = f"{g6.cor_retrecie_part_irr.iloc[0]:.2f}", f"{g6.cor_retrecie_ecart_alt.iloc[0]:.2f}"
    n["ForestP"] = pv(pd.read_csv(TAB / "phase7_foret_causale.csv").p_differential.iloc[0])
    eo = pd.read_csv(TAB / "phase7_eolien.csv")
    n["WindIrrPct"], n["WindIrrP"] = pct(eo.effet_pct_par_unite.iloc[0], 2), pv(eo.p_wcb_annee.iloc[0])
    n["WindMinP"] = pv(eo.p_wcb_annee.iloc[1:].min())
    cf = pd.read_csv(TAB / "phase7_prevision_conforme.csv")
    cf = cf[(cf.variante == "principale_2010") & (cf.modele != "B1")]
    n["ConfCovMin"], n["ConfCovMax"] = pct(100 * cf.couverture_moyenne.min(), 0), pct(100 * cf.couverture_moyenne.max(), 0)
    vb = pd.read_csv(TAB / "phase7_prevision_vs_B0.csv")
    trees = vb[vb.modele.isin(["RF_B0", "GBM_B0"])]
    n["BzeroTreeMin"], n["BzeroTreeMax"] = pct(100 * trees.skill_vs_B0.min(), 0), pct(100 * trees.skill_vs_B0.max(), 0)
    n["BzeroTreeSig"] = str(int((trees.ic95_haut < 0).sum()))
    n["EobsSdEffect"] = pct(100 * (math.exp(qe["estimation"] * qe["sd_intra_eobs"]) - 1), 1)
    n["SimSdEffect"] = pct(100 * (math.exp(h.loc["H1", "estimation"] * qe["sd_intra_sim"]) - 1), 1)
    n["QoneReplPtwo"] = f"{h.loc['réplication', 'p_wcb_annee']:.2f}"
    n["QoneRainfedPct"] = pct(-h.loc["H2b", "effet_pct_par_unite"])
    n["QoneIrrigatedPct"] = pct(-h.loc["H2c", "effet_pct_par_unite"])
    n["QoneRatio"] = pct(h.loc["H2b", "estimation"] / h.loc["H2c", "estimation"])
    n["QoneHtwoaP"] = pv(h.loc["H2a", "p_holm"])
    n["QoneHtwobP"] = pv(h.loc["H2b", "p_holm"])
    n["QoneHtwocP"] = pv(h.loc["H2c", "p_holm"])
    n["QoneHthreeP"] = pv(h.loc["H3", "p_holm"])
    size1 = pd.read_csv(TAB / "phase4bis_q1_taille.csv").set_index("inference")["taille_5pct"] * 100
    n["QoneSizeWCR"], n["QoneSizeDep"], n["QoneSizeConley"] = (pct(size1[k]) for k in ["wcr_annee", "cluster_dep", "conley_200"])
    rob = pd.read_csv(TAB / "phase4bis_q1_robustesse.csv")
    r3 = rob[rob.specification.str.startswith("Q1-R3")].iloc[0]
    n["QoneAreaPct"] = pct(r3["effet_pct_par_unite"])
    n["QoneAreaP"] = pv(r3["p_wcb_annee_unilateral_droite"])
    r9 = pd.read_csv(TAB / "phase4bis_q1_r9_masque2008.csv").iloc[0]
    n["QoneMaskPct"] = pct(r9["effet_pct_par_unite"])
    n["QoneMaskP"] = pv(r9["p_wcb_annee_unilateral_droite"])
    val = pd.read_csv(TAB / "phase4bis_q1_valorisation.csv").set_index("annee")
    n["QoneValTwoThousandThree"] = f"{val.loc[2003, 'millions_eur_estimation']:.0f}"
    n["QoneValLow"] = f"{val.loc[2003, 'millions_eur_ic90_bas']:.0f}"
    n["QoneValHigh"] = f"{val.loc[2003, 'millions_eur_ic90_haut']:.0f}"

    # Été 2003 : exposition moyenne (pondérée par la surface de référence) des 17 départements principaux.
    mz = pd.read_parquet(ROOT / "data" / "processed" / "panel_mais_long.parquet")
    mz = mz[mz.echantillon_principal & (mz.modalite == "irrigue")]
    by_year = mz.groupby("annee").apply(lambda d: (d.dd_32_ja * d.surface_ref_ha).sum() / d.surface_ref_ha.sum())
    n["HeatTwoThousandThree"] = f"{by_year.loc[2003]:.1f}"
    n["HeatSecondYear"] = f"{by_year.drop(2003).max():.1f}"
    n["HeatRatio"] = f"{by_year.loc[2003] / by_year.drop(2003).max():.1f}"

    # Départements de relief : sous-estimation de la chaleur 2003 par la pondération surfacique (> 5 °C·jour).
    mes = pd.read_csv(TAB / "phase4bis_q1_mesures_departement.csv")
    gap = -mes.loc[mes.ecart_surface_moins_masque_2003 < -5, "ecart_surface_moins_masque_2003"]
    n["ReliefGapMin"], n["ReliefGapMax"] = f"{gap.min():.1f}", f"{gap.max():.1f}"

    # --- Q2, blé 1959-2025 --------------------------------------------------------------
    q2 = pd.read_csv(TAB / "phase4bis_q2_hypotheses.csv")
    m = q2[q2.periode == "1959-2025"].iloc[0]
    n["QtwoPct"] = pct(-m["effet_pct_par_unite"])
    n["QtwoP"] = pv(m["p_wcb_annee_unilateral_gauche"])
    n["QtwoN"] = f"{int(m['n']):,}"
    n["QtwoWaldP"] = f"{q2['p_wald_wcr_annee'].dropna().iloc[0]:.2f}"
    size2 = pd.read_csv(TAB / "phase4bis_q2_taille.csv").set_index("inference")["taille_5pct"] * 100
    n["QtwoSizeWCR"], n["QtwoSizeDep"], n["QtwoSizeConley"] = (pct(size2[k]) for k in ["wcr_annee", "cluster_dep", "conley_200"])

    # --- Blé 2010-2025 (phase 4) ------------------------------------------------------
    p4 = pd.read_csv(TAB / "phase4_principal.csv")
    m1 = p4[(p4.specification == "M1") & (p4.terme == "dd_32_remplissage")].iloc[0]
    n["WheatPct"] = pct(-m1["effet_pct_par_unite"])
    n["WheatPdep"] = pv(m1["p_cluster_dep"])
    n["WheatPwcr"] = pv(m1["p_wcb_annee"])
    sim = pd.read_csv(TAB / "phase4_simulation_inference.csv")
    s0 = sim[sim.beta_vrai == 0].set_index("inference")["taux_rejet_5pct"] * 100
    n["WheatSizeDep"], n["WheatSizeConley"], n["WheatSizeWCR"] = (pct(s0[k], 0) for k in ["cluster_dep", "conley_200", "wcr_annee"])
    s1 = sim[sim.beta_vrai.round(3) == -0.015].set_index("inference")["taux_rejet_5pct"] * 100  # puissance, beta = -1,5 %
    n["WheatPowerWCR"] = pct(s1["wcr_annee"], 0)

    # --- Prévision (phase 5, variante principale) -------------------------------------------
    f = pd.read_csv(TAB / "phase5_synthese_vs_B0.csv")
    fm = f[(f.variante != "longue_1990") & ~f.modele.isin(["B0", "B1"])]
    n["ForecastWorstPct"] = pct(-100 * fm.skill_moyen_vs_B0.min(), 0)
    n["ForecastBestPct"] = pct(-100 * fm.skill_moyen_vs_B0.max(), 0)

    # Fourchettes transversales de taille (cluster département et Conley, toutes analyses)
    usual = [size1["cluster_dep"], size1["conley_200"], size2["cluster_dep"], size2["conley_200"], s0["cluster_dep"], s0["conley_200"]]
    n["UsualSizeMin"], n["UsualSizeMax"] = pct(min(usual), 0), pct(max(usual), 0)

    data_numbers(n)
    spec_hashes(n)
    exposure_numbers(n)
    inference_tables(n)
    maize_tables(n)
    wheat_tables(n)
    forecast_tables(n)
    appendix_tables(n)

    # Résumé court pour les métadonnées arXiv (limite de 1 920 caractères), généré à partir des mêmes chiffres.
    abstract = (
        "Does the yield advantage of irrigated maize grow with extreme summer heat? Using French department-level yields "
        "reported separately for irrigated and rainfed grain maize (2000-2025), daily SAFRAN-ISBA weather, and heat "
        "measured on maize parcels, I compare the two modes within the same department and year. The specification was "
        "written after an exploratory analysis of 2010-2025 and before any estimate on 2000-2009; it entered the public "
        "repository together with the results, so this order rests on the author's log. In 17 departments, which exclude "
        "the South-West, each degree-day above 32 C in July-August is associated with a "
        f"{n['QonePct']}% wider gap in favour of irrigated maize (one-sided wild cluster bootstrap by year, "
        f"p = {n['QoneP']}). This meets the pre-specified rule, but {n['ExploSharePct']}% of the sample comes from the "
        "exploratory years. The only new evidence, 2000-2009, keeps the sign at about half the magnitude, a "
        f"difference driven by 2003 (p = {n['QoneReplP']}, power about {n['ReplPower']}%), and does not hold with heat averaged "
        f"over whole departments. Without the six departments with uplands it is not significant (p = {n['NoReliefP']}), "
        f"nor with a cluster jackknife (p = {n['CvThreeP']}). "
        "The result holds with E-OBS "
        "temperatures. A pre-specified interaction with crisis-level water restrictions has the opposite sign to the "
        "hypothesis. The result is an association, not the causal effect of irrigation. In these panels, standard "
        "errors clustered by department, or Conley with a uniform 200 km kernel, reject a true null in "
        f"{n['UsualSizeMin']}% to {n['UsualSizeMax']}% of placebo simulations. Wheat yields over 1959-2025 and "
        "out-of-sample yield forecasts give null results.")
    if len(abstract) > 1920:
        raise RuntimeError(f"résumé trop long : {len(abstract)} caractères")
    (ROOT / "memoire" / "arxiv_abstract.txt").write_text(abstract + "\n")

    lines = ["% GÉNÉRÉ par scripts/26_tables_memoire.py à partir de reports/tables/ : ne pas modifier à la main."]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in n.items()]
    (OUT / "numbers.tex").write_text("\n".join(lines) + "\n")
    print(f"{len(n)} macros écrites dans {(OUT / 'numbers.tex').relative_to(ROOT)}")
    for k, v in n.items():
        print(f"  {k} = {v}")


if __name__ == "__main__":
    main()
