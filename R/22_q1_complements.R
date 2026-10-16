# Étape 22 (R) : analyses complémentaires (G1-G10 sauf G11-G12), déclarées avant calcul dans docs/decisions.md
# (« Analyses complémentaires ») ; non pré-spécifiées, exploratoires.
# Prérequis : uv run python scripts/28_complements_python.py preparer ; uv run python scripts/29_eolien.py
# Usage : Rscript R/22_q1_complements.R ; sorties : reports/tables/phase7_*.csv

source("R/common.R")

long <- as.data.frame(nanoparquet::read_parquet("data/processed/panel_mais_long.parquet"))
long <- subset(long, echantillon_principal)
irr <- subset(long, modalite == "irrigue")
non <- subset(long, modalite == "non_irrigue")[, c("dep_code", "annee", "log_rendement")]
names(non)[3] <- "log_non_irrigue"
d <- merge(irr, non, by = c("dep_code", "annee"))
names(d)[names(d) == "log_rendement"] <- "log_irrigue"
d$ecart_log <- d$log_irrigue - d$log_non_irrigue
stopifnot(nrow(d) == 435, !anyDuplicated(d[, c("dep_code", "annee")]))
cov <- as.data.frame(nanoparquet::read_parquet("data/processed/phase7_covariables_dep.parquet"))
d <- merge(d, cov[, c("dep_code", "part_irriguee", "ecart_alt_m", "relief")], by = "dep_code")
stopifnot(nrow(d) == 435)
RHS <- c("dd_32_ja", "swi_ja")
FE <- c("dep_code", "annee")
years <- sort(unique(d$annee))

one <- function(df, term, rhs, label, y = "ecart_log") {
  s <- summarise_term(fit(df, rhs, y = y), df, term, rhs, label = label, y = y)
  s$p_wcb_annee_unilateral_droite <- 1 - s$p_wcb_annee_unilateral_gauche
  s$n_departements <- length(unique(df$dep_code))
  s
}
one_sided_right <- function(ct) {
  p <- ct[["Pr(>|t|)"]]
  if (ct[["t value"]] > 0) p / 2 else 1 - p / 2
}

# --- Corrélations entre variables départementales retenues (règle : |r| > 0,7 -> pas dans le même modèle) --------
wind <- as.data.frame(nanoparquet::read_parquet("data/processed/eolien_dep_annee.parquet"))
w25 <- subset(wind, annee == 2025)[, c("dep_code", "mw_par_10kha_sau")]
dep17 <- merge(unique(d[, c("dep_code", "part_irriguee", "ecart_alt_m", "relief")]), w25, by = "dep_code")
cm <- cor(cbind(part_irriguee = dep17$part_irriguee, ecart_alt_m = dep17$ecart_alt_m, relief = as.numeric(dep17$relief),
                eolien_2025 = dep17$mw_par_10kha_sau))
write.csv(data.frame(variable = rownames(cm), cm, row.names = NULL), "reports/tables/phase7_correlations_variables.csv",
          row.names = FALSE)
cat("Corrélations entre départements (17) :\n"); print(round(cm, 2))

# --- G1 (relief) et G5 (intensité d'irrigation) : interactions --------------------------------------------------
d$dd32_x_relief <- d$dd_32_ja * d$relief
d$part_irr_c <- d$part_irriguee - mean(unique(d[, c("dep_code", "part_irriguee")])$part_irriguee)
d$dd32_x_part_irr <- d$dd_32_ja * d$part_irr_c
g1 <- one(d, "dd32_x_relief", c(RHS, "dd32_x_relief"), "G1 A1 + chaleur x relief")
g1_base <- one(d, "dd_32_ja", c(RHS, "dd32_x_relief"), "G1 pente hors relief (11 départements)")
g5 <- one(d, "dd32_x_part_irr", c(RHS, "dd32_x_part_irr"), "G5 A1 + chaleur x part irriguée (centrée)")
inter <- rbind(g1, g1_base, g5)
write.csv(inter, "reports/tables/phase7_interactions.csv", row.names = FALSE)
print(inter[, c("specification", "terme", "estimation", "p_wcb_annee", "p_wcb_annee_unilateral_droite")], row.names = FALSE)

