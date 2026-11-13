"""Construit la présentation (20 slides, style « Document sécurisé ») avec python-pptx.
Usage : python outils/build_deck.py  -> presentation/CNIE_Urbanisation.pptx
"""
import os

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "presentation", "assets")
FIG = os.path.join(ROOT, "rapport", "figures")
OUT = os.path.join(ROOT, "presentation", "CNIE_Urbanisation.pptx")

# ---- palette « Document sécurisé »
NAVY = RGBColor(0x0B, 0x1F, 0x3A)
NAVY2 = RGBColor(0x13, 0x2A, 0x4F)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
GREEN = RGBColor(0x2E, 0x8B, 0x6E)
ICE = RGBColor(0xE8, 0xEE, 0xF6)
INK = RGBColor(0x1B, 0x24, 0x30)
MUTED = RGBColor(0x6B, 0x76, 0x86)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
CARD_DARK = RGBColor(0x16, 0x30, 0x58)
RED = RGBColor(0xC6, 0x28, 0x28)
ORANGE = RGBColor(0xE0, 0x8A, 0x2E)
YEL = RGBColor(0xFF, 0xF4, 0xB5)
ORA = RGBColor(0xFF, 0xD3, 0x8A)
GRN = RGBColor(0xB9, 0xF0, 0xB9)
HEAD = "Cambria"
BODY = "Calibri"
MONO = "Courier New"

SW, SH = 13.333, 7.5
prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]
TOTAL = 20
_n = [0]


