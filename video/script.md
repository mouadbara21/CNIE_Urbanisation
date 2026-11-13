# Vidéo de démonstration (10 min) — Urbanisation du SI CNIE

Format : enregistrement d'écran des slides + webcam des intervenants (PowerPoint « Enregistrer le diaporama » ou OBS), démos Blueworks et Bonita en capture d'écran, montage par Zineb. Chaque bloc ≈ 2'30. Parler **lentement**, une idée par slide, ne pas lire le rapport.

| Temps | Intervenant | Slides | Message clé |
|---|---|---|---|
| 0:00–0:30 | **Zineb** | 1–2 | Qui nous sommes, la commande, le plan en 5 livrables |
| 0:30–2:30 | **Hafsa** | 3–7 | Existant + diagnostic + stratégie + cas d'usage IA |
| 2:30–5:00 | **Najib** | 8–11 | Processus as-is / to-be (démo Blueworks) |
| 5:00–6:30 | **Hafsa** | 12–13 | Cartographie fonctionnelle (POS) |
| 6:30–8:30 | **Mouad** | 14–17 | Cartographie applicative + démo Bonita (Najib en voix off sur la démo) + architecture technique |
| 8:30–9:30 | **Mouad** | 18 | Trajectoire 2027–2030, gouvernance |
| 9:30–10:00 | **Zineb** | 19–20 | Conclusion, perspectives, remerciements |

## Plan des slides (20)
1. **Titre** — Urbanisation du SI du portail CNIE · équipe · date.
2. **La commande** — DGSN veut un SI plus efficace, réactif, personnalisé, avec IA ; 5 livrables ; notre fil rouge « une CNIE, un processus ».
3. **L'existant en chiffres** — 15 M CNIE2 (85 % des +16 ans), 3,69 M cartes en 2025, TCN depuis 2022, 30+ partenaires, E-Police 2024.
4. **Le parcours actuel** — 7 étapes, 3 ruptures (papier, contrôle tardif, 2e déplacement).
5. **Diagnostic** — SWOT en 4 cases.
6. **Stratégie captée** — Digital Morocco 2030, loi 55-19, priorités DGSN → 5 objectifs G1–G5 + 5 principes.
7. **5 cas d'usage IA** — IA-1 à IA-5, chacun ancré à une étape du processus.
8. **Cartographie métier** — services, acteurs (nouvel acteur : instructeur), P0 et ses 4 sous-processus.
9. **BPMN as-is** (capture Blueworks) — commenter les 3 ruptures.
10. **BPMN to-be** (capture Blueworks) — 6 transformations, 2 nouveaux couloirs.
11. **Démo Blueworks** (30 s vidéo) — navigation dans le blueprint, documentation d'une activité IA.
12. **Cartographie fonctionnelle** — POS 6 zones, 32 blocs, légende E/V/N.
13. **Zoom zone Opérationnelle + Pilotage IA** — ce qui change concrètement.
14. **Cartographie applicative** — 15 composants, moteur BPM + API Gateway au centre.
15. **Démo Bonita** (90 s vidéo) — pré-demande → pièces → score IA → créneau recommandé → QR ; cas « doute » routé vers l'instructeur.
16. **Architecture technique** — zones, cloud souverain, HSM, zone IA sur site.
17. **Sécurité & conformité** — tableau risques/mesures, CNDP, biais des modèles.
18. **Trajectoire** — 3 paliers, 5 chantiers, comité d'architecture + comité d'éthique IA.
19. **Ce que gagne le citoyen / la DGSN** — avant/après en 4 indicateurs.
20. **Conclusion & perspectives** — extension aux autres téléservices DGSN ; merci.

## Script détaillé

### Zineb — Ouverture (0:00–0:30)
« Bonjour. Nous sommes Mouad, Najib, Hafsa et Zineb, et nous jouons le rôle d'un cabinet d'urbanisation mandaté par la DGSN. Notre mission : cartographier le système d'information du portail de la Carte Nationale d'Identité Électronique et proposer un système cible qui intègre l'intelligence artificielle. En dix minutes, nous allons parcourir les cinq livrables : la stratégie, le métier, le fonctionnel, l'applicatif et la technique — avec un seul fil rouge : le processus de demande et de renouvellement de la CNIE. »

### Hafsa — Existant, diagnostic, stratégie (0:30–2:30)
« Quelques chiffres pour situer l'enjeu : la CNIE de nouvelle génération équipe quinze millions de Marocains ; la DGSN en a produit près de 3,7 millions rien qu'en 2025. Depuis 2022, la plateforme Tiers de Confiance National permet de s'authentifier en ligne avec sa carte auprès de plus de trente organismes.
Le portail cnie.ma, lui, impose depuis 2020 une pré-demande et un rendez-vous en ligne. Mais regardez le parcours actuel [slide 4] : après la saisie en ligne, le citoyen imprime et signe un formulaire papier, le contrôle des pièces n'a lieu qu'au guichet — un dossier incomplet signifie un nouveau rendez-vous — et il faut revenir une deuxième fois pour retirer la carte. Trois ruptures de canal.
Notre diagnostic [slide 5] : des forces réelles — couverture nationale, identité numérique souveraine sans registre central — mais un contrôle manuel tardif, des créneaux saturés et des portails en silos.
Nous avons capté la stratégie [slide 6] à partir de Digital Morocco 2030, qui vise le 50e rang mondial en e-gouvernement, de la loi 55-19 sur la simplification, et des priorités de la DGSN sur l'identité numérique. Cela donne cinq objectifs mesurables — par exemple moins de 5 % de dossiers incomplets au guichet — et cinq principes, dont "dites-le nous une fois" et la protection des données dès la conception.
Enfin [slide 7], cinq cas d'usage d'IA, chacun à sa place dans le processus : un assistant multilingue, le contrôle automatique des pièces, la vérification biométrique anti-fraude, la prévision d'affluence, et la détection d'anomalies. »

