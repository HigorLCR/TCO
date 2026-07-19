# `cobertura.py` — relatório de cobertura e `node_matrix.txt`

## Papel

Análise de cobertura de nós AST dos fontes do benchmark, com **um único
parse** (`ast.parse` + `ast.walk` por arquivo) alimentando duas saídas:

- **relatório no terminal** (sempre): quanto dos **110 nós-alvo** os fontes
  cobrem — global, por categoria da gramática ASDL, faltantes e por arquivo;
- **matriz** (`--matriz`): grava `arquivos/txt/node_matrix.txt`, a fonte
  oficial de "quem cobre o quê", consumida pelo `planilha_cobertura.py`.

Substituiu os scripts antigos `printa_cobertura` (só o relatório) e
`gera_matriz_cobertura` (só a matriz), que faziam a mesma análise estática em
duplicidade — e divergiam na cobertura demonstrativa, que o relatório antigo
não aplicava (os 4 nós de runtime constavam como faltantes no terminal e como
cobertos na matriz). Agora ela vale para as duas saídas.

## Uso

```
python scripts/cobertura.py [diretorio] [--matriz]
```

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `diretorio` | `recursive_functions/benchmark` | onde estão os fontes |
| `--matriz` | — | além do relatório, grava o `node_matrix.txt` |

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `.py` do diretório, **excluindo** `*_nonrec.py` e `output_*` (35 arquivos) |
| Saída (sempre) | relatório no stdout |
| Saída (`--matriz`) | `arquivos/txt/node_matrix.txt` |

## Como funciona

1. **Coleta estática** (`coletar`): para cada arquivo-fonte, `ast.parse`
   (parse padrão, sem `type_comments`) + `ast.walk` → conjunto dos tipos de
   nó presentes. Arquivos com `SyntaxError` são logados e contam como
   conjunto vazio.

2. **Cobertura demonstrativa (`manipula_no_*`)**, aplicada na coleta — vale
   para relatório E matriz. Quatro nós **nunca** aparecem num parse estático
   padrão:
   - `Interactive`, `Expression`, `FunctionType` — raízes *mod* de outros
     modos de parse (`mode="single"/"eval"/"func_type"`);
   - `TypeIgnore` — só existe com `type_comments=True`, em
     `Module.type_ignores`.

   Cada arquivo `manipula_no_<no>.py` cobre seu nó-alvo **em runtime**
   (constrói/manipula o nó de fato). O alvo é deduzido pelo sufixo do nome,
   casando com o catálogo `dir(ast)` em minúsculas
   (`manipula_no_typeignore.py` → `TypeIgnore`), e injetado no conjunto do
   arquivo. Sufixo que não casa com nó nenhum gera `[AVISO]`.

3. **Relatório** (`relatorio`): mede contra `TARGET_NODES` — os 110 nós
   recomendados, organizados por categoria da gramática ASDL:

   | Categoria | Exemplos |
   |---|---|
   | `mod` | Module, Interactive, Expression, FunctionType |
   | `stmt` | FunctionDef, Return, For, While, If, Try, TryStar, Match, ... |
   | `expr` | BinOp, Lambda, ListComp, Await, Yield, Call, Constant, ... |
   | `expr_context` | Load, Store, Del |
   | `operator` | Add, Sub, Mult, MatMult, Div, Mod, Pow, ... |
   | `unaryop` / `boolop` / `cmpop` | Not, USub / And, Or / Eq, Lt, In, ... |
   | `pattern` | MatchValue, MatchSequence, MatchAs, ... |
   | `type_param` | TypeVar, ParamSpec, TypeVarTuple |
   | `auxiliar` | arguments, arg, keyword, alias, withitem, ExceptHandler, ... |

   Seções: cobertura global (`X/110, %`), tabela da demonstrativa aplicada,
   barra por categoria com faltantes, lista consolidada dos não cobertos e
   cobertura por arquivo.

4. **Matriz** (`gravar_matriz`): linhas = **união dos nós presentes**
   (ordenada — não se limita aos 110 alvo), colunas = arquivos, célula `X`
   se o nó aparece naquele arquivo, `.` caso contrário. Formato preservado
   do arquivo original do projeto:
   - codificação **UTF-16-LE com BOM** (`﻿`);
   - separador `|` (sem espaços);
   - quebras de linha **CRLF**;
   - primeira célula do cabeçalho: `NO`.

   ```
   NO|binary_search.py|conta.py|...
   Add|X|X|...
   Assign|X|X|...
   ...
   ```

## Relação com os outros scripts

```
fontes .py ──→ cobertura.py ──┬─→ relatório no terminal
                (--matriz)    └─→ node_matrix.txt ──→ planilha_cobertura.py ──→ xlsx
```

O `planilha_cobertura.py` **não parseia Python** — herda toda a informação da
matriz. Se o benchmark mudou, rode `cobertura.py --matriz` antes de regenerar
a planilha.

## Observações

- Os dois universos de nós são intencionais: o **relatório** responde "quanto
  da meta de 110 nós já cobrimos?" (interseção com `TARGET_NODES`); a
  **matriz** registra tudo que existe nos fontes (união), mesmo nós fora da
  meta — quem filtra é o consumidor.
- O relatório e a matriz agora concordam sobre a demonstrativa; a diferença
  de percentual que existia entre `printa_cobertura` e a matriz desapareceu.