# --- G2 : ensilage (part du maïs non irrigué récolté en fourrage), 2010-2025 ------------------------------------
fou <- as.data.frame(nanoparquet::read_parquet("data/processed/phase7_fourrage.parquet"))
d2 <- merge(subset(d, annee >= 2010), fou, by = c("dep_code", "annee"))
stopifnot(nrow(d2) == nrow(subset(d, annee >= 2010)), !anyNA(d2$part_fourrage_non_irr))
g2 <- one(d2, "dd_32_ja", RHS, "G2 part fourrage du maïs non irrigué ~ chaleur", y = "part_fourrage_non_irr")
g2$moyenne_part <- weighted.mean(d2$part_fourrage_non_irr, d2$surface_ref_ha)
g2_ctrl <- NULL
if (g2$p_wcb_annee_unilateral_droite < 0.05) {
  g2_ctrl <- one(d2, "dd_32_ja", c(RHS, "part_fourrage_non_irr"), "G2 A1 2010-2025 + part fourrage")
  g2_ctrl$moyenne_part <- NA
}
write.csv(rbind(g2, g2_ctrl), "reports/tables/phase7_ensilage.csv", row.names = FALSE)
cat(sprintf("G2 : pente %.5f par °C·jour (moyenne %.2f), p unilatérale = %.4f\n", g2$estimation, g2$moyenne_part,
            g2$p_wcb_annee_unilateral_droite))

# --- G3 (c) : levier partiel par année ; N_eff sur 2000-2025 et 2000-2009 ---------------------------------------
leverage <- function(df) {
  w <- df$surface_ref_ha
  dm <- fixest::demean(as.matrix(df[, c("dd_32_ja", "swi_ja")]), df[, FE], weights = w)
  xt <- dm[, 1] - dm[, 2] * sum(w * dm[, 1] * dm[, 2]) / sum(w * dm[, 2]^2)
  s <- tapply(w * xt^2, df$annee, sum)
  s / sum(s)
}
lev_all <- leverage(d); lev_early <- leverage(subset(d, annee <= 2009))
lev <- rbind(data.frame(periode = "2000-2025", annee = as.integer(names(lev_all)), part_sxx = as.numeric(lev_all)),
             data.frame(periode = "2000-2009", annee = as.integer(names(lev_early)), part_sxx = as.numeric(lev_early)))
lev$n_eff_periode <- ave(lev$part_sxx, lev$periode, FUN = function(s) 1 / sum(s^2))
write.csv(lev, "reports/tables/phase7_levier_annees.csv", row.names = FALSE)
cat(sprintf("Levier : part de 2003 = %.2f (2000-2025, N_eff %.1f) ; %.2f (2000-2009, N_eff %.1f)\n",
            lev_all[["2003"]], 1 / sum(lev_all^2), lev_early[["2003"]], 1 / sum(lev_early^2)))

# --- G3 (a), G3 (b), G4, G9 (c) : placebos -----------------------------------------------------------------
field <- tapply(d$dd_32_ja, list(d$dep_code, d$annee), identity)
R <- 300
p_wcr_right <- function(sim, y = "ecart_log", seed) {
  1 - wcr_pvalue(sim, y, "x_placebo", "swi_ja", FE, "annee", "surface_ref_ha", B = 399, seed = seed)$p_left
}
p_wcr_left <- function(sim, y, seed) {
  wcr_pvalue(sim, y, "x_placebo", "swi_ja", FE, "annee", "surface_ref_ha", B = 399, seed = seed)$p_left
}

