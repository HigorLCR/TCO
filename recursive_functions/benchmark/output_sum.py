def Sum_Rec(L, n, acc=0):
    while not n == 0:
        L, n, acc = (L, n - 1, acc + L[n - 1])
    return acc

N = [1 for i in range(5000000)]
print(Sum_Rec(N, 5000000))