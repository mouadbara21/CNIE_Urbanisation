# CNIE-Urbanisation — check-list d'équipe

Voir [PLAN.md](PLAN.md) pour le calendrier et [modeles/referentiel.md](modeles/referentiel.md) pour le vocabulaire commun.

## Ce qui est prêt (généré)
- `modeles/bpmn/*.bpmn` : 3 processus BPMN 2.0 (as-is, to-be, SP1) importables dans Blueworks Live et Bonita.
- `modeles/archimate/cnie.archimate` : modèle ArchiMate complet (143 éléments, 118 relations, 6 vues) à ouvrir dans Archi.
- `rapport/` : rapport LaTeX IEEE complet (11 sections, bibliographie, figures provisoires).
- `bonita/specs/prototype-bonita.md` + `bonita/bdm/bom.xml` : spécifications du prototype.
- `video/script.md` : plan des 20 slides et script minuté par intervenant.

## À faire par l'équipe
### Mouad
- [ ] Dans un terminal (hors Claude) : `miktex packages install ieeetran biblatex-ieee` puis `cd rapport && latexmk -pdf main.tex` ; vérifier ≤ 30 pages.
- [ ] Relire les sections 7–9 (applicatif, technique, trajectoire).

### Najib
- [ ] Créer le compte Blueworks Live (essai), importer `P0_demande_cnie_asis.bpmn` et `P0_demande_cnie_tobe.bpmn`, mettre en page, documenter 5 activités clés (onglet Details), exporter PNG → `rapport/figures/bpmn/` (remplacer les PNG provisoires, mêmes noms).
- [ ] Installer Bonita Studio, importer `SP1_predemande_bonita.bpmn`, créer BDM + formulaires selon `bonita/specs/prototype-bonita.md`, enregistrer la démo (90 s) et les captures listées en §7 de la spec.

### Hafsa
- [ ] Captures d'écran de cnie.ma (accueil, pré-demande, RDV, suivi, cas particuliers) → `sources/captures-cnie/` ; vérifier les points marqués CONFLIT dans `sources/recherche-existant.md` (e-timbre saisi en ligne ou payé au centre ? délai de fabrication ?).
- [ ] Relire les sections 3–6 (existant, stratégie, métier, fonctionnel) et proposer des reformulations personnelles (anti-plagiat : chaque membre doit pouvoir expliquer sa section).

### Zineb
- [ ] Installer Archi, ouvrir `modeles/archimate/cnie.archimate`, ajuster la mise en page si nécessaire, exporter les 6 vues en PNG 300 dpi → `rapport/figures/archimate/` (mêmes noms de fichiers).
- [ ] Valider la direction artistique de la présentation (proposée par Claude), puis préparer le montage vidéo.

## Génération (si on modifie les modèles)
```powershell
python -I outils\gen_bpmn.py
python -I outils\gen_archimate.py
powershell -NoProfile -File outils\export_drawio.ps1 modeles\bpmn\P0_demande_cnie_asis.drawio rapport\figures\bpmn\P0_demande_cnie_asis.png
```
