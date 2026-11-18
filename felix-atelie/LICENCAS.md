# Licenças e dependências (Editor de Artes e Ateliê 148)

Tudo que o editor usa é gratuito e de código aberto: sem assinatura, créditos, chave de API ou cartão. Nenhuma função principal depende de serviço pago.

| Dependência | Para que serve | Licença | Precisa de internet? |
| --- | --- | --- | --- |
| [Fabric.js 5.3.0](https://github.com/fabricjs/fabric.js) | Prancheta: imagens, textos, camadas, seleção, exportação | MIT (uso comercial livre) | Não: cópia local em `vendor/fabric.min.js` (a CDN jsDelivr é só o primeiro caminho) |
| [OpenType.js 1.3.4](https://github.com/opentypejs/opentype.js) | Ler arquivos de fonte e converter letras em contornos vetoriais | MIT (uso comercial livre) | Não: cópia local em `vendor/opentype.min.js` |
| [Google Fonts](https://fonts.google.com) | Mostrar as fontes do catálogo na tela | Cada fonte tem a sua: quase todas SIL OFL 1.1 ou Apache 2.0, que permitem uso comercial em estampas | Sim (gratuito, sem chave) |
| [Fontsource](https://fontsource.org) (API e arquivos via jsDelivr) | Busca no catálogo (nome, categoria, estilo, licença) e arquivos TTF/WOFF para converter em curvas | Projeto MIT; as fontes mantêm a licença original (OFL/Apache etc.) | Sim (gratuito, sem chave). Sem internet: lista curada do editor + fontes importadas |
| Suas fontes OTF/TTF | Usar e vetorizar fontes que você tem | A licença de quem distribuiu a fonte; confira antes de vender | Não (ficam salvas dentro do projeto) |
| Three.js 0.169.0 (só no Ateliê 3D) | Camiseta 3D | MIT | Sim (CDN) |

## Avisos exigidos

- `vendor/LICENSE-fabric.txt` e `vendor/LICENSE-opentype.txt` são os avisos MIT das bibliotecas, mantidos junto das cópias locais.
- Fontes SIL OFL 1.1: podem ser usadas em estampas e produtos vendidos. O que a licença proíbe é **vender o arquivo da fonte** sozinho. Ao embutir uma fonte num arquivo (por exemplo, projeto `.json` com fonte importada), mantenha o nome e a licença dela.
- Ao converter um texto em curvas, a estampa deixa de conter o arquivo da fonte (é só desenho), o que é permitido pela OFL e pela Apache.

## O que não é usado

Nenhuma API paga de IA, remoção de fundo, identificação de fonte, vetorização ou geração de imagem. Essas funções têm alternativas manuais no editor (veja o painel “O que funciona aqui”).
