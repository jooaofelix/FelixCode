# 148 Ateliê: guia para o Claude

Editor pessoal de mockup de camiseta. A pessoa monta a arte nos **moldes 2D** e vê o resultado no **modo Foto** (padrão, fotorrealista) ou no **modo 3D** (gira livre). Tudo é um arquivo só: `index.html` (sem build). Responda e escreva textos de interface em **português do Brasil**.

## Identidade visual (marca 148)

O app segue a marca de roupa **148** ("Toda a criação louva", streetwear com raízes no Salmo 148). Mantenha:
- **Cores**: tinta `#0a0a0a` (fundo) e papel `#e7e1cf` (texto/destaque) no tema escuro; invertido no claro. Sem cor de destaque extra: o destaque é o próprio papel sobre tinta.
- **Tipos**: Anton (títulos, caixa-alta), Geist (texto), Geist Mono (medidas). Rótulos pequenos (9–11 px), caixa-alta, `letter-spacing` entre .14em e .3em.
- **Forma**: cantos retos (`border-radius: 0`, exceto as bolinhas de cor), bordas finas de 1 px, botões transparentes com borda.
- **Símbolo**: estrela de quatro pontas (`STAR` no path SVG, `viewBox="-2.2 0 28.4 28.4"`), animada com `spark`.
- **Cores das peças 148** (tecidos): Preto `#141414`, Off-white `#e7e1cf`, Navy `#16213f`, Marrom `#6f4e30`, Cinza `#a3a3a0`.
- Exemplo inicial: camiseta preta, "148" no peito, estrela + "TODA A CRIAÇÃO LOUVA" + "SALMO 148" nas costas (`loadSample`).

## Arquivos

| Arquivo | O que é |
| --- | --- |
| `index.html` | O app inteiro: HTML, CSS e um `<script type="module">`. Carrega `three@0.169.0` (ESM, jsDelivr) e `fabric@5.3.0` (UMD, jsDelivr). |
| `tools/gerar_modelo.py` | Gera o modelo (perfil, sombreamento, recorte) a partir de um mockup em 3 vistas e embute no `index.html`. |
| `tools/testar.js` | Teste visual: capturas das 3 vistas nos 2 modos + exportação + erros do console. |
| `wrangler.jsonc`, `.assetsignore` | Publicação na Cloudflare (Workers Static Assets). `tools/` e os `.md` não sobem. |
| `README.md` | Manual para a pessoa usuária. Mantenha em dia quando mudar funcionalidades. |

## Como a imagem vai do 2D para a camiseta

1. **Editor 2D (Fabric.js)** em escala real: `PX = 10` unidades por cm. Os moldes ficam em `PIECES` (frente, costas, 2 mangas, gola frente/costas), dispostos numa "mesa de corte" de `AW × AH` cm. Cada peça tem `x, y, w, h` (cm) e `poly` (contorno, cm, y para baixo a partir do topo da peça).
2. **Textura**: `renderTexture()` redesenha o canvas do Fabric num canvas de `TEX = 18` px/cm usando `fc.renderCanvas(ctx, objetos)` com o `viewportTransform` trocado. Depois recorta pelos moldes (`maskCanvas`, `destination-in`) e desenha os pespontos. Disparado por `after:render` com limite de 33 ms.
3. **Malhas 3D (Three.js)**: `bodyGeo`, `sleeveGeo` e `ribGeo` constroem grades onde **cada vértice tem UV apontando para o seu ponto no molde** (`uvOf(peça, x, y)`). Por isso a arte cai no mesmo lugar nos dois mundos. As posições vêm de `bodyPos(s, h, lado)`, `sleevePos(s, h, lado)` e `neckCurve`.
4. **Modo 3D**: `MeshPhysicalMaterial` com a textura + `onBeforeCompile` que multiplica pelo sombreamento real da foto (escolhe frente, lado ou costas pela normal do vértice). O lado de dentro escurece com `gl_FrontFacing`.
5. **Modo Foto** (`renderAlbedo` + `composePhoto` + `drawScene`): desenha a camiseta **sem luz** com câmera **ortográfica alinhada à foto** num render target, lê os pixels e combina, pixel a pixel, com o recorte (`MASK_URL`) e o sombreamento (`SHADE_URL`) da foto: multiplica pelas sombras (`L / photo.hi`, curva 1,25) e soma um brilho para tecidos escuros. Onde a malha não cobre a silhueta da foto, usa a cor do tecido.

## Coordenadas (importante para não errar o encaixe)

