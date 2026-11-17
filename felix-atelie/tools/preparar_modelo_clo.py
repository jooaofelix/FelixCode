#!/usr/bin/env python3
"""
Prepara um modelo de camiseta exportado do CLO 3D (OBJ) para o 148 Ateliê.

O OBJ do CLO traz cada peça com frente e verso do tecido, a borda (espessura),
as ribanas e as costuras 3D (pesadas). Este script:
  1. escolhe a camada externa de cada peça e mantém bordas e ribanas;
  2. descarta as costuras 3D;
  3. normaliza o UV para o retângulo dos moldes e tira o contorno de cada molde em cm;
  4. reduz a malha com o gltfpack (npm) e grava ../modelo-oversized.js
     (moldes + malha em base64), que o index.html carrega.

Uso:
  pip install numpy
  python tools/preparar_modelo_clo.py caminho/obj.obj            # usa 170 cm por unidade de UV
  python tools/preparar_modelo_clo.py caminho/obj.obj --cm-uv 175 --reducao 0.45

A ordem dos blocos (usemtl) segue o modelo "Male oversized tshirt": 0-2 costas,
3-5 frente, 6-8 manga direita, 9-11 manga esquerda, 12-23 ribanas, 24+ costuras.
Para outro modelo, ajuste a lista `info` (peças e blocos) mais abaixo.
"""
import argparse, base64, json, os, subprocess, sys, tempfile
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('obj')
ap.add_argument('--cm-uv', type=float, default=170.0, help='cm por unidade de UV (calibração do tamanho real)')
ap.add_argument('--reducao', type=float, default=0.45, help='fração de triângulos mantida pelo gltfpack')
ap.add_argument('--saida', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'modelo-oversized.js'))
args = ap.parse_args()
CMU = args.cm_uv
tmp = tempfile.mkdtemp()
OUT_OBJ, OUT_JSON = os.path.join(tmp, 'reduzido.obj'), os.path.join(tmp, 'moldes.json')

print('lendo o OBJ (pode levar um minuto)...')
V, VT, VN, blocks, cur = [], [], [], [], None
with open(args.obj) as f:
    for line in f:
        c = line[:2]
        if c == 'v ': V.append(line[2:].split())
        elif c == 'vt': VT.append(line[3:].split()[:2])
        elif c == 'vn': VN.append(line[3:].split())
        elif c == 'f ': cur['f'].append([p.split('/') for p in line[2:].split()])
        elif line.startswith('usemtl'):
            cur = {'mtl': line.split()[1], 'f': []}; blocks.append(cur)
V = np.array(V, np.float32); VT = np.array(VT, np.float32); VN = np.array(VN, np.float32)
B = []
for b in blocks:
    fa = np.array(b['f'], np.int64)
    B.append({'mtl': b['mtl'], 'v': fa[:, :, 0] - 1, 't': fa[:, :, 1] - 1})


center = V[np.unique(np.concatenate([B[i]['v'].ravel() for i in (0, 3)]))].mean(0)

def outer_of(a, b):
    va, vb = np.unique(B[a]['v']), np.unique(B[b]['v'])
    off = V[va] - V[vb]                      # direção de b para a
    rad = V[va] - center
    vote = np.sign((off * rad).sum(1)).sum()  # a está mais "para fora" que b?
    return a if vote > 0 else b

pairs = [(0, 1), (3, 4), (6, 7), (9, 10)]
outer = {p[0]: outer_of(*p) for p in pairs}
print('camadas externas', outer)
keep = [outer[0], outer[3], outer[6], outer[9], 2, 5, 8, 11] + list(range(12, 24))

# retângulo dos moldes no UV
used_t = np.unique(np.concatenate([B[i]['t'].ravel() for i in keep]))
u0, v0 = VT[used_t].min(0)
u1, v1 = VT[used_t].max(0)
pad = 0.004
u0, v0, u1, v1 = u0 - pad, v0 - pad, u1 + pad, v1 + pad
AW, AH = (u1 - u0) * CMU, (v1 - v0) * CMU

# escala 3D: área real (3D) × área no molde, na frente
def area3(tris):
    p = V[tris]; return 0.5 * np.linalg.norm(np.cross(p[:, 1] - p[:, 0], p[:, 2] - p[:, 0]), axis=1).sum()
def area2(tris):
    p = VT[tris]; e1, e2 = p[:, 1] - p[:, 0], p[:, 2] - p[:, 0]
    return 0.5 * np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]).sum()
k = np.sqrt(area3(B[outer[3]]['v']) / area2(B[outer[3]]['t']))  # unidades 3D por unidade de UV
cm_per_unit = CMU / k
print(f'3D: {k:.4f} unid/UV  ->  {cm_per_unit:.1f} cm por unidade 3D')

# ---- OBJ reduzido ----
vidx = np.unique(np.concatenate([B[i]['v'].ravel() for i in keep]))
remap = -np.ones(len(V), np.int64); remap[vidx] = np.arange(len(vidx))
P = (V[vidx] - np.array([center[0], 0, center[2]])) * cm_per_unit  # em cm, centrado em x/z
ymid = (P[:, 1].min() + P[:, 1].max()) / 2
P[:, 1] -= ymid
T = VT[vidx].copy(); T[:, 0] = (T[:, 0] - u0) / (u1 - u0); T[:, 1] = (T[:, 1] - v0) / (v1 - v0)
N = VN[vidx]
with open(OUT_OBJ, 'w') as f:
    f.write('# Atelie 148 - oversized reduzido\n')
    for p in P: f.write(f'v {p[0]:.3f} {p[1]:.3f} {p[2]:.3f}\n')
    for t in T: f.write(f'vt {t[0]:.5f} {t[1]:.5f}\n')
    for n in N: f.write(f'vn {n[0]:.4f} {n[1]:.4f} {n[2]:.4f}\n')
    f.write('o camiseta\nusemtl tecido\n')
    for i in keep:
        for tri in remap[B[i]['v']] + 1:
            a, b, c = tri
            f.write(f'f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c}\n')
