# Étape 27 (R) : réserve utile des sols et eau d'irrigation (R1, W1, W2), déclarés avant calcul dans docs/decisions.md
# (« Réserve utile des sols et eau d'irrigation ») ; non pré-spécifiés, exploratoires.
#   R1 : hétérogénéité de β selon la réserve utile (RU) sous le maïs grain (scripts/35_reserve_utile.py)
#   W1 : les volumes prélevés pour l'irrigation suivent-ils la chaleur ? (BNPE, scripts/36_volumes_irrigation.py)
#   W2 : valeur apparente du m³ dans les 6 départements où le maïs grain domine l'irrigation
# Usage : Rscript R/27_q1_sol_eau.R ; sorties : reports/tables/phase7_r1_*.csv, phase7_w1_*.csv, phase7_w2_*.csv

source("R/common.R")
FE <- c("dep_code", "annee")
RHS <- c("dd_32_ja", "swi_ja")
one <- function(df, term, rhs, label, y = "ecart_log", pct = TRUE) {
  s <- summarise_term(fit(df, rhs, y = y), df, term, rhs, label = label, y = y, pct_meaningful = pct)
  s$p_wcb_annee_unilateral_droite <- 1 - s$p_wcb_annee_unilateral_gauche
  s$n_departements <- length(unique(df$dep_code))
  s
}

# Paires irrigué / non irrigué : 38 départements, puis l'échantillon principal (17).
long <- as.data.frame(nanoparquet::read_parquet("data/processed/panel_mais_long.parquet"))
irr <- subset(long, modalite == "irrigue")
non <- subset(long, modalite == "non_irrigue")[, c(FE, "log_rendement", "rendement_q_ha")]
names(non)[3:4] <- c("log_non_irrigue", "rendement_non_irrigue")
all38 <- merge(irr, non, by = FE)
all38$ecart_log <- all38$log_rendement - all38$log_non_irrigue
vpd <- as.data.frame(nanoparquet::read_parquet("data/processed/vpd_dep_ja.parquet"))
all38 <- merge(all38, vpd, by = FE)
stopifnot(nrow(all38) == 981)
d <- subset(all38, echantillon_principal)
stopifnot(nrow(d) == 435, length(unique(d$dep_code)) == 17)

# --- R1 : réserve utile ---------------------------------------------------------------------------------------
ru <- as.data.frame(nanoparquet::read_parquet("data/processed/ru_dep_mais.parquet"))
cov <- as.data.frame(nanoparquet::read_parquet("data/processed/phase7_covariables_dep.parquet"))
d <- merge(d, ru[, c("dep_code", "ru_mm")], by = "dep_code")
d <- merge(d, cov[, c("dep_code", "part_irriguee")], by = "dep_code")
stopifnot(nrow(d) == 435, !anyNA(d$ru_mm))
dep17 <- unique(d[, c("dep_code", "ru_mm", "part_irriguee")])
d$ru_c <- d$ru_mm - mean(dep17$ru_mm)                          # centrée sur la moyenne des 17 départements
d$part_irr_c <- d$part_irriguee - mean(dep17$part_irriguee)    # comme G5
d$dd32_x_ru <- d$dd_32_ja * d$ru_c
d$dd32_x_part_irr <- d$dd_32_ja * d$part_irr_c
d$vpd_x_ru <- d$vpd_ja * d$ru_c
r1 <- rbind(
  one(d, "dd32_x_ru", c(RHS, "dd32_x_ru"), "R1a A1 + chaleur x RU (centrée, mm)", pct = FALSE),
  one(d, "dd_32_ja", c(RHS, "dd32_x_ru"), "R1a pente de la chaleur à la RU moyenne"),
  one(d, "dd32_x_ru", c(RHS, "dd32_x_ru", "dd32_x_part_irr"), "R1b avec chaleur x part irriguée : RU", pct = FALSE),
  one(d, "dd32_x_part_irr", c(RHS, "dd32_x_ru", "dd32_x_part_irr"), "R1b avec chaleur x part irriguée : part", pct = FALSE),
  one(d, "vpd_x_ru", c("vpd_ja", "swi_ja", "vpd_x_ru"), "R1c VPD à la place de la chaleur : VPD x RU", pct = FALSE))
