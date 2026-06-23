def mdc(a, b):
    a = a
    b = b
    if b == 0:
        return a
    else:
        return mdc(b, a % b)

print(mdc(48, 18))
