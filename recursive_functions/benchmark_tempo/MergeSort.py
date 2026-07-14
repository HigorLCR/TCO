
def MergeSort_Rec(L, i, j):
	#variáveis locais: L, i, j, m, 
	def Merge(L, i, m, j):
		Ln = []; p1 = i; p2 = m+1
		for _ in range(j-i+1):
			if p2 > j or (p1 <= m and L[p1] < L[p2]):
				Ln.append(L[p1]); p1 += 1
			else:
				Ln.append(L[p2]); p2 += 1
		for k in range(j-i+1):
			L[i+k] = Ln[k]


	if i < j:
		m = (i+j)//2
		MergeSort_Rec(L, i, m)
		MergeSort_Rec(L, m+1, j)
		Merge(L, i, m, j)



import timeit

n = 1_000


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: MergeSort_Rec(list(range(n, 0, -1)), 0, n - 1))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
