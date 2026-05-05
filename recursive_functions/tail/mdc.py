
def tail_mdc(a, b):
    na, nb = abs(a), abs(b)

    if nb == 0:
        return na
    else:
        return tail_mdc(nb, na % nb)
