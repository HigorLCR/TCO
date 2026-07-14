# `planilha_cobertura.py` — planilha colorida de nós cobertos

## Papel

Produtor visual da cobertura: transforma o `node_matrix.txt` na planilha
`arquivos/xlsx/nos_ast_cobertos.xlsx` (aba `Nós_AST_Cobertos`), colorindo cada
célula conforme a regra de "quem identificou cada nó primeiro".

Fica no **fim da cadeia** de cobertura: não parseia nenhum arquivo Python —
toda a informação vem da matriz. Se o benchmark mudou, rode
`gera_matriz_cobertura.py` antes.

## Uso

```
python scripts/planilha_cobertura.py
```

Sem parâmetros — caminhos fixos no script.

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `arquivos/txt/node_matrix.txt` |
| Saída | `arquivos/xlsx/nos_ast_cobertos.xlsx` (aba `Nós_AST_Cobertos`) |

## Estrutura da planilha

- **Colunas** (B em diante): os 107 nós AST com cabeçalho `ast.<No>`, em ordem
  ASDL fixa (constante `NODE_HEADERS`) — a mesma ordem da planilha original do
  projeto.
- **Linhas** (2 em diante): as funções do benchmark. Primeiro as 24 da ordem
  histórica (`DISPLAY_ORDER`, com os nomes de exibição originais tipo
  `Factorial()`, `Binary_Search_Tree()`); depois, as funções presentes na
  matriz que ainda não estão na lista, em ordem alfabética, com nome derivado
  `<stem>()`.
- `DISPLAY_TO_STEM` resolve nome de exibição → arquivo da matriz
  (ex.: `is_valid_bst()` → `valid_bst`, `quick_select()` → `quickselect`);
  nomes derivados usam o próprio stem.

## Regra de cor

Por **coluna** (nó), varrendo as linhas de cima para baixo:

| Cor | RGB | Significado |
|---|---|---|
| **VERDE** | `FF70AD47` | primeira função que cobre o nó (quem o "identificou") |
| **CINZA** | `FFA6A6A6` | qualquer função **abaixo** da verde (nó já coberto por outra) |
| **BRANCO** | `FFFFFFFF` | funções acima da verde, ou coluna de nó que ninguém cobre |

Nós sem cobertura alguma são listados no resumo do console
(tipicamente os async/geradores: `AsyncFunctionDef`, `AsyncFor`, `AsyncWith`,
`Await`, `YieldFrom`...).

## Como funciona

1. **Carrega a matriz** (`carregar_cobertura`): decodifica UTF-16, separa por
   `|`, monta `{stem_do_arquivo: set(nós com X)}`.
2. **Monta a aba do zero** (`openpyxl.Workbook()`): cabeçalho, coluna A com as
   funções (ordem histórica + novas), e o mapeamento linha → stem.
3. **Coloração** por coluna: procura a primeira linha cujo stem cobre o nó
   (VERDE), pinta o restante abaixo de CINZA e o que ficou acima de BRANCO.
4. **Estilo manual:** cabeçalho verde escuro `FF217346` + fonte branca +
   `wrap_text`, altura uniforme 22.5 em todas as linhas, coluna A com largura
   30, `freeze_panes="B2"`.

## Por que não usa Tabela/ListObject

A versão original da aba tinha uma Tabela do Excel cujo **row banding
(zebrado) mascarava os preenchimentos manuais** nas linhas que ela cobria — e
o Google Sheets reaplica o banding ao importar, escondendo as cores de novo.
A planilha gerada não define tabela nenhuma: todo o visual é aplicado célula a
célula, o que importa de forma estável no Excel e no Sheets.

## Resumo impresso

Ao final: aba, nº de funções (linhas), nº de nós (colunas), funções
adicionadas além da ordem histórica e a lista de nós sem cobertura.
