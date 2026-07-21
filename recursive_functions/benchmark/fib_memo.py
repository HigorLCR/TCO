
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_with_counter(n):
    count = 0
    cache = {}

    def _fib(k):
        nonlocal count
        count += 1
        if k in cache:
            return cache[k]
        if k <= 1:
            return k
        cache[k] = _fib(k - 1) + _fib(k - 2)
        return cache[k]

    return _fib(n), count


warm_cache = {k: fib_memo(k) for k in range(20)}

n = 35

# --- benchmark ---
def chamada():
    return fib_memo(n)
