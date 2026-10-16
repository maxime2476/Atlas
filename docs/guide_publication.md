# ATLAS — Guide de publication (HAL, GitHub, Zenodo)

*Préparé le 2026-10-11. Les dépôts se font avec les comptes de l'auteur : Claude prépare les fichiers, l'auteur valide et dépose. Les intitulés exacts des formulaires HAL et Zenodo sont à vérifier au moment du dépôt.*

## Décisions prises

| Point | Choix |
|---|---|
| Licence du code | MIT (`LICENSE`) |
| Licence du texte et de la documentation | CC BY 4.0 |
| Affiliation | Aucune (chercheur indépendant) |
| Historique Git | Regroupé en un seul commit au moment de la publication finale. L'historique de travail est conservé en privé par l'auteur (étiquette locale) ; les dates des décisions sont celles consignées dans le journal, que Git ne permet pas de vérifier |

## État (2026-10-12)

- GitHub : https://github.com/maxime2476/Atlas (public, licence MIT détectée).
- Zenodo : archive créée ; le mémoire et le README citent le DOI de concept 10.5281/zenodo.23305095, qui renvoie toujours à la dernière archive.
- Reste : regroupement final de l'historique en un seul commit et envoi (auteur) ; mise à jour de l'archive Zenodo ; dépôt du PDF sur HAL, puis ajout de l'identifiant HAL au README et à `CITATION.cff`.

## Étapes, dans l'ordre

1. **GitHub (auteur).** ~~Créer un dépôt vide et public~~ : fait (`maxime2476/Atlas`).
2. **Regroupement et envoi (auteur), à la fin du projet.**
   - Étiquette de sauvegarde de l'historique de travail, conservée en local et non poussée.
   - Un seul commit sur `main`, puis envoi sur GitHub (qui remplace l'historique publié).
3. **Zenodo (auteur).**
   - Le dépôt `Atlas` est déjà relié à Zenodo. Une *release* GitHub déclenche l'archivage ; le DOI de concept cité dans le mémoire reste valable.
4. **Mise à jour du mémoire** : fait.
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
- **Lien vers le code :** https://doi.org/10.5281/zenodo.23305095 et https://github.com/maxime2476/Atlas.
- **Résumé anglais :** le résumé complet du PDF (recommandé : c'est la version relue), ou sa version courte `memoire/arxiv_abstract.txt` (générée par le script 26, avec les mêmes réserves).
- **Résumé français :** à relire par l'auteur.

> L'avantage de rendement du maïs irrigué augmente-t-il avec la chaleur estivale extrême ? À partir des rendements départementaux du maïs grain, publiés séparément pour l'irrigué et le non irrigué (2000-2025), de la réanalyse météorologique SAFRAN-ISBA et d'une chaleur mesurée sur les parcelles de maïs, je compare les deux modes dans un même département et une même année. La spécification a été écrite après une analyse exploratoire de 2010-2025 et avant toute estimation sur 2000-2009 ; elle est publiée avec les résultats, de sorte que cet ordre repose sur le journal de l'auteur. Dans 17 départements, hors Sud-Ouest, chaque degré-jour au-delà de 32 °C en juillet-août est associé à un écart de rendement plus large d'environ 1,6 % en faveur du maïs irrigué (bootstrap par année unilatéral, p = 0,007). La règle fixée d'avance est remplie, mais 62 % de l'échantillon vient des années exploratoires. La seule preuve nouvelle, 2000-2009, garde le signe à environ la moitié de l'estimation, un écart dû à 2003 (p = 0,049, puissance d'environ 11 %), et ne tient pas avec une chaleur moyennée sur tout le département. Sans les six départements de relief, l'estimation n'est pas significative (p = 0,146), sans que les pentes des deux groupes diffèrent de façon détectable ; avec un jackknife par grappes, plus conservateur, le test principal ne l'est pas non plus (p = 0,074). Le résultat tient avec les températures E-OBS. L'interaction pré-spécifiée avec les restrictions d'eau de niveau crise a le signe opposé à l'hypothèse. C'est une association, et non l'effet causal de l'irrigation. Sur ces panels, les erreurs-types regroupées par département, ou de Conley à noyau uniforme de 200 km, rejettent à tort l'hypothèse nulle dans 17 à 63 % des simulations placebo. Les rendements du blé sur 1959-2025 et la prévision hors échantillon donnent des résultats nuls.

*Ce résumé français reprend les chiffres du résumé anglais généré. S'ils changent, il faut le mettre à jour à la main.*

## Après HAL

- Soumettre une communication à une conférence d'économie agricole (par exemple les Journées de recherches en sciences sociales).
- Préparer une version article de 25 à 30 pages pour une revue de spécialité.
