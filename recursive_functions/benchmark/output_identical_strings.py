def equal_strings_tail(s, t):
    while not (len(s) != len(t) or s == '' or s[0] != t[0]):
        s, t = (s[1:], t[1:])
    if len(s) != len(t):
        return False
    elif s == '':
        return True
    else:
        return False

import timeit

n = 10_000
s = "a" * n
t = s
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: equal_strings_tail(s, t), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")