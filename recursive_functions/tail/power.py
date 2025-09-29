"""
Função recursiva tail para calcular potência (base^expoente)
"""

def tail_power(base, exponent, accumulator=1):
    """
    Calcula base elevado ao expoente usando recursão tail.
    
    Args:
        base: número base
        exponent: expoente (deve ser inteiro não-negativo)
        accumulator: acumulador para o resultado (inicializado em 1)
    
    Returns:
        base^exponent
    """
    if exponent == 0:
        return accumulator
    else:
        # Recursão tail: toda a computação acontece antes da chamada recursiva
        return tail_power(base, exponent - 1, accumulator * base)

# Teste da função
if __name__ == "__main__":
    # Testes básicos
    print("Testando função tail_power:")
    print(f"2^3 = {tail_power(2, 3)}")
    print(f"5^4 = {tail_power(5, 4)}")
    print(f"10^0 = {tail_power(10, 0)}")
    print(f"3^1 = {tail_power(3, 1)}")
    
    # Teste com números maiores
    print(f"2^10 = {tail_power(2, 10)}")
    print(f"3^5 = {tail_power(3, 5)}")
    
    # Comparação com função não-tail para verificar correção
    def power_non_tail(base, exponent):
        if exponent == 0:
            return 1
        elif exponent == 1:
            return base
        else:
            return base * power_non_tail(base, exponent - 1)
    
    print("\nVerificação de correção:")
    for base in [2, 3, 5]:
        for exp in [0, 1, 3, 5]:
            tail_result = tail_power(base, exp)
            non_tail_result = power_non_tail(base, exp)
            print(f"{base}^{exp}: tail={tail_result}, non-tail={non_tail_result}, iguais={tail_result == non_tail_result}")
