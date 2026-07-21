# Scripts do projeto TCO

Visão geral dos scripts e do fluxo de dados. A documentação detalhada de cada
script (papel, uso, etapas, funcionamento interno) está em [`docs/`](docs/).

## Índice

| Script | Papel | Doc |
|---|---|---|
| `benchmark.py` | Verifica versões e mede no modo clássico (iterações → tempo) ou por tempo (`--duracao T` → execuções); grava o CSV do modo | [docs/benchmark.md](docs/benchmark.md) |
| `benchmark_worker.py` | Worker do `benchmark.py`: roda **um** arquivo em subprocesso e responde o resultado em JSON | [docs/benchmark.md](docs/benchmark.md#o-worker-benchmark_workerpy) |
| `planilha_tempos.py` | Gera o xlsx de tempos a partir do `benchmark_results.csv` | [docs/planilha_tempos.md](docs/planilha_tempos.md) |
| `cobertura.py` | Relatório de cobertura de nós AST no terminal; `--matriz` grava a matriz nós × arquivos (`node_matrix.txt`) | [docs/cobertura.md](docs/cobertura.md) |
| `planilha_cobertura.py` | Gera o xlsx colorido de nós cobertos a partir da matriz | [docs/planilha_cobertura.md](docs/planilha_cobertura.md) |
| `consts/` | Constantes compartilhadas: caminhos, convenção de nomes, colunas dos CSVs, `QTD_EXECUCOES` | — |
| `utils/` | Funções compartilhadas: extração de entrada por AST e nomes das versões | — |

Os scripts são **independentes entre si**: nenhum importa o outro. O que dois
deles precisam dividir mora em `consts/` (constantes) ou `utils/` (funções), e
quem gera se liga a quem apresenta pelo arquivo intermediário (o CSV, a matriz
de nós):

```
scripts/
├── consts/
│   ├── caminhos.py      onde cada arquivo do projeto fica
│   ├── nomes.py         convenção output_ / _nonrec / .py (3 scripts usam)
│   ├── formato_csv.py   colunas dos CSVs (benchmark grava, planilha lê)
│   └── execucoes.py     QTD_EXECUCOES: iterações do modo clássico
├── utils/
│   ├── entrada_ast.py   entrada_de(): argumentos da chamada(), via AST
│   └── versoes.py       versoes_de('sum') -> os 3 nomes de arquivo
├── benchmark.py         ─┐
├── benchmark_worker.py   │ importam consts/utils,
├── planilha_tempos.py    │ nunca uns aos outros
├── cobertura.py          │
└── planilha_cobertura.py─┘
```

## Convenções do diretório de benchmark

Os scripts assumem a estrutura de `recursive_functions/benchmark/`, onde cada
função existe em até 3 versões:

- `<nome>.py` — versão **recursiva** original;
- `<nome>_nonrec.py` — versão **iterativa** gerada pelo `recpython3`;
- `output_<nome>.py` — versão **tail-recursion → iteração** (só quem já foi convertida).

Os arquivos **não contêm lógica de benchmark** (sem `timeit`, sem prints de
medição). Cada um define a função, as entradas e, no fim, a chamada medida:

```python
# --- benchmark ---
def chamada():
    return Sum_Rec(N, 10000)
```

Essa `chamada()` é a "API" que o `benchmark.py` explora: a verificação a
executa 1× (hash da saída), o modo clássico mede
`timeit.timeit(chamada, number=N)` — com `N` vindo do dict central
`QTD_EXECUCOES` (em `consts/execucoes.py`) — e o modo `--duracao T` a itera em
lotes até somar `T` segundos. Toda a medição acontece no
`benchmark_worker.py`, em subprocesso isolado.

**Atenção:** `python recursive_functions/benchmark/sum.py` direto não mede
mais nada (só define a função). A execução avulsa é:

```powershell
python scripts/benchmark.py recursive_functions/benchmark/sum.py   # 1 arquivo, sem CSV
python scripts/benchmark.py                                        # pipeline completo
python scripts/benchmark.py --duracao 3                            # por tempo
```

Os dois arquivos `manipula_no_expression*.py` são demos sem `chamada()` e
saem como `sem_chamada` nos relatórios/CSV.

## Fluxo de dados

```
                        DOMÍNIO BENCHMARK
recursive_functions/benchmark/*.py
    │
    └── benchmark.py  ──(subprocesso por arquivo)──→ benchmark_worker.py
        ├── (clássico) ──────────────→ arquivos/csv/benchmark_results.csv
        │   verifica + timeit               │
        │                        planilha_tempos.py
        │                                   │
        │                                   └─→ arquivos/xlsx/tempos_execucao.xlsx
        │
        └── (--duracao T) ───────────→ arquivos/csv/execucoes_por_tempo.csv
            verifica + execuções em T segundos

                        DOMÍNIO COBERTURA
recursive_functions/benchmark/*.py   (sem _nonrec / output_)
    │
    └── cobertura.py ──┬─────────────→ (relatório no terminal)
                       │
                       └─ (--matriz) → arquivos/txt/node_matrix.txt
                                            │
                          planilha_cobertura.py
                                            │
                                            └─→ arquivos/xlsx/nos_ast_cobertos.xlsx
```

## Técnicas compartilhadas

- **Worker com protocolo JSON:** o `benchmark_worker.py`
  (`verificar|classico|tempo <arquivo> [param]`) executa o módulo do arquivo,
  opera sobre `chamada()` e responde um JSON em stdout — sem regex sobre
  prints, sem variáveis de ambiente. O stdout do arquivo medido é desviado no
  início, então a resposta nunca se mistura com ele.
- **Extração de entrada por AST:** os parâmetros exibidos (planilha e
  verificação) vêm de `ast.parse` do fonte (a chamada dentro de
  `def chamada()`), com variáveis de módulo resolvidas e inteiros gigantes
  abreviados (`3534...(207dig)`). Fica em `utils/entrada_ast.py`, usada pelo
  `benchmark.py` e pelo `planilha_tempos.py`.
- **Caminhos em um lugar só:** `consts/caminhos.py` define cada arquivo do
  projeto uma vez. Onde um script grava e outro lê (`benchmark_results.csv`,
  `node_matrix.txt`), a constante de lá é o contrato — antes o mesmo caminho
  era redefinido em cada script, com nomes diferentes.
- **Canonicalização de saída:** para comparar resultados entre versões, o
  retorno é serializado sem endereço de memória e reduzido a hash md5.
- **Subprocesso por script:** um worker por arquivo isola erros, timeouts e
  estouros de pilha.
- **Fórmulas por rótulo no xlsx:** as sobrecargas usam
  `INDEX($A:$AA, MATCH("<rótulo>", $A:$A, 0), COLUMN())` — localizam a linha
  pelo texto da coluna A, então inserir/reordenar linhas não quebra nada.
