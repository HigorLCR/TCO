# Scripts do projeto TCO

Visão geral dos scripts e do fluxo de dados. A documentação detalhada de cada
script (papel, uso, etapas, funcionamento interno) está em [`docs/`](docs/).

## Índice

| Script | Papel | Doc |
|---|---|---|
| `benchmark.py` | Verifica versões e mede no modo clássico (iterações → tempo) ou por tempo (`--duracao T` → execuções); grava o CSV do modo | [docs/benchmark.md](docs/benchmark.md) |
| `planilha_tempos.py` | Gera o xlsx de tempos a partir do `benchmark_results.csv` | [docs/planilha_tempos.md](docs/planilha_tempos.md) |
| `printa_cobertura.py` | Relatório de cobertura de nós AST no terminal | [docs/printa_cobertura.md](docs/printa_cobertura.md) |
| `gera_matriz_cobertura.py` | Gera a matriz nós × arquivos (`node_matrix.txt`) | [docs/gera_matriz_cobertura.md](docs/gera_matriz_cobertura.md) |
| `planilha_cobertura.py` | Gera o xlsx colorido de nós cobertos a partir da matriz | [docs/planilha_cobertura.md](docs/planilha_cobertura.md) |

## Convenções do diretório de benchmark

Os scripts assumem a estrutura de `recursive_functions/benchmark/`, onde cada
função existe em até 3 versões:

- `<nome>.py` — versão **recursiva** original;
- `<nome>_nonrec.py` — versão **iterativa** gerada pelo `recpython3`;
- `output_<nome>.py` — versão **tail-recursion → iteração** (só quem já foi convertida).

Cada script de benchmark termina com um **driver condicional**, controlado
pela variável de ambiente `BENCH_DURACAO`:

```python
if _os.environ.get("BENCH_DURACAO") is None:
    # modo CLÁSSICO: qtd_execucoes iterações -> tempo
    tempo = timeit.timeit(lambda: f(args), number=qtd_execucoes)
    print(f"tempo médio de {qtd_execucoes}: ...s total | ...ms por chamada")
else:
    # modo POR TEMPO: T é PISO — itera até a soma dos tempos alcançar >= T s
    _bench = timeit.Timer(lambda: f(args))    # a MESMA chamada
    ...  # laço de lotes até _e >= T (iterações completas)
    print(f"benchmark por tempo (piso {T}s): K iteracoes | Es total | Xms por chamada")
```

```powershell
python recursive_functions/benchmark/sum.py                          # clássico
$env:BENCH_DURACAO='3'; python recursive_functions/benchmark/sum.py  # por tempo
```

Os dois ramos são a "API" que o `benchmark.py` explora: a verificação e o modo
clássico rodam os scripts **sem** `BENCH_DURACAO` (interceptam/parseiam o ramo
clássico); o modo `--duracao T` roda cada script **com** `BENCH_DURACAO=T` e
parseia o `print` de execuções do ramo por tempo.

## Fluxo de dados

```
                        DOMÍNIO BENCHMARK
recursive_functions/benchmark/*.py
    │
    └── benchmark.py
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
    ├── printa_cobertura.py ─────────→ (relatório no terminal)
    │
    └── gera_matriz_cobertura.py ────→ arquivos/txt/node_matrix.txt
                                            │
                          planilha_cobertura.py
                                            │
                                            └─→ arquivos/xlsx/nos_ast_cobertos.xlsx
```

## Técnicas compartilhadas

- **Interceptação do `timeit`:** os runners substituem `timeit.timeit` em
  runtime (via `runpy.run_path`) para capturar o `lambda: f(args)` de cada
  script sem alterar nenhum arquivo do diretório.
- **Extração de entrada por AST:** os parâmetros exibidos (planilha e
  verificação) vêm de `ast.parse` do fonte, com variáveis de módulo resolvidas
  e inteiros gigantes abreviados (`3534...(207dig)`).
- **Canonicalização de saída:** para comparar resultados entre versões, o
  retorno é serializado sem endereço de memória e reduzido a hash md5.
- **Subprocesso por script:** isolamento de erros e patches; no Windows, os
  filhos rodam com `PYTHONIOENCODING=utf-8` para o `print` acentuado casar com
  o regex no pai.
- **Fórmulas por rótulo no xlsx:** as sobrecargas usam
  `INDEX($A:$AA, MATCH("<rótulo>", $A:$A, 0), COLUMN())` — localizam a linha
  pelo texto da coluna A, então inserir/reordenar linhas não quebra nada.
