"""
Função recursiva tail para inverter uma lista
"""

def tail_reverse_list(lst, accumulator=None):
    """
    Inverte uma lista usando recursão tail.
    
    Args:
        lst: lista a ser invertida
        accumulator: lista acumuladora para o resultado (inicializada automaticamente)
    
    Returns:
        Lista invertida
    """
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
    """
    Versão alternativa usando índices para evitar slicing.
    
    Args:
        lst: lista a ser invertida
        index: índice atual
        accumulator: lista acumuladora para o resultado
    
    Returns:
        Lista invertida
    """
    if accumulator is None:
        accumulator = []
    
    # Caso base: chegamos ao fim da lista
    if index >= len(lst):
        return accumulator
    else:
        # Recursão tail: toda a computação acontece antes da chamada recursiva
        return tail_reverse_list_index(lst, index + 1, [lst[index]] + accumulator)

# Teste das funções
if __name__ == "__main__":
    # Testes básicos
    print("Testando função tail_reverse_list:")
    
    test_lists = [
        [],
        [1],
        [1, 2],
        [1, 2, 3],
        [1, 2, 3, 4, 5],
        ["a", "b", "c"],
        list(range(10))
    ]
    
    for lst in test_lists:
        tail_result = tail_reverse_list(lst)
        index_result = tail_reverse_list_index(lst)
        builtin_result = lst[::-1]
        
        print(f"Original: {lst}")
        print(f"  Tail slicing: {tail_result}")
        print(f"  Tail index: {index_result}")
        print(f"  Built-in: {builtin_result}")
        print(f"  Correto: {tail_result == builtin_result == index_result}")
        print()
    
    # Teste de performance com lista grande
    print("Teste com lista grande (500 elementos):")
    big_list = list(range(500))
    
    import time
    
    # Teste da versão com slicing
    start = time.time()
    result_slicing = tail_reverse_list(big_list)
    time_slicing = time.time() - start
    
    # Teste da versão com índice
    start = time.time()
    result_index = tail_reverse_list_index(big_list)
    time_index = time.time() - start
    
    # Teste da versão built-in
    start = time.time()
    result_builtin = big_list[::-1]
    time_builtin = time.time() - start
    
    print(f"Slicing: {len(result_slicing)} elementos em {time_slicing:.6f}s")
    print(f"Índice: {len(result_index)} elementos em {time_index:.6f}s")
    print(f"Built-in: {len(result_builtin)} elementos em {time_builtin:.6f}s")
    print(f"Primeiros 5 elementos - Slicing: {result_slicing[:5]}, Índice: {result_index[:5]}, Built-in: {result_builtin[:5]}")
    print(f"Todos iguais: {result_slicing == result_index == result_builtin}")
