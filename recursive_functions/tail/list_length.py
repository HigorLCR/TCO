

def tail_list_length(lst, accumulator=0):
    if not lst:
        return accumulator
    else:
        return tail_list_length(lst[1:], accumulator + 1)




