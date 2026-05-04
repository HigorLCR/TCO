import sys
sys.setrecursionlimit(10000000)

def Sum_Rec(L, n, acc = 0):
	if n == 0:
		return acc
	else:
		return Sum_Rec(L, n-1, acc + L[n-1])
	
N = [5000000] * 1; f = Sum_Rec 
for n in N:
	L = [2 for i in range(n)]
	f(L, n)
print(f(L, n))