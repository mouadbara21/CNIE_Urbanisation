# Prototype Bonita — SP1 « Pré-demande en ligne, contrôle IA des pièces et prise de RDV »

Responsable : **Najib** (réalisation dans Bonita Studio Community 2024.x) · Spécifications : cabinet (Claude) · Démo vidéo : Najib + Zineb

## 0. Mise en route (30 min)
1. Installer Bonita Studio Community (https://www.bonitasoft.com/downloads), lancer, créer le projet `cnie-predemande`.
2. **Importer le processus** : *File → Import → BPMN 2.0* → `modeles/bpmn/SP1_predemande_bonita.bpmn`. Le diagramme arrive avec le pool, 3 lanes et 15 nœuds. Renommer le pool `SP1_PreDemandeCNIE` si besoin.
3. **Créer le BDM** (Development → Business Data Model → Define) d'après la section 2 (ou importer `bonita/bdm/bom.xml` dans un zip nommé `bdm.zip` via *Import*).
4. **Organisation** (Organization → Manage) : créer les utilisateurs du tableau §1, puis *Set as active* et mapper les acteurs.
5. Ajouter les contrats, les variables, les connecteurs et générer les formulaires (§3–§5), puis *Run*.

## 1. Acteurs (lanes → acteurs Bonita)
| Lane BPMN | Acteur Bonita | Utilisateur de démo | Groupe |
|---|---|---|---|
| Citoyen | `Citoyen` (initiateur du processus) | `salma.benali` / `bpm` | /citoyens |
| Agent instructeur | `AgentInstructeur` | `karim.idrissi` / `bpm` | /dgsn/instruction |
| Services automatiques | — (tâches service, pas d'acteur) | — | — |

## 2. BDM (Business Data Model) — package `com.dgsn.cnie.model`
### `DemandeCNIE` (objet racine, variable métier `demande`)
| Champ | Type | Contraintes | Remarque |
|---|---|---|---|
| numeroDemande | STRING(20) | unique, généré | `CNIE-2026-000123` |
| typeDemande | STRING(20) | PREMIERE / RENOUVELLEMENT / DUPLICATA | |
| nomLatin, prenomLatin | STRING(80) | obligatoire | |
| nomArabe, prenomArabe | STRING(80) | obligatoire | saisie arabe |
| dateNaissance | DATE ONLY | obligatoire, ≥ 12 ans pour empreintes | |
| lieuNaissance | STRING(80) | | |
| numeroActeNaissance, anneeActe | STRING(20), INTEGER | | |
| nomPere, nomMere | STRING(80) | | filiation |
| adresse, ville, codeCEDI | STRING | adresse = certificat de résidence | |
| email, telephone | STRING | format vérifié | notifications |
| contactUrgence | STRING(120) | optionnel | stocké sur la puce |
| codeETimbre | STRING(16) | 16 chiffres | 75 DH / 50 DH |
| statut | STRING(20) | voir machine d'états | PRE_DEMANDE → … → RDV_CONFIRME |
| scoreConformite | INTEGER | 0–100 | résultat IA |
| anomalies | TEXT | liste séparée par `;` | |
| dateCreation | DATE-TIME | | |
| pieces | `PieceJustificative` (collection, composition) | | |
| rendezVous | `RendezVous` (composition) | | |

### `PieceJustificative`
| Champ | Type | Remarque |
|---|---|---|
| typePiece | STRING | ACTE_NAISSANCE / CERTIFICAT_RESIDENCE / PHOTO / ANCIENNE_CNIE / DECLARATION_PERTE |
| nomFichier | STRING | document Bonita associé |
| documentId | STRING | référence du document |
| verdictIA | STRING | CONFORME / DOUTE / NON_CONFORME |
| commentaireIA | STRING(255) | ex. « photo : fond non uniforme » |

### `RendezVous`
| Champ | Type |
|---|---|
| codeCEDI, nomCEDI | STRING |
| dateRdv | DATE ONLY |
| creneau | STRING (ex. `09:00-09:20`) |
| recommandeIA | BOOLEAN |
| codeQR | STRING (contenu encodé : numéroDemande|date|creneau) |

### `Centre` (référentiel chargé au démarrage, 6 lignes de démo)
`codeCEDI, nom, ville, capaciteJour, chargePrevue` — ex. `CAS-01, CEDI Casablanca-Anfa, Casablanca, 180, 92` …

## 3. Variables et contrats
- Variable métier : `demande : DemandeCNIE` (instanciée au démarrage à partir du contrat).
- Documents de processus : `docActe`, `docResidence`, `docPhoto` (type *Document*, multiple = non).
- Variables de processus : `verdict : String`, `score : Integer`.

| Tâche | Contrat (entrées) | Opérations (sorties) |
|---|---|---|
| Instanciation / *Saisir la pré-demande* | `demandeInput` (complex) : typeDemande, nomLatin, prenomLatin, nomArabe, prenomArabe, dateNaissance, lieuNaissance, numeroActeNaissance, anneeActe, nomPere, nomMere, adresse, ville, email, telephone, contactUrgence | `demande = new DemandeCNIE(...)`, `statut = "PRE_DEMANDE"`, `numeroDemande` généré (script Groovy : `"CNIE-" + new Date().format("yyyy") + "-" + String.format("%06d", processInstanceId)`) |
| *Téléverser les pièces* | `acteFile`, `residenceFile`, `photoFile` (FILE) | affecte les 3 documents ; crée 3 `PieceJustificative` |
| *[IA] Contrôle IA des pièces* (service) | — | connecteur Groovy §5 → `score`, `verdict`, `demande.scoreConformite`, `demande.anomalies`, `demande.statut = "CONTROLE_IA"` |
| *Corriger les anomalies signalées* | mêmes FILE que l'upload (optionnels) | remplace les documents fournis |
| *Instruire manuellement le dossier* | `decision` (TEXT : VALIDE / A_CORRIGER / REJET), `motif` (TEXT) | `demande.statut` selon décision |
| *Choisir le centre et le créneau recommandé* | `codeCEDI`, `dateRdv` (DATE), `creneau` (TEXT) | `demande.rendezVous = new RendezVous(...)`, `recommandeIA` |
| *Régler les frais (code e-timbre)* | `codeETimbre` (TEXT, 16 chiffres) | `demande.codeETimbre` |
| *Vérifier l'e-timbre et réserver le créneau* (service) | — | script : valide le format (`^\d{16}$`), simule l'appel Trésorerie, `statut = "RDV_CONFIRME"` |
| *Générer le récépissé, le QR code et notifier* (service) | — | `codeQR`, connecteur e-mail (optionnel, SMTP de test) |
| *Consulter la confirmation et le récépissé* | — (lecture seule) | — |

**Conditions des passerelles** (expressions Groovy sur `score` / `decision`) :
- `Score de conformité ?` : `score >= 85` → *conforme* ; `score >= 60 && score < 85` → *doute* ; défaut → *non conforme*.
- `Décision ?` : `decision == "VALIDE"` ; `decision == "A_CORRIGER"` ; défaut → rejet.

## 4. Écrans (UI Designer) — 5 formulaires citoyen + 1 formulaire agent
Charte : bandeau vert institutionnel `#0F6E56`, titres `#1F3B57`, boutons arrondis, logo « CNIE — Portail de pré-demande » (texte), bilingue FR + libellés AR en sous-titre.

### F1 — Pré-demande (instanciation)
- Étape 1/5 « Ma demande » : radio `typeDemande` (Première délivrance / Renouvellement / Duplicata).
- Groupe « Identité » : nomLatin, prenomLatin, nomArabe (dir=rtl), prenomArabe (rtl), dateNaissance (datepicker), lieuNaissance.
- Groupe « État civil et filiation » : numeroActeNaissance, anneeActe, nomPere, nomMere.
- Groupe « Résidence et contact » : adresse (aide : « telle que sur le certificat de résidence »), ville (select), email, telephone, contactUrgence.
- Validation : champs obligatoires, e-mail valide, téléphone `^0[5-7]\d{8}$`, âge ≥ 0. Bouton *Continuer*.

### F2 — Pièces justificatives
- 3 widgets *File upload* : acte de naissance (< 3 mois), certificat de résidence, photo d'identité (JPG/PNG).
- Encadré « Ce que vérifie l'IA » : lisibilité, nom/prénom identiques à la saisie, date < 3 mois, photo : fond uni, visage centré, pas de lunettes teintées.
- Bouton *Soumettre au contrôle automatique*.

### F3 — Résultat du contrôle IA (affiché sur « Corriger les anomalies »)
- Jauge `scoreConformite` (0–100, rouge < 60, orange 60–85, vert > 85).
- Tableau des pièces : type, verdict (badge coloré), commentaire IA.
- Re-upload uniquement des pièces non conformes. Bouton *Renvoyer*.

### F4 — Choix du centre et du créneau
- Select `codeCEDI` alimenté par l'API BDM `../API/bdm/businessData/com.dgsn.cnie.model.Centre?q=find&p=0&c=20`.
- Pour le centre choisi : affichage `chargePrevue` / `capaciteJour` et un bandeau « Créneaux recommandés par l'IA (affluence faible) » listant 3 créneaux ; datepicker + select créneau. Checkbox implicite `recommandeIA` si un créneau recommandé est pris.

### F5 — Paiement e-timbre
- Rappel du montant (75 DH, ou 50 DH si âge < 12 calculé), champ `codeETimbre` (16 chiffres, masque), lien « Acheter un e-timbre ».

### F6 — Confirmation (tâche « Consulter la confirmation »)
- Récapitulatif : numéro de demande, centre, date, créneau, statut `RDV_CONFIRME`, QR code (widget image via `https://api.qrserver.com/v1/create-qr-code/?data=<codeQR>` ou widget QR personnalisé), bouton *Télécharger le récépissé* (PDF facultatif).

### FA — Instruction (agent)
- Lecture seule du dossier (données + aperçu des documents), score et anomalies, radio `decision`, champ `motif`, bouton *Valider*.

## 5. Connecteur « Contrôle IA des pièces » (simulation déterministe, script Groovy)
Objectif démo : produire un score reproductible sans service externe. Règles :
```groovy
int score = 100
def anomalies = []
def nomFichierPhoto = docPhoto?.fileName?.toLowerCase() ?: ""
if (!docActe)       { score -= 40; anomalies << "Acte de naissance manquant" }
if (!docResidence)  { score -= 30; anomalies << "Certificat de résidence manquant" }
if (!docPhoto)      { score -= 30; anomalies << "Photo manquante" }
if (nomFichierPhoto.contains("flou") || nomFichierPhoto.contains("lunettes")) { score -= 25; anomalies << "Photo non conforme (netteté / lunettes)" }
if (docActe?.fileName?.toLowerCase()?.contains("ancien")) { score -= 20; anomalies << "Acte de naissance de plus de 3 mois" }
if (demande.nomLatin?.trim()?.length() < 2) { score -= 15; anomalies << "Nom illisible / incohérent" }
score = Math.max(0, score)
```
Sorties : `score`, `verdict` (`CONFORME` ≥ 85, `DOUTE` 60–84, `NON_CONFORME` < 60), `anomalies.join("; ")`.
> Pour la vidéo : nommer les fichiers de test `acte_naissance.pdf`, `certificat_residence.pdf`, `photo.jpg` (→ 100, conforme) puis `photo_lunettes.jpg` (→ 75, doute → tâche agent) puis omettre un document (→ < 60, correction).

*Option (si temps)* : remplacer le script par un connecteur REST vers un micro-service Python `POST /controle` fourni dans `bonita/ia-service/` (à coder sur demande).

## 6. Scénario de démonstration (3 min dans la vidéo)
1. Connexion `salma.benali` → *Nouvelle demande* → F1 rempli (données de démo) → F2 upload des 3 pièces conformes → contrôle IA → score 100 → F4 choix CEDI Rabat-Agdal, créneau recommandé → F5 code e-timbre `1234567890123456` → F6 confirmation + QR.
2. Deuxième instance avec `photo_lunettes.jpg` → score 75 → bascule vers `karim.idrissi` → FA : décision *A_CORRIGER* → retour citoyen F3 → re-upload → conforme.
3. Montrer dans Bonita Admin la liste des cas, le BDM rempli et le diagramme avec le chemin suivi.

## 7. Captures attendues pour le rapport (`rapport/figures/bonita/`)
`bonita-diagramme.png`, `bonita-bdm.png`, `F1-predemande.png`, `F2-pieces.png`, `F3-resultat-ia.png`, `F4-creneau.png`, `F6-confirmation.png`, `FA-instruction.png`, `bonita-portail-cases.png` (1600 px de large minimum, thème clair).
