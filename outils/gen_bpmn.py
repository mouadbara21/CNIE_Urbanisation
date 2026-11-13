"""Génère les processus BPMN du projet CNIE en deux formats :
  - BPMN 2.0 XML (avec DI)  -> import dans IBM Blueworks Live et Bonita Studio
  - draw.io XML             -> export PNG pour le rapport (en attendant les captures Blueworks)

Usage : python outils/gen_bpmn.py
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from xml.sax.saxutils import escape, quoteattr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_BPMN = os.path.join(ROOT, "modeles", "bpmn")
OUT_FIG = os.path.join(ROOT, "rapport", "figures", "bpmn")

# ---------------------------------------------------------------- modèle
@dataclass
class Node:
    id: str
    kind: str          # start | end | user | service | manual | ai | xor | par | msg | timer
    lane: str
    name: str
    col: int

@dataclass
class Flow:
    src: str
    dst: str
    name: str = ""

@dataclass
class Process:
    id: str
    name: str
    pool: str
    lanes: list[str]
    nodes: list[Node] = field(default_factory=list)
    flows: list[Flow] = field(default_factory=list)

    def n(self, id, kind, lane, name, col):
        self.nodes.append(Node(id, kind, lane, name, col))
        return self

    def f(self, src, dst, name=""):
        self.flows.append(Flow(src, dst, name))
        return self

# ---------------------------------------------------------------- layout
LANE_H = 180
COL_W = 175
X0 = 40
TASK_W, TASK_H = 130, 70
EV_D = 36
GW_D = 50
HEADER_W = 36          # bandeau vertical des lanes
POOL_HEADER = 36


def geometry(p: Process):
    """Renvoie {node_id: (x, y, w, h)} en coordonnées absolues (pool en 0,0)."""
    lane_index = {l: i for i, l in enumerate(p.lanes)}
    geo = {}
    for nd in p.nodes:
        cx = X0 + POOL_HEADER + HEADER_W + nd.col * COL_W + TASK_W / 2
        cy = lane_index[nd.lane] * LANE_H + LANE_H / 2
        if nd.kind in ("start", "end", "msg", "timer"):
            w = h = EV_D
        elif nd.kind in ("xor", "par"):
            w = h = GW_D
        else:
            w, h = TASK_W, TASK_H
        geo[nd.id] = (cx - w / 2, cy - h / 2, w, h)
    return geo


def pool_size(p: Process):
    maxcol = max(nd.col for nd in p.nodes)
    width = X0 + POOL_HEADER + HEADER_W + (maxcol + 1) * COL_W + 40
    return width, LANE_H * len(p.lanes)

# ---------------------------------------------------------------- BPMN 2.0
BPMN_TAG = {
    "start": "startEvent", "end": "endEvent", "user": "userTask", "service": "serviceTask",
    "manual": "manualTask", "ai": "serviceTask", "xor": "exclusiveGateway", "par": "parallelGateway",
    "msg": "intermediateCatchEvent", "timer": "intermediateCatchEvent",
}


def to_bpmn(p: Process) -> str:
    geo = geometry(p)
    W, H = pool_size(p)
    lane_index = {l: i for i, l in enumerate(p.lanes)}
    incoming = {nd.id: [] for nd in p.nodes}
    outgoing = {nd.id: [] for nd in p.nodes}
    for i, fl in enumerate(p.flows):
        fid = f"flow_{i+1}"
        outgoing[fl.src].append(fid)
        incoming[fl.dst].append(fid)

    o = []
    o.append('<?xml version="1.0" encoding="UTF-8"?>')
    o.append('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
             'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
             'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
             'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
             'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
             f'id="defs_{p.id}" targetNamespace="http://cnie.ma/urbanisation" exporter="gen_bpmn.py" exporterVersion="1.0">')
    o.append(f'  <bpmn:collaboration id="collab_{p.id}">')
    o.append(f'    <bpmn:participant id="pool_{p.id}" name={quoteattr(p.pool)} processRef={quoteattr(p.id)} />')
    o.append('  </bpmn:collaboration>')
    o.append(f'  <bpmn:process id={quoteattr(p.id)} name={quoteattr(p.name)} isExecutable="true">')
    o.append(f'    <bpmn:laneSet id="laneset_{p.id}">')
    for li, lane in enumerate(p.lanes):
        o.append(f'      <bpmn:lane id="lane_{p.id}_{li}" name={quoteattr(lane)}>')
        for nd in p.nodes:
            if nd.lane == lane:
                o.append(f'        <bpmn:flowNodeRef>{nd.id}</bpmn:flowNodeRef>')
        o.append('      </bpmn:lane>')
    o.append('    </bpmn:laneSet>')
    for nd in p.nodes:
        tag = BPMN_TAG[nd.kind]
        name = nd.name if nd.kind != "ai" else f"[IA] {nd.name}"
        o.append(f'    <bpmn:{tag} id={quoteattr(nd.id)} name={quoteattr(name)}>')
        for fid in incoming[nd.id]:
            o.append(f'      <bpmn:incoming>{fid}</bpmn:incoming>')
        for fid in outgoing[nd.id]:
            o.append(f'      <bpmn:outgoing>{fid}</bpmn:outgoing>')
        if nd.kind == "msg":
            o.append(f'      <bpmn:messageEventDefinition id="med_{nd.id}" />')
        if nd.kind == "timer":
            o.append(f'      <bpmn:timerEventDefinition id="ted_{nd.id}" />')
        o.append(f'    </bpmn:{tag}>')
    for i, fl in enumerate(p.flows):
        fid = f"flow_{i+1}"
        nm = f' name={quoteattr(fl.name)}' if fl.name else ''
        o.append(f'    <bpmn:sequenceFlow id="{fid}"{nm} sourceRef={quoteattr(fl.src)} targetRef={quoteattr(fl.dst)} />')
    o.append('  </bpmn:process>')

    # --- DI
    o.append(f'  <bpmndi:BPMNDiagram id="diag_{p.id}">')
    o.append(f'    <bpmndi:BPMNPlane id="plane_{p.id}" bpmnElement="collab_{p.id}">')
    o.append(f'      <bpmndi:BPMNShape id="shape_pool_{p.id}" bpmnElement="pool_{p.id}" isHorizontal="true">')
    o.append(f'        <dc:Bounds x="0" y="0" width="{W}" height="{H}" />')
    o.append('      </bpmndi:BPMNShape>')
    for li, lane in enumerate(p.lanes):
        o.append(f'      <bpmndi:BPMNShape id="shape_lane_{p.id}_{li}" bpmnElement="lane_{p.id}_{li}" isHorizontal="true">')
        o.append(f'        <dc:Bounds x="{POOL_HEADER}" y="{li*LANE_H}" width="{W-POOL_HEADER}" height="{LANE_H}" />')
        o.append('      </bpmndi:BPMNShape>')
    for nd in p.nodes:
        x, y, w, h = geo[nd.id]
        marker = ' isMarkerVisible="true"' if nd.kind == "xor" else ''
        o.append(f'      <bpmndi:BPMNShape id="shape_{nd.id}" bpmnElement={quoteattr(nd.id)}{marker}>')
        o.append(f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" />')
        o.append('      </bpmndi:BPMNShape>')
    for i, fl in enumerate(p.flows):
        fid = f"flow_{i+1}"
        sx, sy, sw, sh = geo[fl.src]
        tx, ty, tw, th = geo[fl.dst]
        pts = route((sx, sy, sw, sh), (tx, ty, tw, th))
        o.append(f'      <bpmndi:BPMNEdge id="edge_{fid}" bpmnElement="{fid}">')
        for (px, py) in pts:
            o.append(f'        <di:waypoint x="{px:.0f}" y="{py:.0f}" />')
        o.append('      </bpmndi:BPMNEdge>')
    o.append('    </bpmndi:BPMNPlane>')
    o.append('  </bpmndi:BPMNDiagram>')
    o.append('</bpmn:definitions>')
    return "\n".join(o)


def route(s, t):
    sx, sy, sw, sh = s
    tx, ty, tw, th = t
    scx, scy = sx + sw / 2, sy + sh / 2
    tcx, tcy = tx + tw / 2, ty + th / 2
    if tx > sx + sw:                       # vers la droite
        if abs(scy - tcy) < 1:
            return [(sx + sw, scy), (tx, tcy)]
        midx = (sx + sw + tx) / 2
        return [(sx + sw, scy), (midx, scy), (midx, tcy), (tx, tcy)]
    if tx + tw < sx:                       # retour vers la gauche : passe par le bas
        yb = max(sy + sh, ty + th) + 25
        return [(scx, sy + sh), (scx, yb), (tcx, yb), (tcx, ty + th)]
    # même colonne : vertical
    if tcy > scy:
        return [(scx, sy + sh), (tcx, ty)]
    return [(scx, sy), (tcx, ty + th)]

# ---------------------------------------------------------------- draw.io
STYLE = {
    "user":    "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10;",
    "service": "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;",
    "manual":  "rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=10;",
    "ai":      "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=10;fontStyle=1;",
    "xor":     "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=9;verticalLabelPosition=bottom;verticalAlign=top;labelBackgroundColor=#ffffff;",
    "par":     "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=9;verticalLabelPosition=bottom;verticalAlign=top;",
    "start":   "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#2e7d32;strokeWidth=2;fontSize=9;verticalLabelPosition=bottom;verticalAlign=top;",
    "end":     "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#c62828;strokeWidth=4;fontSize=9;verticalLabelPosition=bottom;verticalAlign=top;",
    "msg":     "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#1565c0;strokeWidth=2;fontSize=9;verticalLabelPosition=bottom;verticalAlign=top;",
    "timer":   "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#ef6c00;strokeWidth=2;fontSize=9;verticalLabelPosition=bottom;verticalAlign=top;",
}
GW_SYMBOL = {"xor": "<b>X</b>", "par": "<b>+</b>"}
LANE_FILL = ["#f8f9fb", "#eef3fa", "#f8f9fb", "#eef3fa", "#f8f9fb", "#eef3fa", "#f8f9fb"]


def to_drawio(p: Process) -> str:
    geo = geometry(p)
    W, H = pool_size(p)
    o = []
    o.append('<mxfile host="gen_bpmn.py" type="device">')
    o.append(f'<diagram name={quoteattr(p.name)} id="d_{p.id}"><mxGraphModel dx="0" dy="0" grid="1" gridSize="10" '
             'guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">')
    o.append('<root><mxCell id="0"/><mxCell id="1" parent="0"/>')
    pool_id = "pool"
    o.append(f'<mxCell id="{pool_id}" value={quoteattr(p.pool)} style="swimlane;horizontal=0;html=1;startSize={POOL_HEADER};fontStyle=1;fontSize=12;fillColor=#1f3b57;fontColor=#ffffff;strokeColor=#1f3b57;" vertex="1" parent="1">')
    o.append(f'<mxGeometry x="20" y="20" width="{W}" height="{H}" as="geometry"/></mxCell>')
    for li, lane in enumerate(p.lanes):
        o.append(f'<mxCell id="lane{li}" value={quoteattr(lane)} style="swimlane;horizontal=0;html=1;startSize={HEADER_W};fontSize=10;fontStyle=1;fillColor={LANE_FILL[li]};strokeColor=#6b7a8f;swimlaneFillColor={LANE_FILL[li]};" vertex="1" parent="{pool_id}">')
        o.append(f'<mxGeometry x="{POOL_HEADER}" y="{li*LANE_H}" width="{W-POOL_HEADER}" height="{LANE_H}" as="geometry"/></mxCell>')
    lane_index = {l: i for i, l in enumerate(p.lanes)}
    for nd in p.nodes:
        x, y, w, h = geo[nd.id]
        li = lane_index[nd.lane]
        rx = x - POOL_HEADER
        ry = y - li * LANE_H
        if nd.kind in ("xor", "par"):
            label = f'{GW_SYMBOL[nd.kind]}<br>{escape(nd.name)}' if nd.name else GW_SYMBOL[nd.kind]
            # symbole au centre, question en dessous : on utilise deux cellules
            o.append(f'<mxCell id="{nd.id}" value={quoteattr(GW_SYMBOL[nd.kind])} style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="lane{li}">')
            o.append(f'<mxGeometry x="{rx:.0f}" y="{ry:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
            if nd.name:
                o.append(f'<mxCell id="{nd.id}_lbl" value={quoteattr(nd.name)} style="text;html=1;align=center;verticalAlign=top;fontSize=9;fontStyle=2;" vertex="1" parent="lane{li}">')
                o.append(f'<mxGeometry x="{rx-40:.0f}" y="{ry+h+2:.0f}" width="{w+80:.0f}" height="24" as="geometry"/></mxCell>')
            continue
        name = nd.name if nd.kind != "ai" else f"[IA] {nd.name}"
        o.append(f'<mxCell id="{nd.id}" value={quoteattr(name)} style="{STYLE[nd.kind]}" vertex="1" parent="lane{li}">')
        o.append(f'<mxGeometry x="{rx:.0f}" y="{ry:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
    node_lane = {nd.id: nd.lane for nd in p.nodes}
    node_col = {nd.id: nd.col for nd in p.nodes}
    for i, fl in enumerate(p.flows):
        fid = f"flow_{i+1}"
        o.append(f'<mxCell id="{fid}" value={quoteattr(fl.name)} style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=9;labelBackgroundColor=#ffffff;strokeColor=#1f3b57;" edge="1" parent="1" source="{fl.src}" target="{fl.dst}">')
        # libellé près de la cible quand le flux change de lane (évite les chevauchements en sortie de gateway)
        if fl.name and node_lane[fl.src] != node_lane[fl.dst]:
            o.append('<mxGeometry x="0.55" relative="1" as="geometry"/></mxCell>')
        elif fl.name and node_col[fl.dst] < node_col[fl.src]:
            o.append('<mxGeometry x="-0.5" relative="1" as="geometry"/></mxCell>')
        else:
            o.append('<mxGeometry relative="1" as="geometry"/></mxCell>')
    o.append('</root></mxGraphModel></diagram></mxfile>')
    return "\n".join(o)

# ================================================================ PROCESSUS
# Lanes communes
CIT = "Citoyen"
POR = "Portail cnie.ma"
CED = "Agent CEDI"
CPC = "Centre de production (CPC)"

# ---------- P0 as-is -----------------------------------------------------
asis = Process("P0_asis", "Demande et renouvellement de la CNIE - Actuel (as-is)",
               "DGSN - Demande et renouvellement de la CNIE (actuel)", [CIT, POR, CED, CPC])
(asis
 .n("s1", "start", CIT, "Besoin de CNIE (1re demande, renouvellement, duplicata)", 0)
 .n("t1", "manual", CIT, "Rassembler les pièces (acte, certificat de résidence, 4 photos)", 1)
 .n("t2", "manual", CIT, "Acheter l'e-timbre (75 DH)", 2)
 .n("t3", "user", CIT, "Saisir la pré-demande (identité, filiation, adresse, AR/FR)", 3)
 .n("t4", "service", POR, "Générer le numéro de pré-demande", 4)
 .n("t5", "user", CIT, "Choisir le CEDI, la date et le créneau", 5)
 .n("g1", "xor", POR, "Créneau disponible ?", 6)
 .n("t6", "service", POR, "Émettre le récépissé de rendez-vous", 7)
 .n("t7", "manual", CIT, "Imprimer et signer le formulaire", 8)
 .n("t8", "manual", CIT, "Se présenter au CEDI avec le dossier", 9)
 .n("t9", "manual", CED, "Contrôler l'identité et les pièces", 10)
 .n("g2", "xor", CED, "Dossier complet ?", 11)
 .n("t10", "service", POR, "Statut « Dossier incomplet »", 12)
 .n("t11", "manual", CED, "Capturer la biométrie (photo, empreintes, signature)", 12)
 .n("t12", "manual", CED, "Valider le dossier et remettre le récépissé daté", 13)
 .n("t13", "service", CPC, "Contrôler l'unicité (AFIS) et la qualité", 14)
 .n("t14", "service", CPC, "Personnaliser la carte (puce, Lasink)", 15)
 .n("t15", "manual", CPC, "Expédier la carte au CEDI", 16)
 .n("t16", "service", POR, "Statut « Disponible » + e-mail/SMS", 17)
 .n("t17", "manual", CIT, "Se présenter au CEDI avec le récépissé", 18)
 .n("t18", "manual", CED, "Remettre la carte et le code PIN", 19)
 .n("t19", "service", POR, "Statut « Remise »", 20)
 .n("e1", "end", CIT, "Carte remise", 21)
 .f("s1", "t1").f("t1", "t2").f("t2", "t3").f("t3", "t4").f("t4", "t5").f("t5", "g1")
 .f("g1", "t5", "non : autre centre / autre date").f("g1", "t6", "oui").f("t6", "t7").f("t7", "t8").f("t8", "t9").f("t9", "g2")
 .f("g2", "t10", "non").f("t10", "t5", "nouveau RDV").f("g2", "t11", "oui").f("t11", "t12").f("t12", "t13").f("t13", "t14")
 .f("t14", "t15").f("t15", "t16").f("t16", "t17").f("t17", "t18").f("t18", "t19").f("t19", "e1"))

# ---------- P0 to-be -----------------------------------------------------
NUM = "Canal numérique (portail, app)"
IA = "Plateforme IA"
INS = "Agent instructeur"
tobe = Process("P0_tobe", "Demande et renouvellement de la CNIE - Cible (to-be)",
               "DGSN - Demande et renouvellement de la CNIE (cible)", [CIT, NUM, IA, INS, CED, CPC])
(tobe
 .n("s1", "start", CIT, "Besoin de CNIE", 0)
 .n("t1", "user", CIT, "S'authentifier (Identité numérique) ou créer un compte", 1)
 .n("t2", "service", NUM, "Pré-remplir la demande (données de la carte / état civil)", 2)
 .n("t3", "ai", IA, "Assistant conversationnel : guider et vérifier la saisie", 3)
 .n("t4", "user", CIT, "Compléter la pré-demande et téléverser les pièces", 4)
 .n("t5", "ai", IA, "Contrôle documentaire (OCR, cohérence, photo ICAO)", 5)
 .n("g1", "xor", IA, "Résultat du contrôle ?", 6)
 .n("t6", "user", CIT, "Corriger les pièces signalées", 7)
 .n("t7", "user", INS, "Instruire le dossier signalé", 7)
 .n("g2", "xor", INS, "Dossier validé ?", 8)
 .n("t8", "service", NUM, "Payer les frais en ligne (e-timbre intégré)", 9)
 .n("t9", "ai", IA, "Recommander les créneaux (prévision d'affluence)", 10)
 .n("t10", "user", CIT, "Confirmer le créneau au CEDI", 11)
 .n("t11", "service", NUM, "Émettre la convocation QR + rappels automatiques", 12)
 .n("t12", "manual", CED, "Scanner le QR et capturer la biométrie", 13)
 .n("t13", "ai", IA, "Vérifier la biométrie (dédoublonnage, anti-fraude)", 14)
 .n("g3", "xor", IA, "Alerte fraude ?", 15)
 .n("t14", "user", INS, "Traiter l'alerte (enquête)", 16)
 .n("t15", "service", CPC, "Contrôler, personnaliser et expédier (suivi temps réel)", 17)
 .n("t16", "service", NUM, "Notifier « Disponible » (push, SMS, e-mail)", 18)
 .n("g4", "xor", CIT, "Mode de remise ?", 19)
 .n("t17", "manual", CED, "Remettre la carte au CEDI (PIN sécurisé)", 20)
 .n("t18", "service", NUM, "Livrer par la Poste avec authentification à la remise", 20)
 .n("t19", "user", CIT, "Activer la carte numérique dans Mon e-ID", 21)
 .n("e1", "end", CIT, "Carte remise et identité numérique active", 22)
 .n("e2", "end", INS, "Demande rejetée", 9)
 .f("s1", "t1").f("t1", "t2").f("t2", "t3").f("t3", "t4").f("t4", "t5").f("t5", "g1")
 .f("g1", "t6", "non conforme").f("t6", "t5").f("g1", "t7", "doute").f("t7", "g2").f("g2", "t6", "à compléter")
 .f("g2", "e2", "rejet").f("g2", "t8", "oui").f("g1", "t8", "conforme")
 .f("t8", "t9").f("t9", "t10").f("t10", "t11").f("t11", "t12").f("t12", "t13").f("t13", "g3")
 .f("g3", "t14", "oui").f("t14", "e2").f("g3", "t15", "non").f("t15", "t16").f("t16", "g4")
 .f("g4", "t17", "au centre").f("g4", "t18", "à domicile").f("t17", "t19").f("t18", "t19").f("t19", "e1"))

# ---------- SP1 Bonita ---------------------------------------------------
SYS = "Services automatiques"
sp1 = Process("SP1_predemande", "SP1 - Pré-demande en ligne, contrôle IA des pièces et prise de RDV",
              "DGSN - SP1 Pré-demande CNIE (prototype Bonita)", [CIT, SYS, INS])
(sp1
 .n("s1", "start", CIT, "Nouvelle demande", 0)
 .n("t1", "user", CIT, "Saisir la pré-demande (type, identité, état civil, adresse, contact)", 1)
 .n("t2", "user", CIT, "Téléverser les pièces (acte, résidence, photo)", 2)
 .n("t3", "ai", SYS, "Contrôle IA des pièces (OCR + cohérence + photo)", 3)
 .n("g1", "xor", SYS, "Score de conformité ?", 4)
 .n("t4", "user", CIT, "Corriger les anomalies signalées", 5)
 .n("t5", "user", INS, "Instruire manuellement le dossier", 5)
 .n("g2", "xor", INS, "Décision ?", 6)
 .n("e2", "end", INS, "Demande rejetée", 7)
 .n("t6", "user", CIT, "Choisir le centre et le créneau recommandé", 7)
 .n("t7", "user", CIT, "Régler les frais (code e-timbre)", 8)
 .n("t8", "service", SYS, "Vérifier l'e-timbre et réserver le créneau", 9)
 .n("t9", "service", SYS, "Générer le récépissé, le QR code et notifier", 10)
 .n("t10", "user", CIT, "Consulter la confirmation et le récépissé", 11)
 .n("e1", "end", CIT, "Pré-demande confirmée", 12)
 .f("s1", "t1").f("t1", "t2").f("t2", "t3").f("t3", "g1")
 .f("g1", "t4", "< 60 % : non conforme").f("t4", "t3").f("g1", "t5", "60-85 % : doute").f("t5", "g2")
 .f("g2", "t4", "à corriger").f("g2", "e2", "rejet").f("g2", "t6", "validé").f("g1", "t6", "> 85 % : conforme")
 .f("t6", "t7").f("t7", "t8").f("t8", "t9").f("t9", "t10").f("t10", "e1"))

# ================================================================ main
if __name__ == "__main__":
    os.makedirs(OUT_BPMN, exist_ok=True)
    os.makedirs(OUT_FIG, exist_ok=True)
    for p, fname in ((asis, "P0_demande_cnie_asis"), (tobe, "P0_demande_cnie_tobe"), (sp1, "SP1_predemande_bonita")):
        with open(os.path.join(OUT_BPMN, fname + ".bpmn"), "w", encoding="utf-8") as fh:
            fh.write(to_bpmn(p))
        with open(os.path.join(OUT_BPMN, fname + ".drawio"), "w", encoding="utf-8") as fh:
            fh.write(to_drawio(p))
        print("OK", fname, len(p.nodes), "noeuds", len(p.flows), "flux")