# ---------------------------------------------------------------- helpers
def text(slide, x, y, w, h, s, size=16, bold=False, color=INK, font=BODY, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False, spacing=None, line=1.0, margin=0.0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = anchor
    lines = s if isinstance(s, list) else [s]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line
        if spacing:
            p.space_after = Pt(spacing)
        runs = ln if isinstance(ln, list) else [(ln, {})]
        for rt, ro in runs:
            r = p.add_run()
            r.text = rt
            f = r.font
            f.name = ro.get("font", font)
            f.size = Pt(ro.get("size", size))
            f.bold = ro.get("bold", bold)
            f.italic = ro.get("italic", italic)
            f.color.rgb = ro.get("color", color)
    return tb


def bullets(slide, x, y, w, h, items, size=15, color=INK, gap=6, bullet="▪", bcolor=GOLD):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r0 = p.add_run()
        r0.text = bullet + "  "
        r0.font.color.rgb = bcolor
        r0.font.size = Pt(size)
        r0.font.name = BODY
        runs = it if isinstance(it, list) else [(it, {})]
        for rt, ro in runs:
            r = p.add_run()
            r.text = rt
            r.font.name = BODY
            r.font.size = Pt(ro.get("size", size))
            r.font.bold = ro.get("bold", False)
            r.font.color.rgb = ro.get("color", color)
    return tb


def rect(slide, x, y, w, h, fill, line=None, radius=False, shadow=False, lw=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    if radius:
        shp.adjustments[0] = 0.08
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    if not shadow:
        shp.shadow.inherit = False
    shp.text_frame.text = ""
    return shp


def picture_fit(slide, path, x, y, w, h, align="center"):
    """Insère une image dans la boîte (x,y,w,h) en conservant les proportions."""
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    px = x + (w - pw) / 2 if align == "center" else x
    py = y + (h - ph) / 2
    return slide.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(ph))


def chip_number(slide, x, y, num, dark=False):
    slide.shapes.add_picture(os.path.join(ASSETS, "chip.png"), Inches(x), Inches(y), Inches(0.62), Inches(0.465))
    text(slide, x, y, 0.62, 0.465, num, size=13, bold=True, color=NAVY, font=MONO, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def new_slide(kicker, title, dark=False, notes=""):
    _n[0] += 1
    s = prs.slides.add_slide(BLANK)
    s.shapes.add_picture(os.path.join(ASSETS, "bg_dark.png" if dark else "bg_light.png"), 0, 0, prs.slide_width, prs.slide_height)
    tcol = ICE if dark else NAVY
    if title:
        chip_number(s, 0.6, 0.5, f"{_n[0]:02d}")
        text(s, 1.4, 0.48, 10, 0.3, kicker, size=11, bold=True, color=GOLD, font=BODY)
        text(s, 1.4, 0.74, 11.2, 0.8, title, size=28, bold=True, color=tcol, font=HEAD, anchor=MSO_ANCHOR.TOP)
    # pied MRZ
    mrz = "P<MAR<URBANISATION<SI<CNIE<<DGSN<<CABINET<<2026"
    mrz = mrz + "<" * (74 - len(mrz)) + f"{_n[0]:02d}<{TOTAL}"
    text(s, 0.6, 7.05, 12.1, 0.3, mrz, size=10, color=(GOLD if dark else MUTED), font=MONO)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def card(slide, x, y, w, h, title, body, dark=False, accent=GOLD, tsize=14, bsize=12.5):
    rect(slide, x, y, w, h, CARD_DARK if dark else CARD, line=(GOLD if dark else RGBColor(0xD9, 0xDE, 0xE6)), radius=True)
    rect(slide, x + 0.18, y + 0.2, 0.28, 0.06, accent)
    text(slide, x + 0.18, y + 0.32, w - 0.36, 0.5, title, size=tsize, bold=True, color=(ICE if dark else NAVY), font=HEAD)
    text(slide, x + 0.18, y + 0.82, w - 0.36, h - 0.95, body, size=bsize, color=(ICE if dark else INK), line=1.05)


def stat(slide, x, y, w, value, label, dark=False):
    text(slide, x, y, w, 0.9, value, size=44, bold=True, color=(GOLD if dark else NAVY), font=HEAD)
    text(slide, x, y + 0.95, w, 0.7, label, size=13, color=(ICE if dark else MUTED))


def legend(slide, x, y):
    for i, (c, lab) in enumerate(((YEL, "existant"), (ORA, "à faire évoluer"), (GRN, "nouveau"))):
        rect(slide, x + i * 1.75, y + 0.05, 0.22, 0.18, c, line=MUTED, lw=0.5)
        text(slide, x + i * 1.75 + 0.3, y, 1.4, 0.3, lab, size=11, color=MUTED)


# ================================================================ slides
# 1 — Titre
s = new_slide("", "", dark=True, notes="Zineb : qui nous sommes, la commande, le plan en 5 livrables.")
s.shapes.add_picture(os.path.join(ASSETS, "rosette.png"), Inches(8.3), Inches(0.9), Inches(5.2), Inches(5.2))
s.shapes.add_picture(os.path.join(ASSETS, "card_frame.png"), Inches(0.6), Inches(1.1), Inches(7.6), Inches(4.8))
s.shapes.add_picture(os.path.join(ASSETS, "chip.png"), Inches(1.05), Inches(1.55), Inches(0.95), Inches(0.71))
text(s, 2.2, 1.5, 5.5, 0.35, "ROYAUME DU MAROC · DGSN · PROJET D'URBANISATION", size=11, bold=True, color=GOLD)
text(s, 1.05, 2.45, 6.7, 1.9, "Urbanisation du SI du portail de la Carte Nationale d'Identité Électronique",
     size=30, bold=True, color=ICE, font=HEAD, line=1.0)
text(s, 1.05, 4.2, 6.7, 0.6, "Cartographie de l'existant · système cible · intelligence artificielle", size=14, color=GOLD, italic=True)
text(s, 1.05, 4.95, 6.7, 0.4, "Mouad · Najib · Hafsa · Zineb", size=15, bold=True, color=ICE)
text(s, 1.05, 5.3, 6.7, 0.4, "E-services dans l'administration marocaine — sujet 2 · novembre 2026", size=12, color=ICE)
text(s, 0.6, 6.25, 7.6, 0.4, "SUJET<2<<CNIE<<DEMANDE<ET<RENOUVELLEMENT<<<<<<<<<<<<<<", size=11, color=GOLD, font=MONO)

# 2 — La commande
s = new_slide("CONTEXTE", "La commande du cabinet d'urbanisation", dark=True,
              notes="Zineb : la DGSN veut un SI plus efficace, réactif, personnalisé, avec IA. Cinq livrables, un seul fil rouge : le processus de demande et de renouvellement de la CNIE.")
text(s, 1.4, 1.65, 11, 0.8, [[("Objectif : ", {"bold": True, "color": GOLD}), ("un SI plus efficace, plus réactif et plus personnalisé, intégrant l'intelligence artificielle — sans rupture de service.", {})]], size=15, color=ICE)
livr = [("01", "Stratégie", "Captation des nouvelles orientations"), ("02", "Métier", "BPMN as-is / to-be sous Blueworks Live"),
        ("03", "Fonctionnel", "Plan d'occupation des sols, blocs actuels / cibles"), ("04", "Applicatif", "Cartographie cible + prototype Bonita"),
        ("05", "Technique", "Architecture cible, sécurité, IA")]
for i, (n, t, d) in enumerate(livr):
    x = 0.6 + i * 2.5
    card(s, x, 2.75, 2.3, 1.9, t, d, dark=True, tsize=16)
    text(s, x + 0.18, 2.9, 1, 0.3, n, size=11, bold=True, color=GOLD, font=MONO)
rect(s, 0.6, 5.05, 12.1, 0.85, CARD_DARK, line=GOLD, radius=True)
text(s, 0.85, 5.12, 11.6, 0.7, [[("Fil rouge : ", {"bold": True, "color": GOLD}), ("« une CNIE, un processus » — chaque livrable décline le même processus P0, de la stratégie jusqu'à la technique.", {})]],
     size=14, color=ICE, anchor=MSO_ANCHOR.MIDDLE)

# 3 — Existant en chiffres
s = new_slide("EXISTANT", "La CNIE en chiffres",
              notes="Hafsa : 15 M de CNIE2 (85 % des +16 ans), 3,69 M produites en 2025, Tiers de Confiance National depuis 2022 avec plus de 30 partenaires, E-Police lancé fin 2024.")
stats = [("15 M", "cartes de nouvelle génération émises (2023)"), ("85 %", "de la population de plus de 16 ans équipée"),
         ("3,69 M", "cartes produites en 2025 (Rabat + Marrakech)"), ("30+", "organismes accrédités au Tiers de Confiance National")]
for i, (v, l) in enumerate(stats):
    stat(s, 0.7 + i * 3.1, 1.75, 2.8, v, l)
rect(s, 0.6, 4.0, 12.1, 2.7, CARD, line=RGBColor(0xD9, 0xDE, 0xE6), radius=True)
text(s, 0.85, 4.15, 6, 0.35, "Chronologie", size=14, bold=True, color=NAVY, font=HEAD)
tl = [("2020", "CNIE 2 (loi 04-20) ; pré-demande et RDV en ligne obligatoires sur cnie.ma ; loi 55-19"),
      ("2022", "Plateforme Tiers de Confiance National (DGSN + ADD), app « Mon identité numérique »"),
      ("2024", "Digital Morocco 2030 (113e → 50e rang EGDI) ; portail E-Police"),
      ("2025", "Vérification d'identité à distance en test ; annonces JPO 2026 : demande de CNIE en ligne")]
for i, (yr, d) in enumerate(tl):
    x = 0.85 + i * 2.95
    rect(s, x, 4.65, 0.14, 0.14, GOLD)
    if i < 3:
        rect(s, x + 0.14, 4.71, 2.81, 0.02, GOLD)
    text(s, x, 4.9, 2.7, 0.35, yr, size=15, bold=True, color=NAVY, font=HEAD)
    text(s, x, 5.25, 2.7, 1.3, d, size=11.5, color=INK, line=1.05)

# 4 — Parcours actuel
s = new_slide("EXISTANT", "Le parcours actuel du citoyen : sept étapes, trois ruptures",
              notes="Hafsa : après la saisie en ligne, formulaire papier à imprimer ; contrôle des pièces seulement au guichet ; deuxième déplacement pour le retrait.")
steps = ["Pré-demande sur cnie.ma", "Choix du CEDI et du créneau", "Impression et signature du formulaire", "Dépôt et contrôle manuel au guichet",
         "Capture biométrique", "Production (Rabat / Marrakech)", "Retrait au CEDI avec récépissé"]
rupt = {2: "Rupture 1 : retour au papier", 3: "Rupture 2 : dossier incomplet découvert trop tard", 6: "Rupture 3 : second déplacement"}
for i, st in enumerate(steps):
    x = 0.6 + i * 1.75
    bad = i in rupt
    rect(s, x, 2.2, 1.6, 1.45, CARD, line=(RED if bad else RGBColor(0xD9, 0xDE, 0xE6)), radius=True, lw=(1.5 if bad else 0.75))
    text(s, x + 0.12, 2.28, 1.36, 0.3, f"{i+1:02d}", size=11, bold=True, color=GOLD, font=MONO)
    text(s, x + 0.12, 2.58, 1.36, 1.0, st, size=12, bold=True, color=NAVY, line=1.05)
    if i < 6:
        text(s, x + 1.58, 2.65, 0.2, 0.5, "›", size=22, color=GOLD, align=PP_ALIGN.CENTER)
for i, (k, v) in enumerate(rupt.items()):
    x = 0.6 + i * 4.05
    rect(s, x, 4.3, 3.85, 1.25, RGBColor(0xFD, 0xEC, 0xEC), line=RED, radius=True)
    text(s, x + 0.2, 4.4, 3.5, 1.05, [[(v.split(" : ")[0], {"bold": True, "color": RED}), ("\n" + v.split(" : ")[1], {})]], size=13, color=INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 5.85, 12, 0.9, "Six statuts de suivi, aucun délai annoncé, e-timbre de 75 DH acheté à part, portails séparés (cnie.ma, epolice.ma, identitenumerique.ma).",
     size=13, color=MUTED, italic=True)

# 5 — Diagnostic
s = new_slide("DIAGNOSTIC", "Diagnostic de l'existant",
              notes="Hafsa : forces réelles (couverture, identité numérique souveraine sans registre central), mais contrôle manuel tardif, créneaux saturés, silos.")
sw = [("Forces", "Couverture nationale quasi complète · RDV en ligne généralisé · plateforme d'identité souveraine, sans registre central, 30+ partenaires · production éprouvée", GREEN),
      ("Faiblesses", "Contrôle des pièces manuel et tardif · double saisie (portail puis papier) · suivi grossier, délai inconnu · renouvellement aussi lourd qu'une première demande · canaux en silos", RED),
      ("Opportunités", "Digital Morocco 2030 et loi 55-19 · maturité de l'OCR, de la vision et des modèles de langue · app mobile comme canal unique · historique des RDV exploitable", GOLD),
      ("Menaces", "Fraude documentaire et usurpation · saturation aux pics de renouvellement · fracture numérique · exigences CNDP / DGSSI, biais des modèles biométriques", NAVY)]
for i, (t, b, c) in enumerate(sw):
    x = 0.6 + (i % 2) * 6.15
    y = 1.75 + (i // 2) * 2.55
    card(s, x, y, 5.95, 2.35, t, b, accent=c, tsize=16, bsize=13)

# 6 — Stratégie
s = new_slide("STRATÉGIE", "Stratégie captée : cinq objectifs, cinq principes",
              notes="Hafsa : Digital Morocco 2030, loi 55-19, priorités DGSN → G1–G5 mesurables et 5 principes d'urbanisation.")
text(s, 0.6, 1.7, 3.6, 0.35, "Moteurs", size=14, bold=True, color=NAVY, font=HEAD)
bullets(s, 0.6, 2.1, 3.6, 3.5, [[("Digital Morocco 2030", {"bold": True}), (" : 50e rang EGDI, IA au centre", {})],
                                  [("Loi 55-19", {"bold": True}), (" : simplification, « dites-le nous une fois »", {})],
                                  [("DGSN", {"bold": True}), (" : identité numérique généralisée, lutte contre la fraude", {})],
                                  [("Qualité de service", {"bold": True}), (" : attente, délais, inclusion", {})]], size=13, gap=8)
text(s, 4.5, 1.7, 8, 0.35, "Objectifs du système cible", size=14, bold=True, color=NAVY, font=HEAD)
goals = [("G1", "Démarche 100 % en ligne jusqu'à la biométrie ; renouvellement sans déplacement"),
         ("G2", "Délai et attente divisés par deux : < 5 % de dossiers incomplets au guichet, < 15 min en centre"),
         ("G3", "Unicité garantie, fraude détectée dès l'enrôlement"),
         ("G4", "Identité numérique activée pour chaque carte (> 80 %)"),
         ("G5", "Pilotage par la donnée et l'IA")]
for i, (g, d) in enumerate(goals):
    y = 2.1 + i * 0.66
    rect(s, 4.5, y, 0.62, 0.52, NAVY, radius=True)
    text(s, 4.5, y, 0.62, 0.52, g, size=12, bold=True, color=GOLD, font=MONO, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 5.25, y, 7.4, 0.52, d, size=12.5, color=INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 5.6, 6, 0.35, "Principes d'urbanisation", size=14, bold=True, color=NAVY, font=HEAD)
for i, p in enumerate(["Dites-le nous une fois", "Données protégées dès la conception", "Souveraineté et sécurité", "API d'abord", "Multicanal inclusif"]):
    x = 0.6 + i * 2.45
    rect(s, x, 6.0, 2.3, 0.6, CARD, line=GOLD, radius=True)
    text(s, x, 6.0, 2.3, 0.6, p, size=11.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 7 — Cas d'usage IA
s = new_slide("INTELLIGENCE ARTIFICIELLE", "Cinq cas d'usage d'IA, chacun à sa place dans le processus",
              notes="Hafsa : assistant multilingue, contrôle automatique des pièces, biométrie anti-fraude, prévision d'affluence, détection d'anomalies.")
ia = [("IA-1", "Assistant conversationnel multilingue", "Modèle de langue + base de connaissances DGSN", "Saisie de la pré-demande", "G1, G2"),
      ("IA-2", "Contrôle documentaire automatique", "OCR, cohérence avec la saisie, photo conforme ICAO", "Dès le téléversement des pièces", "G2"),
      ("IA-3", "Vérification biométrique anti-fraude", "Dédoublonnage facial, détection du vivant", "Enrôlement au CEDI", "G3"),
      ("IA-4", "Prévision d'affluence", "Séries temporelles par centre, créneaux recommandés", "Prise de rendez-vous", "G2, G5"),
      ("IA-5", "Détection d'anomalies et pilotage", "Scoring des demandes, suivi prédictif des délais", "Back-office et pilotage", "G3, G5")]
text(s, 1.55, 1.65, 3.6, 0.3, "Cas d'usage", size=11, bold=True, color=MUTED)
text(s, 5.3, 1.65, 3.6, 0.3, "Technique", size=11, bold=True, color=MUTED)
text(s, 9.0, 1.65, 2.6, 0.3, "Étape du processus", size=11, bold=True, color=MUTED)
text(s, 11.7, 1.65, 1, 0.3, "Objectif", size=11, bold=True, color=MUTED)
for i, (c, t, tech, step, g) in enumerate(ia):
    y = 2.05 + i * 0.95
    rect(s, 0.6, y, 12.1, 0.8, CARD, line=RGBColor(0xD9, 0xDE, 0xE6), radius=True)
    rect(s, 0.75, y + 0.17, 0.68, 0.46, GREEN, radius=True)
    text(s, 0.75, y + 0.17, 0.68, 0.46, c, size=11, bold=True, color=WHITE, font=MONO, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 1.55, y, 3.6, 0.8, t, size=13.5, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 5.3, y, 3.6, 0.8, tech, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.0, y, 2.6, 0.8, step, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 11.7, y, 1, 0.8, g, size=12, bold=True, color=GOLD, anchor=MSO_ANCHOR.MIDDLE)

# 8 — Cartographie métier
s = new_slide("CARTOGRAPHIE MÉTIER", "Services, acteurs et processus du système cible",
              notes="Najib : cinq services, processus P0 en quatre sous-processus ; nouvel acteur : l'agent instructeur.")
picture_fit(s, os.path.join(FIG, "archimate", "V2_metier.png"), 0.6, 1.7, 8.0, 5.1)
card(s, 8.9, 1.75, 3.8, 1.45, "5 services métier", "Demande et renouvellement · rendez-vous · suivi · identité numérique · authentification des partenaires", bsize=12)
card(s, 8.9, 3.35, 3.8, 1.45, "P0 = 4 sous-processus", "SP1 pré-demande et contrôle IA (nouveau) · SP2 enrôlement · SP3 production · SP4 remise et activation", bsize=12)
card(s, 8.9, 4.95, 3.8, 1.5, "Nouvel acteur", "L'agent instructeur traite à distance les dossiers que l'IA ne tranche pas : la charge quitte le guichet.", accent=GREEN, bsize=12)

# 9 — BPMN as-is
s = new_slide("CARTOGRAPHIE MÉTIER", "Processus actuel (as-is) modélisé sous Blueworks Live",
              notes="Najib : quatre couloirs ; on retrouve les trois ruptures : papier, contrôle tardif, second déplacement.")
picture_fit(s, os.path.join(FIG, "bpmn", "P0_demande_cnie_asis.png"), 0.6, 1.7, 12.1, 3.6)
for i, (t, d) in enumerate([("Papier", "le formulaire est imprimé et signé après la saisie en ligne"), ("Contrôle tardif", "les pièces ne sont vérifiées qu'au guichet : nouveau RDV si dossier incomplet"), ("Second déplacement", "retrait de la carte et PIN uniquement au CEDI")]):
    x = 0.6 + i * 4.05
    rect(s, x, 5.5, 3.85, 1.25, RGBColor(0xFD, 0xEC, 0xEC), line=RED, radius=True)
    text(s, x + 0.2, 5.58, 3.5, 1.1, [[(t, {"bold": True, "color": RED}), ("\n" + d, {})]], size=12.5, color=INK, anchor=MSO_ANCHOR.MIDDLE)

# 10 — BPMN to-be
s = new_slide("CARTOGRAPHIE MÉTIER", "Processus cible (to-be) : six transformations",
              notes="Najib : entrée par l'identité numérique, contrôle IA des pièces, paiement intégré, créneaux recommandés, enrôlement allégé et vérifié, remise au choix puis activation Mon e-ID.")
picture_fit(s, os.path.join(FIG, "bpmn", "P0_demande_cnie_tobe.png"), 0.6, 1.65, 12.1, 3.2)
tr = ["Entrée par l'identité numérique, demande pré-remplie", "Contrôle IA des pièces en quelques secondes, score de conformité", "E-timbre vérifié en ligne",
      "Créneaux recommandés par la prévision d'affluence, convocation QR", "Au CEDI : biométrie seule, vérifiée en temps réel (anti-fraude)", "Retrait ou livraison, puis activation dans Mon e-ID"]
for i, t in enumerate(tr):
    x = 0.6 + (i % 3) * 4.05
    y = 5.05 + (i // 3) * 0.9
    rect(s, x, y, 0.5, 0.5, NAVY, radius=True)
    text(s, x, y, 0.5, 0.5, str(i + 1), size=13, bold=True, color=GOLD, font=MONO, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.62, y - 0.05, 3.3, 0.7, t, size=12, color=INK, anchor=MSO_ANCHOR.MIDDLE)

# 11 — Démo Blueworks
s = new_slide("DÉMONSTRATION", "Blueworks Live : le blueprint du processus cible", dark=True,
              notes="Najib : insérer ici la capture vidéo (30 s) : navigation dans le blueprint, onglet Details d'une activité IA (entrées, sorties, système support).")
rect(s, 0.6, 1.7, 8.2, 5.0, CARD_DARK, line=GOLD, radius=True)
text(s, 0.6, 1.7, 8.2, 5.0, "▶\nVidéo de démonstration\n(capture d'écran Blueworks Live, 30 s)", size=20, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=HEAD)
card(s, 9.1, 1.75, 3.6, 1.5, "À montrer", "Espace « Urbanisation CNIE », blueprints as-is et to-be", dark=True, bsize=12)
card(s, 9.1, 3.4, 3.6, 1.5, "Documentation", "Onglet Details de « Contrôle documentaire » : entrées, sorties, système, risques", dark=True, bsize=12)
card(s, 9.1, 5.05, 3.6, 1.65, "Analyse", "Vue Analyse : temps et coût d'un dossier incomplet avant / après", dark=True, bsize=12)

# 12 — POS fonctionnel
s = new_slide("CARTOGRAPHIE FONCTIONNELLE", "Plan d'occupation des sols : six zones, trente-deux blocs",
              notes="Hafsa : légende jaune/orange/vert. Deux blocs nouveaux dans la zone opérationnelle, une zone pilotage et IA entièrement nouvelle.")
picture_fit(s, os.path.join(FIG, "archimate", "V3_fonctionnel.png"), 0.6, 1.6, 12.1, 5.0)
legend(s, 0.6, 6.7)
text(s, 6.6, 6.68, 6.1, 0.3, "12 blocs nouveaux · 9 à faire évoluer · 11 conservés", size=11.5, bold=True, color=NAVY, align=PP_ALIGN.RIGHT)

# 13 — Zoom
s = new_slide("CARTOGRAPHIE FONCTIONNELLE", "Ce qui change : zone opérationnelle et zone pilotage & IA",
              notes="Hafsa : gestion des pièces avec contrôle IA et instruction des dossiers ; pilotage : BI, prévision, anomalies, gouvernance des modèles. Enrôlement et production ne changent pas.")
text(s, 0.6, 1.7, 6, 0.35, "Zone opérationnelle", size=15, bold=True, color=NAVY, font=HEAD)
card(s, 0.6, 2.15, 2.85, 1.75, "Pièces et contrôle IA", "Téléversement, OCR, cohérence, photo ICAO, score de conformité", accent=GREEN, bsize=12)
card(s, 3.65, 2.15, 2.85, 1.75, "Instruction des dossiers", "Back-office mutualisé pour les cas en zone de doute et les alertes", accent=GREEN, bsize=12)
card(s, 0.6, 4.1, 2.85, 1.75, "Pré-demandes, RDV, remise", "Intégrés au moteur de processus, statuts fins, notifications", accent=ORANGE, bsize=12)
card(s, 3.65, 4.1, 2.85, 1.75, "Enrôlement, production", "Conservés : équipements et procédures de sécurité éprouvés", accent=GOLD, bsize=12)
text(s, 0.6, 6.1, 12.1, 0.6, "Enrôlement biométrique et production ne changent pas : ils reposent sur des équipements et des procédures de sécurité éprouvés.", size=12.5, color=MUTED, italic=True)
text(s, 6.9, 1.7, 6, 0.35, "Zone pilotage et IA (nouvelle)", size=15, bold=True, color=NAVY, font=HEAD)
for i, (t, d) in enumerate([("Tableaux de bord", "Indicateurs de délai, d'attente, de conformité"), ("Prévision d'affluence", "Charge par centre, créneaux recommandés"),
                            ("Anomalies et fraude", "Scoring des demandes, alertes vers l'instructeur"), ("Gouvernance des modèles", "Versions, performances, biais, décision humaine")]):
    x = 6.9 + (i % 2) * 3.05
    y = 2.15 + (i // 2) * 1.95
    card(s, x, y, 2.85, 1.75, t, d, accent=GREEN, bsize=12)

# 14 — Applicatif
s = new_slide("CARTOGRAPHIE APPLICATIVE", "Quinze composants orchestrés par un moteur de processus",
              notes="Mouad : moteur BPM qui orchestre de bout en bout ; passerelle d'API unique vers l'état civil, l'e-timbre, la Poste, les consulats ; services d'IA autonomes.")
picture_fit(s, os.path.join(FIG, "archimate", "V4_applicatif.png"), 0.6, 1.6, 8.3, 5.1)
card(s, 9.2, 1.7, 3.5, 1.55, "Moteur de processus", "APP-04 orchestre la demande ; les canaux ne portent plus de logique métier", accent=GREEN, bsize=12)
card(s, 9.2, 3.4, 3.5, 1.55, "Passerelle d'API", "APP-11 : un seul point d'échange avec l'état civil, la Trésorerie, la Poste, les consulats", accent=GREEN, bsize=12)
card(s, 9.2, 5.1, 3.5, 1.55, "IA en composants", "APP-03, 05, 06, 08 : autonomes, hébergés sur site, remplaçables", accent=GREEN, bsize=12)

# 15 — Démo Bonita
s = new_slide("DÉMONSTRATION", "Bonita : le sous-processus SP1 en action", dark=True,
              notes="Najib (voix off) : cas 1 conforme (score 100) jusqu'au QR code ; cas 2 photo non conforme (score 75) routé vers l'agent instructeur.")
rect(s, 0.6, 1.7, 8.2, 5.0, CARD_DARK, line=GOLD, radius=True)
text(s, 0.6, 1.7, 8.2, 5.0, "▶\nVidéo de démonstration\n(Bonita Portal, 90 s)", size=20, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=HEAD)
card(s, 9.1, 1.75, 3.6, 2.35, "Cas 1 — conforme", "Pré-demande → pièces → score 100 → créneau recommandé → e-timbre → QR code de convocation", dark=True, bsize=12)
card(s, 9.1, 4.25, 3.6, 2.45, "Cas 2 — zone de doute", "Photo non conforme → score 75 → tâche de l'agent instructeur → demande de correction → re-contrôle", dark=True, accent=GREEN, bsize=12)

# 16 — Technique
s = new_slide("ARCHITECTURE TECHNIQUE", "Architecture cible en zones, hébergée souverainement",
              notes="Mouad : DMZ avec pare-feu et passerelle ; zone applicative Kubernetes + Bonita + bus d'événements ; données chiffrées ; zone IA sur site ; HSM pour les clés.")
picture_fit(s, os.path.join(FIG, "archimate", "V5_technique.png"), 0.6, 1.6, 8.3, 5.1)
bullets(s, 9.2, 1.75, 3.5, 5, [[("Exposition", {"bold": True}), (" : WAF, anti-DDoS, passerelle d'API", {})],
                                 [("Applicative", {"bold": True}), (" : Kubernetes, Bonita, bus d'événements, IAM OpenID Connect", {})],
                                 [("Données", {"bold": True}), (" : PostgreSQL HA, stockage objet chiffré, entrepôt", {})],
                                 [("IA", {"bold": True}), (" : inférence sur site, registre de modèles, MLOps", {})],
                                 [("Sécurité", {"bold": True}), (" : HSM / PKI, SIEM, accès privilégiés", {})],
                                 [("Sites", {"bold": True}), (" : postes CEDI en mode dégradé, centres de production", {})]], size=12.5, gap=9)

# 17 — Sécurité
s = new_slide("SÉCURITÉ ET CONFORMITÉ", "Chaque risque a sa parade",
              notes="Mouad : authentification forte, chiffrement, contrôle documentaire + instruction humaine, HSM, évaluation des biais, haute disponibilité, conformité CNDP.")
rows = [("Usurpation d'identité en ligne", "Authentification forte via le Tiers de Confiance (OpenID Connect), détection du vivant"),
        ("Fuite de pièces justificatives", "Chiffrement, rétention limitée, accès journalisés, zones étanches"),
        ("Fraude documentaire", "Contrôle automatique + rapprochement état civil + instruction humaine des cas douteux"),
        ("Compromission des clés", "HSM certifiés, double contrôle, rotation"),
        ("Biais ou dérive des modèles", "Évaluation d'équité avant mise en service, surveillance, décision humaine sur toute alerte"),
        ("Indisponibilité", "Haute disponibilité multi-zones, mode dégradé des CEDI, plan de reprise"),
        ("Non-conformité CNDP", "Registre des traitements, consentement explicite, minimisation, analyse d'impact")]
tbl = s.shapes.add_table(len(rows) + 1, 2, Inches(0.6), Inches(1.7), Inches(12.1), Inches(4.9)).table
tbl.columns[0].width = Inches(3.6)
tbl.columns[1].width = Inches(8.5)
for j, h in enumerate(("Risque", "Mesure")):
    c = tbl.cell(0, j)
    c.text = h
    c.fill.solid(); c.fill.fore_color.rgb = NAVY
    p = c.text_frame.paragraphs[0]; p.runs[0].font.bold = True; p.runs[0].font.size = Pt(13); p.runs[0].font.color.rgb = GOLD; p.runs[0].font.name = BODY
for i, (r, m) in enumerate(rows, start=1):
    for j, v in enumerate((r, m)):
        c = tbl.cell(i, j)
        c.text = v
        c.fill.solid(); c.fill.fore_color.rgb = WHITE if i % 2 else RGBColor(0xF0, 0xF3, 0xF8)
        p = c.text_frame.paragraphs[0]; p.runs[0].font.size = Pt(12); p.runs[0].font.name = BODY
        p.runs[0].font.color.rgb = NAVY if j == 0 else INK; p.runs[0].font.bold = (j == 0)
        c.margin_top = c.margin_bottom = Inches(0.05)

# 18 — Trajectoire
s = new_slide("TRAJECTOIRE", "Trois paliers de 2027 à 2030",
              notes="Mouad : 2027 socle (BPM, API, contrôle documentaire) ; 2028 extension (mobile, assistant, prévision) ; 2030 cible (renouvellement en ligne, pilotage prédictif). Comité d'architecture + comité d'éthique de l'IA.")
pal = [("2027", "Palier 1 — Socle", "Moteur de processus, passerelle d'API, bus d'événements · e-timbre et état civil raccordés · contrôle documentaire en assistance puis automatique · back-office d'instruction", "Formulaire papier supprimé, dossiers incomplets ÷ 2"),
       ("2028", "Palier 2 — Étendu", "Application Mon e-ID · assistant conversationnel · prévision d'affluence et créneaux recommandés · livraison à domicile · tableaux de bord", "Canal mobile majoritaire, < 15 min en centre"),
       ("2030", "Palier 3 — Cible", "Renouvellement 100 % en ligne (biométrie récente) · détection d'anomalies, pilotage prédictif · MLOps complet · interconnexion RNP", "Objectifs G1 à G5 atteints")]
for i, (yr, t, d, res) in enumerate(pal):
    x = 0.6 + i * 4.1
    rect(s, x, 1.7, 3.9, 3.35, CARD, line=RGBColor(0xD9, 0xDE, 0xE6), radius=True)
    text(s, x + 0.2, 1.8, 1.5, 0.6, yr, size=30, bold=True, color=GOLD, font=HEAD)
    text(s, x + 1.7, 1.95, 2.1, 0.45, t, size=14, bold=True, color=NAVY, font=HEAD)
    text(s, x + 0.2, 2.55, 3.5, 1.6, d, size=12, color=INK, line=1.08)
    rect(s, x + 0.2, 4.2, 3.5, 0.7, RGBColor(0xEA, 0xF5, 0xEF), radius=True)
    text(s, x + 0.3, 4.2, 3.3, 0.7, res, size=11.5, bold=True, color=GREEN, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.6, 5.4, 12.1, 0.85, NAVY, radius=True)
text(s, 0.85, 5.4, 11.6, 0.85, [[("Gouvernance : ", {"bold": True, "color": GOLD}), ("comité d'architecture (cartographies, principes, dette) · comité d'éthique de l'IA avec la CNDP (biais, équité) · conduite du changement des agents", {})]],
     size=12.5, color=ICE, anchor=MSO_ANCHOR.MIDDLE)

# 19 — Avant / après
s = new_slide("RÉSULTATS", "Ce que gagnent le citoyen et la DGSN", dark=True,
              notes="Zineb : un seul déplacement, dossier validé avant de partir, créneaux sans attente ; pour la DGSN : guichets désengorgés, fraude détectée à l'enrôlement, pilotage par la donnée.")
text(s, 0.6, 1.7, 5.9, 0.4, "AUJOURD'HUI", size=12, bold=True, color=MUTED, font=MONO)
text(s, 6.8, 1.7, 5.9, 0.4, "CIBLE 2030", size=12, bold=True, color=GOLD, font=MONO)
pairs = [("2 déplacements au CEDI", "1 déplacement (biométrie), ou 0 pour un renouvellement"), ("Dossier contrôlé au guichet", "Dossier validé par l'IA avant de partir, < 5 % d'incomplets"),
         ("Créneaux saturés, intermédiaires", "Créneaux recommandés, convocation QR, < 15 min en centre"), ("Activation de l'identité numérique à part", "Carte numérique activée à la remise, > 80 %")]
for i, (a, b) in enumerate(pairs):
    y = 2.2 + i * 1.1
    rect(s, 0.6, y, 5.9, 0.9, CARD_DARK, line=MUTED, radius=True)
    text(s, 0.85, y, 5.5, 0.9, a, size=14, color=ICE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 6.5, y, 0.3, 0.9, "›", size=24, color=GOLD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 6.8, y, 5.9, 0.9, CARD_DARK, line=GOLD, radius=True)
    text(s, 7.05, y, 5.5, 0.9, b, size=14, bold=True, color=ICE, anchor=MSO_ANCHOR.MIDDLE)

# 20 — Conclusion
s = new_slide("CONCLUSION", "Un socle réutilisable pour tous les téléservices de la DGSN", dark=True,
              notes="Zineb : trois messages, perspectives, merci.")
for i, (t, d) in enumerate([("Cohérence", "Un seul fil rouge décliné sur les cinq livrables, de la stratégie à la technique"),
                            ("IA utile", "Cinq cas d'usage ancrés dans le processus, gouvernés et évalués sur leurs biais"),
                            ("Trajectoire réaliste", "Trois paliers à valeur mesurable, sans rupture de service")]):
    card(s, 0.6 + i * 4.1, 1.75, 3.9, 2.4, t, d, dark=True, tsize=17, bsize=13)
s.shapes.add_picture(os.path.join(ASSETS, "rosette.png"), Inches(10.3), Inches(4.0), Inches(3.0), Inches(3.0))
text(s, 0.6, 4.6, 9, 0.6, "Perspectives", size=16, bold=True, color=GOLD, font=HEAD)
bullets(s, 0.6, 5.1, 9, 1.6, ["Étendre le socle (BPM, API, plateforme IA) aux autres téléservices de la DGSN", "Instrumenter les indicateurs dès le palier 1 pour mesurer l'apport réel de l'IA"], size=13.5, color=ICE)
text(s, 0.6, 6.3, 9, 0.5, "Merci de votre attention — Mouad · Najib · Hafsa · Zineb", size=15, bold=True, color=ICE, font=HEAD)

prs.save(OUT)
print("deck OK ->", OUT, "| slides:", len(prs.slides))
