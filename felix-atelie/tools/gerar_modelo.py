#!/usr/bin/env python3
"""
Gera o modelo da camiseta do Ateliê 3D a partir de um mockup em três vistas.

Entrada: uma imagem (JPG/PNG) com a camiseta de FRENTE, de LADO e de COSTAS,
lado a lado, nessa ordem, sobre fundo claro (branco ou xadrez de "transparente").
A vista de lado deve mostrar o lado DIREITO de quem veste, com o peito virado
para a DIREITA da imagem.

Saída (na pasta indicada em --saida):
  profile.json  medidas por altura (largura, centro e profundidade) + linha do ombro
  shade.jpg     sombreamento das três vistas (cinza; 127 = tom médio do tecido)
  mask.png      recorte suave das três vistas

Com --embutir caminho/index.html, as três coisas são gravadas direto no app
(linhas `const MODEL = ...`, `const SHADE_URL = ...` e `const MASK_URL = ...`).

Uso:
  python tools/gerar_modelo.py mockup.jpg --saida tools/saida --embutir index.html
  python tools/gerar_modelo.py mockup.jpg --limiar 185 --comprimento 74

Requer: pip install pillow numpy
"""
import argparse, base64, json, os, re, sys
import numpy as np
from PIL import Image, ImageFilter

BASE_W = 2048  # todas as medidas internas usam a imagem redimensionada para 2048 px de largura


def runs(flags, min_len=20):
    """Trechos contínuos de True num vetor booleano: [(início, fim), ...]."""
    out, start = [], None
    for i, v in enumerate(flags):
        if v and start is None:
            start = i
        if not v and start is not None:
            if i - start >= min_len:
                out.append((start, i))
            start = None
    if start is not None and len(flags) - start >= min_len:
        out.append((start, len(flags)))
    return out


def extent(mask, y, x0, x1):
    r = np.where(mask[y, x0:x1])[0]
    return (r.min() + x0, r.max() + x0) if len(r) else None


def erode(mk, n):
    for _ in range(n):
        e = mk.copy()
        e[1:] &= mk[:-1]; e[:-1] &= mk[1:]; e[:, 1:] &= mk[:, :-1]; e[:, :-1] &= mk[:, 1:]
        mk = e
    return mk


