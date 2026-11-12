/* =========================================================
   CONFIGURAÇÃO DA LOJA
   Edite só este arquivo para trocar dados e produtos.
   ========================================================= */

const LOJA = {
  nome: "NOVA ORDEM",
  slogan: "Streetwear feito pra durar.",
  // Número com DDI + DDD, só números. Ex.: 5511987654321
  whatsapp: "5511999999999",
  instagram: "novaordem",
  email: "contato@novaordem.com.br",
  cidade: "São Paulo — SP",
  // Texto exibido na faixa e no FAQ
  frete: "Frete grátis acima de R$ 299",
};

/* ---------------------------------------------------------
   PRODUTOS
   tipo:      "camiseta" | "moletom" | "bone"  (define o desenho)
   categoria: usada nos filtros
   cor:       cor da peça (hex)
   detalhe:   cor da estampa (hex)
   foto:      opcional — caminho da foto real, ex.: "images/camiseta-preta.jpg"
              (se tiver foto, ela substitui o desenho)
   tag:       opcional — "Novo", "Últimas", "Esgotado"
   --------------------------------------------------------- */

const PRODUTOS = [
  { id: 1,  nome: "Camiseta Essencial Preta",  categoria: "Camisetas",  tipo: "camiseta", preco: 89.9,  cor: "#151515", detalhe: "#f2efe8", tamanhos: ["P", "M", "G", "GG"], tag: "Novo" },
  { id: 2,  nome: "Camiseta Essencial Off",    categoria: "Camisetas",  tipo: "camiseta", preco: 89.9,  cor: "#ebe6da", detalhe: "#151515", tamanhos: ["P", "M", "G", "GG"] },
  { id: 3,  nome: "Camiseta Oversized Marrom", categoria: "Camisetas",  tipo: "camiseta", preco: 109.9, cor: "#5a3d2b", detalhe: "#ebe6da", tamanhos: ["M", "G", "GG"], tag: "Últimas" },
  { id: 4,  nome: "Camiseta Oversized Marinho",categoria: "Camisetas",  tipo: "camiseta", preco: 109.9, cor: "#1d2840", detalhe: "#ff5b2e", tamanhos: ["P", "M", "G", "GG", "XG"] },
  { id: 5,  nome: "Moletom Canguru Preto",     categoria: "Moletons",   tipo: "moletom",  preco: 219.9, cor: "#1a1a1a", detalhe: "#ff5b2e", tamanhos: ["P", "M", "G", "GG"], tag: "Novo" },
  { id: 6,  nome: "Moletom Canguru Cinza",     categoria: "Moletons",   tipo: "moletom",  preco: 219.9, cor: "#8d8a84", detalhe: "#151515", tamanhos: ["M", "G", "GG"] },
  { id: 7,  nome: "Boné Aba Curva Preto",      categoria: "Acessórios", tipo: "bone",     preco: 79.9,  cor: "#161616", detalhe: "#ebe6da", tamanhos: ["Único"] },
  { id: 8,  nome: "Boné Aba Curva Laranja",    categoria: "Acessórios", tipo: "bone",     preco: 79.9,  cor: "#ff5b2e", detalhe: "#151515", tamanhos: ["Único"], tag: "Esgotado" },
];
