/* =========================================================
   LÓGICA DO SITE — normalmente não precisa editar.
   Dados da loja e produtos ficam em js/produtos.js
   ========================================================= */

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];

const reais = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
const linkWhats = (msg = "") =>
  `https://wa.me/${LOJA.whatsapp}${msg ? "?text=" + encodeURIComponent(msg) : ""}`;

/* ---------- Desenhos das peças (usados quando não há foto) ---------- */
function desenhoPeca(p) {
  const marca = LOJA.nome.split(" ")[0].slice(0, 6);
  const formas = {
    camiseta: `
      <path d="M72 32 L48 40 L18 66 L34 92 L54 82 L54 178 L146 178 L146 82 L166 92 L182 66 L152 40 L128 32 Q100 56 72 32 Z" fill="${p.cor}"/>
      <path d="M72 32 Q100 56 128 32" fill="none" stroke="rgba(0,0,0,.18)" stroke-width="3"/>
      <text x="100" y="112" text-anchor="middle" font-family="Anton, sans-serif" font-size="20" fill="${p.detalhe}">${marca}</text>`,
    moletom: `
      <path d="M74 36 L48 44 L22 128 L42 134 L58 86 L58 180 L142 180 L142 86 L158 134 L178 128 L152 44 L126 36 Q100 18 74 36 Z" fill="${p.cor}"/>
      <path d="M76 38 Q100 70 124 38" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="3"/>
      <rect x="74" y="138" width="52" height="26" rx="4" fill="rgba(0,0,0,.15)"/>
      <text x="100" y="114" text-anchor="middle" font-family="Anton, sans-serif" font-size="18" fill="${p.detalhe}">${marca}</text>`,
    bone: `
      <path d="M44 124 Q44 62 100 60 Q156 62 156 124 Z" fill="${p.cor}"/>
      <path d="M30 124 Q100 142 178 128 L174 138 Q100 154 26 134 Z" fill="${p.cor}" stroke="rgba(0,0,0,.25)" stroke-width="2"/>
      <circle cx="100" cy="62" r="5" fill="rgba(0,0,0,.25)"/>
      <text x="100" y="108" text-anchor="middle" font-family="Anton, sans-serif" font-size="18" fill="${p.detalhe}">${marca}</text>`,
  };
  return `<svg viewBox="0 0 200 200" role="img" aria-label="${p.nome}" stroke="rgba(0,0,0,.08)" stroke-width="1.5">${formas[p.tipo] || formas.camiseta}</svg>`;
}

const imagemPeca = (p) =>
  p.foto ? `<img src="${p.foto}" alt="${p.nome}" loading="lazy">` : desenhoPeca(p);

/* ---------- Dados da loja nos textos ---------- */
function preencherLoja() {
  document.title = `${LOJA.nome} — Streetwear`;
  $$("[data-nome-loja]").forEach((el) => (el.textContent = LOJA.nome));
  $$("[data-slogan]").forEach((el) => (el.textContent = LOJA.slogan));
  $$("[data-cidade]").forEach((el) => (el.textContent = LOJA.cidade));
  $$("[data-frete]").forEach((el) => (el.textContent = LOJA.frete + "."));
  $$("[data-link-whats]").forEach((el) => {
    el.href = linkWhats(`Olá! Vim pelo site da ${LOJA.nome}.`);
    el.target = "_blank";
    el.rel = "noopener";
  });
  $$("[data-link-insta]").forEach((el) => (el.href = `https://instagram.com/${LOJA.instagram}`));
  $$("[data-link-email]").forEach((el) => (el.href = `mailto:${LOJA.email}`));
  $("#ano").textContent = new Date().getFullYear();

  const frases = [LOJA.frete, "Envio para todo o Brasil", "Pix com desconto", "Troca fácil em 7 dias", "Edição limitada"];
  const bloco = frases.map((f) => `<span>${f}</span><i>✦</i>`).join("");
  $("#faixa").innerHTML = bloco + bloco;

  // Vitrine do topo: 3 primeiros produtos
  $("#hero-vitrine").innerHTML = PRODUTOS.slice(0, 3)
    .map((p, i) => `<div class="vitrine__peca vitrine__peca--${i + 1}">${imagemPeca(p)}</div>`)
    .join("");
}

/* ---------- Catálogo ---------- */
let filtroAtual = "Todos";

