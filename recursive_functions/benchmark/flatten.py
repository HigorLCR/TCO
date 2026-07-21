from typing import Any

def flatten(lst, acc=None):
    if acc is None:
        acc = []
    if not lst:
        return acc
    head, *tail = lst
    if isinstance(head, list):
        return flatten(head + tail, acc)
    return flatten(tail, acc + [head])


def _placeholder() -> Any:
    pass

# --- benchmark ---
def chamada():
    return flatten([[i, [i + 1]] for i in range(0, 20, 2)])
