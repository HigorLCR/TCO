import os
import timeit

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
qtd_execucoes = 1


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: tail_mdc(353410009178752575339944833520459068284945046358154977604109175253890696634271360121583566110064725510836075851584985143412396868586425109102723291106570618750075392710633321729992106743321640281356794177320, 571829406815633979529643697006273045106845980748991112071673038743714031497887739023091610769764627307772654802298784361803421747114571265690519449915873452164193174293407940201977897716937097604164288130909),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: tail_mdc(353410009178752575339944833520459068284945046358154977604109175253890696634271360121583566110064725510836075851584985143412396868586425109102723291106570618750075392710633321729992106743321640281356794177320, 571829406815633979529643697006273045106845980748991112071673038743714031497887739023091610769764627307772654802298784361803421747114571265690519449915873452164193174293407940201977897716937097604164288130909))
    _k, _e = 0, 0.0                        # iteracoes completas, tempo somado
    _lote = 1
    while _e < _T:                         # T e piso: so para ao alcanca-lo
        _e += _bench.timeit(number=_lote)
        _k += _lote
        if _e >= _T:
            break
        _est = int((_T - _e) / (_e / _k))  # estimativa do que falta pela taxa
        _lote = max(1, min(_est, _lote * 10))
    print(f"benchmark por tempo (piso {_T}s): {_k} iteracoes | {_e:.4f}s total | {_e/_k*1000:.4f}ms por chamada")