# Information : 38 départements (tous statuts), RU centrée sur la moyenne des 38.
a <- merge(all38, ru[, c("dep_code", "ru_mm")], by = "dep_code")
stopifnot(nrow(a) == 981)
a$dd32_x_ru <- a$dd_32_ja * (a$ru_mm - mean(unique(a[, c("dep_code", "ru_mm")])$ru_mm))
r1 <- rbind(r1, one(a, "dd32_x_ru", c(RHS, "dd32_x_ru"), "R1d 38 départements (information) : chaleur x RU", pct = FALSE))
# Pente du VPD (en % par kPa) aux RU extrêmes des 17 départements, dans le modèle R1c.
cv <- coef(fit(d, c("vpd_ja", "swi_ja", "vpd_x_ru"), y = "ecart_log"))
r1$effet_vpd_pct_ru_min <- r1$effet_vpd_pct_ru_max <- NA
r1$effet_vpd_pct_ru_min[5] <- 100 * (exp(cv[["vpd_ja"]] + cv[["vpd_x_ru"]] * (min(dep17$ru_mm) - mean(dep17$ru_mm))) - 1)
r1$effet_vpd_pct_ru_max[5] <- 100 * (exp(cv[["vpd_ja"]] + cv[["vpd_x_ru"]] * (max(dep17$ru_mm) - mean(dep17$ru_mm))) - 1)
r1$correlation_ru_part_irriguee_17 <- cor(dep17$ru_mm, dep17$part_irriguee)
r1$ru_min_17 <- min(dep17$ru_mm)
r1$ru_max_17 <- max(dep17$ru_mm)
write.csv(r1, "reports/tables/phase7_r1_reserve_utile.csv", row.names = FALSE)
write.csv(merge(dep17, ru, by = c("dep_code", "ru_mm")), "reports/tables/phase7_r1_ru_departements.csv", row.names = FALSE)
print(r1[, c("specification", "estimation", "p_wcb_annee", "n", "n_departements")], row.names = FALSE)
cat(sprintf("RU des 17 départements : %.0f à %.0f mm ; corrélation avec la part irriguée %.2f\n",
            min(dep17$ru_mm), max(dep17$ru_mm), cor(dep17$ru_mm, dep17$part_irriguee)))

# --- W1 : volumes d'irrigation et chaleur, 2012-2023 ----------------------------------------------------------
vol <- as.data.frame(nanoparquet::read_parquet("data/processed/bnpe_irr_dep_annee.parquet"))
w <- merge(subset(d, annee >= 2012 & annee <= 2023), vol, by = FE)
stopifnot(nrow(w) == nrow(subset(d, annee >= 2012 & annee <= 2023)))
w$log_volume <- log(w$volume_m3)
w1 <- rbind(one(w, "dd_32_ja", RHS, "W1a log volume BNPE ~ chaleur", y = "log_volume"),
            one(w, "vpd_ja", c("vpd_ja", "swi_ja"), "W1b log volume BNPE ~ VPD", y = "log_volume"),
            one(w, "swi_ja", RHS, "W1a log volume BNPE : SWI", y = "log_volume"))
w1$part_volume_mesure_mediane <- median(w$part_volume_mesure)
write.csv(w1, "reports/tables/phase7_w1_volumes.csv", row.names = FALSE)
print(w1[, c("specification", "estimation", "effet_pct_par_unite", "p_wcb_annee", "p_wcb_annee_unilateral_droite", "n")],
      row.names = FALSE)

