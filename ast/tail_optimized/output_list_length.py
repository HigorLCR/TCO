def tail_list_length(lst, accumulator=0):
    while not not lst:
        lst, accumulator = (lst[1:], accumulator + 1)
    return accumulator