- Unidade do mundo 3D: **cm**. Barra da camiseta em `y = G.Y0 = -40`. `+z` é a frente; `+x` é o lado esquerdo de quem veste (direita de quem olha).
- Molde da frente/costas: `s` = posição ao longo da largura (0…`W`), `h` = altura a partir da barra (0…`G.H`). `thetaAt(s)` converte comprimento de arco em ângulo da seção elíptica.
- Mockup → mundo: `x = (coluna − centro) × K`, `y = (hem − linha) × K + Y0`, com `K` em cm por pixel na imagem de **2048 px de largura**. Costas: coluna espelhada. Lado: a foto mostra o lado `−x` (direito de quem veste) com o peito para a direita; o lado `+x` usa a mesma foto espelhada.
- Rotação das vistas: frente `0`, lado `π/2`, costas `π`.

## Onde ajustar

| Quer mudar | Onde |
| --- | --- |
| Formato do corpo | `MODEL` (gerado). Regere com `tools/gerar_modelo.py`; não edite à mão. |
| Gola (largura, profundidade, ribana) | `G.NW`, `G.DROP_F`, `G.DROP_B`, `G.RIB`; inclinação da ribana em `ribGeo` (`dir`). |
| Manga | `G.SL` (comprimento), `G.RT`/`G.RC` (raios), `G.ANG` (ângulo), `G.SX/SH0/SZ` (início do eixo), perfil do raio em `sleevePos`. |
| Ombro "quadrado" | Afinamento do tronco em `bodyPos` (`a0 − 1.8 × smoothstep(58…69)`) e curva do ombro `G.K`. |
| Posições prontas (peito, costas…) | `PRESETS` (cm a partir do topo-esquerdo da peça + largura). |
| Força das dobras da foto | Controle "Dobras reais" → `S.ao`. No 3D: `pow(shd, 1.6)` no shader. Na Foto: `photo.hi` (percentil 92) e a curva 1,25 em `composePhoto`. |
| Resolução | `TEX` (textura, px/cm) e `--escala` do gerador (atlas da foto). |
| Padrões da interface | `DEFAULT_SETTINGS`. |

**Ao mudar medidas dos moldes ou padrões salvos**, troque as chaves do `localStorage` (`atelie3d:project3`, `atelie3d:settings4`) para versões novas. Senão, projetos antigos abrem com as artes fora do lugar.

## Trocar ou adicionar um mockup

1. O mockup precisa ter frente, lado e costas **lado a lado**, fundo claro, mesma escala, e o lado mostrando o peito para a direita.
2. `pip install pillow numpy`, depois `python tools/gerar_modelo.py mockup.jpg --embutir index.html` (opções: `--limiar`, `--comprimento`, `--escala`). O script imprime topo, barra, cava e escala detectados; confira se fazem sentido.
3. Ajuste gola e manga em `G` comparando com a foto (veja "Testar").
4. O sombreamento e o recorte vão como data URL dentro do `index.html` (~300 KB). A pessoa forneceu a imagem original; avise sobre a licença se o site for público.

## Testar

```bash
cd tools && npm install && npx playwright install chromium
node testar.js                      # capturas em tools/capturas
```
- Compare `foto-*.png` e `3d-*.png` com o mockup. Para comparar o formato, deixe o tecido cinza e esconda as camadas.
- Em sessões na nuvem do Claude Code a CDN pode estar bloqueada: o script já serve `three` e `fabric` do `node_modules`. O Playwright global da nuvem funciona; não instale outro navegador. As fontes do Google ficam bloqueadas, então os textos usam fonte reserva nas capturas.
- O app abre com a arte de exemplo da 148 (veja Identidade visual), útil para checar o encaixe.

## Armadilhas já resolvidas (não repetir)

- Duas operações `destination-in` seguidas fazem a **interseção** (só sobra a borda). Use uma máscara pronta (`maskCanvas`) de uma vez.
- `fabric.Object.scaleToWidth` considera o zoom da tela. Para medidas reais, use `scaleX/scaleY = (cm × PX) / obj.width`. E use `obj.set('fontSize', …)`, não atribuição direta, para recalcular a largura.
- `fc.renderCanvas` desenha os controles de seleção se `fc.interactive` for true, e cancela o render pendente. Por isso `renderTexture` desliga `interactive` e repõe `requestRenderAll`.
- Regras com `display` sobrescrevem o atributo `hidden`: o CSS tem `[hidden]{display:none!important}`.
- O arraste no 3D tem inércia. Em testes, use os botões de vista, não o mouse.
- Render target com `colorSpace: SRGBColorSpace` já devolve sRGB. Tone mapping não se aplica fora da tela.

## Publicar

- **Link do Claude (Artifact)**: gere uma cópia sem `<!doctype>`, `<html>`, `<head>`, `<body>` e as metas de charset/viewport (o publicador adiciona). Downloads ficam bloqueados lá; por isso a exportação também mostra a imagem num modal.
- **Cloudflare**: `cd felix-atelie && npx wrangler deploy` (login com `npx wrangler login`). Worker `atelie-3d`.
- Commits em português, sem identificar o modelo de IA na mensagem.