# --- W2 : valeur apparente du m³ (6 départements où le maïs grain domine l'irrigation en 2020) ----------------
ra <- as.data.frame(nanoparquet::read_parquet("data/processed/ra_irrigation_dep.parquet"))
s20 <- setNames(subset(ra, annee_ra == 2020)[, c("dep_code", "part_mais_grain_irrigue")], c("dep_code", "part_2020"))
s10 <- setNames(subset(ra, annee_ra == 2010)[, c("dep_code", "part_mais_grain_irrigue")], c("dep_code", "part_2010"))
deps6 <- sort(subset(s20, dep_code %in% dep17$dep_code & part_2020 > 0.5)$dep_code)
stopifnot(identical(deps6, c("01", "03", "18", "63", "67", "68")))      # liste déclarée avant calcul
price <- as.data.frame(nanoparquet::read_parquet("data/processed/prix_mais.parquet"))
v <- merge(merge(merge(subset(w, dep_code %in% deps6), s20, by = "dep_code"), s10, by = "dep_code"), price, by = "annee")
v$gain_q_ha <- v$rendement_q_ha - v$rendement_non_irrigue
dose <- function(part) v$volume_m3 * part / v$surface_ha                  # m³ par ha de maïs grain irrigué
v$dose_m3_ha <- dose(v$part_2020)
v$dose_m3_ha_2010 <- dose(v$part_2010)
v$plausible <- v$dose_m3_ha >= 500 & v$dose_m3_ha <= 3000                 # règle fixée d'avance
v$kg_par_m3 <- ifelse(v$plausible, 100 * v$gain_q_ha / v$dose_m3_ha, NA)
v$eur_par_m3 <- ifelse(v$plausible, v$gain_q_ha * v$prix_eur_q / v$dose_m3_ha, NA)
v$eur_par_m3_part_2010 <- with(v, ifelse(dose_m3_ha_2010 >= 500 & dose_m3_ha_2010 <= 3000,
                                         gain_q_ha * prix_eur_q / dose_m3_ha_2010, NA))
write.csv(v[order(v$dep_code, v$annee), c("dep_code", "annee", "volume_m3", "part_2020", "part_2010", "surface_ha",
                                           "dose_m3_ha", "dose_m3_ha_2010", "plausible", "gain_q_ha", "prix_eur_q",
                                           "kg_par_m3", "eur_par_m3", "eur_par_m3_part_2010", "dd_32_ja")],
          "reports/tables/phase7_w2_departement_annee.csv", row.names = FALSE)
med <- function(x) median(x, na.rm = TRUE)
by_dep <- do.call(rbind, lapply(split(v, v$dep_code), function(g) data.frame(
  dep_code = g$dep_code[1], annees = nrow(g), exclues = sum(!g$plausible), part_2020 = g$part_2020[1],
  dose_mediane_m3_ha = med(g$dose_m3_ha), gain_median_q_ha = med(g$gain_q_ha), kg_par_m3_median = med(g$kg_par_m3),
  eur_par_m3_median = med(g$eur_par_m3), eur_par_m3_median_part_2010 = med(g$eur_par_m3_part_2010))))
by_dep <- rbind(by_dep, data.frame(dep_code = "ensemble", annees = nrow(v), exclues = sum(!v$plausible), part_2020 = NA,
                                   dose_mediane_m3_ha = med(v$dose_m3_ha), gain_median_q_ha = med(v$gain_q_ha),
                                   kg_par_m3_median = med(v$kg_par_m3), eur_par_m3_median = med(v$eur_par_m3),
                                   eur_par_m3_median_part_2010 = med(v$eur_par_m3_part_2010)))
write.csv(by_dep, "reports/tables/phase7_w2_valeur_m3.csv", row.names = FALSE)
print(by_dep, row.names = FALSE, digits = 3)

# Pentes de l'écart (q/ha) et de la dose (m³/ha) sur la chaleur : rapport = kg de grain par m³ supplémentaire
# des étés chauds (descriptif, sans inférence sur le rapport).
vp <- subset(v, plausible)
w2s <- rbind(one(vp, "dd_32_ja", RHS, "W2 écart irrigué - non irrigué (q/ha) ~ chaleur", y = "gain_q_ha", pct = FALSE),
             one(vp, "dd_32_ja", RHS, "W2 dose (m³/ha) ~ chaleur", y = "dose_m3_ha", pct = FALSE))
w2s$kg_par_m3_supplementaire <- 100 * w2s$estimation[1] / w2s$estimation[2]
write.csv(w2s, "reports/tables/phase7_w2_pentes.csv", row.names = FALSE)
print(w2s[, c("specification", "estimation", "p_wcb_annee", "n", "kg_par_m3_supplementaire")], row.names = FALSE)
