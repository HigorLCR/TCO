"""
Função recursiva tail para calcular o Máximo Divisor Comum (GCD)
"""

def tail_gcd(a, b):
    """
    Calcula o Máximo Divisor Comum usando recursão tail.
    
    Args:
        a: primeiro número
        b: segundo número
    
    Returns:
        O MDC de a e b
    """
    # Garante que trabalhamos com valores absolutos
    a, b = abs(a), abs(b)
    
    def gcd_helper(a, b):
        # Caso base
        if b == 0:
            return a
        else:
            # Recursão tail: toda a computação acontece antes da chamada recursiva
            return gcd_helper(b, a % b)
    
    return gcd_helper(a, b)

# Teste da função
if __name__ == "__main__":
    # Testes básicos
    print("Testando função tail_gcd:")
    print(f"MDC(48, 18) = {tail_gcd(48, 18)}")
    print(f"MDC(100, 25) = {tail_gcd(100, 25)}")
    print(f"MDC(17, 13) = {tail_gcd(17, 13)}")
    print(f"MDC(56, 42) = {tail_gcd(56, 42)}")
    print(f"MDC(0, 5) = {tail_gcd(0, 5)}")
    print(f"MDC(5, 0) = {tail_gcd(5, 0)}")
    
    # Teste com números negativos
    print(f"MDC(-48, 18) = {tail_gcd(-48, 18)}")
    print(f"MDC(48, -18) = {tail_gcd(48, -18)}")
    
    # Comparação com função não-tail para verificar correção
    def gcd_non_tail(a, b):
        a, b = abs(a), abs(b)
        if b == 0:
            return a
        else:
            return gcd_non_tail(b, a % b)
    
    print("\nVerificação de correção:")
    test_cases = [(48, 18), (100, 25), (17, 13), (56, 42), (0, 5), (5, 0), (-48, 18), (48, -18)]
    for a, b in test_cases:
        tail_result = tail_gcd(a, b)
        non_tail_result = gcd_non_tail(a, b)
        print(f"MDC({a}, {b}): tail={tail_result}, non-tail={non_tail_result}, iguais={tail_result == non_tail_result}")
