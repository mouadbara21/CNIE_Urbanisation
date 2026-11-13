# Urbanisation du SI du portail CNIE (DGSN) — Plan de travail

**Sujet 2 — E-services dans l'administration marocaine : Portail de la Carte Nationale d'Identité Électronique (cnie.ma)**
Équipe : Mouad · Najib · Hafsa · Zineb — Rendu : **lundi 30 novembre 2026** (rapport ≤ 30 pages + vidéo 10 min, lien Drive)

## Décisions de cadrage (13 nov. 2026)

| Sujet | Décision |
|---|---|
| Processus principal (BPMN as-is / to-be, Blueworks Live) | **Demande & renouvellement de la CNIE** : pré-demande en ligne → RDV → enrôlement biométrique au centre → instruction → production → notification → retrait |
| Sous-processus prototypé (Bonitasoft) | **Pré-demande en ligne + prise de RDV + contrôle IA des pièces** |
| Prototype Bonita | Workflow exécutable + formulaires UI Designer (4–5 écrans) + BDM |
| Rapport | LaTeX, classe IEEEtran (conférence, 2 colonnes), français, ≤ 30 pages, compilé avec MiKTeX (`latexmk`) |
| Présentation | PowerPoint .pptx, ~20 slides, direction artistique inspirée du sujet (document d'identité sécurisé / gov-tech) |
| Vidéo | 10 min, 4 prises de parole ≈ 2'30, démo Blueworks + Bonita |

### Répartition des rôles

| Membre | Responsabilités | Prise de parole vidéo |
|---|---|---|
| **Mouad** | Pilotage, cartographie applicative & architecture technique, intégration LaTeX | Partie 4–5 (applicatif, technique, trajectoire) |
| **Najib** | BPMN sous Blueworks Live, prototype Bonita | Partie 2 + démo (métier, BPMN, Bonita) |
| **Hafsa** | Captation de la stratégie, cartographie fonctionnelle, rédaction | Partie 1 + 3 (stratégie, fonctionnel) |
| **Zineb** | Cas d'usage IA, design de la présentation, montage vidéo | Introduction, IA, conclusion |

## Arborescence du projet

```
CNIE-Urbanisation/
├── PLAN.md                     ← ce fichier
├── rapport/                    ← LaTeX IEEEtran (main.tex, sections/, biblio.bib)
│   └── figures/{archimate,bpmn,bonita,schemas}
├── modeles/
│   ├── archimate/              ← modèle .archimate (Archi) + exports
│   ├── bpmn/                   ← BPMN 2.0 XML (as-is, to-be, sous-processus) à importer dans Blueworks / Bonita
│   └── plantuml/               ← sources .puml des schémas
├── bonita/{specs,bdm}          ← spécifications des écrans, BDM, acteurs, contrats
├── presentation/               ← .pptx + planche de direction artistique
├── video/                      ← script minuté, consignes d'enregistrement
├── sources/{captures-cnie,biblio}
└── outils/                     ← plantuml.jar, scripts de génération
```

## Calendrier (17 jours)

| Phase | Dates | Contenu | Livrables |
|---|---|---|---|
| **0. Cadrage & outillage** | 13–14 nov. | Décisions, arborescence, installation Archi / Bonita Studio / Blueworks Live, PlantUML+Graphviz | Dossier projet, outils prêts |
| **1. Étude de l'existant** | 14–16 nov. | Inventaire e-services cnie.ma + app Identité Numérique, cartographie as-is (4 couches), SWOT | Section « Existant », diagrammes as-is |
| **2. Captation de la stratégie** | 16–17 nov. | Parties prenantes, drivers, objectifs, principes, 5 cas d'usage IA, matrice d'alignement | Section « Stratégie », vue Motivation ArchiMate |
| **3. Cartographie métier** | 17–20 nov. | BPMN as-is & to-be (XML généré → import Blueworks → mise en page) | Section « Métier », 2 BPMN Blueworks |
| **4. Cartographie fonctionnelle** | 20–22 nov. | POS zones/quartiers/îlots/blocs, légende existant / évolué / nouveau | Section « Fonctionnel », carte fonctionnelle |
| **5. Applicatif + Bonita** | 22–26 nov. | Carte applicative cible, flux, prototype Bonita (process, BDM, 5 écrans) | Section « Applicatif », captures Bonita |
| **6. Architecture technique** | 26–27 nov. | Infra cible, sécurité, PKI, biométrie, plateforme IA, déploiement | Section « Technique » |
| **7. Rapport** | 16 → 28 nov. (continu) | Rédaction originale, figures, biblio, compilation, contrôle 30 pages, anti-plagiat | `rapport/main.pdf` |
| **8. Présentation + script** | 26–28 nov. | Direction artistique, PPTX, script 10 min / 4 voix | `.pptx`, `video/script.md` |
| **9. Enregistrement & livraison** | 28–30 nov. | Tournage, montage, upload Drive, check-list | Lien Drive + PDF |

## Phase 0 — Guide d'installation (équipe)

### IBM Blueworks Live (obligatoire pour la cartographie métier)
1. Aller sur <https://www.blueworkslive.com> → *Try it free* (essai 30 jours, e-mail universitaire recommandé) ; un seul compte suffit, inviter les 3 autres comme éditeurs.
2. Créer un *Space* « Urbanisation CNIE », puis deux *Process blueprints* : « Demande CNIE — As-Is » et « Demande CNIE — To-Be ».
3. Importer les fichiers `modeles/bpmn/*.bpmn` (menu *Import → BPMN 2.0*) puis réorganiser les lanes, ajouter la documentation des activités (onglet *Details*), exporter en PNG et en PDF (menu *Export*).

### Bonita Studio Community (obligatoire pour le prototype)
1. Télécharger Bonita Studio Community 2024.x : <https://www.bonitasoft.com/downloads> (Windows 64 bits, ~1 Go, Java embarqué).
2. Créer un projet « cnie-predemande », importer `modeles/bpmn/sous-processus-predemande.bpmn`, créer le BDM d'après `bonita/bdm/`, puis les formulaires dans UI Designer d'après `bonita/specs/`.
3. Lancer (*Run*) : le portail Bonita s'ouvre dans le navigateur ; enregistrer le parcours complet (captures + vidéo).

### Archi (ArchiMate, recommandé par l'enseignant)
1. Télécharger <https://www.archimatetool.com/download/> (Windows 64 bits zip, pas d'installation, Java embarqué).
2. Ouvrir `modeles/archimate/cnie.archimate` fourni ; exporter chaque vue en PNG (*File → Export → View as image*, 300 dpi) vers `rapport/figures/archimate/`.

### Outils en ligne de commande (gérés par Claude)
- MiKTeX (déjà installé) : `latexmk -pdf main.tex` dans `rapport/`.
- PlantUML : `java -jar outils/plantuml.jar -tpng modeles/plantuml/*.puml` (moteur de layout `smetana` si Graphviz absent).

## Fil conducteur des 5 livrables

```
Stratégie (drivers → objectifs → capacités)       Livrable 1
        ↓
Processus « Demande & renouvellement CNIE »        Livrable 2  (BPMN as-is / to-be, Blueworks)
        ↓
Blocs fonctionnels existants / évolués / nouveaux  Livrable 3  (POS fonctionnel)
        ↓
Applications cibles + prototype Bonita            Livrable 4  (sous-processus pré-demande)
        ↓
Infrastructure, sécurité, plateforme IA           Livrable 5
```

### Cas d'usage IA retenus (à valider)
1. **Assistant conversationnel** multilingue (arabe, français, amazighe) sur le portail et l'application mobile.
2. **Contrôle automatique des pièces** : OCR + vérification de cohérence (nom, date, photo conforme ICAO).
3. **Biométrie faciale** : détection de doublons et de tentatives de fraude à l'enrôlement.
4. **Prévision d'affluence** et optimisation dynamique des créneaux de rendez-vous par centre.
5. **Détection d'anomalies** sur les demandes (profils atypiques, documents falsifiés) et pilotage prédictif.

## Structure cible du rapport (IEEEtran, ≤ 30 pages)

1. Résumé / Abstract + mots-clés
2. Introduction (contexte, problématique, objectifs, plan)
3. Cadre méthodologique (urbanisation du SI, démarche en 4 couches, ArchiMate, BPMN, outils)
4. Étude de l'existant (organisation, e-services actuels, cartographie as-is, diagnostic)
5. Captation de la stratégie (orientations, objectifs, IA, principes d'urbanisation)
6. Cartographie métier (processus principal as-is / to-be, BPMN Blueworks)
7. Cartographie fonctionnelle (POS, blocs actuels vs cibles)
8. Cartographie applicative cible + prototype Bonita
9. Architecture technique cible
10. Trajectoire de migration, gouvernance, risques
11. Conclusion et perspectives
12. Références (IEEE)

## Règles de qualité
- Texte 100 % original (outil anti-plagiat annoncé) : aucune phrase copiée des sites ou de documents existants ; les sources sont citées.
- Chaque figure : numérotée, légendée, référencée dans le texte ; export ≥ 300 dpi.
- Cohérence des noms d'acteurs, de processus et de blocs entre les 5 livrables, le rapport et les slides.
- Compilation sans erreur, 30 pages maximum vérifiées à chaque itération.
