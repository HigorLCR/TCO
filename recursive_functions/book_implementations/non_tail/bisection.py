def f(x):
    return x * x - 2

def bisection(a, b, f, epsilon):
    z = (a + b) / 2
    if f(z) == 0 or b - a <= 2 * epsilon:
        return z
    elif (f(a) > 0 and f(z) < 0) or (f(a) < 0 and f(z) > 0):
        return bisection(a, z, f, epsilon)
    else:
        return bisection(z, b, f, epsilon)

# Print an approximation of the square root of 2
print(bisection(0, 4, f, 10**(-10) ))