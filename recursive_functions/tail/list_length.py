

def tail_list_length(lst, accumulator=0):
    if not lst:
        return accumulator
    else:
        return tail_list_length(lst[1:], accumulator + 1)


#alternativa
def tail_list_length_index(lst, index=0, length=0):
    if index >= len(lst):
        return length
    else:
        return tail_list_length_index(lst, index + 1, length + 1)