# (b) et (c) : permutations de R/14 rejouées. wcr_pvalue() ne modifiant pas l'état du générateur, R/14 tire ses
# permutations à la suite après set.seed(20261013) : on refait cette séquence (contrôlée ci-dessous par la taille
# du WCR enregistrée par R/14).
set.seed(20261013)
perms <- vector("list", R)
for (r in seq_len(R)) {
  perm <- sample(years)
  while (any(perm == years)) perm <- sample(years)
  perms[[r]] <- perm
}
derange <- function(perm) {
  sim <- d
  sim$x_placebo <- field[cbind(d$dep_code, as.character(perm[match(d$annee, years)]))]
  sim[!is.na(sim$x_placebo), ]
}
t0 <- Sys.time()
pl <- do.call(rbind, lapply(seq_len(R), function(r) {
  sim <- derange(perms[[r]])
  m <- fit(sim, c("swi_ja", "x_placebo"), y = "ecart_log")
  conley_fixed <- FALSE
  withCallingHandlers(vcov_conley(m, lat = ~lat_centroide, lon = ~lon_centroide, cutoff = CONLEY_KM),
                      warning = function(w) {
                        if (grepl("positive definite", conditionMessage(w))) conley_fixed <<- TRUE
                        invokeRestart("muffleWarning")
                      })
  data.frame(r = r, annee_recoit_2003 = years[perms[[r]] == 2003],
             rejet_wcr = p_wcr_right(sim, seed = r) < 0.05, conley_corrigee = conley_fixed,
             rejet_h2b = p_wcr_left(sim, "log_non_irrigue", seed = r) < 0.05,   # G4
             rejet_h2c = p_wcr_left(sim, "log_irrigue", seed = r) < 0.05)
}))
cat(sprintf("Placebos par dérangement : %.0f s\n", as.numeric(difftime(Sys.time(), t0, units = "secs"))))
size_r14 <- read.csv("reports/tables/phase4bis_q1_taille.csv")
stopifnot(abs(mean(pl$rejet_wcr) - size_r14$taille_5pct[size_r14$inference == "wcr_annee"]) < 1e-12)  # rejoue R/14
write.csv(pl, "reports/tables/phase7_placebo_derangement.csv", row.names = FALSE)

# (a) placebo intra-année : chaque année, valeurs de dd_32_ja permutées au hasard entre départements.
set.seed(20261014)
within_perms <- lapply(seq_len(R), function(r) lapply(years, function(y) sample(which(d$annee == y))))
pa <- vapply(seq_len(R), function(r) {
  sim <- d
  sim$x_placebo <- NA_real_
  for (k in seq_along(years)) {
    idx <- which(d$annee == years[k])
    sim$x_placebo[idx] <- d$dd_32_ja[within_perms[[r]][[k]]]
  }
  p_wcr_right(sim, seed = r)
}, numeric(1))
sizes <- data.frame(
  diagnostic = c("G3a H1, placebo intra-année", "G4 H2b (non irrigué), dérangement", "G4 H2c (irrigué), dérangement",
                 "rappel H1, dérangement (R/14)", "G9c matrices de Conley corrigées (dérangement)"),
  taux = c(mean(pa < 0.05), mean(pl$rejet_h2b), mean(pl$rejet_h2c), mean(pl$rejet_wcr), mean(pl$conley_corrigee)),
  R = R)
sizes$erreur_monte_carlo <- sqrt(sizes$taux * (1 - sizes$taux) / R)
write.csv(sizes, "reports/tables/phase7_tailles.csv", row.names = FALSE)
print(sizes, row.names = FALSE)
by03 <- aggregate(rejet_wcr ~ annee_recoit_2003, data = pl, FUN = function(x) c(n = length(x), taux = mean(x)))
by03 <- data.frame(annee_recoit_2003 = by03$annee_recoit_2003, n = by03$rejet_wcr[, "n"], taux_rejet = by03$rejet_wcr[, "taux"])
write.csv(by03, "reports/tables/phase7_placebo_par_annee_2003.csv", row.names = FALSE)

# --- G6 : pentes départementales et rétrécissement empirique bayésien -----------------------------------------
m6 <- feols(ecart_log ~ dd_32_ja:dep_code + swi_ja | dep_code + annee, data = d, weights = ~surface_ref_ha,
            vcov = "hetero")
