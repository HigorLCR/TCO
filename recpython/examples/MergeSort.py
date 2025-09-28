
def MergeSort_Rec(L, i, j):
	#variáveis locais: L, i, j, m, 
	def Merge(L, i, m, j):
		Ln = []; p1 = i; p2 = m+1
		for _ in range(j-i+1):
			if p2 > j or (p1 <= m and L[p1] < L[p2]):
				Ln.append(L[p1]); p1 += 1
			else:
				Ln.append(L[p2]); p2 += 1
		for k in range(j-i+1):
			L[i+k] = Ln[k]


	if i < j:
		m = (i+j)//2
		MergeSort_Rec(L, i, m)
		MergeSort_Rec(L, m+1, j)
		Merge(L, i, m, j)



N = [1000000]*1; f = MergeSort_Rec 
for n in N:
	L = [i for i in range(n, 0, -1)]
	f(L, 0, len(L)-1)
L = [i for i in range(n, 0, -1)]
f(L, 0, len(L)-1)
print(L)
