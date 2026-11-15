# Ateliê 3D

Editor pessoal de mockup de camiseta: você monta a estampa nos **moldes 2D** (frente, costas, mangas e gola) e vê o resultado em tempo real numa **camiseta 3D** oversized, com rugas, textura de malha e luz de estúdio.

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
- **Acabamento**: rugas, sombra nas dobras, textura da malha e brilho do algodão.
- **Cenário e luz**: cor do fundo, sombra projetada (persiana, folhas, janela), força e direção da luz, giro 360°.
- **Exportar imagem**: PNG em alta resolução da vitrine 3D.
- **Baixar molde (PNG)**: a arte plana de cada peça na escala de 14 px por cm, para mandar para a estamparia.
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
- A cada mudança, o canvas é redesenhado numa textura (14 px/cm), recortada no formato de cada molde.
- A camiseta 3D é gerada por código com **Three.js**: cada peça é uma malha cujas coordenadas UV apontam exatamente para o seu molde na textura. Por isso o que você desenha no molde aparece no mesmo lugar da camiseta.
- Rugas e sombras de dobra vêm de ruído 3D aplicado aos vértices; a malha do tecido é um mapa normal gerado na hora.

As medidas da peça ficam no objeto `G` no começo do script, caso você queira ajustar o comprimento, a largura ou a manga.
