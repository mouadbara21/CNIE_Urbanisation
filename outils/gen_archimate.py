"""Génère le modèle ArchiMate du projet CNIE :
  - modeles/archimate/cnie.archimate  -> à ouvrir dans Archi (export des vues en PNG 300 dpi)
  - modeles/archimate/*.drawio        -> rendu provisoire des vues pour le rapport (export PNG via export_drawio.ps1)

Usage : python outils/gen_archimate.py
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from xml.sax.saxutils import quoteattr, escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "modeles", "archimate")

# ------------------------------------------------------------------ modèle
FOLDER_OF = {
    "Stakeholder": "motivation", "Driver": "motivation", "Assessment": "motivation", "Goal": "motivation",
    "Outcome": "motivation", "Principle": "motivation", "Requirement": "motivation", "Constraint": "motivation",
    "Capability": "strategy", "CourseOfAction": "strategy", "Resource": "strategy",
    "BusinessActor": "business", "BusinessRole": "business", "BusinessProcess": "business",
    "BusinessFunction": "business", "BusinessService": "business", "BusinessObject": "business", "BusinessEvent": "business",
    "ApplicationComponent": "application", "ApplicationService": "application", "ApplicationInterface": "application",
    "ApplicationFunction": "application", "DataObject": "application",
    "Node": "technology", "Device": "technology", "SystemSoftware": "technology", "TechnologyService": "technology",
    "CommunicationNetwork": "technology", "Artifact": "technology",
    "WorkPackage": "implementation_migration", "Deliverable": "implementation_migration",
    "Plateau": "implementation_migration", "Gap": "implementation_migration",
    "Grouping": "other", "Location": "other",
}
FILL = {  # couleurs ArchiMate standard (draw.io + fallback)
    "motivation": "#CCCCFF", "strategy": "#F5DEAA", "business": "#FFFFB5", "application": "#B5FFFF",
    "technology": "#C9E7B7", "implementation_migration": "#FFE0E0", "other": "#FFFFFF",
}
STATUS_FILL = {"E": "#FFFFB5", "V": "#FFD38A", "N": "#B9F0B9"}  # existant / à faire évoluer / nouveau
APPTYPE = {  # draw.io mxgraph.archimate3.application appType
    "Stakeholder": "stakeholder", "Driver": "driver", "Assessment": "assess", "Goal": "goal", "Outcome": "outcome",
    "Principle": "princ", "Requirement": "requirement", "Constraint": "constraint",
    "Capability": "capability", "CourseOfAction": "course", "Resource": "resource",
    "BusinessActor": "actor", "BusinessRole": "role", "BusinessProcess": "proc", "BusinessFunction": "func",
    "BusinessService": "serv", "BusinessObject": "passive", "BusinessEvent": "event",
    "ApplicationComponent": "comp", "ApplicationService": "serv", "ApplicationInterface": "interface",
    "ApplicationFunction": "func", "DataObject": "passive",
    "Node": "node", "Device": "device", "SystemSoftware": "sysSw", "TechnologyService": "serv",
    "CommunicationNetwork": "netw", "Artifact": "artifact",
    "WorkPackage": "workPkg", "Deliverable": "deliverable", "Plateau": "plateau", "Gap": "gap",
}
ARCHITYPE = {"Driver": "oct", "Stakeholder": "oct", "Assessment": "oct", "Goal": "oct", "Outcome": "oct",
             "Principle": "oct", "Requirement": "oct", "Constraint": "oct",
             "BusinessService": "rounded", "ApplicationService": "rounded", "TechnologyService": "rounded",
             "Capability": "square", "CourseOfAction": "rounded", "WorkPackage": "rounded", "Deliverable": "square"}

REL_XML = {"serving": "ServingRelationship", "flow": "FlowRelationship", "realization": "RealizationRelationship",
           "assignment": "AssignmentRelationship", "composition": "CompositionRelationship",
           "aggregation": "AggregationRelationship", "triggering": "TriggeringRelationship",
           "association": "AssociationRelationship", "influence": "InfluenceRelationship", "access": "AccessRelationship"}
REL_STYLE = {
    "serving": "endArrow=open;endFill=0;",
    "flow": "endArrow=block;endFill=1;dashed=1;dashPattern=8 4;",
    "realization": "endArrow=block;endFill=0;dashed=1;dashPattern=2 2;",
    "assignment": "startArrow=oval;startFill=1;endArrow=block;endFill=1;",
    "composition": "startArrow=diamondThin;startFill=1;startSize=10;endArrow=none;",
    "aggregation": "startArrow=diamondThin;startFill=0;startSize=10;endArrow=none;",
    "triggering": "endArrow=block;endFill=1;",
    "association": "endArrow=none;",
    "influence": "endArrow=open;endFill=0;dashed=1;",
    "access": "endArrow=open;endFill=0;dashed=1;dashPattern=1 3;",
}

_counter = [0]


def nid(prefix="id"):
    _counter[0] += 1
    return f"{prefix}-{_counter[0]:04d}"


@dataclass
class Element:
    key: str
    type: str
    name: str
    status: str = ""      # E / V / N (cartographies)
    doc: str = ""
    id: str = field(default_factory=lambda: nid("el"))


@dataclass
class Relation:
    src: str
    dst: str
    type: str
    name: str = ""
    id: str = field(default_factory=lambda: nid("rel"))


@dataclass
class Group:
    """Zone d'une vue : grille d'éléments (keys) à la position (x, y)."""
    title: str
    keys: list[str]
    x: int
    y: int
    cols: int = 3
    cw: int = 150
    ch: int = 55
    key: str = ""         # key d'un Element Grouping existant (optionnel)


@dataclass
class View:
    key: str
    name: str
    groups: list[Group]
    rels: list[str]       # ids de relations à dessiner (clé "src>dst")
    note: str = ""


class Model:
    def __init__(self, name):
        self.name = name
        self.elements: dict[str, Element] = {}
        self.relations: list[Relation] = []
        self.views: list[View] = []

    def e(self, key, type, name, status="", doc=""):
        self.elements[key] = Element(key, type, name, status, doc)
        return self

    def r(self, src, dst, type, name=""):
        self.relations.append(Relation(src, dst, type, name))
        return self

    def rel(self, src, dst):
        for r in self.relations:
            if r.src == src and r.dst == dst:
                return r
        raise KeyError(f"relation {src}>{dst} inconnue")


# ------------------------------------------------------------------ layout d'une vue
def layout(view: View, model: Model):
    """Renvoie (boxes, groups) ; boxes[key] = (x, y, w, h) absolu ; groups = [(title, x, y, w, h, key)]."""
    boxes, groups = {}, []
    PAD, TITLE = 15, 28
    for g in view.groups:
        n = len(g.keys)
        rows = (n + g.cols - 1) // g.cols
        gw = PAD * 2 + g.cols * (g.cw + 10) - 10
        gh = TITLE + PAD + rows * (g.ch + 10) - 10 + PAD
        groups.append((g.title, g.x, g.y, gw, gh, g.key))
        for i, k in enumerate(g.keys):
            c, r = i % g.cols, i // g.cols
            boxes[k] = (g.x + PAD + c * (g.cw + 10), g.y + TITLE + PAD + r * (g.ch + 10), g.cw, g.ch)
    return boxes, groups


# ------------------------------------------------------------------ export .archimate
def to_archimate(model: Model) -> str:
    folders = {"strategy": ("Strategy", []), "business": ("Business", []), "application": ("Application", []),
               "technology": ("Technology & Physical", []), "motivation": ("Motivation", []),
               "implementation_migration": ("Implementation & Migration", []), "other": ("Other", [])}
    for el in model.elements.values():
        folders[FOLDER_OF[el.type]][1].append(el)
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com" '
         f'name={quoteattr(model.name)} id="{nid("model")}" version="5.0.0">']
    for ftype, (fname, els) in folders.items():
        o.append(f'  <folder name={quoteattr(fname)} id="{nid("folder")}" type="{ftype}">')
        for el in els:
            o.append(f'    <element xsi:type="archimate:{el.type}" name={quoteattr(el.name)} id="{el.id}">')
            if el.doc:
                o.append(f'      <documentation>{escape(el.doc)}</documentation>')
            if el.status:
                o.append(f'      <property key="Statut" value={quoteattr({"E": "Existant", "V": "A faire évoluer", "N": "Nouveau"}[el.status])}/>')
            o.append('    </element>')
        o.append('  </folder>')
    o.append(f'  <folder name="Relations" id="{nid("folder")}" type="relations">')
    for r in model.relations:
        nm = f' name={quoteattr(r.name)}' if r.name else ''
        o.append(f'    <element xsi:type="archimate:{REL_XML[r.type]}" id="{r.id}"{nm} source="{model.elements[r.src].id}" target="{model.elements[r.dst].id}"/>')
    o.append('  </folder>')
    o.append(f'  <folder name="Views" id="{nid("folder")}" type="diagrams">')
    for v in model.views:
        boxes, groups = layout(v, model)
        o.append(f'    <element xsi:type="archimate:ArchimateDiagramModel" name={quoteattr(v.name)} id="{nid("view")}">')
        # ids des objets de diagramme et des connexions (connexion déclarée dans l'objet source,
        # référencée par targetConnections dans l'objet cible)
        child_ids = {k: nid("obj") for k in boxes}
        conns = {}  # key -> list of (connId, targetChild, relId)
        targets = {}  # key -> list of connId
        for key in v.rels:
            src, dst = key.split(">")
            if src in child_ids and dst in child_ids:
                r = model.rel(src, dst)
                cid = nid("conn")
                conns.setdefault(src, []).append((cid, child_ids[dst], r.id))
                targets.setdefault(dst, []).append(cid)
        for g, (title, gx, gy, gw, gh, gkey) in zip(v.groups, groups):
            gid = nid("grp")
            o.append(f'      <child xsi:type="archimate:Group" id="{gid}" name={quoteattr(title)} fillColor="#f4f4f4">')
            o.append(f'        <bounds x="{gx}" y="{gy}" width="{gw}" height="{gh}"/>')
            for k in g.keys:
                el = model.elements[k]
                bx, by, bw, bh = boxes[k]
                cid = child_ids[k]
                fill = f' fillColor="{STATUS_FILL[el.status]}"' if el.status else ''
                tc = f' targetConnections="{" ".join(targets[k])}"' if k in targets else ''
                o.append(f'        <child xsi:type="archimate:DiagramObject" id="{cid}" archimateElement="{el.id}"{fill}{tc}>')
                o.append(f'          <bounds x="{bx-gx}" y="{by-gy}" width="{bw}" height="{bh}"/>')
                for (conn_id, tgt, rel_id) in conns.get(k, []):
                    o.append(f'          <sourceConnection xsi:type="archimate:Connection" id="{conn_id}" source="{cid}" target="{tgt}" archimateRelationship="{rel_id}"/>')
                o.append('        </child>')
            o.append('      </child>')
        if v.note:
            o.append(f'      <child xsi:type="archimate:Note" id="{nid("note")}" textAlignment="1">')
            o.append('        <bounds x="20" y="-70" width="760" height="55"/>')
            o.append(f'        <content>{escape(v.note)}</content>')
            o.append('      </child>')
        o.append('    </element>')
    o.append('  </folder>')
    o.append('</archimate:model>')
    return "\n".join(o)


# ------------------------------------------------------------------ export draw.io
def to_drawio(view: View, model: Model) -> str:
    boxes, groups = layout(view, model)
    o = ['<mxfile host="gen_archimate.py" type="device">',
         f'<diagram name={quoteattr(view.name)} id="d_{view.key}"><mxGraphModel grid="1" gridSize="10" page="1" pageWidth="1654" pageHeight="1169">',
         '<root><mxCell id="0"/><mxCell id="1" parent="0"/>']
    ids = {}
    for i, (title, gx, gy, gw, gh, gkey) in enumerate(groups):
        o.append(f'<mxCell id="g{i}" value={quoteattr(title)} style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;fillColor=#f7f7f7;strokeColor=#8a8a8a;verticalAlign=top;align=left;spacingLeft=8;fontStyle=1;fontSize=11;" vertex="1" parent="1">')
        o.append(f'<mxGeometry x="{gx}" y="{gy}" width="{gw}" height="{gh}" as="geometry"/></mxCell>')
    for k, (x, y, w, h) in boxes.items():
        el = model.elements[k]
        folder = FOLDER_OF[el.type]
        fill = STATUS_FILL[el.status] if el.status else FILL[folder]
        app = APPTYPE.get(el.type, "comp")
        arch = ARCHITYPE.get(el.type, "square")
        style = (f"html=1;outlineConnect=0;whiteSpace=wrap;fillColor={fill};strokeColor=#5a5a5a;fontSize=10;"
                 f"shape=mxgraph.archimate3.application;appType={app};archiType={arch};")
        if el.type == "Plateau":
            style = f"html=1;whiteSpace=wrap;fillColor={fill};strokeColor=#5a5a5a;fontSize=10;shape=mxgraph.archimate3.application;appType=plateau;archiType=square;"
        cid = f"n_{k}"
        ids[k] = cid
        label = el.name if not el.status else f"{el.name}<br><font style='font-size:8px'>[{ {'E':'existant','V':'à faire évoluer','N':'nouveau'}[el.status]}]</font>"
        o.append(f'<mxCell id="{cid}" value={quoteattr(label)} style="{style}" vertex="1" parent="1">')
        o.append(f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    for key in view.rels:
        src, dst = key.split(">")
        r = model.rel(src, dst)
        if src not in ids or dst not in ids:
            continue
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#333333;fontSize=9;labelBackgroundColor=#ffffff;{REL_STYLE[r.type]}"
        o.append(f'<mxCell id="e_{r.id}" value={quoteattr(r.name)} style="{style}" edge="1" parent="1" source="{ids[src]}" target="{ids[dst]}">')
        o.append('<mxGeometry relative="1" as="geometry"/></mxCell>')
    if view.note:
        o.append(f'<mxCell id="note" value={quoteattr(view.note)} style="text;html=1;align=left;verticalAlign=middle;fontSize=9;fontStyle=2;" vertex="1" parent="1">')
        o.append('<mxGeometry x="20" y="-60" width="900" height="40" as="geometry"/></mxCell>')
    o.append('</root></mxGraphModel></diagram></mxfile>')
    return "\n".join(o)


# ================================================================== CONTENU
m = Model("Urbanisation SI CNIE - DGSN (cible 2030)")

# ---- Motivation & stratégie
m.e("sk_cit", "Stakeholder", "Citoyens et MRE").e("sk_dgsn", "Stakeholder", "DGSN / Ministère de l'Intérieur")
m.e("sk_add", "Stakeholder", "ADD / DGTN").e("sk_cndp", "Stakeholder", "CNDP / DGSSI").e("sk_part", "Stakeholder", "Fournisseurs de services accrédités")
m.e("dr_dm2030", "Driver", "Digital Morocco 2030 (EGDI 113e → 50e)").e("dr_loi", "Driver", "Loi 55-19 : simplification et numérisation")
m.e("dr_fraude", "Driver", "Lutte contre la fraude et l'usurpation").e("dr_qs", "Driver", "Qualité de service : attente, délais, saturation")
m.e("dr_incl", "Driver", "Inclusion numérique (ruraux, seniors, MRE)")
m.e("as_silos", "Assessment", "Canaux en silos (cnie.ma, epolice.ma, identitenumerique.ma)")
m.e("as_manuel", "Assessment", "Contrôle des pièces manuel et tardif").e("as_rdv", "Assessment", "Créneaux saturés, intermédiaires frauduleux")
m.e("g1", "Goal", "G1 - Démarche CNIE 100 % en ligne jusqu'à la biométrie").e("g2", "Goal", "G2 - Diviser par 2 le délai et l'attente en centre")
m.e("g3", "Goal", "G3 - Unicité garantie, zéro fraude à l'enrôlement").e("g4", "Goal", "G4 - Identité numérique activée pour chaque carte")
m.e("g5", "Goal", "G5 - Pilotage par la donnée et l'IA")
m.e("o1", "Outcome", "Dossiers incomplets au CEDI < 5 %").e("o2", "Outcome", "Temps moyen en centre < 15 min")
m.e("o3", "Outcome", "Taux d'activation Mon e-ID > 80 %")
m.e("p1", "Principle", "Dites-le nous une fois").e("p2", "Principle", "Protection des données dès la conception (CNDP)")
m.e("p3", "Principle", "Souveraineté et sécurité (DGSSI)").e("p4", "Principle", "Interopérabilité et API d'abord").e("p5", "Principle", "Multicanal inclusif")
m.e("cap1", "Capability", "Gestion des demandes de titre").e("cap2", "Capability", "Enrôlement biométrique")
m.e("cap3", "Capability", "Identité numérique et authentification").e("cap4", "Capability", "Contrôle documentaire par IA")
m.e("cap5", "Capability", "Pilotage prédictif et gestion de la capacité")
m.e("coa", "CourseOfAction", "Programme « CNIE numérique 2030 »")
for s, d in (("sk_cit", "dr_qs"), ("sk_dgsn", "dr_fraude"), ("sk_add", "dr_dm2030"), ("sk_cndp", "dr_fraude"), ("sk_part", "dr_dm2030"), ("sk_cit", "dr_incl")):
    m.r(s, d, "association")
for s, d in (("dr_dm2030", "g1"), ("dr_loi", "g1"), ("dr_qs", "g2"), ("dr_fraude", "g3"), ("dr_dm2030", "g4"), ("dr_qs", "g5"), ("dr_incl", "g2")):
    m.r(s, d, "influence", "+")
for s, d in (("as_silos", "g1"), ("as_manuel", "g2"), ("as_rdv", "g2")):
    m.r(s, d, "influence", "-")
for s, d in (("o1", "g2"), ("o2", "g2"), ("o3", "g4")):
    m.r(s, d, "realization")
for s, d in (("p1", "g1"), ("p2", "g3"), ("p3", "g3"), ("p4", "g1"), ("p5", "g2")):
    m.r(s, d, "influence")
for s, d in (("cap1", "g1"), ("cap2", "g3"), ("cap3", "g4"), ("cap4", "g2"), ("cap5", "g5")):
    m.r(s, d, "realization")
for c in ("cap1", "cap2", "cap3", "cap4", "cap5"):
    m.r("coa", c, "realization")

m.views.append(View("V1_motivation", "V1 - Captation de la stratégie (motivation et capacités)", [
    Group("Parties prenantes", ["sk_cit", "sk_dgsn", "sk_add", "sk_cndp", "sk_part"], 20, 20, cols=5),
    Group("Moteurs (drivers) et constats", ["dr_dm2030", "dr_loi", "dr_fraude", "dr_qs", "dr_incl", "as_silos", "as_manuel", "as_rdv"], 20, 150, cols=5),
    Group("Objectifs stratégiques", ["g1", "g2", "g3", "g4", "g5"], 20, 345, cols=5),
    Group("Capacités cibles (réalisent les objectifs)", ["cap1", "cap4", "cap2", "cap3", "cap5"], 20, 475, cols=5),
    Group("Programme", ["coa"], 850, 475, cols=1),
    Group("Résultats attendus (indicateurs)", ["o1", "o2", "o3"], 20, 605, cols=3),
    Group("Principes d'urbanisation", ["p1", "p2", "p3", "p4", "p5"], 20, 735, cols=5),
], ["sk_cit>dr_qs", "sk_dgsn>dr_fraude", "sk_add>dr_dm2030", "sk_cndp>dr_fraude", "sk_part>dr_dm2030", "sk_cit>dr_incl",
    "dr_dm2030>g1", "dr_loi>g1", "dr_qs>g2", "dr_fraude>g3", "dr_dm2030>g4", "dr_qs>g5", "dr_incl>g2",
    "as_silos>g1", "as_manuel>g2", "as_rdv>g2",
    "cap1>g1", "cap2>g3", "cap3>g4", "cap4>g2", "cap5>g5", "coa>cap5"],
    note="Flèches pleines : association · pointillés « + / - » : influence · pointillés à triangle : réalisation. Les résultats attendus mesurent G2 (o1, o2) et G4 (o3)."))

# ---- Métier
m.e("ba_cit", "BusinessActor", "Citoyen").e("ba_cedi", "BusinessActor", "Agent CEDI").e("ba_ins", "BusinessActor", "Agent instructeur", "N")
m.e("ba_cpc", "BusinessActor", "Centre de production (CPC)").e("ba_part", "BusinessActor", "Partenaires (Trésorerie, Poste, état civil, consulats)")
m.e("bs_dem", "BusinessService", "Demande et renouvellement de CNIE").e("bs_rdv", "BusinessService", "Prise de rendez-vous")
m.e("bs_suivi", "BusinessService", "Suivi de la demande").e("bs_idn", "BusinessService", "Identité numérique (TCN)")
m.e("bs_auth", "BusinessService", "Authentification pour les fournisseurs accrédités")
m.e("bp_p0", "BusinessProcess", "P0 - Demande et renouvellement de la CNIE")
m.e("bp_sp1", "BusinessProcess", "SP1 - Pré-demande, contrôle IA des pièces, RDV", "N").e("bp_sp2", "BusinessProcess", "SP2 - Enrôlement au CEDI", "V")
m.e("bp_sp3", "BusinessProcess", "SP3 - Production et personnalisation", "E").e("bp_sp4", "BusinessProcess", "SP4 - Notification, remise, activation e-ID", "V")
m.e("bo_dem", "BusinessObject", "Demande").e("bo_dossier", "BusinessObject", "Dossier de pièces").e("bo_rdv", "BusinessObject", "Rendez-vous")
m.e("bo_carte", "BusinessObject", "Carte CNIE").e("bo_idn", "BusinessObject", "Identité numérique")
for s in ("bp_sp1", "bp_sp2", "bp_sp3", "bp_sp4"):
    m.r("bp_p0", s, "composition")
m.r("bp_sp1", "bp_sp2", "triggering").r("bp_sp2", "bp_sp3", "triggering").r("bp_sp3", "bp_sp4", "triggering")
m.r("bp_p0", "bs_dem", "realization").r("bp_sp1", "bs_rdv", "realization").r("bp_sp4", "bs_suivi", "realization").r("bp_sp4", "bs_idn", "realization")
m.r("ba_cit", "bp_sp1", "assignment").r("ba_cedi", "bp_sp2", "assignment").r("ba_ins", "bp_sp1", "assignment").r("ba_cpc", "bp_sp3", "assignment").r("ba_part", "bp_sp4", "assignment")
m.r("bp_sp1", "bo_dem", "access").r("bp_sp1", "bo_dossier", "access").r("bp_sp1", "bo_rdv", "access").r("bp_sp3", "bo_carte", "access").r("bp_sp4", "bo_idn", "access")
m.r("bp_p0", "cap1", "realization").r("bp_sp2", "cap2", "realization")
m.views.append(View("V2_metier", "V2 - Cartographie métier cible (processus et services)", [
    Group("Services métier offerts", ["bs_dem", "bs_rdv", "bs_suivi", "bs_idn", "bs_auth"], 20, 20, cols=5),
    Group("Acteurs", ["ba_cit", "ba_cedi", "ba_ins", "ba_cpc", "ba_part"], 20, 150, cols=5),
    Group("Processus principal et sous-processus", ["bp_p0", "bp_sp1", "bp_sp2", "bp_sp3", "bp_sp4"], 20, 280, cols=5),
    Group("Objets métier", ["bo_dem", "bo_dossier", "bo_rdv", "bo_carte", "bo_idn"], 20, 410, cols=5),
], ["bp_p0>bp_sp1", "bp_p0>bp_sp2", "bp_p0>bp_sp3", "bp_p0>bp_sp4", "bp_sp1>bp_sp2", "bp_sp2>bp_sp3", "bp_sp3>bp_sp4",
    "bp_p0>bs_dem", "bp_sp1>bs_rdv", "bp_sp4>bs_suivi", "bp_sp4>bs_idn",
    "ba_cit>bp_sp1", "ba_cedi>bp_sp2", "ba_ins>bp_sp1", "ba_cpc>bp_sp3", "ba_part>bp_sp4",
    "bp_sp1>bo_dem", "bp_sp1>bo_dossier", "bp_sp1>bo_rdv", "bp_sp3>bo_carte", "bp_sp4>bo_idn"],
    note="Couleurs : jaune = existant, orange = à faire évoluer, vert = nouveau."))

# ---- Fonctionnel (POS)
FUNCS = [
    # zone Échange
    ("f_portail", "Portail citoyen web (AR/FR/AMZ)", "V"), ("f_mobile", "Application mobile Mon e-ID", "N"), ("f_assist", "Assistant conversationnel IA", "N"),
    ("f_guichet", "Guichet CEDI et kits hors-ligne", "E"), ("f_notif", "Notifications multicanal", "V"), ("f_partn", "Portail partenaires TCN", "E"),
    # zone Opérationnelle
    ("f_predem", "Gestion des pré-demandes", "V"), ("f_pieces", "Gestion des pièces et contrôle IA", "N"), ("f_rdv", "Gestion des RDV et créneaux", "V"),
    ("f_enrol", "Enrôlement biométrique", "E"), ("f_instr", "Instruction des dossiers", "N"), ("f_prod", "Production et personnalisation", "E"),
    ("f_remise", "Remise et activation", "V"), ("f_cas", "Gestion des cas particuliers", "V"), ("f_cycle", "Cycle de vie de la carte (révocation, PIN)", "E"),
    # zone Support
    ("f_paie", "Paiement et e-timbre", "V"), ("f_abis", "Référentiel biométrique (ABIS/AFIS)", "E"), ("f_tcn", "Identité numérique (TCN)", "E"),
    ("f_ged", "Gestion documentaire et archivage", "N"), ("f_grc", "Réclamations (GRC)", "N"),
    # zone Pilotage & IA
    ("f_bi", "Tableaux de bord et BI", "N"), ("f_prev", "Prévision d'affluence", "N"), ("f_anom", "Détection d'anomalies et fraude", "N"), ("f_mlops", "Gouvernance des modèles (MLOps)", "N"),
    # zone Ressources
    ("f_rh", "RH des agents", "E"), ("f_log", "Logistique des centres", "E"), ("f_achat", "Consommables (cartes vierges)", "E"),
    # zone Référentiels
    ("f_ec", "État civil (RNEC)", "V"), ("f_rnp", "RNP / RSU", "N"), ("f_revoc", "Base des cartes révoquées", "E"), ("f_annu", "Annuaire des centres", "E"), ("f_api", "Interopérabilité (API Gateway)", "N"),
]
for k, n, s in FUNCS:
    m.e(k, "BusinessFunction", n, s)
m.views.append(View("V3_fonctionnel", "V3 - Cartographie fonctionnelle cible (plan d'occupation des sols)", [
    Group("Zone Échange (canaux)", ["f_portail", "f_mobile", "f_assist", "f_guichet", "f_notif", "f_partn"], 20, 20, cols=6),
    Group("Zone Opérationnelle (cœur métier CNIE)", ["f_predem", "f_pieces", "f_rdv", "f_enrol", "f_instr", "f_prod", "f_remise", "f_cas", "f_cycle"], 20, 150, cols=5),
    Group("Zone Pilotage et IA", ["f_bi", "f_prev", "f_anom", "f_mlops"], 850, 150, cols=2),
    Group("Zone Support", ["f_paie", "f_abis", "f_tcn", "f_ged", "f_grc"], 20, 345, cols=5),
    Group("Zone Ressources", ["f_rh", "f_log", "f_achat"], 850, 345, cols=2),
    Group("Zone Référentiels et échanges", ["f_ec", "f_rnp", "f_revoc", "f_annu", "f_api"], 20, 475, cols=5),
], [], note="Légende : jaune = bloc existant conservé · orange = bloc existant à faire évoluer · vert = bloc nouveau (cible)."))

# ---- Applicatif
APPS = [
    ("a01", "APP-01 Portail citoyen CNIE", "V"), ("a02", "APP-02 App mobile Mon e-ID", "N"), ("a03", "APP-03 Assistant conversationnel", "N"),
    ("a04", "APP-04 Moteur BPM (Bonita)", "N"), ("a05", "APP-05 Contrôle documentaire IA", "N"), ("a06", "APP-06 Rendez-vous et prévision", "V"),
    ("a07", "APP-07 Poste d'enrôlement CEDI", "E"), ("a08", "APP-08 ABIS / AFIS", "V"), ("a09", "APP-09 Production et personnalisation", "E"),
    ("a10", "APP-10 Plateforme TCN (OpenID Connect)", "E"), ("a11", "APP-11 API Gateway et bus d'intégration", "N"), ("a12", "APP-12 Notifications multicanal", "V"),
    ("a13", "APP-13 Entrepôt de données, BI et MLOps", "N"), ("a14", "APP-14 GRC / réclamations", "N"), ("a15", "APP-15 GED et archivage probant", "N"),
    ("x_ec", "SI État civil", "E"), ("x_tim", "e-Timbre (Trésorerie)", "E"), ("x_poste", "Barid Al-Maghrib", "E"), ("x_cons", "SI consulaire", "E"), ("x_fs", "Fournisseurs accrédités", "E"),
]
for k, n, s in APPS:
    m.e(k, "ApplicationComponent", n, s)
APP_FLOWS = [("a01", "a04", "demande"), ("a02", "a04", "demande"), ("a03", "a01", "assistance"), ("a04", "a05", "pièces"), ("a05", "a04", "score"),
             ("a04", "a06", "créneau"), ("a06", "a13", "historique"), ("a04", "a11", "paiement"), ("a11", "x_tim", "e-timbre"), ("a11", "x_ec", "acte"),
             ("a04", "a07", "convocation QR"), ("a07", "a08", "biométrie"), ("a08", "a09", "dossier validé"), ("a09", "a04", "statut"),
             ("a04", "a12", "événements"), ("a09", "a15", "archivage"), ("a11", "x_poste", "livraison"), ("a11", "x_cons", "MRE"),
             ("a10", "a01", "authentification"), ("a10", "a02", "authentification"), ("x_fs", "a10", "OIDC"), ("a04", "a13", "journal"), ("a14", "a04", "réclamation")]
for s, d, n in APP_FLOWS:
    m.r(s, d, "flow", n)
m.views.append(View("V4_applicatif", "V4 - Cartographie applicative cible", [
    Group("Canaux", ["a01", "a02", "a03"], 20, 20, cols=3),
    Group("Identité numérique", ["a10", "x_fs"], 540, 20, cols=2),
    Group("Orchestration et services IA", ["a04", "a05", "a06", "a12"], 20, 160, cols=4),
    Group("Cœur métier CNIE", ["a07", "a08", "a09"], 20, 300, cols=3),
    Group("Support et données", ["a13", "a14", "a15"], 540, 300, cols=3),
    Group("Intégration", ["a11"], 20, 440, cols=1),
    Group("Systèmes externes", ["x_ec", "x_tim", "x_poste", "x_cons"], 220, 440, cols=4),
], [], note="Les flux entre applications sont décrits dans la matrice des flux du rapport (et portés par le modèle Archi). Couleurs : jaune = existant, orange = à faire évoluer, vert = nouveau."))

# ---- Technique
TECH = [
    ("n_dmz", "Node", "Zone d'exposition (DMZ)"), ("n_app", "Node", "Zone applicative (cluster Kubernetes)"), ("n_data", "Node", "Zone données"),
    ("n_ia", "Node", "Zone IA (GPU, inférence)"), ("n_sec", "Node", "Zone sécurité"), ("n_cedi", "Node", "Site CEDI"), ("n_cpc", "Node", "Site de production"),
    ("s_waf", "SystemSoftware", "WAF / anti-DDoS"), ("s_apigw", "SystemSoftware", "API Gateway (Kong)"), ("s_iam", "SystemSoftware", "IAM / OIDC (Keycloak)"),
    ("s_k8s", "SystemSoftware", "Kubernetes + conteneurs"), ("s_bpm", "SystemSoftware", "Bonita Runtime"), ("s_kafka", "SystemSoftware", "Bus d'événements (Kafka)"),
    ("s_pg", "SystemSoftware", "PostgreSQL (HA)"), ("s_s3", "SystemSoftware", "Stockage objet chiffré"), ("s_dwh", "SystemSoftware", "Entrepôt de données"),
    ("s_ml", "SystemSoftware", "Serveur d'inférence (OCR, vision, LLM)"), ("s_mlops", "SystemSoftware", "MLOps (registre de modèles)"),
    ("s_hsm", "Device", "HSM (PKI nationale)"), ("s_siem", "SystemSoftware", "SIEM / SOC"), ("s_pam", "SystemSoftware", "Gestion des accès privilégiés"),
    ("d_poste", "Device", "Poste d'enrôlement (capteurs biométriques, lecteur NFC)"), ("d_kiosk", "Device", "Borne / kit hors-ligne"),
    ("d_perso", "Device", "Machines de personnalisation (laser, encodage puce)"),
    ("net_wan", "CommunicationNetwork", "Réseau interministériel sécurisé (VPN)"), ("net_int", "CommunicationNetwork", "Internet"),
    ("ts_cloud", "TechnologyService", "Cloud souverain (hébergement DGSSI)"),
]
for k, t, n in TECH:
    m.e(k, t, n)
TECH_REL = [("n_dmz", "s_waf", "assignment"), ("n_dmz", "s_apigw", "assignment"), ("n_app", "s_k8s", "assignment"), ("n_app", "s_bpm", "assignment"),
            ("n_app", "s_kafka", "assignment"), ("n_app", "s_iam", "assignment"), ("n_data", "s_pg", "assignment"), ("n_data", "s_s3", "assignment"),
            ("n_data", "s_dwh", "assignment"), ("n_ia", "s_ml", "assignment"), ("n_ia", "s_mlops", "assignment"), ("n_sec", "s_hsm", "assignment"),
            ("n_sec", "s_siem", "assignment"), ("n_sec", "s_pam", "assignment"), ("n_cedi", "d_poste", "composition"), ("n_cedi", "d_kiosk", "composition"),
            ("n_cpc", "d_perso", "composition"), ("net_int", "n_dmz", "association"), ("n_dmz", "n_app", "flow"), ("n_app", "n_data", "flow"),
            ("n_app", "n_ia", "flow"), ("net_wan", "n_cedi", "association"), ("net_wan", "n_cpc", "association"), ("net_wan", "n_dmz", "association"),
            ("ts_cloud", "n_app", "serving"), ("ts_cloud", "n_data", "serving"), ("ts_cloud", "n_ia", "serving")]
for s, d, t in TECH_REL:
    m.r(s, d, t)
m.views.append(View("V5_technique", "V5 - Architecture technique cible", [
    Group("Accès", ["net_int", "net_wan"], 20, 20, cols=2),
    Group("Zone d'exposition (DMZ)", ["n_dmz", "s_waf", "s_apigw"], 20, 150, cols=3),
    Group("Zone sécurité", ["n_sec", "s_hsm", "s_siem", "s_pam"], 540, 150, cols=4),
    Group("Zone applicative", ["n_app", "s_k8s", "s_bpm", "s_kafka", "s_iam"], 20, 290, cols=5),
    Group("Zone IA", ["n_ia", "s_ml", "s_mlops"], 860, 290, cols=3),
    Group("Zone données", ["n_data", "s_pg", "s_s3", "s_dwh"], 20, 430, cols=4),
    Group("Hébergement", ["ts_cloud"], 700, 430, cols=1),
    Group("Sites physiques", ["n_cedi", "d_poste", "d_kiosk", "n_cpc", "d_perso"], 20, 570, cols=5),
], [f"{s}>{d}" for s, d, _ in TECH_REL if _ in ("flow", "serving", "association")]))

# ---- Trajectoire
m.e("pl0", "Plateau", "Palier 0 - Existant (2026)").e("pl1", "Plateau", "Palier 1 - Socle (2027) : BPM, API Gateway, contrôle IA des pièces, e-timbre intégré")
m.e("pl2", "Plateau", "Palier 2 - Étendu (2028) : app Mon e-ID, assistant IA, prévision d'affluence, livraison à domicile")
m.e("pl3", "Plateau", "Palier 3 - Cible (2030) : renouvellement 100 % en ligne, pilotage prédictif, MLOps")
m.e("wp1", "WorkPackage", "WP1 - Socle d'intégration et BPM").e("wp2", "WorkPackage", "WP2 - Services IA documentaires et biométriques")
m.e("wp3", "WorkPackage", "WP3 - Canaux citoyens (portail, mobile, assistant)").e("wp4", "WorkPackage", "WP4 - Données, BI et MLOps")
m.e("wp5", "WorkPackage", "WP5 - Conduite du changement et gouvernance")
m.e("gap1", "Gap", "Contrôle documentaire manuel").e("gap2", "Gap", "Canaux en silos").e("gap3", "Gap", "Absence de pilotage prédictif")
m.r("pl0", "pl1", "triggering").r("pl1", "pl2", "triggering").r("pl2", "pl3", "triggering")
m.r("wp1", "pl1", "association").r("wp2", "pl1", "association").r("wp3", "pl2", "association").r("wp4", "pl3", "association").r("wp5", "pl3", "association")
m.r("gap1", "pl0", "association").r("gap2", "pl0", "association").r("gap3", "pl0", "association")
m.views.append(View("V6_trajectoire", "V6 - Trajectoire de migration", [
    Group("Écarts constatés", ["gap1", "gap2", "gap3"], 20, 20, cols=3),
    Group("Paliers", ["pl0", "pl1", "pl2", "pl3"], 20, 150, cols=4, cw=200, ch=70),
    Group("Chantiers", ["wp1", "wp2", "wp3", "wp4", "wp5"], 20, 300, cols=5),
], ["pl0>pl1", "pl1>pl2", "pl2>pl3", "wp1>pl1", "wp2>pl1", "wp3>pl2", "wp4>pl3", "wp5>pl3", "gap1>pl0", "gap2>pl0", "gap3>pl0"]))

# ================================================================== main
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "cnie.archimate"), "w", encoding="utf-8") as fh:
        fh.write(to_archimate(m))
    for v in m.views:
        with open(os.path.join(OUT, v.key + ".drawio"), "w", encoding="utf-8") as fh:
            fh.write(to_drawio(v, m))
        print("OK vue", v.key)
    print("Éléments :", len(m.elements), "| Relations :", len(m.relations))
