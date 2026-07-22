# `benchmark.py` — verificação e medição do benchmark

## Papel

Ponto de entrada do benchmark. Em uma execução: **verifica** que as
versões de cada função são comparáveis e **mede** em um de dois modos:

- **clássico** (padrão): "N iterações → tempo" com `timeit.timeit(chamada,
  number=N)`, `N` vindo do dict central `QTD_EXECUCOES`;
- **por tempo** (`--duracao T`): "T segundos → execuções", iterando a chamada
  em lotes até a soma dos tempos alcançar `T` (piso).

Os arquivos medidos **não contêm lógica de benchmark**: cada um define a
função, as entradas e um `def chamada()` com a chamada medida. Toda a
execução/medição acontece no **worker**
([`benchmark_worker.py`](../benchmark_worker.py)), rodado em subprocesso
isolado — um por arquivo/operação.

A planilha de tempos é gerada à parte por
[`planilha_tempos.py`](planilha_tempos.md), a partir do CSV do modo clássico.

## Uso

```
python scripts/benchmark.py [diretorio] [--timeout segundos]
python scripts/benchmark.py --duracao 3             # modo por tempo (3 s/script)
```

O worker também roda sozinho, útil para depurar um arquivo específico sem o
pipeline em volta (responde o JSON do resultado em stdout):

```
python scripts/benchmark_worker.py verificar <arquivo>
python scripts/benchmark_worker.py classico  <arquivo> <N>
python scripts/benchmark_worker.py tempo     <arquivo> <T>
```

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `diretorio` | `recursive_functions/benchmark/` | diretório com os arquivos medidos; roda o pipeline completo sobre os `.py` dele |
| `--timeout` | 120 s | limite por worker (subprocesso) |
| `--duracao` | — (clássico) | ativa o modo por tempo, com T segundos por script |

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `recursive_functions/benchmark/*.py` (82 arquivos, 35 funções) |
| Saída (fase 2, clássico) | `arquivos/csv/benchmark_results.csv` |
| Saída (fase 2, `--duracao`) | `arquivos/csv/execucoes_por_tempo.csv` |

## O contrato dos arquivos medidos

Cada arquivo termina com:

```python
# --- benchmark ---
def chamada():
    return Sum_Rec(N, 10000)
```

Função, entradas e `sys.setrecursionlimit` (quando necessário) são conteúdo
do arquivo; `timeit`, contagem de iterações, laço por tempo e prints de
medição vivem SÓ aqui no runner. O nº de iterações do modo clássico fica no
dict `QTD_EXECUCOES`, em [`consts/execucoes.py`](../consts/execucoes.py)
(chave = função-base via `base_de`; as versões `output_`/`_nonrec` usam o N da
base). Arquivos sem `chamada()` (as duas demos `manipula_no_expression*`) saem
como `sem_chamada`; função-base fora do dict sai como `sem_qtd`.

## O worker (`benchmark_worker.py`)

Script separado, **nunca importado** pelo `benchmark.py`: a comunicação é só
processo→processo (argv na ida, JSON na volta). É o subprocesso que dá o
isolamento — estouro de pilha e travamento derrubam o filho, não o pipeline.

Sempre: `sys.set_int_max_str_digits(0)` (libera repr/print de inteiros
gigantes — sem isso `factorial.py` quebra no Python ≥3.12), `sys.path` com o
diretório do arquivo, e `runpy.run_path(..., run_name="__main__")` para
executar o módulo. O `setrecursionlimit` do módulo vale na medição
porque tudo roda no mesmo processo. Depois:

- `verificar` — executa `chamada()` **uma vez**, canoniza o retorno
  (`_canonical`) e responde hash md5 + preview;
- `classico N` — `timeit.timeit(chamada, number=N)`;
- `tempo T` — lotes de iterações completas até a soma alcançar `>= T` s
  (T é **piso**; o lote seguinte é estimado pela taxa medida, então o
  excedente é pequeno).

**stdout é do resultado, e só dele.** Logo no início o worker guarda o stdout
real e troca `sys.stdout` por um buffer descartável, então nada do arquivo
medido (prints de demonstração, prints dentro da `chamada()`, em qualquer um
dos três modos) vaza para a resposta. No fim, o JSON é impresso no stdout real
— o pai lê `stdout` inteiro com `json.loads`, sem procurar linha nenhuma.

