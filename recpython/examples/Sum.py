import sys
sys.setrecursionlimit(10000000)

def Sum_Rec(L, n):
	if n == 0:
		return 0
	else:
		res = Sum_Rec(L, n-1) + L[n-1]
		return res
	
N = [5000000] * 1; f = Sum_Rec 
for n in N:
	L = [2 for i in range(n)]
	f(L, n)
print(f(L, n))