# `benchmark.py` — verificação e medição do benchmark

## Papel

Ponto de entrada do benchmark. Em uma execução: **verifica** que as
versões de cada função são comparáveis e **mede** em um de dois modos:

- **clássico** (padrão): "N iterações → tempo" com o `timeit` completo;
- **por tempo** (`--duracao T`): "T segundos → execuções (float)", usando o
  ramo por tempo do driver condicional dos próprios scripts.

A planilha de tempos é gerada à parte por
[`planilha_tempos.py`](planilha_tempos.md), a partir do CSV do modo clássico.

Substituiu os scripts antigos `verifica_benchmark` e `executa_benchmark`
(fases 1 e 2) e `benchmark_por_tempo` (modo `--duracao`).

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
  → o próprio script roda um **laço de lotes de iterações completas até a
  soma dos tempos alcançar >= T** (T é **piso** — a execução nunca para
  antes; o lote seguinte é estimado pela taxa medida até então, então o
  excedente após o piso é pequeno). Imprime `benchmark por tempo (piso Ts):
  K iteracoes | Es total | Xms por chamada`, parseado por `EXEC_RE`.
  CSV: `arquivo, tipo, piso_s, iteracoes, tempo_total_s,
  tempo_ms_por_chamada, status` → `execucoes_por_tempo.csv`.

Status possíveis em ambos: `ok`, `sem_timing` (rodou mas não imprimiu
timing), `erro: <última linha do stderr>`, `timeout (>Ts)`.

## Referência: função a função

Mapa do fluxo (do ponto de entrada às folhas):

```
python benchmark.py
        │
   bloco __main__ ─── se "--harness <arq>": este processo vira o FILHO da
        │             fase 1 (_harness) e termina
        │
      main() ── parseia flags
        │
        ├─ 1) fase_verificacao(files)          "a comparação é justa?"
        │       └─ por arquivo: entrada_de() [AST] + _saida_de() [subproc --harness]
        │
        └─ 2) fase_benchmark(files, duracao)   "mede de verdade"
                └─ por arquivo: _medir() [subprocesso real] → CSV
```

A planilha é gerada depois, por `planilha_tempos.py` (lê o CSV do modo
clássico).

### Nomenclatura

| Função | O que faz |
|---|---|
| `classify(name)` | Tipo do arquivo pela convenção de nomes: `output_*` → `output`, `*_nonrec.py` → `nonrec`, senão `recursivo`. |
| `base_de(name)` | Reduz qualquer versão à função-base (tira `.py`, `output_`, `_nonrec`); é o que permite agrupar as versões na fase 1. |

### Extração da ENTRADA (estática, via AST — nada é executado)

Cadeia usada por `entrada_de()` para descobrir os argumentos reais da chamada:

| Função | O que faz |
|---|---|
| `_assignments(tree)` | Dicionário `{variável: nó AST do valor}` das atribuições de nível de módulo — a "tabela de símbolos". |
| `_substitute(node, amap, depth)` | `NodeTransformer` que troca cada `Name` dos argumentos pelo seu valor, recursivamente (profundidade ≤ 4): `f(N, 10000)` → `f([1 for i in range(10000)], 10000)`. |
| `_achar_timeit_lambda(tree)` | Localiza a chamada `timeit.timeit(lambda: f(args))` na AST e devolve o `Call` de dentro do lambda. |
| `_abreviar_numeros(texto)` | Inteiros com 16+ dígitos viram `353410...177320(207dig)`. |
| `entrada_de(path)` | Orquestra os quatro acima e devolve `"p1, p2, ..."`; `"-"` se o arquivo não tem timeit. Usada na fase 1 e importada pelo `planilha_tempos.py` (linha `Parametros`). |

### Captura da SAÍDA (dinâmica — processo-filho `--harness`)

| Função | O que faz |
|---|---|
| `_canonical(v, depth)` | Serializa o retorno da função de forma canônica e sem endereço de memória (nós AST → `ast.dump`; objetos → `Tipo({__dict__})`; sets ordenados; coleções recursivas), para que resultados iguais de processos diferentes batam byte a byte. |
| `_harness(path_str)` | Corpo do filho da fase 1: (1) substitui `timeit.timeit` por versão que chama o lambda **uma vez** e captura o retorno (devolvendo 0.0); (2) roda o arquivo com `runpy.run_path`, stdout descartado; (3) canoniza o retorno, tira hash md5 e imprime a linha-protocolo `__OUTPUT__\t<hash>\t<preview>`. Também libera o `repr` de inteiros gigantes. |

### FASE 1 — verificação

| Função | O que faz |
|---|---|
| `_saida_de(path, timeout)` | Lado pai do harness: dispara `python benchmark.py --harness <arq>` (removendo `BENCH_DURACAO` do ambiente, garantindo o ramo clássico interceptável) e extrai `(hash, preview)` da linha `__OUTPUT__`; `ERRO`/`TIMEOUT` em falha. |
| `fase_verificacao(files, timeout)` | Coleta entrada+saída de cada arquivo, agrupa por `base_de`, ordena `recursivo | output | nonrec` e emite o veredito por função (`OK`/`DIVERGE`/`incompleto`). Devolve o nº de divergências (o `main` só avisa, não interrompe). |

### FASE 2 — benchmark

| Função | O que faz |
|---|---|
| `_medir(path, timeout, duracao)` | Roda **um** script em subprocesso real; o `duracao` escolhe o ramo do driver condicional via ambiente: `None` remove `BENCH_DURACAO` (clássico, parse `TIMING_RE`) e `T` injeta `BENCH_DURACAO=T` (piso, parse `EXEC_RE`). Sempre com `PYTHONIOENCODING=utf-8`. Devolve a linha do CSV com `status`. |
| `fase_benchmark(files, timeout, duracao)` | Laço de `_medir` sobre todos os arquivos, print por script e escrita do CSV do modo (`benchmark_results.csv` ou `execucoes_por_tempo.csv`). |

### Orquestração

| Função | O que faz |
|---|---|
| `main()` | Parseia `--timeout` / `--duracao` / diretório e roda as fases 1→2 no modo escolhido (clássico ou por tempo). |
| bloco `__main__` | Configura stdout UTF-8 e despacha o papel do processo: `--harness` → filho da fase 1 (`_harness`); senão → pai (`main`). Um arquivo só faz os dois lados do protocolo. |

**Resumo do design:** o script explora a "API" implícita dos benchmarks (o
`timeit.timeit(lambda: f(args))` + o print padronizado) por três vias —
**lendo** o fonte (AST → entradas), **interceptando** o timeit em subprocesso
(→ saídas, fase 1) e **executando** de verdade com o ambiente escolhendo o
ramo do driver (→ tempos ou iterações, fase 2) — sempre em subprocesso
isolado, para que erro ou patch de um script não contamine os demais.

## Decisões de projeto

- **Subprocesso por script**: um import quebrado, estouro de pilha ou loop
  infinito afeta só aquele arquivo (`status=erro`/`timeout`); patches do
  harness não contaminam o pai nem os demais scripts.
- **Planilha em script à parte**: a geração do xlsx não mede nada e só
  depende do CSV, então vive em `planilha_tempos.py` — o benchmark mede, a
  planilha apresenta.

## Limitações conhecidas

- `manipula_no_expression*.py` não usa `timeit(lambda: ...)` → `n/d` na fase 1
  e `sem_timing` na fase 2 (é uma demo, sem chamada a medir).
- A fase 1 executa cada função 1×; um script pode passar na fase 1 e falhar na
  fase 2 com `number` alto (ex.: estouro de recursos só nas N repetições).
