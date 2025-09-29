"""
Função recursiva não-tail para busca binária
"""

def binary_search(arr, target, left=0, right=None):
    """
    Busca binária recursiva não-tail.
    
    Args:
        arr: lista ordenada onde buscar
        target: valor a ser encontrado
        left: índice esquerdo (início)
        right: índice direito (fim)
    
    Returns:
        Índice do elemento se encontrado, -1 caso contrário
    """
    if right is None:
        right = len(arr) - 1
    
    # Caso base: elemento não encontrado
    if left > right:
        return -1
    
    # Calcula o meio
    mid = (left + right) // 2
    
    # Caso base: elemento encontrado
    if arr[mid] == target:
        return mid
    # Recursão não-tail: a comparação acontece após a chamada recursiva
    elif arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, right)

# Teste da função
if __name__ == "__main__":
    # Teste com lista ordenada
    test_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print("Lista de teste:", test_list)
    print("Testando busca binária:")
    
    # Testes
    print(f"Buscar 7: índice {binary_search(test_list, 7)}")
    print(f"Buscar 1: índice {binary_search(test_list, 1)}")
    print(f"Buscar 19: índice {binary_search(test_list, 19)}")
    print(f"Buscar 6: índice {binary_search(test_list, 6)}")
    print(f"Buscar 20: índice {binary_search(test_list, 20)}")
    
    # Teste com lista maior
    big_list = list(range(1, 101))  # [1, 2, 3, ..., 100]
    print(f"\nBuscar 50 em lista de 100 elementos: índice {binary_search(big_list, 50)}")
    print(f"Buscar 1 em lista de 100 elementos: índice {binary_search(big_list, 1)}")
    print(f"Buscar 100 em lista de 100 elementos: índice {binary_search(big_list, 100)}")
