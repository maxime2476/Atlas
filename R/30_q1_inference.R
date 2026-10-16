# Étape 30 (R) : pistes d'amélioration L1, L2a et S1, déclarées avant calcul dans docs/decisions.md
# (« Pistes d'amélioration (L1-L4, S1-S3) ») ; non pré-spécifiées, exploratoires.
#   L1a : levier partiel et influence de chaque année dans A1 (MacKinnon, Nielsen et Webb 2023) ;
#   L1b : bootstrap sauvage restreint par année dont la statistique t utilise l'erreur-type du jackknife (CV3) ;
#   L2a : A1 sans les département-années dont le rapport irrigué / pluvial est reconduit de l'année précédente ;
#   S1  : pentes départementales, modèle hiérarchique normal-normal (postérieure exacte sur une grille de tau).
# Usage : Rscript R/30_q1_inference.R ; sorties : reports/tables/phase7_l1_*.csv, phase7_l2_*.csv, phase7_s1_*.csv

source("R/common.R")

long <- as.data.frame(nanoparquet::read_parquet("data/processed/panel_mais_long.parquet"))
irr <- subset(long, modalite == "irrigue")
non <- subset(long, modalite == "non_irrigue")[, c("dep_code", "annee", "log_rendement", "rendement_q_ha")]
names(non)[3:4] <- c("log_non_irrigue", "rdt_non_irrigue")
d <- merge(irr, non, by = c("dep_code", "annee"))
d <- subset(d, echantillon_principal)
d$ecart_log <- d$log_rendement - d$log_non_irrigue
d <- d[order(d$annee, d$dep_code), ]
stopifnot(nrow(d) == 435)
FE <- c("dep_code", "annee")
years <- sort(unique(d$annee))
G <- length(years)

# Matrice complète du modèle A1 (effets fixes en indicatrices), pondérée : le coefficient de `x` par moindres carrés,
# et, pour chaque année g, le vecteur a_g tel que beta_(-g) = a_g . y_(-g) (formule exacte de suppression de lignes).
design <- function(df, x) {
  X <- model.matrix(~ df[[x]] + swi_ja + factor(dep_code) + factor(annee), data = df)
  colnames(X)[2] <- "x"
  X
}
coef_rows <- function(X, w) {
  # Ligne de (X'WX)^-1 X'W correspondant au coefficient de x, après retrait des colonnes nulles.
  # Colonnes linéairement indépendantes (QR avec pivot) : sans l'année de référence, une indicatrice d'année
  # devient redondante avec la constante. La chaleur (colonne 2) n'est jamais redondante.
  q <- qr(sqrt(w) * X)
  Xk <- X[, sort(q$pivot[seq_len(q$rank)]), drop = FALSE]
  stopifnot("x" %in% colnames(Xk))
  A <- solve(crossprod(Xk, w * Xk), t(w * Xk))
  A[which(colnames(Xk) == "x"), ]
}
jack_rows <- function(df, x) {
  X <- design(df, x)
  w <- df$surface_ref_ha
  full <- coef_rows(X, w)
  loo <- lapply(years, function(g) {
    keep <- df$annee != g
    list(idx = which(keep), a = coef_rows(X[keep, , drop = FALSE], w[keep]))
  })
  list(full = full, loo = loo)
}
cv3_t <- function(J, Y) {
  # Y : matrice n x B de variables expliquées ; renvoie beta et t avec l'erreur-type CV3.
  b <- as.vector(J$full %*% Y)
  bl <- sapply(J$loo, function(l) as.vector(l$a %*% Y[l$idx, , drop = FALSE]))
  bl <- matrix(bl, ncol = G)
  se <- sqrt((G - 1) / G * rowSums((bl - b)^2))
  list(b = b, t = b / se, se = se)
}
wcr_cv3 <- function(df, x, B = 9999, seed = 20261010) {
  J <- jack_rows(df, x)
  obs <- cv3_t(J, matrix(df$ecart_log))
  # Modèle restreint (beta = 0) : écart sur le SWI et les effets fixes.
  r <- feols(ecart_log ~ swi_ja | dep_code + annee, data = df, weights = ~surface_ref_ha,
             fixef.tol = 1e-11)  # tolérance resserrée comme dans wcr.R (feols refuse moins de 2,2e-12)
  yhat <- fitted(r)
  e <- resid(r)
  g <- as.integer(factor(df$annee))
  tstar <- with_seed(seed, {
    tstar <- numeric(0)
    for (start in seq(1, B, by = 1000)) {
      nb <- min(1000, B - start + 1)
      V <- vapply(seq_len(nb), function(i) webb_weights(G)[g], numeric(nrow(df)))
      tstar <- c(tstar, cv3_t(J, yhat + e * V)$t)
    }
    tstar
  })
  list(b = obs$b, se = obs$se, t = obs$t, p_right = mean(tstar >= obs$t))
}

# --- Contrôle : le CV3 exact redonne celui de G9a (R/22, par réestimations) -----------------------------------
J0 <- jack_rows(d, "dd_32_ja")
chk <- cv3_t(J0, matrix(d$ecart_log))
g9 <- read.csv("reports/tables/phase7_inferences.csv")
g9a <- g9[grepl("CV3", g9$specification), ]
stopifnot(abs(chk$se - g9a$se) < 1e-10, abs(chk$b - g9a$estimation) < 1e-12)

