# Ateliê 3D

Editor pessoal de mockup de camiseta: você monta a estampa nos **moldes 2D** (frente, costas, mangas e gola) e vê o resultado em tempo real numa **camiseta 3D** tradicional (gola careca), com dobras reais, textura de malha e luz de estúdio.

## Como usar

Abra `index.html` direto no navegador (Chrome, Edge ou Firefox). Não precisa instalar nada; só precisa de internet para carregar as bibliotecas (Three.js e Fabric.js) e as fontes.

Se preferir rodar como servidor local:

```bash
cd felix-atelie
python -m http.server 8000
# abra http://localhost:8000
```

## O que dá para fazer

- **Imagem**: envie PNG/JPG (de preferência PNG com fundo transparente) e posicione nos moldes.
- **Texto**: 9 fontes (Anton, Bebas Neue, Archivo Black, Playfair, Permanent Marker, Pacifico…). Dê dois cliques no texto para editar direto no molde.
- **Faixa / Círculo**: formas para punhos, faixas e detalhes.
- **Balde**: pinta uma peça só (por exemplo, gola e punhos de outra cor, no estilo *ringer*) ou muda a cor de um item.
- **Posicionar em**: atalhos para peito, logo no peito, costas, nuca, barras e mangas, já no tamanho certo em cm.
- **Tecido**: cor da camiseta inteira.
- **Modo Foto** (padrão): o resultado usa a própria foto do mockup (silhueta, dobras e luz originais) com a sua cor e estampa aplicadas por cima, como num mockup de PSD. É o modo para exportar a imagem final.
- **Modo 3D**: a camiseta gira livremente; serve para conferir a estampa por todos os ângulos.
- **Vistas**: botões Frente, Lado e Costas, nos dois modos.
- **Acabamento**: dobras reais (da foto), rugas extras, textura da malha e brilho do algodão.
- **Cenário e luz**: cor do fundo, sombra projetada (persiana, folhas, janela), força e direção da luz, giro 360°.
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