Um único `except BaseException` no topo cobre as três operações: falha ao
carregar o módulo, exceção dentro da `chamada()`, `RecursionError` e até
`sys.exit()` do arquivo medido viram `{"status": "erro", "msg": ...}`. O que
não vira exceção (estouro de pilha C, `os._exit`) mata o filho antes da
resposta; aí não há JSON e o pai (`executar`) reporta a última linha do
stderr ou `sem saida (rc=N)`.

## Etapas

### FASE 1 — Verificação (entrada e saída das versões)

Objetivo: confirmar que `<nome>.py`, `output_<nome>.py` e `<nome>_nonrec.py`
usam a **mesma entrada** e produzem a **mesma saída** — senão a comparação de
tempos não é justa.

Para cada arquivo, duas coletas independentes:

1. **Entrada — estática, via AST** (`entrada_de`, de
   [`utils`](../utils/entrada_ast.py) — a planilha usa a mesma função):
   - `ast.parse` do fonte;
   - `_achar_chamada` acha o `Call` dentro de `def chamada(): return f(...)`;
   - `_assignments` mapeia as atribuições de nível de módulo e `_substitute`
     troca cada `Name` pelo seu valor (recursivo, profundidade ≤ 4) — assim
     `f(N, 10000)` vira `f([1 for i in range(10000)], 10000)`;
   - inteiros com 16+ dígitos são abreviados: `353410...177320(207dig)`.

   Nada é executado nesta coleta.

2. **Saída — dinâmica, via worker** (`coleta_saida` → modo `verificar`):
   executa `chamada()` 1× em subprocesso; o retorno vira uma representação
   **canônica** (`_canonical`) e um hash md5 truncado, empacotados num
   `Saida(hash, preview, comparavel)` — `comparavel=False` marca os casos em
   que não houve saída (erro, timeout, sem `chamada()`), então esses hashes
   nunca são usados numa comparação.

   A canonicalização remove tudo que varia entre processos:
   - nós AST → `ast.dump` (estrutural);
   - objetos com `repr` de endereço (`<X object at 0x...>`) → `X({__dict__})`;
   - `set`/`frozenset` → elementos ordenados;
   - listas/tuplas/dicts → recursivo.

3. **Relatório agrupado**: as versões são agrupadas pela função-base
   (`base_de` remove `output_` e `_nonrec`) e impressas na ordem
   `recursivo | output | nonrec`. `compara_versao` dá o veredito e `printa_grupo`
   imprime o bloco:
   - `OK` — entradas iguais e hashes de saída iguais;
   - `DIVERGE` — indica se divergiu a entrada, a saída, ou se ficou
     `incompleto` (alguma versão sem saída comparável).

   Divergências não interrompem o pipeline — geram um `[AVISO]` antes da fase 2.

### FASE 2 — Benchmark (clássico ou por tempo)

Para cada arquivo, `medir` dispara um worker:

- **Modo clássico** (padrão): worker no modo `classico <arq> N`, com
  `N = QTD_EXECUCOES[base]`. Colunas `COLUNAS_CSV` (`arquivo, tipo,
  qtd_execucoes, tempo_total_s, tempo_ms_por_chamada, status`) →
  `benchmark_results.csv`.
- **Modo por tempo** (`--duracao T`): worker no modo `tempo <arq> T`.
  Colunas `COLUNAS_CSV_TEMPO` (`arquivo, tipo, piso_s, iteracoes,
  tempo_total_s, tempo_ms_por_chamada, status`) → `execucoes_por_tempo.csv`.

Os nomes das colunas vivem em [`consts/formato_csv.py`](../consts/formato_csv.py):
o `benchmark.py` grava por eles e o `planilha_tempos.py` lê por eles, então
renomear uma coluna é uma edição só.

Status possíveis: `ok`, `sem_chamada` (arquivo sem `def chamada()`),
`sem_qtd` (base fora de `QTD_EXECUCOES`, só no clássico),
`erro: <detalhe>`, `timeout: >Ts`.

## Referência: função a função

Mapa do fluxo (do ponto de entrada às folhas):

