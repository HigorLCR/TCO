def tail_reverse_list(lst, accumulator=None):
    while not not lst:
        if accumulator is None:
            accumulator = []
        lst, accumulator = (lst[1:], [lst[0]] + accumulator)
    if accumulator is None:
        accumulator = []
    return accumulator