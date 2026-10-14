# Revues simulées du mémoire (2026-10-14)

Ces rapports viennent de quatre skills publics pour Claude Code, appliqués au mémoire (`memoire/main.pdf`, état du 2026-10-14) par une IA. Ils ont été écrits avant les corrections décrites plus bas.

**Ce ne sont pas des revues par des pairs** : un seul modèle a tenu tous les rôles, sans indépendance réelle entre les relecteurs.

| Fichier | Skill | Ce qu'il fait |
|---|---|---|
| `2026-10-14_1_econ-review_*.md` | hanlulong/econ-paper-review-skill | Rapport d'arbitre, remarques de rédaction, plan de corrections |
| `2026-10-14_2_ai-research-feedback.md` | claesbackman/AI-research-feedback (`review-paper`) | Revue de pré-soumission en 8 rôles |
| `2026-10-14_3_claude-workflow.md` | nemmerel/claude-workflow (`/research-excellence`) | Barèmes de qualité, audit de réplication (25 chiffres recalculés) |
| `2026-10-14_4_literature-review.md` | chenlu-hung/literature-review | Recherche documentée (OpenAlex, Crossref, Semantic Scholar), vérification des DOI |

**Ce qui n'a pas été exécuté.** Les validateurs, finaliseurs et correcteurs automatiques des skills tiers, ainsi que le modèle de projet claude-workflow (hooks et règles). Les recherches brutes au format JSON de la revue 4 ne sont pas versionnées.

**Suites données** (voir `docs/decisions.md`, « Revues simulées du 2026-10-14 ») :
- textes corrigés : littérature, limites des projections, unité du résultat, notes et libellés de tableaux, renvois, borne basse de la valeur par m³ ;
- deux analyses déclarées avant calcul : la taille du jackknife CV3 (V1 : 7,3 %, « à peu près calibré ») et les signatures d'imputation de la ventilation irrigué/pluvial de la SAA (V2 : signature retenue dans l'ancienne série ; menace « active » selon la règle).

Les remarques mineures (notation, termes, verbes, notes de tableaux, figures) ont ensuite été traitées. Les analyses nouvelles suggérées (moyenne SAFRAN/E-OBS, hétérogénéité selon le statut de qualité, humidité du sol dans les projections) n'ont pas été faites.

**Erreur connue dans ces rapports.** La revue 2 (section 3, point 6) affirme que l'hypothèse « même dose pour toutes les cultures » gonflerait la dose du maïs. C'est l'inverse : si le maïs reçoit plus d'eau par hectare que les autres cultures, sa dose est sous-estimée et la valeur par m³ surestimée. Le mémoire écrit le sens correct.
