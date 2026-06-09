import timeit

def count_bits(n, acc=0):
    _P = []
    _P.append((n, acc, None, 0))
    while len(_P) > 0:
        n, acc, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = acc
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((n, acc, _r1, 1))
                _P.append((n >> 1, acc + (n & 1), None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
mask = 255
n = 255
a = n | mask
b = n ^ mask
c = n << 2
d = ~n
n_pos = +n
results = []
for i in range(100):
    if i % 2 == 0:
        continue
    results.append(count_bits(i))
n = (1 << 20) - 1
qtd_execucoes = 100000
tempo = timeit.timeit(lambda: count_bits(n), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')