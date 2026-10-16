# Étape 31 (R) : L4, A1 avec une fenêtre centrée sur le pic de végétation du maïs (MODIS MCD12Q2), 2001-2025.
# Déclarée avant calcul dans docs/decisions.md (« Pistes d'amélioration (L1-L4, S1-S3) », L4) ; exploratoire.
# Prérequis : uv run --with pyhdf==0.11.6 python scripts/44_phenologie_mais.py construire
# Usage : Rscript R/31_q1_phenologie.R ; sortie : reports/tables/phase7_l4_phenologie.csv

source("R/common.R")

long <- as.data.frame(nanoparquet::read_parquet("data/processed/panel_mais_long.parquet"))
irr <- subset(long, modalite == "irrigue")
non <- subset(long, modalite == "non_irrigue")[, c("dep_code", "annee", "log_rendement")]
names(non)[3] <- "log_non_irrigue"
d <- merge(irr, non, by = c("dep_code", "annee"))
d <- subset(d, echantillon_principal & annee >= 2001)
d$ecart_log <- d$log_rendement - d$log_non_irrigue
ph <- as.data.frame(nanoparquet::read_parquet("data/processed/phenologie_mais.parquet"))
d <- merge(d, ph[, c("dep_code", "annee", "pic_doy", "dd_32_ph", "swi_ph")], by = c("dep_code", "annee"))
n_all <- nrow(d)
d <- d[!is.na(d$dd_32_ph), ]
cat(sprintf("couples 2001-2025 : %d ; avec une date de pic : %d\n", n_all, nrow(d)))

FE <- c("dep_code", "annee")
p_right <- function(df, x, z, B = 9999, seed = 20261010) {
  1 - wcr_pvalue(df, "ecart_log", x, z, FE, "annee", "surface_ref_ha", B = B, seed = seed)$p_left
}
b_ph <- coef(fit(d, c("dd_32_ph", "swi_ph"), y = "ecart_log"))[["dd_32_ph"]]
p_ph <- p_right(d, "dd_32_ph", "swi_ph")
size <- placebo_size(d, "dd_32_ph", "dep_code", "annee",
                     list(wcr = function(sim) p_right(sim, "x_placebo", "swi_ph", B = 399)), R = 300)
# Même échantillon, fenêtre juillet-août, pour comparer.
b_ja <- coef(fit(d, c("dd_32_ja", "swi_ja"), y = "ecart_log"))[["dd_32_ja"]]
p_ja <- p_right(d, "dd_32_ja", "swi_ja")
pic <- tapply(d$pic_doy, d$annee, mean)
trend <- coef(lm(as.numeric(pic) ~ as.numeric(names(pic))))[[2]]
out <- data.frame(
  specification = c("L4 A1, fenêtre phénologique [pic - 20 j, pic + 40 j]", "même échantillon, juillet-août"),
  estimation = c(b_ph, b_ja), effet_pct_par_unite = 100 * (exp(c(b_ph, b_ja)) - 1),
  p_wcb_annee_unilateral_droite = c(p_ph, p_ja), taille_placebo = c(size$taille, NA), n = nrow(d),
  n_retires_sans_date = n_all - nrow(d), pic_doy_moyen = mean(d$pic_doy), pic_doy_2003 = pic[["2003"]],
  tendance_pic_jours_par_an = trend, correlation_dd_ph_ja = cor(d$dd_32_ph, d$dd_32_ja))
out$lecture <- c(ifelse(p_ph < 0.05 & size$taille <= 0.10, "soutenue avec la fenêtre phénologique",
                        "non soutenue avec la fenêtre phénologique"), NA)
write.csv(out, "reports/tables/phase7_l4_phenologie.csv", row.names = FALSE)
print(out, row.names = FALSE)
