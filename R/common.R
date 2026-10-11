# Fonctions communes de la phase 4 : chargement du panel, estimation, résumé à trois inférences.
# Spécification : docs/specification_phase4.md (pré-spécifiée).

suppressPackageStartupMessages(library(fixest))
source("R/wild_bootstrap.R")

CONLEY_KM <- 200

load_panel <- function(path = "data/processed/panel_ble.parquet") {
  df <- as.data.frame(nanoparquet::read_parquet(path))
  df$swi_remplissage_2 <- df$swi_remplissage^2
  df
}

# Formule « log_rendement ~ rhs | effets fixes ».
# `y` : variable expliquée (log_rendement par défaut ; ecart_log pour le maïs en phase 6).
make_formula <- function(rhs, fe = "dep_code + annee", y = "log_rendement") {
  as.formula(paste(y, "~", paste(rhs, collapse = " + "), "|", fe))
}

fit <- function(df, rhs, fe = "dep_code + annee", weighted = TRUE, y = "log_rendement") {
  feols(make_formula(rhs, fe, y), data = df, weights = if (weighted) ~surface_ref_ha else NULL)
}

# Une ligne par coefficient d'intérêt : estimation, trois inférences, effet en %.
# p-valeurs de Conley : degrés de liberté par défaut de fixest ; noyau uniforme, sans dimension temporelle.
summarise_term <- function(model, df, term, rhs, fe_vars = c("dep_code", "annee"), weighted = TRUE,
                           label = "", conley_km = CONLEY_KM, exposure_2019 = NA, B = 9999,
                           pct_meaningful = TRUE, y = "log_rendement") {
  b <- coef(model)[[term]]
  ct_dep <- coeftable(model, vcov = ~dep_code)[term, ]
  # fixest « corrige » une matrice de Conley non définie positive (avertissement) : on le trace,
  # car les p-valeurs correspondantes ne sont alors pas fiables.
  conley_fixed <- FALSE
  v_con <- withCallingHandlers(
    vcov_conley(model, lat = ~lat_centroide, lon = ~lon_centroide, cutoff = conley_km),
    warning = function(w) {
      if (grepl("positive definite", conditionMessage(w))) {
        conley_fixed <<- TRUE
        invokeRestart("muffleWarning")
      }
    })
  ct_con <- coeftable(model, vcov = v_con)[term, ]
  df_w <- df
  if (!weighted) df_w$surface_ref_ha <- 1
  boot <- wcr_pvalue(df_w, y, term, setdiff(rhs, term), fe_vars, "annee", "surface_ref_ha", B = B)
  data.frame(
    specification = label, terme = term, estimation = b,
    se_cluster_dep = ct_dep[["Std. Error"]], p_cluster_dep = ct_dep[["Pr(>|t|)"]],
    # Matrice de Conley « corrigée » par fixest : erreur-type et p-valeur non fiables -> NA.
    se_conley = if (conley_fixed) NA else ct_con[["Std. Error"]],
    p_conley = if (conley_fixed) NA else ct_con[["Pr(>|t|)"]], conley_km = conley_km,
    conley_non_dp_corrigee = conley_fixed,
    p_wcb_annee = boot$p, p_wcb_annee_unilateral_gauche = boot$p_left, n_grappes_annee = boot$G,
    # Pour les termes d'un polynôme (SWI, SWI²), un « effet en % par unité » n'a pas de sens.
    effet_pct_par_unite = if (pct_meaningful) 100 * (exp(b) - 1) else NA,
    effet_pct_exposition_2019 = 100 * (exp(b * exposure_2019) - 1),
    n = nobs(model), r2_within = unname(r2(model, "wr2")),
    row.names = NULL
  )
}
