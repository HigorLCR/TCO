def Fib_It(n):
	r = 1; a = 1
	for _ in range(3, n+1):
		t = r
		r = r + a
		a = t
	return r

def Fib_Rec(n):
	if n <= 2:
		return 1
	else:
		return Fib_Rec(n-1) + Fib_Rec(n-2)

M = None

"""
def Fib_RecMem(n):
	global M
	M = [-1]*100
	return Fib_RecMem2(n)


def Fib_RecMem2(n):
	if M[n] == -1:
		if n <= 2:
			M[n] = 1
		else:
			M[n] = Fib_RecMem2(n-1) + Fib_RecMem2(n-2)
	return M[n]
"""

N = [35]; f = Fib_Rec #N=10 6,179s; 

for n in N:
	f(n)
print(f(n))