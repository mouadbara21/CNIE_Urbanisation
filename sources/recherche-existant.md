# Notes de recherche — Existant CNIE / DGSN (13 nov. 2026)

> Matière première pour le rapport. Reformuler systématiquement (anti-plagiat), citer la source.
> Le portail cnie.ma n'a pas pu être lu directement (connexion refusée) : les faits « portail » viennent de sites tiers à jour (infopratique.ma 27/09/2026, wadifa-info.com 14/10/2026) → **à vérifier par l'équipe avec des captures d'écran de cnie.ma**.

## 1. Chronologie et chiffres clés

| Date | Fait | Source |
|---|---|---|
| 2020 (loi 04-20) | Loi sur la CNIE : la carte certifie aussi l'identité numérique ; obligatoire dès 16 ans ; anciennes cartes restent valables | bladi.net, medias24 |
| Août 2020 | Lancement de la CNIE 2 (nouvelle génération) ; polycarbonate, impression Lasink (IDEMIA), puce chiffrée, données facultatives (contact d'urgence…) | lematin.ma, fnh.ma, PDF DGSN id4africa |
| Sept. 2020 | Prise de RDV en ligne obligatoire via cnie.ma (exceptions : personnes âgées, malades chroniques, urgences médicales) | telquel.ma, mapnews |
| 28 sept. 2020 | Entrée en vigueur loi 55-19 (simplification des procédures) : portail national des procédures, délais de réponse, numérisation | mmsp.gov.ma, snrtnews |
| Avril 2022 | Lancement ADD-DGSN du service d'identification/authentification « Tiers de Confiance National » (TCN) ; portail identitenumerique.ma ; app « Mon identité numérique » | lavieeco, telquel, lematin |
| Juin 2023 | Présentation DGSN (id4africa) : 15 M de CNIE2 émises, 85 % de la population +16 ans | PDF DGSN |
| 25 sept. 2024 | Stratégie « Digital Morocco 2030 » : 2 axes (services publics numérisés ; économie numérique), objectif EGDI ONU 113e → 50e rang, >600 services déjà numérisés, IA au cœur | hespress, allafrica, ledesk |
| Déc. 2024 | Bilan DGSN 2024 : >30 organismes publics/privés accrédités au TCN (dont Ministère de la Justice) ; reconnaissance faciale et QR codes pour l'authentification des documents | allafrica, lavieeco |
| 20 déc. 2024 | Lancement du portail **E-Police (epolice.ma)** : fiche anthropométrique en ligne via TCN + Identité Numérique ; RDV CNIE ; concours | telquel, medias24, le360 |
| 2025 | ~3,69 M de CNIE produites (2,65 M Rabat, >1 M Marrakech) ; 303 285 cartes pour les MRE ; vérification d'identité à distance en test (lancement grand public annoncé début 2026) | lavieeco, lematin, ecoactu |
| Mai 2026 (JPO DGSN) | Annonces « à venir » : demande de CNIE en ligne via E-Police/cnie.ma, suivi du certificat de résidence, carte numérique dans l'app « Mon e-ID » | infopratique.ma (non confirmé) |
| Nov. 2026 | Fiche anthropométrique en ligne ouverte aux MRE (identification électronique + paiement en ligne) | fnh.ma, lematin |

## 2. Parcours actuel (as-is) d'obtention / renouvellement

1. **Pré-demande sur cnie.ma** (« Créer votre pré-demande ») : type (première délivrance / renouvellement / duplicata perte-vol-détérioration) ; identité, état civil (n° et année d'acte), filiation (parents, grands-parents), adresse telle que sur le certificat de résidence ; saisie **en latin et en arabe** ; e-mail + téléphone ; contact d'urgence optionnel (stocké sur la puce) ; sauvegarde intermédiaire ; **code e-timbre à 16 chiffres** (75 DH ≥ 12 ans, 50 DH < 12 ans) — *conflit* : une source dit paiement au centre.
2. **Numéro de pré-demande** généré ; rubrique « Suivre ou compléter votre demande » ; statuts : *Pré-demande, En cours, Disponible, Remise, Dossier incomplet, Annulée*.
3. **Rendez-vous** : choix d'un CEDI (centre d'enregistrement des données identitaires), date, créneau ; modifiable/annulable ; samedi réservé aux cartes expirées ; disponibilités très inégales selon les centres ; reçu de RDV à conserver ; retard = annulation.
4. **Formulaire** à télécharger, imprimer, signer, joindre au récépissé.
5. **Dépôt au CEDI** en personne (mineur : avec représentant légal) : contrôle des pièces, capture biométrique (photo, empreintes ≥ 12 ans, signature), récépissé daté.
6. **Production** (centres de Rabat et Marrakech) : personnalisation, puce, contrôles.
7. **Retrait** au CEDI avec récépissé ; remise de la carte + code PIN ; notification e-mail/téléphone quand la carte est prête ; statut « Remise ». Délai de fabrication non publié.

**Pièces** (première demande adulte) : extrait/copie intégrale d'acte de naissance (< 3 mois) ou page du livret de famille ; certificat de résidence (Police en urbain, Gendarmerie en rural) ; 4 photos 3,5×4,5 fond gris/bleu clair ; timbre ; naturalisé : document de nationalité. Renouvellement : ancienne carte + justificatifs de changement. Perte/vol : déclaration police/gendarmerie (+ déclaration sur l'honneur selon une source). Mineur : CNIE du représentant légal + preuve de la qualité. MRE : consulat (consulat.ma), attestation d'immatriculation consulaire (watiqa.ma) à la place du certificat de résidence.

**Validité** : 10 ans (≥ 12 ans) ; ≤ 7 ans et jusqu'à la veille des 12 ans pour les enfants.