def dilate_fill(g, mk, iters, fallback):
    """Preenche o fundo com a média dos vizinhos da camiseta (evita bordas claras/xadrez no 3D)."""
    val = np.where(mk, g, 0).astype(np.float32)
    cnt = mk.astype(np.float32)
    for _ in range(iters):
        sv = np.zeros_like(val); sc = np.zeros_like(cnt)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            sv += np.roll(np.roll(val * cnt, dy, 0), dx, 1)
            sc += np.roll(np.roll(cnt, dy, 0), dx, 1)
        new = (cnt == 0) & (sc > 0)
        val = np.where(new, sv / np.maximum(sc, 1e-6), val)
        cnt = np.where(new, 1, cnt)
    return np.where(cnt > 0, val, fallback)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('imagem')
    ap.add_argument('--saida', default=os.path.join(os.path.dirname(__file__), 'saida'))
    ap.add_argument('--embutir', metavar='INDEX_HTML', help='grava o modelo direto no index.html')
    ap.add_argument('--limiar', type=float, default=190, help='luminância abaixo disso é camiseta (fundo é ~205-255)')
    ap.add_argument('--comprimento', type=float, default=None,
                    help='comprimento real da peça em cm (gola até a barra). Padrão: 0,1 cm por pixel')
    ap.add_argument('--escala', type=float, default=2.0, help='resolução do sombreamento/recorte (2 = 2x de 2048 px)')
    args = ap.parse_args()

    src = Image.open(args.imagem).convert('L')
    H0 = round(src.height * BASE_W / src.width)
    L = np.asarray(src.resize((BASE_W, H0), Image.LANCZOS)).astype(np.float32)
    mask = L < args.limiar

    # --- linhas: a camiseta é o primeiro bloco vertical; a sombra no chão vem depois de uma faixa vazia
    rows_any = mask.sum(1) > 4
    blocks = runs(rows_any, 30)
    if not blocks:
        sys.exit('Não encontrei a camiseta. Tente outro --limiar.')
    top_row, ground = blocks[0]
    mask[ground:] = False

    # --- colunas: três vistas (frente, lado, costas)
    views = runs(mask[:ground].sum(0) > 20, 40)
    if len(views) != 3:
        sys.exit(f'Esperava 3 vistas lado a lado e encontrei {len(views)}: {views}. Ajuste --limiar ou recorte a imagem.')
    F, Sd, B = [(a - 8, b + 8) for a, b in views]

    rows_f = [y for y in range(H0) if extent(mask, y, *F)]
    hem = rows_f[-1]
    top = rows_f[0]
    K = (args.comprimento / (hem - top)) if args.comprimento else 0.1  # cm por pixel

    # cava: a largura da frente cai de repente quando as mangas acabam
    widths = [(extent(mask, y, *F)[1] - extent(mask, y, *F)[0]) if extent(mask, y, *F) else 0 for y in range(H0)]
    ymax = int(np.argmax(widths[: (top + hem) // 2]))
    arm = next((y for y in range(ymax, hem) if widths[y] < widths[ymax] * 0.8), ymax + 40)
    while arm < hem - 10 and widths[arm + 5] < widths[arm] - 3:  # espera a largura do tronco estabilizar
        arm += 1
    arm += 3

    mid = lambda v, y: sum(extent(mask, y, *v)) / 2
    body_rows = range(arm + 10, hem - 30)
    cxF = float(np.mean([mid(F, y) for y in body_rows]))
    cs = float(np.mean([mid(Sd, y) for y in body_rows]))
    cxB = float(np.mean([mid(B, y) for y in body_rows]))
    ash = float(np.mean([(extent(mask, y, *F)[1] - extent(mask, y, *F)[0]) / 2 for y in range(arm, arm + 45)]))

    # --- perfil a cada 0,5 cm: [altura, meia largura, centro z, meia profundidade]
    step = max(1, round(0.5 / K))
    prof = []
    for r in range(hem, top - 8, -step):
        f, s = extent(mask, r, *F), extent(mask, r, *Sd)
        a = ash if r < arm else ((f[1] - f[0]) / 2 if f else ash)
        if s:
            zc, d = ((s[0] + s[1]) / 2 - cs) * K, (s[1] - s[0]) / 2 * K
        else:
            zc, d = 0.0, 0.3
        prof.append([round((hem - r) * K, 2), round(a * K, 2), round(zc, 2), round(max(d, 0.3), 2)])
    ref = next(p for p in prof if p[0] >= 2.0)  # a barra é irregular: copia a linha de 2 cm
    for p in prof:
        if p[0] < 2.0:
            p[1:] = ref[1:]

    # --- linha do ombro (topo) por x normalizado, de -1 a 1
    tops = []
    for i in range(41):
        col = int(round(cxF + (-1 + 2 * i / 40) * ash))
        rr = np.where(mask[:ground, col])[0]
        tops.append(round((hem - rr.min()) * K, 2))

    # --- sombreamento e recorte em alta resolução
    S = args.escala
    big = Image.open(args.imagem).convert('L').resize((int(BASE_W * S), int(H0 * S)), Image.LANCZOS)
    G = np.asarray(big).astype(np.float32)
    M = G < args.limiar
    M[int(ground * S):] = False
    R0, R1 = max(0, top - 10), min(ground, hem + 11)
    half_body = int(round(max(cxF - F[0], F[1] - cxF))) + 4
    half_side = int(round(max(cs - Sd[0], Sd[1] - cs))) + 4
    crops = [('front', cxF - half_body, cxF + half_body), ('side', cs - half_side, cs + half_side), ('back', cxB - half_body, cxB + half_body)]
    tone = float(np.median(G[int((arm + 30) * S):int((hem - 50) * S), int((cxF - ash * 0.8) * S):int((cxF + ash * 0.8) * S)]))
    shades, masks, cols = [], [], {}
    for name, a0, a1 in crops:
        y0, y1, x0, x1 = int(R0 * S), int(R1 * S), int(round(a0 * S)), int(round(a1 * S))
        g, mk = G[y0:y1, x0:x1], M[y0:y1, x0:x1]
        val = dilate_fill(g, erode(mk, 3), int(60 * S), tone)
        shades.append((np.clip(val / tone * 0.5, 0, 1) * 255).astype(np.uint8))
        soft = Image.fromarray((erode(mk, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.55 * S))
        masks.append(np.asarray(soft))
        centre = {'front': cxF, 'side': cs, 'back': cxB}[name]
        cols[name] = [round(a0, 3), round(a1 - a0, 3), round(centre, 3)]
    Hh = shades[0].shape[0]; Wt = sum(p.shape[1] for p in shades)
    sa = np.zeros((Hh, Wt), np.uint8); ma = np.zeros((Hh, Wt), np.uint8); offs, x = {}, 0
    for (name, _, _), p, q in zip(crops, shades, masks):
        w = p.shape[1]; sa[:, x:x + w] = p; ma[:, x:x + w] = q; offs[name] = [x / Wt, w / Wt]; x += w

    model = dict(K=round(K, 5), ASH=round(ash * K, 2), prof=prof, tops=tops,
                 atlas=dict(offs=offs, rows=[R0, R1], hem=hem, cols=cols))
    os.makedirs(args.saida, exist_ok=True)
    json.dump(model, open(os.path.join(args.saida, 'profile.json'), 'w'), separators=(',', ':'))
    Image.fromarray(sa).filter(ImageFilter.GaussianBlur(0.5)).save(os.path.join(args.saida, 'shade.jpg'), quality=84, optimize=True)
    Image.fromarray(ma).save(os.path.join(args.saida, 'mask.png'), optimize=True)

    print(f'vistas (px em 2048): frente {F}, lado {Sd}, costas {B}')
    print(f'topo {top}, barra {hem}, cava {arm}, chão {ground} | escala {K:.4f} cm/px | comprimento {(hem - top) * K:.1f} cm')
    print(f'meia largura do tronco {ash * K:.1f} cm | tom médio do tecido {tone:.0f}')
    print(f'atlas {Wt}x{Hh} | arquivos em {args.saida}')

    if args.embutir:
        html = open(args.embutir, encoding='utf-8').read()
        b64 = lambda p, mime: f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()
        subs = [
            (r"^const MODEL = .*;$", 'const MODEL = ' + json.dumps(model, separators=(',', ':')) + ';'),
            (r"^const SHADE_URL = '.*';$", "const SHADE_URL = '" + b64(os.path.join(args.saida, 'shade.jpg'), 'image/jpeg') + "';"),
            (r"^const MASK_URL = '.*';$", "const MASK_URL = '" + b64(os.path.join(args.saida, 'mask.png'), 'image/png') + "';"),
        ]
        for pat, rep in subs:
            html, n = re.subn(pat, lambda _m: rep, html, count=1, flags=re.M)
            if n != 1:
                sys.exit(f'Não achei a linha para substituir: {pat}')
        open(args.embutir, 'w', encoding='utf-8').write(html)
        print(f'modelo embutido em {args.embutir}. Ajuste a gola e a manga no objeto G se a nova peça for diferente.')


if __name__ == '__main__':
    main()
