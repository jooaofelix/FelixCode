# 148 Ateliê

Estúdio de mockup da **148** (toda a criação louva). Editor de camiseta: você monta a estampa nos **moldes 2D** (frente, costas, mangas e gola) e vê o resultado em tempo real numa **camiseta 3D** tradicional (gola careca), com dobras reais, textura de malha e luz de estúdio.

## Como usar

Abra `index.html` direto no navegador (Chrome, Edge ou Firefox). Não precisa instalar nada; só precisa de internet para carregar as bibliotecas (Three.js e Fabric.js) e as fontes.

Se preferir rodar como servidor local:

```bash
cd felix-atelie
python -m http.server 8000
# abra http://localhost:8000
```

## Modelos de camiseta

- **Oversized 148 (CLO 3D)** — padrão. Modelo 3D de verdade, feito no CLO 3D (o mesmo programa do vídeo de referência), com os **moldes reais** da peça no editor: frente (59,8 × 60,8 cm), costas (59,8 × 63,2 cm), mangas (47,4 × 24,1 cm) e gola em ribana dobrada. A arte cai exatamente onde ficaria na peça costurada. Vitrine sempre em 3D.
- **Tradicional** — o modelo anterior, com o **modo Foto** (mockup fotográfico).

Troque em **Projeto → Modelo da camiseta**. Cada modelo guarda o seu próprio projeto no navegador.

