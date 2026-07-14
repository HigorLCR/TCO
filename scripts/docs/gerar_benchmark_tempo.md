# `gerar_benchmark_tempo.py` — gerador do diretório `benchmark_tempo/`

## Papel

Scaffolding reproduzível: converte `recursive_functions/benchmark/` em
`recursive_functions/benchmark_tempo/`, onde cada script é **autônomo** e
orientado por **tempo** — roda sozinho (sem runner), executa a própria chamada
por `BENCH_DURACAO` segundos e imprime quantas execuções couberam (float).

É a alternativa "materializada" ao `benchmark_por_tempo.py`: lá a medição por
tempo acontece por interceptação em runtime (arquivos originais intactos);
aqui os arquivos convertidos carregam o driver por tempo dentro de si.

## Uso

```
python scripts/gerar_benchmark_tempo.py
```

Sem parâmetros. Origem e destino são fixos no script (`ORIG`/`DEST`).

Executar um script gerado:

```bash
# bash
BENCH_DURACAO=3 python recursive_functions/benchmark_tempo/sum.py
```
```powershell
# PowerShell
$env:BENCH_DURACAO='3'; python recursive_functions/benchmark_tempo/sum.py
```

Saída de cada script gerado:

```
execucoes em 3.0s: 367.431859 | 375 chamadas em 3.0630s
```

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `recursive_functions/benchmark/*.py` |
| Saída | `recursive_functions/benchmark_tempo/*.py` (mesmos nomes) |

## Como funciona

Para cada `.py` da origem:

1. **Localiza o lambda:** `ast.parse` + `achar_lambda` percorre os statements
   do módulo procurando a chamada `timeit.timeit(...)` e extrai o **texto
   exato** do lambda com `ast.get_source_segment` (preserva a grafia original,
   ex.: `lambda: quickselect(a_orig[:], 0, n - 1, k)`), além da linha em que o
   statement do timeit começa.

2. **Preserva o corpo:** mantém todas as linhas **antes** do statement do
   timeit — definições de função e montagem da entrada ficam intactas. Remove
   apenas linhas em branco finais e o `qtd_execucoes = ...` órfão (só era usado
   pelo timeit/print antigos).

3. **Anexa o driver por tempo** (constante `DRIVER`, com `__LAMBDA__`
   substituído pelo lambda extraído):

   ```python
   _DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
   _bench = _timeit.Timer(<lambda original>)
   _ncal, _tcal = _bench.autorange()      # calibra (lote >= 0.2s)
   if _tcal >= _DURACAO:
       _k, _e = _ncal, _tcal              # calibração já cobriu o tempo-alvo
   else:
       _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
       _e = _bench.timeit(number=_alvo)   # roda ~DURACAO segundos
       _k = _alvo
   _execucoes = _k * (_DURACAO / _e)      # normaliza para exatamente DURACAO
   print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
   ```

   Mesma mecânica de calibração/normalização do `benchmark_por_tempo.py`
   (ver `docs/benchmark_por_tempo.md` para o porquê do float normalizado).

4. **Arquivos sem `timeit(lambda: ...)`** — `manipula_no_expression.py` e seu
   `_nonrec` — são **copiados sem alteração** (são demos; não há chamada a
   medir). O gerador loga `[copiado sem timeit]`.

Resultado da última geração: **80 convertidos + 2 copiados = 82**.

## Por que as funções não precisaram mudar

Os scripts do benchmark já foram escritos para `timeit(number=N)` — que chama
o lambda N vezes — então cada chamada já é independente:

- entradas mutáveis usam cópia/reconstrução por chamada
  (`quickselect(a_orig[:], ...)`, `MergeSort_Rec(list(range(n, 0, -1)), ...)`);
- `fib_memo(n)` cria `memo` novo a cada chamada (default `memo=None`);
- as demais são funções puras sobre a mesma entrada.

Rodar "até o tempo ser alcançado" é, portanto, só uma troca de **driver** — o
trabalho por chamada permanece o mesmo.

## Atenção

- O gerador **sobrescreve** `benchmark_tempo/` a cada execução. Não edite os
  arquivos gerados à mão: ajustes devem ser feitos no `DRIVER` (ou na lógica)
  do gerador, e o diretório regenerado.
- Se os fontes de `/benchmark` mudarem (nova função, parâmetro ajustado),
  rode o gerador de novo para sincronizar.
