def MergeSort_Rec(L, i, j):
    _P = []
    _P.append((L, i, j, None, None, None, 0))
    while len(_P) > 0:
        L, i, j, m, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None

        def Merge(L, i, m, j):
            Ln = []
            p1 = i
            p2 = m + 1
            for _ in range(j - i + 1):
                if p2 > j or (p1 <= m and L[p1] < L[p2]):
                    Ln.append(L[p1])
                    p1 += 1
                else:
                    Ln.append(L[p2])
                    p2 += 1
            for k in range(j - i + 1):
                L[i + k] = Ln[k]
        if _s in [1, 2] or (_s == 0 and i < j):
            if _s == 0:
                m = (i + j) // 2
            if _s == 0:
                _P.append((L, i, j, m, _r1, _r2, 1))
                _P.append((L, i, m, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r1
            if _s == 0:
                _P.append((L, i, j, m, _r1, _r2, 2))
                _P.append((L, m + 1, j, None, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r2
            if _s == 0:
                Merge(L, i, m, j)
    return _r
N = [1000000] * 1
f = MergeSort_Rec
for n in N:
    L = [i for i in range(n, 0, -1)]
    f(L, 0, len(L) - 1)
L = [i for i in range(n, 0, -1)]
f(L, 0, len(L) - 1)
print(L)