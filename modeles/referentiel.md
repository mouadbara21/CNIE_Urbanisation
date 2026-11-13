# Référentiel commun du projet (vocabulaire partagé par les 5 livrables)

Toute entité nommée ici doit porter **le même nom** dans Blueworks, Archi, Bonita, le rapport et les slides.

## Organisation
- **DGSN** — Direction Générale de la Sûreté Nationale (propriétaire du SI CNIE).
- **CEDI** — Centre d'Enregistrement des Données Identitaires (guichet de proximité, ~ par arrondissement/préfecture).
- **CPC** — Centre de Production des Cartes (Rabat, Marrakech).
- **TCN** — plateforme Tiers de Confiance National (identité numérique).

## Acteurs (lanes BPMN / Business Actors ArchiMate)
| Code | Acteur | Rôle |
|---|---|---|
| A1 | Citoyen | Demandeur (adulte, mineur via représentant légal, MRE) |
| A2 | Portail & application CNIE | Canal numérique (cnie.ma, app « Mon e-ID ») — *système, lane technique* |
| A3 | Agent CEDI | Accueil, contrôle, enrôlement biométrique, remise |
| A4 | Agent instructeur (back-office) | Instruction à distance des dossiers signalés — *nouveau (cible)* |
| A5 | Plateforme IA | Services IA (contrôle des pièces, prévision, biométrie, assistant) — *nouveau (cible)* |
| A6 | Centre de production (CPC) | Contrôles d'unicité, personnalisation, expédition |
| A7 | Partenaires externes | Trésorerie (e-timbre), Barid Al-Maghrib (livraison), état civil, consulats, fournisseurs accrédités TCN |

## Processus
- **P0 — Demande & renouvellement de la CNIE** (processus principal, as-is / to-be).
  - SP1 — Pré-demande en ligne, prise de RDV et contrôle des pièces (**prototypé Bonita**)
  - SP2 — Enrôlement au CEDI
  - SP3 — Production et personnalisation
  - SP4 — Notification, remise et activation de l'identité numérique
- Processus de support : gestion des RDV, paiement, notifications, gestion des révocations, pilotage.

## Statuts de la demande
`PRE_DEMANDE → CONTROLE_IA → (A_CORRIGER | A_INSTRUIRE) → RDV_CONFIRME → ENROLE → EN_PRODUCTION → DISPONIBLE → REMISE` ; états terminaux : `ANNULEE`, `REJETEE`.

## Zones fonctionnelles (POS) — légende : [E] existant · [V] à faire évoluer · [N] nouveau
1. **Zone Échange (canaux)** : portail web [V], app mobile « Mon e-ID » [N], assistant conversationnel IA [N], guichet CEDI [E], kits hors-ligne [E], notifications multicanal [V], portail partenaires TCN [E].
2. **Zone Opérationnelle (cœur métier)** : gestion des pré-demandes [V], gestion des pièces & contrôle IA [N], gestion des RDV & créneaux [V], enrôlement biométrique [E], instruction des dossiers [N], production/personnalisation [E], remise & activation [V], gestion des cas particuliers [V], cycle de vie de la carte (révocation, PIN) [E].
3. **Zone Support** : paiement & e-timbre [V], référentiel identité & biométrie (AFIS/ABIS) [E], identité numérique TCN [E], gestion documentaire [N], GRC/réclamations [N].
4. **Zone Pilotage & IA** : tableau de bord & BI [N], prévision d'affluence [N], détection d'anomalies/fraude [N], MLOps & gouvernance des modèles [N].
5. **Zone Ressources** : RH agents, logistique des centres, achats de consommables (cartes vierges) [E].
6. **Zone Référentiels & Échanges** : état civil (RNEC), RNP/RSU, base des cartes révoquées, annuaire des centres, interopérabilité (API gateway) [V].

## Applications cibles (cartographie applicative)
| Code | Application | Statut |
|---|---|---|
| APP-01 | Portail citoyen CNIE (web, AR/FR/Amazigh) | V |
| APP-02 | Application mobile « Mon e-ID » (carte numérique + demandes) | N |
| APP-03 | Assistant conversationnel (LLM + RAG sur la base de connaissances DGSN) | N |
| APP-04 | Moteur BPM (orchestration des demandes — Bonita) | N |
| APP-05 | Service de contrôle documentaire IA (OCR, cohérence, conformité photo ICAO) | N |
| APP-06 | Gestion des rendez-vous & prévision d'affluence | V |
| APP-07 | Poste d'enrôlement CEDI (capture biométrique) | E |
| APP-08 | ABIS / AFIS (dédoublonnage biométrique, détection de fraude faciale) | V |
| APP-09 | Système de production & personnalisation (CPC) | E |
| APP-10 | Plateforme TCN / Identité numérique (OpenID Connect) | E |
| APP-11 | API Gateway & bus d'intégration (état civil, e-timbre, Poste, consulats) | N |
| APP-12 | Notifications multicanal (SMS, e-mail, push) | V |
| APP-13 | Entrepôt de données & BI / plateforme MLOps | N |
| APP-14 | GRC / gestion des réclamations | N |
| APP-15 | Gestion documentaire (GED) & archivage probant | N |

## Cas d'usage IA (CU-IA)
| Code | Cas d'usage | Modèle | Valeur |
|---|---|---|---|
| IA-1 | Assistant conversationnel multilingue | LLM + RAG | Réduire les appels/déplacements, guider la pré-demande |
| IA-2 | Contrôle documentaire automatique | OCR + vision + règles | Détecter tôt les dossiers incomplets, zéro double saisie |
| IA-3 | Vérification biométrique & anti-fraude | Reconnaissance faciale, liveness, dédoublonnage | Unicité, lutte contre l'usurpation |
| IA-4 | Prévision d'affluence & optimisation des créneaux | Séries temporelles | Lisser la charge des CEDI, réduire l'attente |
| IA-5 | Détection d'anomalies & pilotage prédictif | Scoring, détection d'outliers | Priorisation, qualité de service, délais |
