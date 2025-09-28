def Fib_It(n):
    r = 1
    a = 1
    for _ in range(3, n + 1):
        t = r
        r = r + a
        a = t
    return r

def Fib_Rec(n):
    _P = []
    _P.append((n, None, None, 0))
    while len(_P) > 0:
        n, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n <= 2):
            if _s == 0:
                _r = 1
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s == 0:
                _P.append((n, _r1, _r2, 1))
                _P.append((n - 1, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _P.append((n, _r1, _r2, 2))
                _P.append((n - 2, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r = _r1 + _r2
                _s = -1
    return _r
M = None
'\ndef Fib_RecMem(n):\n\tglobal M\n\tM = [-1]*100\n\treturn Fib_RecMem2(n)\n\n\ndef Fib_RecMem2(n):\n\tif M[n] == -1:\n\t\tif n <= 2:\n\t\t\tM[n] = 1\n\t\telse:\n\t\t\tM[n] = Fib_RecMem2(n-1) + Fib_RecMem2(n-2)\n\treturn M[n]\n'
N = [35]
f = Fib_Rec
for n in N:
    f(n)
print(f(n))