```
python benchmark.py
        │
      main() ── parseia flags; alvo = diretório com os arquivos medidos
        │
        ├─ 1) fase_verificacao(files)          "a comparação é justa?"
        │       └─ por arquivo: entrada_de() [AST, no proprio processo]
        │                     + coleta_saida() ────┐
        │                                          │
        └─ 2) fase_benchmark(files, duracao)       │  "mede de verdade"
                └─ por arquivo: medir() ───────────┤
                                                   │
                                          executar(modo, arq, timeout, param)
                                                   │  subprocess + timeout
                                                   ▼
                                    python benchmark_worker.py <modo> <arq> [param]
                                       └─ operar(): runpy do modulo → chamada()
                                          → JSON em stdout → volta ao pai
```

A planilha é gerada depois, por `planilha_tempos.py` (lê o CSV do modo
clássico).

### Nomenclatura

| Função | O que faz |
|---|---|
| `classifica(name)` | Tipo do arquivo pela convenção de nomes: `output_*` → `output`, `*_nonrec.py` → `nonrec`, senão `recursivo`. |
| `base_de(name)` | Reduz qualquer versão à função-base (tira `.py`, `output_`, `_nonrec`); agrupa as versões na fase 1 e indexa `QTD_EXECUCOES`. |

Os dois aplicam a convenção de nome definida em
[`consts/nomes.py`](../consts/nomes.py) (`EXT_PY`, `PREFIXO_OUTPUT`,
`SUFIXO_NONREC`) — a mesma que o `cobertura.py` usa para excluir as versões
derivadas e que o `utils/versoes.py` usa no caminho inverso, montando os três
nomes a partir da base.

### Extração da ENTRADA — `utils/entrada_ast.py` (estática, via AST)

Vive em `utils` porque o `planilha_tempos.py` usa a mesma extração na linha
`Parametros` — assim os dois scripts a compartilham sem um importar o outro.
Cadeia usada por `entrada_de()` para descobrir os argumentos reais da chamada:

| Função | O que faz |
|---|---|
| `_assignments(tree)` | Dicionário `{variável: nó AST do valor}` das atribuições de nível de módulo — a "tabela de símbolos". |
| `_substitute(node, amap, depth)` | `NodeTransformer` que troca cada `Name` dos argumentos pelo seu valor, recursivamente (profundidade ≤ 4): `f(N, 10000)` → `f([1 for i in range(10000)], 10000)`. |
| `_achar_chamada(tree)` | Localiza o `Call` dentro de `def chamada(): return f(...)` no nível de módulo. |
| `_abreviar_numeros(texto)` | Inteiros com 16+ dígitos viram `353410...177320(207dig)`. |
| `entrada_de(path)` | Orquestra os quatro acima e devolve `"p1, p2, ..."`; `"-"` se o arquivo não tem `chamada()`. Usada na fase 1 e também pelo `planilha_tempos.py` (linha `Parametros`). |

### Worker — `benchmark_worker.py` (subprocesso das 3 operações)

| Função | O que faz |
|---|---|
| `_canonical(v, depth)` | Serializa o retorno da função de forma canônica e sem endereço de memória (nós AST → `ast.dump`; objetos → `Tipo({__dict__})`; sets ordenados; coleções recursivas), para que resultados iguais de processos diferentes batam byte a byte. |
| `_carregar_chamada(path)` | `runpy.run_path(..., run_name="__main__")` do módulo e devolve a `chamada` dos globais resultantes (`None` se não houver). |
| `_verificar(chamada)` | Roda 1×, canoniza e resume em hash md5 (10 chars) + preview de ≤70 chars. |
| `_classico(chamada, n)` | `timeit.timeit(chamada, number=n)`; `n <= 0` → `sem_qtd`. |
| `_por_tempo(chamada, piso)` | Lotes de iterações até a soma dos tempos alcançar o piso; devolve iterações exatas. |
| `operar(modo, path, param)` | Carrega e despacha para a operação; devolve o dict do resultado. |
| bloco `__main__` | Troca `sys.stdout` por um buffer descartável (o IO do arquivo medido vai para o lixo), chama `operar` sob um `except BaseException` e imprime o JSON no stdout real. |

### Chamada do worker (lado pai, em `benchmark.py`)

| Função | O que faz |
|---|---|
| `executar(modo, path, timeout, param)` | `subprocess.run` do `benchmark_worker.py` com timeout, e `json.loads(proc.stdout)`; timeout → `{"status": "timeout"}`; stdout não-JSON (worker morto antes de responder) → erro com última linha do stderr ou `sem saida (rc=N)`. |