function montarFiltros() {
  const categorias = ["Todos", ...new Set(PRODUTOS.map((p) => p.categoria))];
  $("#filtros").innerHTML = categorias
    .map((c) => `<button role="tab" class="filtro${c === filtroAtual ? " ativo" : ""}" aria-selected="${c === filtroAtual}" data-cat="${c}">${c}</button>`)
    .join("");
}

function montarProdutos() {
  const lista = filtroAtual === "Todos" ? PRODUTOS : PRODUTOS.filter((p) => p.categoria === filtroAtual);
  $("#produtos").innerHTML = lista
    .map((p) => {
      const esgotado = p.tag === "Esgotado";
      const unico = p.tamanhos.length === 1;
      return `
      <article class="produto${esgotado ? " produto--esgotado" : ""}" data-id="${p.id}">
        <div class="produto__img">
          ${p.tag ? `<span class="tag tag--${p.tag.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")}">${p.tag}</span>` : ""}
          ${imagemPeca(p)}
        </div>
        <div class="produto__info">
          <h3>${p.nome}</h3>
          <p class="preco">${reais(p.preco)} <small>ou 3x de ${reais(p.preco / 3)}</small></p>
          <div class="tamanhos" role="radiogroup" aria-label="Tamanho">
            ${p.tamanhos.map((t) => `<button class="tam${unico ? " escolhido" : ""}" data-tam="${t}" ${esgotado ? "disabled" : ""} aria-pressed="${unico}">${t}</button>`).join("")}
          </div>
          <button class="btn btn--escuro btn--cheio adicionar" ${esgotado ? "disabled" : ""}>
            ${esgotado ? "Esgotado" : "Adicionar à sacola"}
          </button>
        </div>
      </article>`;
    })
    .join("");
}

$("#filtros").addEventListener("click", (e) => {
  const b = e.target.closest("[data-cat]");
  if (!b) return;
  filtroAtual = b.dataset.cat;
  montarFiltros();
  montarProdutos();
});

$("#produtos").addEventListener("click", (e) => {
  const card = e.target.closest(".produto");
  if (!card) return;

  const tam = e.target.closest(".tam");
  if (tam) {
    $$(".tam", card).forEach((b) => { b.classList.remove("escolhido"); b.setAttribute("aria-pressed", "false"); });
    tam.classList.add("escolhido");
    tam.setAttribute("aria-pressed", "true");
    return;
  }

  if (e.target.closest(".adicionar")) {
    const escolhido = $(".tam.escolhido", card);
    if (!escolhido) {
      card.classList.remove("tremer"); void card.offsetWidth; card.classList.add("tremer");
      avisar("Escolha um tamanho primeiro");
      return;
    }
    adicionar(Number(card.dataset.id), escolhido.dataset.tam);
  }
});

/* ---------- Sacola (fica salva no navegador) ---------- */
let sacola = [];
try { sacola = JSON.parse(localStorage.getItem("sacola")) || []; } catch { sacola = []; }

const salvar = () => { try { localStorage.setItem("sacola", JSON.stringify(sacola)); } catch {} };

function adicionar(id, tam) {
  const item = sacola.find((i) => i.id === id && i.tam === tam);
  if (item) item.qtd++;
  else sacola.push({ id, tam, qtd: 1 });
  salvar();
  montarSacola();
  const p = PRODUTOS.find((x) => x.id === id);
  avisar(`${p.nome} (${tam}) adicionado`);
}

function montarSacola() {
  const itens = sacola
    .map((i) => ({ ...i, p: PRODUTOS.find((x) => x.id === i.id) }))
    .filter((i) => i.p);
  const qtd = itens.reduce((s, i) => s + i.qtd, 0);
  const total = itens.reduce((s, i) => s + i.qtd * i.p.preco, 0);

  $("#contador").textContent = qtd;
  $("#contador").classList.toggle("visivel", qtd > 0);
  $("#total").textContent = reais(total);
  $("#form-pedido").hidden = qtd === 0;

  $("#sacola-itens").innerHTML = qtd === 0
    ? `<p class="sacola__vazia">Sua sacola está vazia.<br><a href="#loja" data-fechar>Ver produtos →</a></p>`
    : itens.map((i, idx) => `
      <div class="item">
        <div class="item__img">${imagemPeca(i.p)}</div>
        <div class="item__info">
          <p class="item__nome">${i.p.nome}</p>
          <p class="item__det">Tam. ${i.tam} · ${reais(i.p.preco)}</p>
          <div class="qtd">
            <button data-acao="menos" data-idx="${idx}" aria-label="Diminuir">−</button>
            <span>${i.qtd}</span>
            <button data-acao="mais" data-idx="${idx}" aria-label="Aumentar">+</button>
          </div>
        </div>
        <button class="item__remover" data-acao="remover" data-idx="${idx}" aria-label="Remover">✕</button>
      </div>`).join("");
}

$("#sacola-itens").addEventListener("click", (e) => {
  if (e.target.closest("[data-fechar]")) return fecharSacola();
  const b = e.target.closest("[data-acao]");
  if (!b) return;
  const i = Number(b.dataset.idx);
  if (b.dataset.acao === "mais") sacola[i].qtd++;
  if (b.dataset.acao === "menos") sacola[i].qtd--;
  if (b.dataset.acao === "remover" || sacola[i].qtd < 1) sacola.splice(i, 1);
  salvar();
  montarSacola();
});

$("#form-pedido").addEventListener("submit", (e) => {
  e.preventDefault();
  const dados = new FormData(e.target);
  const linhas = sacola.map((i) => {
    const p = PRODUTOS.find((x) => x.id === i.id);
    return `• ${i.qtd}x ${p.nome} — Tam. ${i.tam} — ${reais(p.preco * i.qtd)}`;
  });
  const total = sacola.reduce((s, i) => s + i.qtd * PRODUTOS.find((x) => x.id === i.id).preco, 0);
  const msg =
    `Olá! Quero fazer um pedido na ${LOJA.nome}:\n\n${linhas.join("\n")}\n\n` +
    `*Total: ${reais(total)}*\n\nNome: ${dados.get("nome")}` +
    (dados.get("cep") ? `\nCEP: ${dados.get("cep")}` : "");
  window.open(linkWhats(msg), "_blank");
});

$("#form-pedido [name=cep]").addEventListener("input", (e) => {
  const n = e.target.value.replace(/\D/g, "").slice(0, 8);
  e.target.value = n.length > 5 ? `${n.slice(0, 5)}-${n.slice(5)}` : n;
});

function abrirSacola() {
  document.body.classList.add("sacola-aberta");
  $("#sacola").setAttribute("aria-hidden", "false");
}
function fecharSacola() {
  document.body.classList.remove("sacola-aberta");
  $("#sacola").setAttribute("aria-hidden", "true");
}
$("#abrir-sacola").addEventListener("click", abrirSacola);
$("#fechar-sacola").addEventListener("click", fecharSacola);
$("#fundo-escuro").addEventListener("click", fecharSacola);
document.addEventListener("keydown", (e) => e.key === "Escape" && fecharSacola());

/* ---------- Aviso rápido ---------- */
let tempoAviso;
function avisar(texto) {
  const el = $("#aviso");
  el.innerHTML = `${texto} <button type="button">Ver sacola</button>`;
  el.classList.add("visivel");
  $("button", el).onclick = () => { el.classList.remove("visivel"); abrirSacola(); };
  clearTimeout(tempoAviso);
  tempoAviso = setTimeout(() => el.classList.remove("visivel"), 2800);
}

/* ---------- Menu mobile ---------- */
$("#btn-menu").addEventListener("click", () => {
  const aberto = document.body.classList.toggle("menu-aberto");
  $("#btn-menu").setAttribute("aria-expanded", aberto);
});
$$("#menu a").forEach((a) => a.addEventListener("click", () => {
  document.body.classList.remove("menu-aberto");
  $("#btn-menu").setAttribute("aria-expanded", "false");
}));

/* ---------- Cabeçalho muda ao rolar + animações de entrada ---------- */
window.addEventListener("scroll", () => {
  $("#topo").classList.toggle("rolado", window.scrollY > 40);
}, { passive: true });

const observador = new IntersectionObserver((entradas) => {
  entradas.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("visivel"); observador.unobserve(en.target); }
  });
}, { threshold: 0.15 });
$$(".revelar").forEach((el) => observador.observe(el));

/* ---------- Início ---------- */
preencherLoja();
montarFiltros();
montarProdutos();
montarSacola();
