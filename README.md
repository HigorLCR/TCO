# TCO — Tail Call Optimization

Projeto de **Teoria da Computação** que implementa uma forma de **otimização de chamadas de cauda (Tail Call Optimization — TCO)** para Python. O núcleo do trabalho é um algoritmo que, a partir da **árvore sintática (AST)** do código, identifica funções **recursivas de cauda** e as reescreve em versões **iterativas** (usando `while`), evitando crescimento da pilha de execução e o risco de *stack overflow*.

---

## Contexto

Em muitas linguagens, cada chamada de função consome espaço na pilha. Em funções recursivas, isso pode levar a **estouro de pilha** (*stack overflow*) quando a profundidade da recursão é grande. Em **recursão de cauda** (tail recursion), a chamada recursiva é a última operação da função — ou seja, não há computação após o retorno. Nesse caso, o quadro de pilha da chamada atual pode ser descartado antes da próxima chamada, o que equivale a um **laço iterativo**. Linguagens como Python não fazem essa otimização automaticamente; este projeto implementa uma transformação **estática** (em tempo de análise do código) que converte recursão de cauda em laço.

---

## Estrutura do Projeto

```
TCO/
├── ast/                          # Núcleo: geração/transformação de AST
│   ├── gerador_arvore.py         # Algoritmo principal de TCO via AST
│   ├── new_gerador_arvore.py    # Versão alternativa/simplificada
│   └── tail_optimized/          # Código otimizado por função
│       ├── output_factorial.py
│       ├── output_mdc.py
│       ├── output_sum.py
│       ├── output_list_length.py
│       └── ...
├── recursive_functions/          # Funções de teste
│   ├── tail/                     # Versões recursivas de cauda
│   │   ├── factorial.py
│   │   ├── mdc.py
│   │   ├── fibonacci.py
│   │   ├── sum.py
│   │   ├── list_length.py
│   │   ├── power.py
│   │   └── reverse_list.py
│   └── non_tail/                 # Recursão não de cauda (para contraste)
│       ├── factorial.py
│       ├── fibonacci.py
│       ├── mdc.py
│       └── ...
├── recpython/                    # Abordagem alternativa (simulação de pilha)
│   ├── recpython.py              # Tradutor baseado em regras de transformação
│   └── examples/                 # Exemplos *_nonrec.py = versão iterativa
│       ├── Tail_Factorial.py / Tail_Factorial_nonrec.py
│       ├── Fibonacci.py / Fibonacci_nonrec.py
│       └── ...
├── code_templates/               # Modelos de código (if, while, assign)
└── README.md
```

---

## Algoritmo Principal: `ast/gerador_arvore.py`

O **gerador de árvore** é o coração do projeto. Ele:

1. **Lê** o código-fonte Python e constrói a AST com `ast.parse()`.
2. **Identifica** se a função indicada é recursiva e se é **recursiva de cauda** (último `return` é chamada à própria função).
3. **Localiza** o bloco condicional que separa o caso base da recursão:
   - `find_recursive_if_block`: encontra o `if` em que um ramo leva à chamada recursiva e o outro ao retorno (caso base).
4. **Extrai**:
   - assinatura da função e parâmetros;
   - condição de parada e blocos “caso base” vs “ramo recursivo”;
   - argumentos passados na chamada recursiva.
5. **Transforma** o corpo da função em um **`while`**:
   - condição do `while`: negação da condição de parada (enquanto não for caso base);
   - corpo: código “inicial” antes do `if`, corpo do ramo recursivo (exceto o `return` recursivo) e uma **atribuição em lote** dos parâmetros com os argumentos da chamada recursiva;
   - após o `while`: bloco do caso base e retorno.

Assim, a recursão de cauda vira um laço que apenas atualiza os parâmetros e repete, sem novas chamadas de função.

### Funções auxiliares (resumo)

| Função | Papel |
|--------|--------|
| `is_function_recursive` | Verifica se existe chamada à própria função em algum `return`. |
| `is_function_tail_recursive` | Verifica se o retorno é *apenas* a chamada recursiva (tail call). |
| `find_recursive_if_block` | Encontra o `if` cujo ramo “true” ou “else” contém a recursão. |
| `find_initial_block` | Estatamentos antes do `if` recursivo. |
| `find_recursion_args` | Argumentos da chamada recursiva. |
| `find_signature` | Nó `FunctionDef` da função. |
| `convert_tail_recursive_to_loop` | Monta a nova AST com o `while` e o caso base. |