**Cas particuliers** : « Cas particuliers » sur cnie.ma pour personnes handicapées/alitées/maladies incurables (formalités à domicile ou à l'hôpital) ; PIN perdu → « Demande PIN » / centre.

## 3. Tiers de Confiance National (TCN) — architecture (PDF DGSN, juin 2023)

- Fondé sur la carte : **pas de registre central d'identité numérique, les données sont sur la carte**.
- Le fournisseur de services (FS) doit être **accrédité** ; il délègue l'authentification à la plateforme.
- **8 moyens d'authentification** : carte (NFC), PIN, facial, empreinte, notification mobile, SMS, e-mail, mot de passe.
- **Mode hors ligne** : kits décentralisés, lecture de la carte, saisie automatique des données, authentification PIN/empreinte, consultation asynchrone des révocations (contrôle d'authenticité, enrôlement face à face).
- **Mode en ligne** : toutes les fonctionnalités, intégration via **OpenID Connect** ; flux : 1) connexion au FS, 2) délégation, 3) demande d'authentification au citoyen, 4) envoi des informations, 5) validation/rejet ; consultation de la **base des cartes révoquées**.
- Besoins couverts : authenticité, identité (saisie automatique après consentement), authentification, unicité, révocation, preuve (non-répudiation).
- Côté citoyen (app « Mon identité numérique », AR/FR) : gestion de l'identité (activer/désactiver), consentement, contrôle des moyens d'authentification, contrôle des données (sur la carte, pas sur serveur), système d'alerte (notification à chaque usage), procédure unique.
- Cas d'usage : fiabilisation de données, sécurisation d'un service en ligne (banque), preuve de vie.
- CNDP : consentement systématique ; séparation stockage données d'usage / données d'identification.

## 4. Irritants / limites identifiés (diagnostic)

- Saturation et inégalité des créneaux selon les centres ; intermédiaires payants frauduleux pour les RDV.
- Double saisie (pré-demande en ligne puis formulaire papier à imprimer et signer).
- Contrôle des pièces entièrement manuel au CEDI → « Dossier incomplet » découvert tard, nouveau RDV.
- Pas de contrôle a priori des photos (fond, lunettes) ni de la cohérence AR/latin ; erreurs fréquentes.
- Délai de fabrication non communiqué, suivi par statuts grossiers, pas de notification push.
- Retrait uniquement en personne ; PIN remis sur papier.
- Renouvellement = même parcours complet qu'une première demande, alors que la biométrie existe déjà.
- Silos : cnie.ma, epolice.ma, identitenumerique.ma, consulat.ma, watiqa.ma (e-timbre) → expérience fragmentée.
- Fracture numérique (ruraux, personnes âgées) : besoin d'assistance et de canaux alternatifs.

## 5. Cadre stratégique et réglementaire à citer

- Digital Morocco 2030 (sept. 2024) ; loi 55-19 (simplification, 2020) ; loi 04-20 (CNIE) ; loi 09-08 (données personnelles, CNDP) ; loi 43-20 (services de confiance pour les transactions électroniques) ; loi 05-20 (cybersécurité, DGSSI) ; loi 54-19 (charte des services publics).
- Acteurs : DGSN (propriétaire), Ministère de l'Intérieur, ADD, Ministère de la Transition numérique (DGTN), CNDP, DGSSI, Trésorerie/DGI (e-timbre), Barid Al-Maghrib, consulats (MAE), partenaires accrédités (banques, Justice…).

## 6. Sources (URLs)

- https://telquel.ma/2020/08/31/prise-de-rendez-vous-en-ligne-obligatoire-pour-demander-lobtention-ou-le-renouvellement-de-la-cnie_1694511
- https://medias24.com/2020/10/01/renouvellement-de-la-cnie-des-capacites-sont-ajoutees-pour-faire-face-a-la-demande/
- https://infopratique.ma/administratif/papiers-identite/cnie/
- https://www.wadifa-info.com/fr/service-cnie
- https://www.lavieeco.com/affaires/cnie-le-service-didentification-et-dauthentification-est-officiellement-lance/
- https://telquel.ma/instant-t/2022/04/26/add-dgsn-lancement-du-service-dauthentification-des-usagers-des-services-numeriques_1764625/
- https://id4africa.com/wp-content/uploads/2023/06/PS1-S3-2-Mouhcine-Yejjou-DGSN-Morocco.pdf
- https://fr.allafrica.com/stories/202412250174.html
- https://www.lavieeco.com/pouvoirs/securite/dgsn-hammouchi-devoile-son-bilan-2024/
- https://telquel.ma/instant-t/2024/12/18/la-dgsn-lance-son-portail-e-police_1909402/
- https://medias24.com/2024/12/19/digitalisation-la-dgsn-lance-le-portail-de-services-numeriques-e-police/
- https://lematin.ma/nation/pres-de-5-millions-de-cartes-didentite-electronique-delivrees-en-24-dgsn/257192
- https://fr.hespress.com/387500-387500.html
- https://fr.allafrica.com/stories/202409260555.html
- https://ledesk.ma/2024/09/25/transition-numerique-les-details-de-la-strategie-maroc-digital-2030/
- https://mmsp.gov.ma/sites/default/files/2022-05/DossierPresse_Loi_55-19_SimplificationProceduresFormalitesAdministratives_18012021_Fr.pdf
- https://fnh.ma/article/alaune/carte-d-identite-nationale-idemia-introduit-l-identite-augmentee-au-maroc-entretien
- https://lematin.ma/journal/2020/voici-caracteristiques-nouvelle-generation-cartes-didentite-nationales-electroniques/339323.html
- https://ecoactu.ma/identite-numerique-le-prochain-grand-coup-de-la-dgsn/
