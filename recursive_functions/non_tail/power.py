"""
Função recursiva não-tail para calcular potência (base^expoente)
"""

def power(base, exponent):
    """
    Calcula base elevado ao expoente usando recursão não-tail.
    
    Args:
        base: número base
        exponent: expoente (deve ser inteiro não-negativo)
    
    Returns:
        base^exponent
    """
    if exponent == 0:
        return 1
    elif exponent == 1:
        return base
    else:
        # Recursão não-tail: a operação de multiplicação acontece após a chamada recursiva
        return base * power(base, exponent - 1)

# Teste da função
if __name__ == "__main__":
    # Testes básicos
    print("Testando função power:")
    print(f"2^3 = {power(2, 3)}")
    print(f"5^4 = {power(5, 4)}")
    print(f"10^0 = {power(10, 0)}")
    print(f"3^1 = {power(3, 1)}")
    
    # Teste com números maiores
    print(f"2^10 = {power(2, 10)}")
    print(f"3^5 = {power(3, 5)}")