# --- L1a : levier partiel et influence par année ---------------------------------------------------------------
xt <- as.vector(resid(feols(dd_32_ja ~ swi_ja | dep_code + annee, data = d, weights = ~surface_ref_ha)))
w <- d$surface_ref_ha
lev <- tapply(w * xt^2, d$annee, sum) / sum(w * xt^2)
b_loo <- sapply(J0$loo, function(l) sum(l$a * d$ecart_log[l$idx]))
l1a <- data.frame(annee = years, levier_partiel = as.numeric(lev[as.character(years)]), beta_sans_annee = b_loo,
                  beta = chk$b, inverse_G = 1 / G)
write.csv(l1a, "reports/tables/phase7_l1_levier.csv", row.names = FALSE)
cat(sprintf("L1a : levier maximal %.2f (%d), soit %.1f fois 1/G ; beta sans 2003 %.4f\n",
            max(lev), years[which.max(lev)], max(lev) * G, b_loo[years == 2003]))

# --- L1b : WCR avec t du CV3, et sa taille sur les permutations de R/14 ----------------------------------------
obs <- wcr_cv3(d, "dd_32_ja")
field <- tapply(d$dd_32_ja, list(d$dep_code, d$annee), identity)
R <- 300
set.seed(20261013)
perms14 <- lapply(seq_len(R), function(r) {
  perm <- sample(years)
  while (any(perm == years)) perm <- sample(years)
  perm
})
size <- vapply(seq_len(R), function(r) {
  sim <- d
  sim$x_placebo <- field[cbind(d$dep_code, as.character(perms14[[r]][match(d$annee, years)]))]
  sim <- sim[!is.na(sim$x_placebo), ]          # panel non cylindré : couple absent l'année permutée
  wcr_cv3(sim, "x_placebo", B = 399, seed = r)$p_right < 0.05
}, logical(1))
l1b <- data.frame(test = "L1b WCR, t avec erreur-type CV3", estimation = obs$b, se_cv3 = obs$se, t = obs$t,
                  p_unilateral_droite = obs$p_right, taille_placebo = mean(size), R = R,
                  erreur_monte_carlo = sqrt(mean(size) * (1 - mean(size)) / R))
l1b$lecture <- if (mean(size) > 0.10) "taille trop élevée : non interprétable" else
  if (obs$p_right < 0.05) "le désaccord WCR / CV3 se résout en faveur de H1" else "le désaccord persiste"
write.csv(l1b, "reports/tables/phase7_l1_wcr_cv3.csv", row.names = FALSE)
print(l1b, row.names = FALSE)

# --- L2a : sans les rapports reconduits ---------------------------------------------------------------------
dd <- d[order(d$dep_code, d$annee), ]
ratio <- round(dd$rendement_q_ha / dd$rdt_non_irrigue, 2)
prev <- ave(seq_along(ratio), dd$dep_code, FUN = function(i) c(NA, ratio[i[-length(i)]]))
prev_year <- ave(dd$annee, dd$dep_code, FUN = function(a) c(NA, a[-length(a)]))
flag <- !is.na(prev) & ratio == prev & dd$annee - prev_year == 1
stopifnot(sum(flag) == 18)
d2 <- dd[!flag, ]
s2 <- summarise_term(fit(d2, c("dd_32_ja", "swi_ja"), y = "ecart_log"), d2, "dd_32_ja", c("dd_32_ja", "swi_ja"),
                     label = "L2a A1 sans les rapports reconduits", y = "ecart_log")
s2$p_wcb_annee_unilateral_droite <- 1 - s2$p_wcb_annee_unilateral_gauche
s2$n_retires <- sum(flag)
s2$lecture <- ifelse(s2$estimation > 0 & s2$p_wcb_annee_unilateral_droite < 0.05,
                     "H1 ne dépend pas des rapports reconduits", "H1 dépend des rapports reconduits")
write.csv(s2, "reports/tables/phase7_l2_sans_reconduits.csv", row.names = FALSE)
print(s2[, c("estimation", "effet_pct_par_unite", "p_wcb_annee_unilateral_droite", "n", "lecture")], row.names = FALSE)

# --- S1 : modèle hiérarchique normal-normal ------------------------------------------------------------------
pd <- read.csv("reports/tables/phase7_pentes_departements.csv", colClasses = c(dep_code = "character"))
b <- pd$pente
s <- pd$se_hetero
taus <- seq(0, 0.05, length.out = 2001)
logpost <- vapply(taus, function(tau) {
  v <- s^2 + tau^2
  Vmu <- 1 / sum(1 / v)
  mu <- Vmu * sum(b / v)
  0.5 * log(Vmu) - 0.5 * sum(log(v)) - 0.5 * sum((b - mu)^2 / v)
}, numeric(1))
post <- exp(logpost - max(logpost))
post <- post / sum(post)
set.seed(20261019)
draws <- sample(taus, 20000, replace = TRUE, prob = post)
theta <- t(vapply(draws, function(tau) {
  v <- s^2 + tau^2
  Vmu <- 1 / sum(1 / v)
  mu <- rnorm(1, Vmu * sum(b / v), sqrt(Vmu))
  Bk <- s^2 / v
  rnorm(length(b), Bk * mu + (1 - Bk) * b, sqrt((1 - Bk) * s^2))
}, numeric(length(b))))
s1 <- data.frame(dep_code = pd$dep_code, pente_brute = b, se = s, pente_eb = pd$pente_retrecie,
                 moyenne_post = colMeans(theta), q05 = apply(theta, 2, quantile, 0.05), q95 = apply(theta, 2, quantile, 0.95))
s1$tau_mediane <- quantile(draws, 0.5)
s1$tau_q95 <- quantile(draws, 0.95)
write.csv(s1, "reports/tables/phase7_s1_hierarchique.csv", row.names = FALSE)
print(round(s1[, -1], 4))
