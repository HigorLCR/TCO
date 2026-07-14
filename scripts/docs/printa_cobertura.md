# `printa_cobertura.py` — relatório de cobertura no terminal

## Papel

Diagnóstico rápido: mede quanto dos **107 nós AST alvo** os fontes de um
diretório cobrem e imprime um relatório legível no console. Não gera arquivo —
para produzir dados consumíveis por outros scripts, use
`gera_matriz_cobertura.py`.

## Uso

```
python scripts/printa_cobertura.py [diretorio]
```

| Parâmetro | Padrão |
|---|---|
| `diretorio` | `recursive_functions/benchmark` |

## Entradas e saídas

| | |
|---|---|
| Entrada | `.py` do diretório, **excluindo** `*_nonrec.py`, `output_*` e o próprio script |
| Saída | relatório no stdout (nenhum arquivo) |

## Como funciona

1. **Meta fixa:** `TARGET_NODES` define os 107 nós recomendados, organizados
   por categoria da gramática ASDL do Python:

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

2. **Coleta por arquivo:** `ast.parse` + `ast.walk` → conjunto dos tipos de nó
   presentes, intersectado com a meta (`ALL_TARGET`).

3. **Relatório:**
   - cobertura global (`X/107 nós, Y%`);
   - barra por categoria (`####....`) com os nós faltantes de cada uma;
   - lista consolidada dos nós não cobertos, por categoria;
   - cobertura por arquivo (`N/107, %`).

## Limitação importante

Usa **apenas parse estático** — não conhece a *cobertura demonstrativa* dos
arquivos `manipula_no_*` (nós `Interactive`, `Expression`, `FunctionType` e
`TypeIgnore` só existem em runtime ou em modos especiais de parse, nunca num
`ast.parse` padrão). Aqui eles aparecem como **faltantes**, enquanto o
`gera_matriz_cobertura.py` os marca como cobertos.

Consequência prática: o percentual deste relatório é sempre ≤ o da matriz.
Use este script para responder "o que ainda falta cobrir com código real?" e a
matriz para a cobertura oficial do projeto.
