# Loja de roupas — site de uma página com pedido pelo WhatsApp

Site pronto para marca de roupas: catálogo com filtros, sacola de compras e pedido
finalizado pelo WhatsApp (sem pagamento online, sem servidor, hospedagem grátis).

## Abrir no computador
Dê dois cliques em `index.html`.

## Personalizar para um cliente (o que muda de um cliente para outro)

1. **Dados da loja** → `js/produtos.js`, objeto `LOJA`
   (nome, slogan, WhatsApp com DDI+DDD, Instagram, e-mail, cidade, frete).
2. **Produtos** → `js/produtos.js`, lista `PRODUTOS`
   (nome, categoria, preço, tamanhos, tag "Novo"/"Últimas"/"Esgotado").
   - Coloque as fotos em `images/` e preencha `foto: "images/arquivo.jpg"`.
     Sem foto, o site desenha a peça automaticamente na cor escolhida.
   - Fotos em formato retrato 4:5 (ex.: 800×1000) ficam melhores.
3. **Cores e fontes** → começo de `css/style.css` (bloco `:root`).
4. **Textos** (título, "Sobre", "Como comprar", "Dúvidas") → `index.html`.

## Publicar grátis
- **Netlify**: arraste a pasta `projeto_03` em https://app.netlify.com/drop
- Depois aponte o domínio do cliente (`.com.br`, ~R$ 40/ano, no nome do cliente).

## O que está incluído (escopo do pacote de R$ 400)
- Página única: topo animado, faixa de avisos, loja, sobre, como comprar, dúvidas, rodapé
- Catálogo com filtro por categoria e seleção de tamanho
- Sacola salva no navegador, total automático e pedido enviado formatado pelo WhatsApp
- Botão flutuante de WhatsApp, menu mobile, layout responsivo
- Até 12 produtos cadastrados e 2 rodadas de ajustes

**Fora do escopo (cobrar à parte):** pagamento online, cálculo de frete automático,
controle de estoque, área de login, páginas extras, produção de fotos/textos.
