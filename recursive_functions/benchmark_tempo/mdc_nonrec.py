def tail_mdc(a, b):
    _P = []
    _P.append((a, b, None, None, None, 0))
    while len(_P) > 0:
        a, b, na, nb, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            na, nb = (abs(a), abs(b))
        if _s in [] or (_s == 0 and nb == 0):
            if _s == 0:
                _r = na
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((a, b, na, nb, _r1, 1))
                _P.append((nb, na % nb, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r

#fib(500) = 139423224561697880139724382870407283950070256587697307264108962948325571622863290691557658876222521294125

#fib(501) = 225591516161936330872512695036072072046011324913758190588638866418474627738686883405015987052796968498626
import timeit


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: tail_mdc(353410009178752575339944833520459068284945046358154977604109175253890696634271360121583566110064725510836075851584985143412396868586425109102723291106570618750075392710633321729992106743321640281356794177320, 571829406815633979529643697006273045106845980748991112071673038743714031497887739023091610769764627307772654802298784361803421747114571265690519449915873452164193174293407940201977897716937097604164288130909))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
