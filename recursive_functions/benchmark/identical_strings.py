import sys

def equal_strings_tail(s, t):
    if len(s) != len(t):
        return False
    elif s == '':
        return True
    elif s[0] != t[0]:
        return False
    else:
        return equal_strings_tail(s[1:], t[1:])
    

sys.setrecursionlimit(11_000)

n = 10_000
s = "a" * n  # pior caso: strings idênticas forçam recursão até o fim
t = s

# --- benchmark ---
def chamada():
    return equal_strings_tail(s, t)
