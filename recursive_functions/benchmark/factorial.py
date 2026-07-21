import sys

sys.setrecursionlimit(100000)

n1 = 5000
n2 = 1

def tail_factorial(n, a):
    if n == 0: 
        return a
    else:
        return tail_factorial(n-1, n*a)



input_list = []
input_list.append((n1, n2))

for n1, n2 in input_list:
    print(f"tail_factorial({n1}, {n2}) = {tail_factorial(n1, n2)}")

# --- benchmark ---
def chamada():
    return tail_factorial(n1, n2)