ct <- coeftable(m6)
ct <- ct[grepl("^dd_32_ja:dep_code", rownames(ct)), ]
b <- ct[, "Estimate"]; se <- ct[, "Std. Error"]
deps <- sub("dd_32_ja:dep_code", "", rownames(ct))
wi <- 1 / se^2
mu_fe <- sum(wi * b) / sum(wi)
Q <- sum(wi * (b - mu_fe)^2)
k <- length(b)
tau2 <- max(0, (Q - (k - 1)) / (sum(wi) - sum(wi^2) / sum(wi)))     # DerSimonian-Laird
mu <- sum(b / (se^2 + tau2)) / sum(1 / (se^2 + tau2))
shrunk <- mu + tau2 / (tau2 + se^2) * (b - mu)
g6 <- data.frame(dep_code = deps, pente = b, se_hetero = se, pente_retrecie = shrunk)
g6 <- merge(g6, cov[, c("dep_code", "part_irriguee", "ecart_alt_m", "relief")], by = "dep_code")
g6$tau <- sqrt(tau2); g6$mu <- mu; g6$Q <- Q; g6$p_Q <- 1 - pchisq(Q, k - 1)
g6$cor_retrecie_part_irr <- cor(g6$pente_retrecie, g6$part_irriguee)
g6$cor_retrecie_ecart_alt <- cor(g6$pente_retrecie, g6$ecart_alt_m)
g6$cor_brute_ecart_alt <- cor(g6$pente, g6$ecart_alt_m)
write.csv(g6, "reports/tables/phase7_pentes_departements.csv", row.names = FALSE)
cat(sprintf("G6 : mu = %.4f, tau = %.4f, Q = %.1f (p = %.3f) ; cor(rétrécie, part irriguée) = %.2f, cor(rétrécie, écart alt.) = %.2f\n",
            mu, sqrt(tau2), Q, 1 - pchisq(Q, k - 1), g6$cor_retrecie_part_irr[1], g6$cor_retrecie_ecart_alt[1]))

# --- G7 : forêt causale ----------------------------------------------------------------------------------------
dm <- fixest::demean(as.matrix(d[, c("ecart_log", "dd_32_ja", "swi_ja")]), d[, FE], weights = d$surface_ref_ha)
res_on_swi <- function(v) v - dm[, "swi_ja"] * sum(d$surface_ref_ha * v * dm[, "swi_ja"]) / sum(d$surface_ref_ha * dm[, "swi_ja"]^2)
Yr <- res_on_swi(dm[, "ecart_log"]); Wr <- res_on_swi(dm[, "dd_32_ja"])
heat_mean <- ave(d$dd_32_ja, d$dep_code); swi_mean <- ave(d$swi_ja, d$dep_code)
X <- cbind(part_irriguee = d$part_irriguee, ecart_alt_m = d$ecart_alt_m, chaleur_moyenne = heat_mean,
           swi_moyen = swi_mean, latitude = d$lat_centroide)
cf <- grf::causal_forest(X, Yr, Wr, Y.hat = rep(0, nrow(d)), W.hat = rep(0, nrow(d)), sample.weights = d$surface_ref_ha,
                         clusters = as.integer(factor(d$annee)), num.trees = 4000, seed = 20261012)
cal <- grf::test_calibration(cf)
ate <- grf::average_treatment_effect(cf)
vi <- grf::variable_importance(cf)
g7 <- data.frame(effet_moyen = ate[["estimate"]], effet_moyen_se = ate[["std.err"]],
                 coef_mean_forest = cal["mean.forest.prediction", "Estimate"],
                 coef_differential = cal["differential.forest.prediction", "Estimate"],
                 p_differential = cal["differential.forest.prediction", "Pr(>t)"],
                 importance_part_irriguee = vi[1], importance_ecart_alt = vi[2], importance_chaleur_moy = vi[3],
                 importance_swi_moy = vi[4], importance_latitude = vi[5])
write.csv(g7, "reports/tables/phase7_foret_causale.csv", row.names = FALSE)
print(g7, row.names = FALSE)