print('vértices', len(vidx), 'triângulos', sum(len(B[i]['v']) for i in keep), 'altura', np.ptp(P[:, 1]).round(1), 'largura', np.ptp(P[:, 0]).round(1))

# ---- contornos dos moldes ----
def outline(block):
    t = B[block]['t']
    e = np.sort(np.concatenate([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]]), axis=1)
    uniq, cnt = np.unique(e, axis=0, return_counts=True)
    border = uniq[cnt == 1]
    adj = {}
    for a, b in border:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen, loops = set(), []
    for s in adj:
        if s in seen: continue
        loop, prev, cur = [s], None, s
        seen.add(s)
        while True:
            nxt = [n for n in adj[cur] if n != prev and n not in seen]
            if not nxt: break
            prev, cur = cur, nxt[0]; seen.add(cur); loop.append(cur)
        loops.append(loop)
    loop = max(loops, key=len)
    pts = VT[loop]
    return np.stack([(pts[:, 0] - u0) * CMU, (v1 - pts[:, 1]) * CMU], 1)

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; ab = b - a; L = np.hypot(*ab) or 1e-9
    dists = np.abs(ab[0] * (pts[:, 1] - a[1]) - ab[1] * (pts[:, 0] - a[0])) / L
    i = int(np.argmax(dists))
    if dists[i] > eps:
        return np.vstack([rdp(pts[:i + 1], eps)[:-1], rdp(pts[i:], eps)])
    return np.vstack([a, b])

def closed_rdp(pts, eps):
    i = int(np.argmax(np.hypot(*(pts - pts[0]).T)))
    return np.vstack([rdp(pts[:i + 1], eps)[:-1], rdp(np.vstack([pts[i:], pts[:1]]), eps)[:-1]])

info = [
    ('ribF', 'Gola · frente', 'ribF', 12), ('ribF2', 'Gola · frente (dobra)', 'ribF', 18),
    ('ribB', 'Gola · costas', 'ribB', 15), ('ribB2', 'Gola · costas (dobra)', 'ribB', 21),
    ('front', 'Frente', 'front', outer[3]), ('back', 'Costas', 'back', outer[0]),
    ('sleeveR', 'Manga direita', 'sleeveR', outer[6]), ('sleeveL', 'Manga esquerda', 'sleeveL', outer[9]),
]
pieces = []
for pid, name, group, blk in info:
    o = closed_rdp(outline(blk), 0.08)
    x0, y0 = o.min(0); x1, y1 = o.max(0)
    poly = [[round(float(x - x0), 2), round(float(y - y0), 2)] for x, y in o]
    pieces.append({'id': pid, 'name': name, 'group': group, 'x': round(float(x0), 2), 'y': round(float(y0), 2),
                   'w': round(float(x1 - x0), 2), 'h': round(float(y1 - y0), 2), 'poly': poly})
    print(pid, 'pontos', len(poly), 'tamanho', round(x1 - x0, 1), 'x', round(y1 - y0, 1), 'cm')

def neck_drop(pc):
    pts = np.array(pc['poly']); cx = pc['w'] / 2
    band = pts[np.abs(pts[:, 0] - cx) < 1.5]
    top = band[band[:, 1] < pc['h'] / 2]
    return round(float(top[:, 1].max() if len(top) else 0), 2)

P_by = {p['id']: p for p in pieces}
meta = {
    'CMU': CMU, 'AW': round(float(AW), 2), 'AH': round(float(AH), 2), 'cmPerUnit': round(float(cm_per_unit), 3),
    'neck': {'front': neck_drop(P_by['front']), 'back': neck_drop(P_by['back'])},
    'height': round(float(np.ptp(P[:, 1])), 2), 'width': round(float(np.ptp(P[:, 0])), 2),
    'pieces': pieces,
}
json.dump(meta, open(OUT_JSON, 'w'), ensure_ascii=False, separators=(',', ':'))
print('atlas', meta['AW'], 'x', meta['AH'], 'cm | gola: frente', meta['neck']['front'], 'costas', meta['neck']['back'])


# ---- malha reduzida + arquivo do Ateliê ----
glb = os.path.join(tmp, 'modelo.glb')
cmd = ['npx', '--yes', 'gltfpack@0.24.0', '-i', OUT_OBJ, '-o', glb, '-si', str(args.reducao), '-kv', '-vtf']
print('gltfpack:', ' '.join(cmd))
subprocess.run(cmd, check=True, shell=(os.name == 'nt'))
js = ("/* 148 Ateliê — modelo Oversized (CLO 3D, otimizado). Gerado por tools/preparar_modelo_clo.py. Moldes em cm. */\n"
      "window.ATELIE_OVERSIZED = {\n  meta: " + json.dumps(json.load(open(OUT_JSON)), ensure_ascii=False, separators=(',', ':')) +
      ",\n  glb: '" + base64.b64encode(open(glb, 'rb').read()).decode() + "'\n};\n")
open(args.saida, 'w', encoding='utf-8').write(js)
print('gravado', os.path.abspath(args.saida), f'({len(js) / 1e6:.1f} MB)')
