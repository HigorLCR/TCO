# `benchmark.py` — pipeline completo do benchmark

## Papel

Ponto de entrada único do benchmark. Em uma execução: **verifica** que as
versões de cada função são comparáveis e **mede** em um de dois modos:

- **clássico** (padrão): "N iterações → tempo" com o `timeit` completo, e ao
  final **gera** a planilha de tempos;
- **por tempo** (`--duracao T`): "T segundos → execuções (float)", usando o
  ramo por tempo do driver condicional dos próprios scripts.

Substituiu os scripts antigos `verifica_benchmark`, `executa_benchmark`,
`planilha_benchmark` (fases 1, 2 e 3) e `benchmark_por_tempo` (modo
`--duracao`).

## Uso

```
python scripts/benchmark.py [diretorio] [--timeout segundos]
python scripts/benchmark.py --duracao 3             # modo por tempo (3 s/script)
python scripts/benchmark.py --harness <arquivo>     # uso interno (fase 1)
```

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `diretorio` | `recursive_functions/benchmark/` | onde estão os scripts |
| `--timeout` | 120 s | limite por script (subprocesso) |
| `--duracao` | — (clássico) | ativa o modo por tempo, com T segundos por script |

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `recursive_functions/benchmark/*.py` (82 arquivos, 35 funções) |
| Saída (fase 2, clássico) | `arquivos/csv/benchmark_results.csv` |
| Saída (fase 2, `--duracao`) | `arquivos/csv/execucoes_por_tempo.csv` |
| Saída (fase 3, só clássico) | `arquivos/xlsx/tempos_execucao.xlsx` (aba `Tempos_Execucao`) |

## Etapas

### FASE 1 — Verificação (entrada e saída das versões)

Objetivo: confirmar que `<nome>.py`, `output_<nome>.py` e `<nome>_nonrec.py`
usam a **mesma entrada** e produzem a **mesma saída** — senão a comparação de
tempos não é justa.

Para cada arquivo, duas coletas independentes:

1. **Entrada — estática, via AST** (`entrada_de`):
   - `ast.parse` do fonte;
   - `_achar_timeit_lambda` acha a chamada `timeit.timeit(lambda: f(args))` e
     devolve o `Call` dentro do lambda;
   - `_assignments` mapeia as atribuições de nível de módulo e `_substitute`
     troca cada `Name` pelo seu valor (recursivo, profundidade ≤ 4) — assim
     `f(N, 10000)` vira `f([1 for i in range(10000)], 10000)`;
   - inteiros com 16+ dígitos são abreviados: `353410...177320(207dig)`.

   Nada é executado nesta coleta.

2. **Saída — dinâmica, via harness em subprocesso** (`_saida_de` → `_harness`):
   - o script se auto-invoca: `python benchmark.py --harness <arquivo>`;
   - o harness substitui `timeit.timeit` por uma versão que chama o lambda
     **uma única vez**, captura o retorno e devolve `0.0` (as N repetições não
     rodam → rápido);
   - roda o arquivo com `runpy.run_path(..., run_name="__main__")`, stdout do
     script descartado;
   - o retorno vira uma representação **canônica** (`_canonical`) e um hash
     md5 truncado, emitidos na linha `__OUTPUT__\t<hash>\t<preview>`.

   A canonicalização remove tudo que varia entre processos:
   - nós AST → `ast.dump` (estrutural);
   - objetos com `repr` de endereço (`<X object at 0x...>`) → `X({__dict__})`;
   - `set`/`frozenset` → elementos ordenados;
   - listas/tuplas/dicts → recursivo;
   - `sys.set_int_max_str_digits(0)` libera o `repr` de inteiros gigantes
     (ex.: `factorial(5000)`).

3. **Relatório agrupado**: as versões são agrupadas pela função-base
   (`base_de` remove `output_` e `_nonrec`) e impressas na ordem
   `recursivo | output | nonrec`, com veredito:
   - `OK` — entradas iguais e hashes de saída iguais;
   - `DIVERGE` — indica se divergiu a entrada, a saída, ou se ficou
     `incompleto` (alguma versão com `ERRO`/`TIMEOUT`/`n/d`).

   Divergências não interrompem o pipeline — geram um `[AVISO]` antes da fase 2.

### FASE 2 — Benchmark (clássico ou por tempo)