# --- G8 : inférence WCR du DML (résidus de scripts/28) -------------------------------------------------------
dml <- as.data.frame(nanoparquet::read_parquet("data/processed/phase7_dml_residus.parquet"))
bt <- wcr_pvalue(dml, "y_res", "d_res", character(0), FE, "annee", "surface_ref_ha", B = 9999)
g8 <- data.frame(specification = "G8 DML (forêts aléatoires, 5 plis par années)",
                 estimation = sum(dml$surface_ref_ha * dml$d_res * dml$y_res) / sum(dml$surface_ref_ha * dml$d_res^2),
                 p_wcb_annee = bt$p, p_wcb_annee_unilateral_droite = 1 - bt$p_left, n = nrow(dml))

# --- G9 (a) jackknife par année (CV3) et (b) inférence par randomisation ------------------------------------
b_hat <- coef(fit(d, RHS, y = "ecart_log"))[["dd_32_ja"]]
b_loo <- vapply(years, function(y) coef(fit(subset(d, annee != y), RHS, y = "ecart_log"))[["dd_32_ja"]], numeric(1))
G <- length(years)
se_cv3 <- sqrt((G - 1) / G * sum((b_loo - b_hat)^2))
set.seed(20261015)
b_ri <- vapply(seq_len(5000), function(i) {
  perm <- sample(years)
  while (any(perm == years)) perm <- sample(years)
  coef(fit(derange(perm), c("swi_ja", "x_placebo"), y = "ecart_log"))[["x_placebo"]]
}, numeric(1))
g9 <- data.frame(
  specification = c("G9a jackknife par année (CV3)", "G9b randomisation (5 000 dérangements, stat. beta)"),
  estimation = b_hat, se = c(se_cv3, NA),
  p_unilateral_droite = c(1 - pt(b_hat / se_cv3, G - 1), mean(b_ri >= b_hat)), n = nrow(d))
write.csv(merge(g8, g9, all = TRUE), "reports/tables/phase7_inferences.csv", row.names = FALSE)
print(rbind(g8[, c("specification", "estimation", "p_wcb_annee_unilateral_droite")],
            setNames(g9[, c("specification", "estimation", "p_unilateral_droite")], names(g8)[c(1, 2, 4)])), row.names = FALSE)

# --- G10 : éolien ---------------------------------------------------------------------------------------------
dw <- merge(d, wind[, c("dep_code", "annee", "mw_par_10kha_sau")], by = c("dep_code", "annee"))
stopifnot(nrow(dw) == 435)
wheat <- merge(subset(load_panel(), echantillon_principal), wind[, c("dep_code", "annee", "mw_par_10kha_sau")],
               by = c("dep_code", "annee"))
stopifnot(nrow(wheat) == 1328)
RHS_M1 <- c("gdd_0_32_remplissage", "dd_32_remplissage", "prec_printemps", "dd_0_automne", "prec_automne")
g10 <- rbind(
  one(dw, "mw_par_10kha_sau", c("mw_par_10kha_sau", RHS), "G10 maïs irrigué ~ éolien", y = "log_irrigue"),
  one(dw, "mw_par_10kha_sau", c("mw_par_10kha_sau", RHS), "G10 maïs non irrigué ~ éolien", y = "log_non_irrigue"),
  one(dw, "mw_par_10kha_sau", c("mw_par_10kha_sau", RHS), "G10 écart ~ éolien", y = "ecart_log"),
  one(wheat, "mw_par_10kha_sau", c("mw_par_10kha_sau", RHS_M1), "G10 blé 2010-2025 ~ éolien", y = "log_rendement"))
g10$moyenne_mw_par_10kha <- c(rep(weighted.mean(dw$mw_par_10kha_sau, dw$surface_ref_ha), 3),
                              weighted.mean(wheat$mw_par_10kha_sau, wheat$surface_ref_ha))
write.csv(g10, "reports/tables/phase7_eolien.csv", row.names = FALSE)
print(g10[, c("specification", "estimation", "p_wcb_annee", "n", "moyenne_mw_par_10kha")], row.names = FALSE)
