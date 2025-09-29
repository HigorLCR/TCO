def tail_reverse_list(lst, accumulator=None):
    if accumulator is None:
        accumulator = []
    
    # Caso base: lista vazia
    if not lst:
        return accumulator
    else:
        # Recursão tail: toda a computação acontece antes da chamada recursiva
        return tail_reverse_list(lst[1:], [lst[0]] + accumulator)

# Versão alternativa mais eficiente usando índices
def tail_reverse_list_index(lst, index=0, accumulator=None):
    if accumulator is None:
        accumulator = []
    
    # Caso base: chegamos ao fim da lista
    if index >= len(lst):
        return accumulator
    else:
        # Recursão tail: toda a computação acontece antes da chamada recursiva
        return tail_reverse_list_index(lst, index + 1, [lst[index]] + accumulator)
