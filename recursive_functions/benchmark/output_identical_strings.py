
def equal_strings_tail(s, t):
    while not (len(s) != len(t) or s == '' or s[0] != t[0]):
        s, t = (s[1:], t[1:])
    if len(s) != len(t):
        return False
    elif s == '':
        return True
    else:
        return False


n = 10_000
s = "a" * n
t = s

# --- benchmark ---
def chamada():
    return equal_strings_tail(s, t)