O modelo oversized fica em `modelo-oversized.js` (moldes + malha 3D otimizada, ~1,7 MB). Para gerar de novo ou trazer outra peça do CLO, use `tools/preparar_modelo_clo.py` (veja o CLAUDE.md). Fonte do modelo: [Male oversized tshirt (CGTrader)](https://www.cgtrader.com/free-3d-models/character/clothing/male-oversized-tshirt) — confira a licença antes de uso comercial.

## O que dá para fazer

- **Imagem**: envie PNG/JPG (de preferência PNG com fundo transparente) e posicione nos moldes.
- **Texto**: 9 fontes (Anton, Bebas Neue, Archivo Black, Playfair, Permanent Marker, Pacifico…). Dê dois cliques no texto para editar direto no molde.
- **Faixa / Círculo**: formas para punhos, faixas e detalhes.
- **Medidas em cm**: cada imagem mostra no molde a largura e a altura em cm (cotas que acompanham rotação e tamanho em tempo real); textos e formas mostram quando selecionados. O botão **Medidas** liga/desliga. As camadas também mostram o tamanho de cada item, e o **molde baixado** sai com as medidas de todas as artes.
- **Guias de alinhamento (como no Canva)**: ao arrastar uma arte, uma linha rosa aparece quando ela passa pelo centro da peça ou se alinha com o centro/bordas de outra arte, e a arte gruda na linha. Um aviso mostra a posição (ex.: "Frente: Centralizado · 15,5 cm abaixo da gola"). Segure **Alt** para arrastar sem grudar.
- **Balde**: pinta uma peça só (por exemplo, gola e punhos de outra cor, no estilo *ringer*) ou muda a cor de um item.
- **Posicionar em**: atalhos para peito, logo no peito, costas, nuca, barras e mangas, já no tamanho certo em cm.
- **Tecido**: cor da camiseta inteira — paleta da 148 ou **qualquer cor**: clique no quadrado colorido (seletor do sistema), digite o código hex (ex.: `#1A3D2B` ou `1a3d2b`) ou use o **conta-gotas** (Chrome/Edge) para pegar uma cor da tela. As cores usadas ficam em **Suas cores** (e também no Balde).
- **Modo Foto** (padrão): o resultado usa a própria foto do mockup (silhueta, dobras e luz originais) com a sua cor e estampa aplicadas por cima, como num mockup de PSD. É o modo para exportar a imagem final.
- **Modo 3D**: a camiseta gira livremente; serve para conferir a estampa por todos os ângulos.
- **Vistas**: botões Frente, Lado e Costas, nos dois modos.
- **Movimento do tecido**: ao girar a camiseta no 3D, a barra e as mangas ficam um pouco para trás, a barra abre levemente e, ao soltar, o tecido balança até assentar. Ajuste a intensidade em Acabamento → Movimento do tecido (0 desliga). As imagens exportadas saem sempre com o tecido parado.
- **Acabamento**: dobras reais (da foto), rugas extras, textura da malha e brilho do algodão.
- **Cenário e luz**: cor do fundo, sombra projetada (persiana, folhas, janela), força e direção da luz, giro 360°.
- **Prompt p/ IA**: gera um texto pronto para colar no ChatGPT, Gemini ou Claude (tipo de foto, frente/costas, formato, português ou inglês) com a peça e cada estampa descritas em cm e posição, mais as imagens de referência da frente e das costas para anexar.
- **Exportar imagem**: PNG em alta resolução (no modo Foto, da vista escolhida; no modo 3D, do ângulo atual).
- **Baixar molde (PNG)**: a arte plana de cada peça na escala de 18 px por cm, para mandar para a estamparia.
- **Projeto**: salva sozinho no navegador; também dá para salvar e abrir arquivos `.json`.

## Atalhos

| Tecla | Ação |
| --- | --- |
| V | Mover |
| T / I / R / O | Texto / Imagem / Faixa / Círculo |
| B | Balde |
| Ctrl+Z / Ctrl+Shift+Z | Desfazer / refazer |
| Ctrl+D | Duplicar |
| Delete | Excluir |
| Setas (Shift = 1 cm) | Mover 1 mm |

## Como funciona por dentro

- O editor 2D é um canvas do **Fabric.js** em escala real (10 unidades = 1 cm).
- A cada mudança, o canvas é redesenhado numa textura (18 px/cm), recortada no formato de cada molde.
- A camiseta 3D é gerada por código com **Three.js**: cada peça é uma malha cujas coordenadas UV apontam exatamente para o seu molde na textura. Por isso o que você desenha no molde aparece no mesmo lugar da camiseta.
- O formato do corpo vem de um mockup em três vistas (frente, lado e costas): a vista de frente dá a largura em cada altura, a vista de lado dá a profundidade, e o modelo é montado fatia por fatia a partir dessas silhuetas.
- As dobras e a luz das três fotos viram um mapa de sombreamento (em tons de cinza, embutido no `index.html`). Na hora de desenhar, cada ponto da camiseta usa a foto que está mais de frente para ele, então as dobras reais aparecem por cima da sua estampa.
- No **modo Foto**, a camiseta 3D é desenhada sem luz por uma câmera ortográfica alinhada com a foto. Isso diz onde cada pedaço da estampa cai na foto. Depois a foto entra por cima: o recorte dá a silhueta e o tom de cinza dá as sombras e o brilho (multiplicação com um pouco de brilho, como num PSD).
- A malha do tecido é um mapa normal gerado na hora; o controle "Rugas" adiciona um pouco de ruído 3D aos vértices.

As medidas da peça ficam nos objetos `MODEL` e `G` no começo do script, caso você queira ajustar a gola ou a manga.

> O mapa de sombreamento foi derivado da imagem de mockup que você forneceu. Se for deixar o repositório público ou usar comercialmente, confira a licença dessa imagem.

## Publicar na Cloudflare

O site é um arquivo só (`index.html`), então dá para publicar de três jeitos:

**1. Arrastar e soltar (mais rápido)**
No painel da Cloudflare: **Workers & Pages → Create → Pages → Upload assets**. Dê o nome `atelie-3d` e arraste a pasta `felix-atelie` (ou só o `index.html`). O site fica em `atelie-3d.pages.dev`.

**2. Ligado ao GitHub (atualiza sozinho a cada push)**
**Workers & Pages → Create → Import a repository** → escolha `felixcode` → em *Root directory* coloque `felix-atelie`. O `wrangler.jsonc` desta pasta já configura tudo (deploy: `npx wrangler deploy`).

**3. Pelo terminal**
```bash
cd felix-atelie
npx wrangler login
npx wrangler deploy
```

## Ferramentas (pasta `tools`)

- `gerar_modelo.py`: transforma um mockup em três vistas (frente, lado, costas) no modelo da camiseta e embute no `index.html`. Assim dá para trocar de peça ou melhorar o encaixe.
- `testar.js`: abre o app num navegador automático e tira fotos das vistas para conferir.
- O `CLAUDE.md` explica como tudo funciona por dentro e onde ajustar cada coisa.