### Uso via linha de comando

```bash
cd ast
python gerador_arvore.py <arquivo> <nome_funcao> [-dump] [-nt]
```

- **`arquivo`**: nome do arquivo em `../recursive_functions/tail/` (ou `non_tail/` com `-nt`).
- **`nome_funcao`**: nome da função a analisar/otimizar.
- **`-dump`**: imprime código original, código transformado e AST (original e nova).
- **`-nt`**: indica que o código está em `../recursive_functions/non_tail/`.

A saída otimizada é escrita em `output_<arquivo>` no diretório atual.

---

## Exemplo Concreto: Fatorial de cauda

**Entrada** (`recursive_functions/tail/factorial.py`):

```python
def tail_factorial(n, a):
    if n == 0:
        return a
    else:
        return tail_factorial(n - 1, n * a)
```

**Saída** (ex.: `ast/tail_optimized/output_factorial.py`):

```python
def tail_factorial(n, a):
    while not n == 0:
        n, a = (n - 1, n * a)
    return a
```

A condição de parada é `n == 0`; o laço roda enquanto `not (n == 0)`, atualizando `n` e `a` com os mesmos valores que seriam passados na chamada recursiva. Assim, o comportamento é equivalente, mas sem usar a pilha de chamadas.

---

## Funções de teste (`recursive_functions/`)

- **`tail/`**: funções escritas em estilo recursivo de cauda (factorial, mdc, fibonacci, sum, list_length, power, reverse_list, etc.), usadas como entrada para o `gerador_arvore.py`.
- **`non_tail/`**: funções recursivas que *não* são de cauda (por exemplo, fatorial clássico que faz `return n * factorial(n-1)`). Servem para contraste e para testes com a flag `-nt` (o algoritmo não as converte em laço da mesma forma que as de cauda).

---

## RecPython (`recpython/`)

O diretório **recpython** contém uma **abordagem alternativa** à otimização:

- **`recpython.py`**: implementa um tradutor baseado em **regras de transformação** sobre a AST. Em vez de converter só tail recursion em `while`, ele simula a pilha de execução de forma explícita (uso de estruturas como `_P`, `_s`, `_r` para pilha e estado).
- Os arquivos **`*_nonrec.py`** nos `examples/` são as versões geradas que não usam recursão “real”, evitando estouro de pilha mesmo em funções que não são estritamente de cauda (por exemplo, `Tail_Factorial_nonrec.py`).

Ou seja: o **ast/gerador_arvore.py** foca em **tail call → while**; o **recpython** oferece uma transformação mais geral baseada em pilha explícita.

---

## Modelos de código (`code_templates/`)

Contêm exemplos mínimos de estruturas Python (e.g. `if`, `while`, `assign`) úteis como referência para padrões que o algoritmo de AST manipula (condicionais e atribuições em lote).

---

## Limitações e observações

- O algoritmo em `gerador_arvore.py` assume um padrão bem definido: um único `if` com caso base em um ramo e tail call no outro. Funções com vários `if`/`elif` ou lógica mais complexa podem exigir extensões.
- Funções com **mais de uma função interna** (ex.: `tail_gcd` com `gcd_helper`) não são tratadas pelo fluxo atual, que trabalha sobre uma função por vez.
- O **new_gerador_arvore.py** é uma versão mais enxuta, com detecção de tail recursion e um esboço de otimização; o pipeline completo (incluindo escrita em arquivo) está em **gerador_arvore.py**.

---

## Resumo

| Componente | Função |
|------------|--------|
| **ast/gerador_arvore.py** | Lê código, gera AST, detecta recursão de cauda e converte em laço `while` com atualização de parâmetros, gerando código que não estoura a pilha. |
| **recursive_functions/tail** | Código-fonte de entrada (funções em estilo tail recursive). |
| **ast/tail_optimized/** | Código gerado (versão iterativa). |
| **recpython** | Alternativa que elimina recursão via pilha explícita, aplicável a mais padrões. |

O projeto oferece, assim, uma **implementação didática e prática** de TCO em Python por transformação estática de AST, com exemplos reutilizáveis e uma segunda estratégia (recpython) para comparação.
