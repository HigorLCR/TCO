import sys
import timeit
sys.setrecursionlimit(10000)

def remove_keys(d, keys):
    _P = []
    _P.append((d, keys, None, None, 0))
    while len(_P) > 0:
        d, keys, key, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and (not keys)):
            if _s == 0:
                _r = d
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                key = keys[0]
            if _s in [] or (_s == 0 and key in d):
                del d[key]
            if _s == 0:
                _P.append((d, keys, key, _r1, 1))
                _P.append((d, keys[1:], None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
base_dict = {str(i): i for i in range(500)}
keys_to_remove = [str(i) for i in range(0, 500, 2)]
qtd_execucoes = 1000
tempo = timeit.timeit(lambda: remove_keys(dict(base_dict), keys_to_remove), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')