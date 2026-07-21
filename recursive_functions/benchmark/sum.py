import sys

sys.setrecursionlimit(10000000)

def Sum_Rec(L, n, acc = 0):
	if n == 0:
		return acc
	else:
		return Sum_Rec(L, n-1, acc + L[n-1])
	
N = [1 for i in range(10000)];

# --- benchmark ---
def chamada():
    return Sum_Rec(N, 10000)