Para cada arquivo (`_medir`), roda em **subprocesso real** (`python
<arquivo>`), sem patch nenhum. O filho recebe `PYTHONIOENCODING=utf-8` (sem
isso, no Windows o `print` sai em cp1252 e o "é" de "tempo médio" quebra o
regex no pai). Os scripts têm um **driver condicional** controlado pela
variável `BENCH_DURACAO`, e é o ambiente do subprocesso que escolhe o ramo:

- **Modo clássico** (padrão): o runner **remove** `BENCH_DURACAO` do ambiente
  → o script executa `timeit(number=qtd_execucoes)` e o stdout é parseado por
  `TIMING_RE` (`tempo médio de N: Xs total | Yms por chamada`).
  CSV: `arquivo, tipo, qtd_execucoes, tempo_total_s, tempo_ms_por_chamada,
  status` → `benchmark_results.csv`.

- **Modo por tempo** (`--duracao T`): o runner **define** `BENCH_DURACAO=T`
  → o próprio script calibra (`autorange`), roda ~T segundos e imprime
  `execucoes em Ts: <float> | K chamadas em Es`, parseado por `EXEC_RE`.
  As execuções são normalizadas pelo script para exatamente T
  (`execucoes = K * (T / E)` — float; frações para chamadas mais longas que
  T). CSV: `arquivo, tipo, duracao_s, execucoes, chamadas_medidas,
  tempo_real_s, status` → `execucoes_por_tempo.csv`.

Status possíveis em ambos: `ok`, `sem_timing` (rodou mas não imprimiu
timing), `erro: <última linha do stderr>`, `timeout (>Ts)`.

### FASE 3 — Planilha (xlsx do zero, só no modo clássico)

`fase_planilha` monta `tempos_execucao.xlsx` com `openpyxl.Workbook()` — sem
template externo. Toda a estrutura vem de constantes editáveis no script:

| Constante | Conteúdo |
|---|---|
| `COLUNA_PARA_BASE` | coluna B..Z → stem da função no CSV (25 funções) |
| `HEADERS` | linha 1: **só o nome** da função (sem parâmetros) |
| `COMPLEXIDADE` | linha 9: `O(n)`, `O(log min(a,b))`, ... (anotação manual) |
| `OBS` | linha 10: observações de pesquisa (anotação manual) |

Layout das linhas (rótulo na coluna A):

```
2  Tempo_Recursao_Media        <- <nome>.py          (ms/chamada)
3  Tempo_Iteracao_Tail_Media   <- output_<nome>.py   ('-' se não há versão tail)
4  Tempo_Iteracao_Media        <- <nome>_nonrec.py
5  Sobrecarga_Tail             =  fórmula rec/tail
6  Sobrecarga                  =  fórmula rec/nonrec
7  Numero_Iteracoes            <- qtd_execucoes
8  Parametros                  <- extração AST (mesma da fase 1)
9  Complexidade de resolução   <- constante
10 Obs                         <- constante
```

Detalhes:
- as fórmulas de sobrecarga usam
  `INDEX($A:$AA, MATCH("<rótulo>", $A:$A, 0), COLUMN())` — localizam a linha
  pelo **texto do rótulo**, então inserir/reordenar linhas não as quebra;
  `IFERROR(..., "-")` faz a divisão por `-` (sem tail) virar `-`;
- visual manual: cabeçalho verde `FF217346` + fonte branca, zebra `FFF2F2F2`
  nas linhas pares, altura 22.5, coluna A larga, `freeze_panes="B2"`;
- **sem Tabela/ListObject**: o banding de tabela mascara preenchimentos
  manuais e o Google Sheets o reaplica na importação.

## Decisões de projeto

- **Subprocesso por script**: um import quebrado, estouro de pilha ou loop
  infinito afeta só aquele arquivo (`status=erro`/`timeout`); patches do
  harness não contaminam o pai nem os demais scripts.
- **Aba com 25 funções**: `COLUNA_PARA_BASE` herda o layout histórico da
  planilha original; as fases 1–2 processam todas as 35 funções — apenas o
  xlsx é restrito ao mapa. Para ampliar, estenda os quatro dicionários e a
  faixa `$A:$AA` das fórmulas.

## Limitações conhecidas

- `manipula_no_expression*.py` não usa `timeit(lambda: ...)` → `n/d` na fase 1
  e `sem_timing` na fase 2 (é uma demo, sem chamada a medir).
- A fase 1 executa cada função 1×; um script pode passar na fase 1 e falhar na
  fase 2 com `number` alto (ex.: estouro de recursos só nas N repetições).
