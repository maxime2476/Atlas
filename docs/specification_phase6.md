# ATLAS — Spécification des extensions exploratoires (phase 6), pré-spécifiée

*Rédigée le 2026-10-10, **avant tout calcul** des analyses A et B. Empreinte SHA-256 consignée dans `docs/decisions.md`. Tout ce qui suit est **exploratoire** : aucune conclusion causale.*

## A. Maïs irrigué et non irrigué (hypothèse H4 de la phase 0)

**Question :** l'écart de rendement entre maïs grain irrigué et non irrigué est-il plus grand les étés plus chauds et plus secs ?

**Données :**

- SAA, codes 14 (maïs grain irrigué) et 15 (maïs grain non irrigué), récoltes 2010-2025.
- **Population :** départements métropolitains dont les surfaces moyennes 2010-2012 sont **chacune** d'au moins 1 000 ha (irrigué et non irrigué).
- **Échantillon principal :** statut qualité 1 pour le maïs irrigué. Le statut du non irrigué n'est pas renseigné, et le statut ne décrit que 2025. Robustesse : tous statuts.

**Variable expliquée :** `ecart_dt` = log(Y irrigué) − log(Y non irrigué). Description complémentaire : chacun des deux log-rendements séparément.

**Météo :**

- **pondération surfacique**, faute de masque maïs (les extraits RPG ont été supprimés) : limite à reconnaître ;
- fenêtre **juillet-août** de l'année de récolte, période de floraison et de début de remplissage, la plus sensible au stress hydrique et thermique ;
- régresseurs : `dd_32_ja` (degrés-jours > 32 °C) et `swi_ja` (SWI moyen).

**Modèle :** `ecart` ~ `dd_32_ja` + `swi_ja` | effets fixes département + année, pondéré par la surface moyenne 2010-2012 de maïs grain (irrigué + non irrigué).

**Attendu sous H4 :** coefficient de `dd_32_ja` > 0 et coefficient de `swi_ja` < 0 (plus sec, écart plus grand).

**Inférence :** cluster département, Conley 200 km et WCR par année (poids de Webb, 9 999 tirages). **Conformément au diagnostic de la phase 4, seul le WCR par année est jugé fiable** ; les deux autres sont rapportés pour information.

**Limites connues d'avance :**

- partage irrigué / non irrigué en partie construit par la SAA ;
- composition des surfaces irriguées variable ;
- restrictions d'eau en cas de sécheresse.

L'écart n'est **pas** un effet causal de l'irrigation.

## B. Valorisation en euros des pertes nationales de blé tendre (descriptif)

**Prix :**

- IPPAP annuel du blé tendre (INSEE, idbank `010776425`, base 2020), raccordé au prix absolu Eurostat (`apri_ap_crpouta`, France, €/100 kg) par le rapport moyen de 2012-2016 : **0,2504 €/q par point d'indice**, stable à ±0,0004 sur ces cinq années.
- Les années Eurostat 2010-2011 (rapport ≈ 0,19) ne sont pas utilisées : rupture de série probable, à signaler.

**Perte de l'année *t*, en volume et en valeur (France métropolitaine, blé tendre d'hiver, SAA code 01) :**

- rendement « normal » du département *d* : moyenne de ses rendements 2010-2025 **hors année *t*** ;
- perte en volume : Σ_d (rendement normal − rendement observé) × surface de l'année *t* ;
- perte en valeur : perte en volume × prix de l'année *t*.

**Restitution :** pour toutes les années, avec mise en avant de 2016, 2020 et 2024, et comparaison à la valeur de la production de l'année.

**Interprétation :** c'est l'écart à une année « moyenne », **pas** une perte attribuée à la météo, ni une perte de revenu (le prix réagit lui-même aux récoltes).

## C. NDVI (MODIS / VIIRS / Copernicus)

**Non traité dans cette phase :**

- le téléchargement MODIS (NASA LP DAAC, AppEEARS) exige un compte NASA Earthdata ;
- la continuité de Terra/MODIS après 2025 est incertaine (phase 0) ;
- aucun identifiant n'est disponible dans le projet.

**Procédure proposée, si l'utilisateur crée un compte gratuit :**

1. ranger le jeton dans `.env` (non versionné ; modèle dans `.env.example`) ;
2. NDVI MOD13Q1 v6.1 à 250 m, composites de 16 jours, avril-juin, masqué sur les parcelles BTH du RPG ;
3. variable prédictive seulement (phase 5), jamais causale.
