import sys
sys.setrecursionlimit(10000000)

def Sum_Rec(L, n, acc = 0):
	if n == 0:
		return acc
	else:
		return Sum_Rec(L, n-1, acc + L[n-1])
	
N = [1 for i in range(5000000)];

print(Sum_Rec(N, 5000000))