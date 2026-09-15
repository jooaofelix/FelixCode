# Site da Desata

Site institucional da **Desata** — *Tecnologia que descomplica*.

Página única, em HTML, CSS e JavaScript puros: sem build, sem dependências,
sem framework. Basta abrir o `index.html` ou subir a pasta em qualquer
hospedagem estática.

---

## ⚠️ Antes de publicar: dados que faltam

Todos os dados de contato ficam em **`assets/js/config.js`**. Enquanto os
campos abaixo estiverem vazios, a seção de contato mostra um aviso amarelo de
configuração (esse aviso some sozinho quando os dados forem preenchidos).

| Campo        | O que é                                            | Situação   |
| ------------ | -------------------------------------------------- | ---------- |
| `whatsapp`   | Número com código do país e DDD, só dígitos        | **Falta**  |
| `email`      | E-mail de contato                                   | **Falta**  |
| `instagram`  | Usuário do Instagram, sem `@` (opcional)           | Opcional   |
| `local`      | Cidade/região exibida no rodapé (opcional)         | Opcional   |

Além disso, ao definir o domínio:

1. Trocar as URLs relativas das tags `og:image` e afins, no `<head>` do
   `index.html`, pelo endereço completo do site (redes sociais exigem URL absoluta).
2. Conferir o texto de `og:description` e o título da página.

Nada de telefone, e-mail, endereço, preço, prazo ou cliente foi inventado no
site — o que não foi confirmado simplesmente não está lá.

---

## Como editar

```
desata/
├── index.html              # todo o conteúdo da página, em HTML semântico
├── assets/
│   ├── css/
│   │   ├── estilo.css      # design do site, com as cores no topo do arquivo
│   │   └── fontes.css      # declarações da fonte Figtree
│   ├── fonts/              # fonte servida pelo próprio site (sem Google Fonts)
│   ├── img/                # logos, ícones e imagem de compartilhamento
│   └── js/
│       ├── config.js       # ← dados de contato (o que muda com frequência)
│       └── main.js         # menu, animações e links de contato
└── marca/                  # arquivos originais da identidade visual
```

**Textos, serviços e dúvidas** ficam no `index.html`, cada seção com um
comentário indicando o que é. **Cores** ficam no começo do `estilo.css`, no
bloco `:root`. **Contato** fica no `config.js`.

### Cores da marca

| Cor            | Código    | Uso                                         |
| -------------- | --------- | ------------------------------------------- |
| Off-white      | `#F4F0E8` | fundo principal                             |
| Grafite        | `#242424` | texto e seções de contraste                 |
| Laranja queimado | `#E66A35` | destaques, botões e os laços gráficos      |

> Sobre contraste: laranja com texto **grafite** tem contraste 4,8:1 (aprovado
> na norma de acessibilidade WCAG AA). Laranja com texto **branco** só passa em
> tamanho grande, por isso o branco sobre laranja aparece apenas em títulos.
> Para texto pequeno em laranja sobre o off-white, o site usa o tom mais escuro
> `#A34517`.

---

## Publicação

A pasta é estática, então funciona em qualquer hospedagem: GitHub Pages,
Netlify, Vercel, Cloudflare Pages ou hospedagem comum via FTP. Basta enviar o
conteúdo de `desata/` para a raiz do site.

Para testar localmente:

```bash
cd desata
python3 -m http.server 8000
# abre http://localhost:8000
```

---

## Se um dia entrar um formulário

O site hoje conversa pelo WhatsApp, sem formulário. Se um formulário for
adicionado, ele **precisa de um destino real** de envio (um serviço como
Formspree/Basin, ou um endpoint próprio) e precisa mostrar mensagem de sucesso
e de erro de verdade. Nada de simular envio concluído.

---

## Acessibilidade e desempenho

- HTML semântico, com link "pular para o conteúdo" e navegação por teclado.
- Menu mobile com `aria-expanded`, fechamento por `Esc` e por clique fora.
- Dúvidas em `<details>`/`<summary>`: funcionam mesmo sem JavaScript.
- Animações discretas, todas desligadas quando o sistema pede
  `prefers-reduced-motion`.
- Sem JavaScript, a página continua legível e navegável por inteiro.
- Fonte servida pelo próprio site (~30 KB) e imagens otimizadas: nenhuma
  requisição a terceiros.

---

## Portfólio

Ainda não há seção de portfólio: ela entra quando houver projetos reais para
mostrar. Demonstrações, se forem incluídas, devem ser identificadas
claramente como demonstrações.
