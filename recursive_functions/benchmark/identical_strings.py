def equal_strings_tail(s, t):
    if len(s) != len(t):
        return False
    elif s == '':
        return True
    elif s[0] != t[0]:
        return False
    else:
        return equal_strings_tail(s[1:], t[1:])
    
import sys
import timeit

sys.setrecursionlimit(11_000)

n = 10_000
s = "a" * n  # pior caso: strings idênticas forçam recursão até o fim
t = s
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: equal_strings_tail(s, t), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
                       