### Najib — Cartographie métier et BPMN (2:30–5:00)
« La cartographie métier [slide 8] organise le périmètre en cinq services et un processus principal, P0, découpé en quatre sous-processus. Un nouvel acteur apparaît : l'agent instructeur, qui traite à distance les dossiers que l'IA n'a pas pu trancher.
Voici le processus actuel modélisé dans Blueworks Live [slide 9] : quatre couloirs, et vous retrouvez les trois ruptures en rouge.
Et voici le processus cible [slide 10]. Six transformations : on entre par l'identité numérique et la demande est pré-remplie ; les pièces sont contrôlées par l'IA en quelques secondes, avec un score qui route vers la confirmation, la correction ou l'instruction humaine ; le paiement est intégré ; l'IA recommande les créneaux les moins chargés ; au centre, l'agent ne fait plus que la biométrie, vérifiée en temps réel ; et la carte est retirée ou livrée, puis activée dans l'application Mon e-ID.
[Démo Blueworks, slide 11] Dans Blueworks, chaque activité est documentée : ici la tâche de contrôle documentaire, avec ses entrées, ses sorties et son système support. »

### Hafsa — Cartographie fonctionnelle (5:00–6:30)
« Le plan d'occupation des sols [slide 12] regroupe trente-deux blocs fonctionnels en six zones. La légende est simple : jaune pour l'existant conservé, orange pour ce qui évolue, vert pour le nouveau.
[slide 13] Dans la zone opérationnelle, deux blocs nouveaux portent l'essentiel de la valeur : la gestion des pièces avec contrôle IA, et l'instruction des dossiers. La zone pilotage et IA est entièrement nouvelle : tableaux de bord, prévision, détection d'anomalies, et surtout la gouvernance des modèles — indispensable pour utiliser l'IA dans un service régalien. L'enrôlement biométrique et la production, eux, ne changent pas : ils fonctionnent. »

### Mouad — Applicatif, Bonita, technique, trajectoire (6:30–9:30)
« La cartographie applicative [slide 14] traduit ces blocs en quinze composants. Deux choix structurants : un moteur de processus qui orchestre la demande de bout en bout, et une passerelle d'API unique vers l'état civil, l'e-timbre, la Poste et les consulats. Les services d'IA sont des composants autonomes, remplaçables.
[Démo Bonita, slide 15 — Najib en voix off] Nous avons prototypé le sous-processus de pré-demande dans Bonita. Le citoyen saisit sa demande, téléverse ses pièces ; le contrôle IA renvoie un score — ici 100, conforme — puis le système propose les créneaux recommandés, vérifie l'e-timbre et génère un QR code de convocation. Deuxième cas : une photo non conforme, score 75 : la demande part chez l'agent instructeur, qui demande une correction.
[slide 16] L'architecture technique est découpée en zones : exposition avec pare-feu et passerelle, applicative sur Kubernetes avec Bonita et un bus d'événements, données chiffrées, et une zone IA sur site : les données biométriques ne quittent jamais le territoire. Les clés sont protégées par HSM.
[slide 17] Côté sécurité et conformité, chaque risque a sa parade, et chaque modèle d'IA est évalué sur ses biais avant mise en service, avec une décision humaine sur toute alerte.
[slide 18] La trajectoire se déroule en trois paliers : 2027 le socle — BPM, API, contrôle documentaire ; 2028 l'extension — application mobile, assistant, prévision ; 2030 la cible — renouvellement 100 % en ligne et pilotage prédictif. Un comité d'architecture et un comité d'éthique de l'IA, avec la CNDP, gouvernent le programme. »

### Zineb — Conclusion (9:30–10:00)
« [slide 19] Pour le citoyen : un seul déplacement au lieu de deux, un dossier validé avant de partir, des créneaux sans attente. Pour la DGSN : moins de guichets saturés, la fraude détectée à l'enrôlement, et un pilotage par la donnée.
[slide 20] Ce socle est réutilisable pour tous les téléservices de la DGSN. Merci de votre attention. »

## Consignes d'enregistrement
- Résolution 1920×1080, micro proche, pièce calme ; chaque membre enregistre son bloc séparément (PowerPoint → Enregistrer → exporter en MP4), Zineb assemble (CapCut / DaVinci Resolve / Clipchamp).
- Démos : enregistrer l'écran en 1080p (OBS ou Xbox Game Bar Win+G), curseur visible, zoom sur les zones commentées.
- Intercaler le nom de l'intervenant en bas à gauche à chaque changement.
- Exporter en MP4 H.264, < 500 Mo, déposer sur Drive en « lecture pour toute personne disposant du lien ».
