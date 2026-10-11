# ATLAS — Guide de publication (HAL, GitHub, Zenodo)

*Préparé le 2026-10-11. Les dépôts se font avec les comptes de l'auteur : Claude prépare les fichiers, l'auteur valide et dépose. Les intitulés exacts des formulaires HAL et Zenodo sont à vérifier au moment du dépôt.*

## Décisions prises

| Point | Choix |
|---|---|
| Licence du code | MIT (`LICENSE`) |
| Licence du texte et de la documentation | CC BY 4.0 |
| Affiliation | Aucune (chercheur indépendant) |
| Historique Git | Regroupé en un seul commit juste avant la première publication, avec une sauvegarde locale de l'ancien historique |

## État (2026-10-11)

- GitHub : https://github.com/maxime2476/Atlas (public, licence MIT détectée).
- Zenodo : version 1.0.0 archivée, DOI 10.5281/zenodo.23305096 ; DOI de toutes les versions 10.5281/zenodo.23305095.
- Reste : dépôt du PDF sur HAL.

## Étapes, dans l'ordre

1. **GitHub (auteur).** Créer un dépôt **vide** (sans README ni licence), public, par exemple `atlas`, et transmettre son adresse.
2. **Regroupement et envoi (Claude, après accord).**
   - Étiquette de sauvegarde de l'ancien historique (`archive/historique-complet`), conservée en local et non poussée.
   - Un seul commit sur `main`, ajout du remote, puis `git push`.
3. **Zenodo (auteur).**
   - Se connecter à Zenodo avec son compte GitHub et activer le dépôt `atlas` dans l'onglet GitHub de Zenodo.
   - Créer sur GitHub une *release* `v1.0.0`. Zenodo l'archive automatiquement et attribue un DOI. Les métadonnées viennent de `.zenodo.json`.
4. **Mise à jour du mémoire (Claude).**
   - Renseigner `\RepoLink` dans `memoire/main.tex` avec l'adresse GitHub et le DOI Zenodo.
   - Ajouter le DOI au README et à `CITATION.cff`, puis recompiler le PDF.
5. **HAL (auteur).** Déposer le PDF `memoire/main.pdf` avec les métadonnées ci-dessous.

## Métadonnées HAL proposées

- **Type de document :** pré-publication / document de travail.
- **Titre :** *Summer Heat, Irrigation and Crop Yields in France: Pre-specified Estimates and the Empirical Size of Tests in Panels with Common Shocks*.
- **Langue :** anglais.
- **Auteur :** Maxime Gourguechon, sans affiliation.
- **Domaines :** Sciences de l'Homme et Société / Économies et finances ; Sciences de l'environnement (à choisir dans la liste de HAL).
- **Mots-clés :** heat stress ; irrigation ; maize ; France ; panel data ; wild cluster bootstrap ; pre-specification.
- **Codes JEL :** Q15, Q54, C23, C12.
- **Licence :** CC BY 4.0.
- **Lien vers le code :** https://doi.org/10.5281/zenodo.23305096 (version 1.0.0) et https://github.com/maxime2476/Atlas.
- **Résumé anglais :** `memoire/arxiv_abstract.txt` (généré, moins de 1 920 caractères).
- **Résumé français :** à relire par l'auteur.

> L'avantage de rendement du maïs irrigué augmente-t-il avec la chaleur estivale extrême ? À partir des rendements départementaux du maïs grain, publiés séparément pour l'irrigué et le non irrigué (2000-2025), de la réanalyse météorologique SAFRAN-ISBA et d'une chaleur mesurée sur les parcelles de maïs, je compare les deux modes de culture dans un même département et une même année. La spécification a été fixée à l'avance, avec son empreinte dans un journal privé. Dans 17 départements, chaque degré-jour au-delà de 32 °C en juillet-août est associé à un écart de rendement plus large d'environ 1,6 % en faveur du maïs irrigué (bootstrap par année, p = 0,007 ; taille empirique de 3,7 %). Le rendement non irrigué est environ 2,6 fois plus sensible à la chaleur que le rendement irrigué. L'estimation garde son signe sur des années jamais utilisées, avec un effet environ deux fois plus faible, mais elle n'est pas significative avec une météo moyennée sur tout le département, qui sous-estime la chaleur dans les départements de relief. C'est une association, et non l'effet causal de l'irrigation. Sur le plan méthodologique, les erreurs-types regroupées par département ou de Conley rejettent à tort l'hypothèse nulle dans 16 à 56 % des simulations placebo sur ces panels. Les rendements du blé sur 1959-2025 et la prévision hors échantillon donnent des résultats nuls.

*Ce résumé français reprend les chiffres du résumé anglais généré. S'ils changent, il faut le mettre à jour à la main.*

## Après HAL

- Soumettre une communication à une conférence d'économie agricole (par exemple les Journées de recherches en sciences sociales).
- Préparer une version article de 25 à 30 pages pour une revue de spécialité.
