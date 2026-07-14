# `benchmark_por_tempo.py` — pipeline por tempo (duração fixa)

## Papel

Inverso do `benchmark.py`: em vez de fixar o **número de iterações** e medir o
tempo, fixa uma **duração** (ex.: 3 s) e mede **quantas execuções (float)**
cabem nesse tempo, para cada script do benchmark.

Não altera nenhum arquivo do diretório medido: o callable executado é
exatamente o mesmo `lambda: f(args)` que o script já passa ao `timeit`
(capturado por interceptação em runtime).

## Uso

```
python scripts/benchmark_por_tempo.py [diretorio] [--duracao seg] [--timeout seg]
python scripts/benchmark_por_tempo.py --saida <arquivo>        # uso interno (fase 1)
python scripts/benchmark_por_tempo.py --tempo <arquivo> <dur>  # uso interno (fase 2)
```

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `diretorio` | `recursive_functions/benchmark/` | onde estão os scripts |
| `--duracao` | 3.0 s | tempo-alvo de medição por script (aceita float) |
| `--timeout` | 300 s | limite do subprocesso por script |

O timeout padrão é generoso porque funções lentas de 1 chamada (ex.:
`fib_memo_nonrec`, ~15 s/chamada) precisam de pelo menos 2 chamadas
(calibração + medição).

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `recursive_functions/benchmark/*.py` |
| Saída | `arquivos/csv/execucoes_por_tempo.csv` |

Colunas do CSV: `arquivo, tipo, duracao_s, execucoes, chamadas_medidas,
tempo_real_s, status`.

## Etapas

### FASE 1 — Verificação

Idêntica à do `benchmark.py` (ver `docs/benchmark.md`): entrada extraída por
AST, saída capturada por harness (`--saida`) com timeit neutralizado e
canonicalização, relatório agrupado por função com veredito `OK`/`DIVERGE`.

### FASE 2 — Medição por tempo

Para cada arquivo, auto-invocação em subprocesso no modo
`--tempo <arquivo> <duracao>` (`_harness_tempo`):

1. Intercepta o `timeit.timeit` do script para **capturar o callable**
   (`lambda: f(args)`) — o script "acha" que mediu (recebe `0.0`), mas quem
   mede é o harness.
2. `timeit.Timer(stmt)` cria um timer real com esse callable
   (o `Timer` não é afetado pelo patch — só a função `timeit.timeit` foi
   substituída).
3. **Calibração:** `autorange()` acha um lote cujo tempo `t_cal ≥ 0.2 s`
   (dobrando o número de chamadas até chegar lá).
4. **Medição:**
   - se `t_cal ≥ duracao`, a própria calibração já cobriu o tempo-alvo:
     usa `K = n_cal`, `E = t_cal`;
   - senão, estima `alvo = round(duracao / (t_cal / n_cal))` chamadas e roda
     o lote inteiro: `E = timer.timeit(number=alvo)`, `K = alvo`.
5. **Normalização:** `execucoes = K * (duracao / E)`.
6. Emite a linha `__EXEC__\t<status>\t<execucoes>\t<K>\t<E>\t<msg>`, parseada
   pelo pai (`_medir_tempo`).

### Por que `execucoes` difere de `K` (a contagem crua)

Os lotes são inteiros — não dá para parar no meio de uma chamada — então o
tempo real `E` nunca cai exatamente na duração-alvo. A normalização projeta a
contagem para **exatamente** T segundos, tornando as linhas comparáveis entre
si:

```
binary_search:  K=1.364.315 em E=2.982s  →  exec = 1.364.315 × (3/2.982) ≈ 1.372.682   (E < T: extrapola)
factorial:      K=237       em E=3.180s  →  exec = 237 × (3/3.180)       ≈ 223.57      (E > T: reduz)
```

Por isso `execucoes` é um **float** — e funções com chamada mais longa que a
duração produzem frações (ex.: ~0.2 execuções em 3 s).

## Relação com o driver condicional dos scripts

Os scripts de `/benchmark` têm um **driver condicional** (`BENCH_DURACAO`):
sem a variável rodam no modo clássico, com ela rodam por tempo de forma
autônoma. Este runner os executa **sem** `BENCH_DURACAO`, então eles caem no
ramo clássico — cujo `timeit.timeit(lambda: ...)` é interceptado para a
medição por tempo daqui.

Ou seja, há duas maneiras equivalentes de medir por tempo:

- **este runner** — para a suíte completa: verificação + CSV consolidado;
- **`BENCH_DURACAO=3 python <script>`** — para rodar um script individual
  avulso, sem runner.

## Status possíveis

| Status | Significado |
|---|---|
| `ok` | mediu e normalizou |
| `sem_timing` | o script não chama `timeit(lambda: ...)` (ex.: `manipula_no_expression`) |
| `erro: ...` | exceção na carga do script ou dentro da chamada |
| `timeout (>Ts)` | o subprocesso estourou `--timeout` |
