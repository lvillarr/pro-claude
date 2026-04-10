#!/usr/bin/env python3
"""
BPMN 2.0 → PNG renderer
Arauco — Excelencia Operacional
Renderiza diagramas BPMN como imágenes PNG legibles.
"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import textwrap
import os
import sys

NS = {
    'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
    'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
    'dc':    'http://www.omg.org/spec/DD/20100524/DC',
    'di':    'http://www.omg.org/spec/DD/20100524/DI',
}

# ── Colores por tipo de elemento ────────────────────────────────────────────
COLORS = {
    'userTask':            ('#DBEAFE', '#1D4ED8'),   # fondo, borde
    'serviceTask':         ('#D1FAE5', '#065F46'),
    'manualTask':          ('#FEF9C3', '#92400E'),
    'task':                ('#DBEAFE', '#1D4ED8'),
    'subProcess':          ('#E0E7FF', '#3730A3'),
    'exclusiveGateway':    ('#FEF3C7', '#B45309'),
    'parallelGateway':     ('#F3E8FF', '#6D28D9'),
    'inclusiveGateway':    ('#FEF3C7', '#B45309'),
    'startEvent':          ('#BBF7D0', '#15803D'),
    'endEvent':            ('#FEE2E2', '#B91C1C'),
    'intermediateThrowEvent': ('#FEF9C3', '#92400E'),
    'intermediateCatchEvent': ('#DBEAFE', '#1D4ED8'),
}

LANE_COLORS = [
    '#F0F9FF', '#F0FDF4', '#FFF7ED', '#FDF4FF',
    '#FFFBEB', '#F0F9FF', '#F7FEE7', '#FFF1F2',
]

GATEWAY_SYMBOLS = {
    'exclusiveGateway': '×',
    'parallelGateway':  '+',
    'inclusiveGateway': '○',
}


def wrap_text(text, max_chars=22):
    """Divide texto largo en líneas cortas."""
    if not text:
        return ''
    lines = textwrap.wrap(text, width=max_chars)
    return '\n'.join(lines[:4])  # máximo 4 líneas


def tag_local(element):
    """Retorna el nombre local del tag XML (sin namespace)."""
    tag = element.tag
    return tag.split('}')[-1] if '}' in tag else tag


def render_bpmn(bpmn_path: str, output_path: str, title_override: str = None):
    tree = ET.parse(bpmn_path)
    root = tree.getroot()

    # ── 1. Construir mapa ID → tipo y nombre ────────────────────────────────
    elem_meta = {}   # id → {'type': str, 'name': str}
    for process in root.findall('.//bpmn:process', NS):
        for child in process:
            eid = child.get('id')
            if eid:
                elem_meta[eid] = {
                    'type': tag_local(child),
                    'name': child.get('name', ''),
                }

    # ── 2. Construir mapa ID → lane ─────────────────────────────────────────
    elem_lane = {}   # id → lane_name
    for i, lane in enumerate(root.findall('.//bpmn:lane', NS)):
        lane_name = lane.get('name', f'Lane {i}')
        for ref in lane.findall('bpmn:flowNodeRef', NS):
            if ref.text:
                elem_lane[ref.text] = (lane_name, i)

    # ── 3. Extraer shapes y edges del diagrama ───────────────────────────────
    plane = root.find('.//bpmndi:BPMNPlane', NS)
    if plane is None:
        print(f"ERROR: No se encontró BPMNPlane en {bpmn_path}")
        return

    shapes = {}   # elem_id → {x,y,w,h,type,name,lane_idx}
    edges  = {}   # elem_id → {waypoints, label}

    for shape in plane.findall('bpmndi:BPMNShape', NS):
        eid = shape.get('bpmnElement')
        bounds = shape.find('dc:Bounds', NS)
        if eid and bounds is not None:
            meta = elem_meta.get(eid, {'type': 'unknown', 'name': eid})
            lane_info = elem_lane.get(eid, ('', 0))
            shapes[eid] = {
                'x': float(bounds.get('x', 0)),
                'y': float(bounds.get('y', 0)),
                'w': float(bounds.get('width', 100)),
                'h': float(bounds.get('height', 80)),
                'type': meta['type'],
                'name': meta['name'],
                'lane_name': lane_info[0],
                'lane_idx':  lane_info[1],
            }

    for edge in plane.findall('bpmndi:BPMNEdge', NS):
        eid = edge.get('bpmnElement')
        waypoints = []
        for wp in edge.findall('di:waypoint', NS):
            waypoints.append((float(wp.get('x', 0)), float(wp.get('y', 0))))
        label_el = edge.find('.//bpmndi:BPMNLabel/dc:Bounds', NS)
        label_pos = None
        if label_el is not None:
            label_pos = (float(label_el.get('x', 0)) + float(label_el.get('width', 0))/2,
                         float(label_el.get('y', 0)))
        # Get name from sequenceFlow
        sf_meta = elem_meta.get(eid, {})
        # Also check the edge element's name attribute
        edge_name = edge.get('name', '') or sf_meta.get('name', '')
        if eid:
            edges[eid] = {
                'waypoints': waypoints,
                'label': edge_name,
                'label_pos': label_pos,
            }

    if not shapes:
        print(f"ERROR: No shapes encontradas en {bpmn_path}")
        return

    # ── 4. Calcular límites del canvas ───────────────────────────────────────
    all_x, all_y = [], []
    for s in shapes.values():
        all_x += [s['x'], s['x'] + s['w']]
        all_y += [s['y'], s['y'] + s['h']]
    for e in edges.values():
        for wx, wy in e['waypoints']:
            all_x.append(wx)
            all_y.append(wy)

    pad = 40
    min_x = min(all_x) - pad
    max_x = max(all_x) + pad
    min_y = min(all_y) - pad
    max_y = max(all_y) + pad * 2  # espacio para título

    canvas_w = max_x - min_x
    canvas_h = max_y - min_y

    # Escalar para imagen legible (~3000px ancho máximo a 150 dpi)
    target_w_in = min(22, canvas_w / 150)
    scale = target_w_in / (canvas_w / 96)
    fig_w = canvas_w * scale / 96 * 1.0
    fig_h = canvas_h * scale / 96 * 1.0
    fig_w = max(fig_w, 12)
    fig_h = max(fig_h, 6)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=180)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(max_y, min_y)   # Y invertido (BPMN: 0 arriba)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # ── 5. Dibujar fondos de lanes ───────────────────────────────────────────
    lanes_seen = {}
    for s in shapes.values():
        ln = s['lane_name']
        li = s['lane_idx']
        if ln not in lanes_seen:
            lanes_seen[ln] = {'idx': li, 'xs': [], 'ys': []}
        lanes_seen[ln]['xs'] += [s['x'], s['x'] + s['w']]
        lanes_seen[ln]['ys'] += [s['y'], s['y'] + s['h']]

    # Extender lanes al ancho total del canvas
    for ln, info in lanes_seen.items():
        if not info['xs']:
            continue
        lx = min_x + pad/2
        lw = max_x - min_x - pad
        ly = min(info['ys']) - 20
        lh = max(info['ys']) - min(info['ys']) + 40
        color = LANE_COLORS[info['idx'] % len(LANE_COLORS)]
        rect = mpatches.FancyBboxPatch(
            (lx, ly), lw, lh,
            boxstyle="square,pad=0",
            linewidth=0.6, edgecolor='#CCCCCC',
            facecolor=color, zorder=1, alpha=0.6,
        )
        ax.add_patch(rect)
        # Etiqueta del lane (vertical, izquierda)
        label_wrapped = '\n'.join(textwrap.wrap(ln, 12))
        ax.text(lx + 14, ly + lh / 2, label_wrapped,
                ha='center', va='center', fontsize=5.5,
                rotation=90, color='#444444', zorder=2,
                linespacing=1.2)

    # ── 6. Dibujar edges (flujos) ────────────────────────────────────────────
    for eid, e in edges.items():
        wps = e['waypoints']
        if len(wps) < 2:
            continue
        xs = [p[0] for p in wps]
        ys = [p[1] for p in wps]
        ax.plot(xs, ys, '-', color='#374151', linewidth=0.7, zorder=3, solid_capstyle='round')
        # Flecha al final
        dx = wps[-1][0] - wps[-2][0]
        dy = wps[-1][1] - wps[-2][1]
        if abs(dx) + abs(dy) > 1:
            ax.annotate('',
                        xy=(wps[-1][0], wps[-1][1]),
                        xytext=(wps[-2][0], wps[-2][1]),
                        arrowprops=dict(arrowstyle='-|>', color='#374151',
                                        lw=0.7, mutation_scale=8),
                        zorder=4)
        # Etiqueta del flow (Sí/No)
        label = e.get('label', '')
        if label:
            mx = (wps[0][0] + wps[1][0]) / 2
            my = (wps[0][1] + wps[1][1]) / 2
            ax.text(mx, my, label, ha='center', va='center', fontsize=5,
                    color='#B45309', fontweight='bold', zorder=5,
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                              edgecolor='none', alpha=0.85))

    # ── 7. Dibujar shapes ────────────────────────────────────────────────────
    for eid, s in shapes.items():
        t = s['type']
        x, y, w, h = s['x'], s['y'], s['w'], s['h']
        name = wrap_text(s['name'], max_chars=int(w / 5.5))
        fc, ec = COLORS.get(t, ('#F3F4F6', '#6B7280'))

        if t in ('startEvent', 'endEvent',
                 'intermediateThrowEvent', 'intermediateCatchEvent'):
            cx, cy, r = x + w/2, y + h/2, min(w, h)/2
            lw = 2.5 if t == 'endEvent' else 1.5
            circle = plt.Circle((cx, cy), r, facecolor=fc, edgecolor=ec,
                                 linewidth=lw, zorder=5)
            ax.add_patch(circle)
            if name:
                ax.text(cx, y + h + 10, name,
                        ha='center', va='top', fontsize=4.5,
                        color='#1F2937', zorder=6, multialignment='center',
                        linespacing=1.3)

        elif t in ('exclusiveGateway', 'parallelGateway', 'inclusiveGateway'):
            cx, cy = x + w/2, y + h/2
            half = min(w, h) / 2
            diamond_x = [cx, cx + half, cx, cx - half, cx]
            diamond_y = [cy - half, cy, cy + half, cy, cy - half]
            ax.fill(diamond_x, diamond_y, facecolor=fc, edgecolor=ec,
                    linewidth=1.2, zorder=5)
            sym = GATEWAY_SYMBOLS.get(t, '')
            ax.text(cx, cy, sym, ha='center', va='center',
                    fontsize=9, color=ec, fontweight='bold', zorder=6)
            if name:
                ax.text(cx, y + h + 8, name,
                        ha='center', va='top', fontsize=4.5,
                        color='#1F2937', zorder=6, multialignment='center',
                        linespacing=1.3)

        else:  # tasks y subProcesos
            rect = mpatches.FancyBboxPatch(
                (x, y), w, h,
                boxstyle="round,pad=2",
                linewidth=1, edgecolor=ec,
                facecolor=fc, zorder=5,
            )
            ax.add_patch(rect)
            # Icono pequeño tipo tarea
            icon = ''
            if t == 'serviceTask':   icon = '⚙ '
            elif t == 'userTask':    icon = '▣ '
            elif t == 'manualTask':  icon = '✋ '
            display = icon + name if name else eid
            fs = max(3.8, min(5.5, 5.5 * (w / 120)))
            ax.text(x + w/2, y + h/2, display,
                    ha='center', va='center',
                    fontsize=fs, color='#111827',
                    multialignment='center', linespacing=1.3,
                    zorder=6)

    # ── 8. Título ────────────────────────────────────────────────────────────
    process_el = root.find('.//bpmn:process', NS)
    title = title_override or (process_el.get('name', '') if process_el is not None else '')
    ax.set_title(title, fontsize=11, fontweight='bold',
                 color='#1E3A5F', pad=10,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#EFF6FF',
                           edgecolor='#BFDBFE', linewidth=1))

    plt.tight_layout(pad=0.5)
    plt.savefig(output_path, dpi=180, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ Guardado: {output_path}")


if __name__ == '__main__':
    base = '/Users/lucianovillarroelparra/Documents/Proyecto_Claude/datos'
    jobs = [
        (
            '2026-04-09_proceso-bpmn-gestion-produccion-contratistas-as-is.bpmn',
            '2026-04-09_proceso-bpmn-gestion-produccion-contratistas-as-is.png',
        ),
        (
            '2026-04-09_proceso-bpmn-gestion-produccion-contratistas-to-be.bpmn',
            '2026-04-09_proceso-bpmn-gestion-produccion-contratistas-to-be.png',
        ),
    ]
    for bpmn_file, png_file in jobs:
        render_bpmn(
            os.path.join(base, bpmn_file),
            os.path.join(base, png_file),
        )