### FASE 1 — verificação

| Função | O que faz |
|---|---|
| `Saida` | `NamedTuple(hash, preview, comparavel)`. `comparavel=False` ⇒ não houve saída para comparar; `hash`/`preview` valem só como texto do relatório. |
| `Versao` | `NamedTuple(arquivo, tipo, base, entrada, saida)`: uma versão de uma função-base, já com entrada (AST) e saída (worker). |
| `coleta_saida(path, timeout)` | Wrapper de `executar("verificar", ...)` → `Saida`; mapeia `sem_chamada` → `n/d`, `timeout` → `TIMEOUT`, falha → `ERRO`, todos com `comparavel=False`. |
| `compara_versao(versoes)` | Só decide: devolve `(categoria, veredito)` com categoria `sozinha`/`igual`/`divergente`. Não imprime nada. |
| `printa_grupo(base, versoes, veredito)` | Só imprime o bloco de uma função-base; repete a entrada por versão apenas quando ela diverge. |
| `fase_verificacao(files, timeout)` | Monta as `Versao`, agrupa por `base_de`, ordena `recursivo | output | nonrec` e delega julgamento/impressão. Devolve o nº de divergências (o `main` só avisa, não interrompe). |

### FASE 2 — benchmark

| Função | O que faz |
|---|---|
| `medir(path, timeout, duracao)` | Dispara `executar("classico", ..., N)` ou `("tempo", ..., T)` e traduz o dict do worker na linha do CSV (com `status`). |
| `fase_benchmark(files, timeout, duracao)` | Laço de `medir`, print por script e escrita do CSV do modo (`benchmark_results.csv` ou `execucoes_por_tempo.csv`). |

### Orquestração

| Função | O que faz |
|---|---|
| `main()` | Parseia `--timeout` / `--duracao` / diretório e roda as fases 1→2 no modo escolhido. |
| bloco `__main__` | Configura stdout UTF-8 e chama `main()`. |

**Resumo do design:** os arquivos expõem uma API mínima (`def chamada()` +
atribuições de módulo) e o runner a explora por duas vias — **lendo** o fonte
(AST → entradas exibidas) e **executando** `chamada()` num worker isolado
(1× para verificar, N× ou T segundos para medir) — sempre em subprocesso,
para que erro, timeout ou estouro de pilha de um script não contamine os
demais. Pai e filho são o mesmo arquivo e conversam por uma linha JSON.

## Decisões de projeto

- **Subprocesso por script**: um import quebrado, estouro de pilha ou loop
  infinito afeta só aquele arquivo (`status=erro`/`timeout`).
- **Medição fora dos arquivos**: o laço por tempo e o `timeit` existem em UM
  lugar (o worker), não replicados em 80 arquivos; os fontes medidos são
  também o corpus de cobertura AST, e sem o driver a cobertura reflete só as
  funções.
- **Protocolo JSON em vez de regex**: pai e filho são scripts separados e a
  fronteira é explícita (argv na ida, JSON na volta) — sem parsing de prints
  humanos, sem variáveis de ambiente, sem problemas de encoding (ASCII puro).
  Como o worker só escreve o JSON em stdout, o pai lê `stdout` inteiro de uma
  vez; e como ele não é importado pelo pai, não há risco de o relatório e a
  medição compartilharem estado.
- **`set_int_max_str_digits(0)` no worker**: sem isso, `repr`/`print` de
  inteiros gigantes (ex.: `factorial(5000)`) quebra no Python ≥3.12.
- **Planilha em script à parte**: a geração do xlsx não mede nada e só
  depende do CSV, então vive em `planilha_tempos.py` — o benchmark mede, a
  planilha apresenta.

## Limitações conhecidas

- `manipula_no_expression*.py` não tem `chamada()` → `n/d` na fase 1 e
  `sem_chamada` na fase 2 (é uma demo, sem chamada a medir).
- A fase 1 executa cada função 1×; um script pode passar na fase 1 e falhar
  na fase 2 com `number` alto (ex.: estouro de recursos só nas N repetições).
- Arquivo novo no diretório exige registrar a função-base em `QTD_EXECUCOES`
  (senão o modo clássico devolve `sem_qtd`; o modo por tempo funciona sem
  registro).
