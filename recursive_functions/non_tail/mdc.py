"""
Função recursiva não-tail para calcular o Máximo Divisor Comum (GCD)
"""

def gcd(a, b):
    """
    Calcula o Máximo Divisor Comum usando o algoritmo de Euclides.
    
    Args:
        a: primeiro número
        b: segundo número
    
    Returns:
        O MDC de a e b
    """
    # Garante que trabalhamos com valores absolutos
    a, b = abs(a), abs(b)
    
    if b == 0:
        return a
    else:
        # Recursão não-tail: a operação de módulo acontece na chamada recursiva
        return gcd(b, a % b)

# Teste da função
if __name__ == "__main__":
    # Testes básicos
    print("Testando função GCD:")
    print(f"MDC(48, 18) = {gcd(48, 18)}")
    print(f"MDC(100, 25) = {gcd(100, 25)}")
    print(f"MDC(17, 13) = {gcd(17, 13)}")
    print(f"MDC(56, 42) = {gcd(56, 42)}")
    print(f"MDC(0, 5) = {gcd(0, 5)}")
    print(f"MDC(5, 0) = {gcd(5, 0)}")
    
    # Teste com números negativos
    print(f"MDC(-48, 18) = {gcd(-48, 18)}")
    print(f"MDC(48, -18) = {gcd(48, -18)}")
