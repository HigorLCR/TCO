# Limitações do `recpython3.py`

Documenta os casos em que o transformador recursão → iteração
(`recpython/recpython3.py`) falha, com repro mínimo, causa-raiz e contorno.

**Tema comum:** o `recpython3` modela a recursão como um conjunto **fixo e
estaticamente conhecido** de pontos de chamada, cada um produzindo **um
resultado escalar**, empilhados num frame de **aridade fixa** (uma tupla
`(param1, ..., local1, ..., _r1, ..., _s)`). Qualquer coisa que introduza
**aridade variável** (comprehensions, `*args`/`**kwargs`) ou um frame
malformado (`return` sem valor) quebra esse modelo.

---

## 1. Chamada recursiva dentro de *list comprehension*

### Repro
```python
def mapeia(no):
    return [mapeia(x) for x in no.filhos]
```

### Erro
`NameError: name 'x' is not defined` (a variável de laço da comprehension).

### Causa
A comprehension tem **escopo próprio**: `x` só existe dentro dos colchetes.
O transformador extrai a chamada recursiva e a move para o corpo da função
(`_P.append((x, ...))`), onde `x` não está definido. Além disso, o modelo de
"um ponto de chamada = um resultado escalar" não comporta a comprehension,
que faz N chamadas e produz uma lista — ele a substituiria por um único `_r1`.

### Contorno ✅
Trocar a comprehension por um laço `for` explícito com acumulador. O `for` é
*function-scoped* (a variável de laço vive no corpo da função) e o `recpython3`
tem regra dedicada para ele (`applyRule4`), salvando inclusive o estado do
iterador (`_forN`) no frame.

```python
def mapeia(no):
    novos = []
    for x in no.filhos:
        novos.append(mapeia(x))
    return novos
```

> Aplicado em `recursive_functions/newfunc/manipula_no_interactive.py` e
> `manipula_no_functiontype.py`.

---

## 2. `return` sem valor (*bare return*)

### Repro
```python
def conta_ate(n):
    if n <= 0:
        return            # <-- sem valor
    conta_ate(n - 1)
```

### Erro
`AttributeError: 'NoneType' object has no attribute '_fields'`
(durante `ast.unparse`, ao escrever o arquivo `_nonrec`).

### Causa
A `applyRule3` (trata `Return`) monta `_r = C.value`:

```python
Rbar = ast.Assign([ast.Name("_r", ast.Store())], C.value)
```

Com `return` puro, `C.value is None`, gerando um `Assign(value=None)` —
nó malformado que o próprio `ast.unparse` rejeita. (Como o arquivo `_nonrec`
é aberto em modo `'w'` **antes** do `unparse` falhar, ele fica vazio.)

### Contorno ✅
Usar `return None` explícito.

```python
def conta_ate(n):
    if n <= 0:
        return None
    conta_ate(n - 1)
```

> **Correção possível na ferramenta (trivial):** na `applyRule3`, se
> `C.value is None`, usar `ast.Constant(value=None)` no lugar.

---

## 3. Repasse de `*args` / `**kwargs` na chamada recursiva

### Repro
```python
def f(n, *args):
    if n <= 0:
        return None
    f(n - 1, *args)        # *args repassado
```
(idem com `**kwargs`)

### Erro
`ValueError: not enough values to unpack (expected 4, got 3)`
(em tempo de execução do `_nonrec`, ao desempacotar o frame da pilha).

### Causa
O frame da pilha é uma **tupla de aridade fixa**, desempacotada com
`p1, p2, ..., _r1, _s = _P.pop()`. Mas:

- `*args` é um nó `Starred` em `Ri.args`; a `getArgs` faz `for x in args:
  elems.append(x)` e o coloca **dentro da tupla**, que então se desfaz por
  *unpacking* (`(f, n-1, *args, _s)`) — a quantidade de elementos passa a
  depender de `len(args)`, desalinhando o `pop()`;
- `**kwargs` fica em `Ri.keywords`, que a `getArgs` **ignora por completo** —
  o argumento nem é repassado.

### Contorno ⚠️ (depende do objetivo)
- **Se o objetivo é encaminhar argumentos de aridade variável na própria
  recursão** (ex.: uma recursão genuinamente variádica): não há contorno no
  nível da função que preserve a semântica — o modelo de frame fixo não
  comporta isso. A correção teria que ser **na ferramenta**: tratar `Starred`
  nos argumentos da chamada e os `keywords` (`**kwargs`), empacotando-os em
  campos próprios do frame em vez de espalhá-los na tupla.
- **Se o objetivo é apenas exercitar o nó `ParamSpec`** (cobertura de AST):
  ✅ há contorno. O nó `ParamSpec` vem do `[**P]` nos `type_params`, **não** do
  repasse de `*args`/`**kwargs`. Basta declarar `[**P]` e passar os argumentos
  de `f` como **parâmetros normais** de aridade fixa, deixando o unpacking
  `*args`/`**kwargs` apenas na chamada a `f` (não-recursiva):

  ```python
  def repete[**P](f: Callable[P, None], n: int, args: tuple, kwargs: dict) -> None:
      if n <= 0:
          return None
      f(*args, **kwargs)          # unpacking aqui (chamada NAO-recursiva)
      repete(f, n - 1, args, kwargs)   # chamada recursiva de aridade FIXA
  ```

  Assim a função gera o nó `ParamSpec`, roda como recursiva **e** é
  transformável pelo `recpython3`.

---

## 4. Funções `async` (corrotinas)

### Repro
```python
async def fatorial(n):
    if n <= 1:
        return 1
    return n * await fatorial(n - 1)
```

### Comportamento
O `recpython3` **não transforma** a corrotina — ela passa intacta para o
`_nonrec` (a recursão via `await` continua lá). Não há erro; simplesmente nada
acontece.

### Causa
`ast.AsyncFunctionDef` **não é subclasse** de `ast.FunctionDef`, e o laço
principal só processa `FunctionDef`:

```python
for F in ast.walk(T):
    if isinstance(F, ast.FunctionDef):   # AsyncFunctionDef nao casa aqui
        Translate(F)
```

Logo corrotinas — e, por tabela, os nós `AsyncFor` / `AsyncWith` / `Await` —
são ignoradas por completo.

### Contorno ❌
Nenhum no nível da função: a recursão via `await` é um modelo de controle
diferente (corrotinas + *event loop*) que o transformador não modela. Serve
apenas para **cobertura de AST** e não é *benchmarkável* no mesmo padrão (exige
`asyncio.run`, cujo overhead dominaria a medição). Ver `gera_no_async.py`.

---

## 5. Recursão com `try/except*` (exception groups)

### Repro (já inválido como fonte!)
```python
def f(n):
    if n <= 0:
        return 0
    try:
        raise ExceptionGroup("g", [ValueError()])
    except* ValueError:
        return 1 + f(n - 1)     # <-- SyntaxError
```

### Erro
`SyntaxError: 'break', 'continue' and 'return' cannot appear in an except* block`

### Causa
Restrição da **própria linguagem** (PEP 654): não se pode sair de um bloco
`except*` com `return`. Ou seja, a forma recursiva "natural" nem chega a
compilar — não é uma limitação do `recpython3`, mas inviabiliza o exemplo
recursivo idiomático.

### Contorno ⚠️
Mover a recursão para uma **atribuição** dentro do handler e deixar o `return`
**fora** do `except*` (além de levantar um `ExceptionGroup` só para ter o que
tratar). É um caso forçado, de cobertura de AST. Ver `gera_no_trystar.py`.

> Curiosidade: como a transformação do `recpython3` troca o `return` por
> atribuições a `_r`, ela "conserta" acidentalmente o fonte inválido com
> `return` dentro do `except*` — mas isso é efeito colateral, não suporte real.

---

## Resumo

| # | Limitação | Repro mínimo | Contorno na função? |
|---|-----------|--------------|:-------------------:|
| 1 | chamada recursiva em *list comprehension* | `[f(x) for x in xs]` | ✅ trocar por laço `for` |
| 2 | `return` sem valor | `return` | ✅ usar `return None` |
| 3 | repasse de `*args` / `**kwargs` | `f(n-1, *args)` | ⚠️ só se não precisar repassar variádicos na recursão |
| 4 | função `async` (corrotina) | `async def f(): ... await f()` | ❌ ignorada pelo transformador (cobertura-only) |
| 5 | recursão em `try/except*` | `except*: return f(n-1)` | ⚠️ `return` no handler é inválido; recursão fora dele |

### Sobre a função `repete` (exemplo do `ParamSpec`)

A versão original da `recursive_functions/benchmark/repete.py` esbarrava em
**duas** limitações ao mesmo tempo: o bug **2** (`return` puro) e o bug **3**
(`repete(f, n-1, *args, **kwargs)`).

A versão atual **contorna ambos** e tem `_nonrec` funcional:
- bug 2 → `return None`;
- bug 3 → `args`/`kwargs` viram parâmetros normais de aridade fixa; a chamada
  recursiva não repassa variádicos (o `*args`/`**kwargs` fica só na chamada a
  `f`, que não é recursiva).

O nó `ParamSpec` continua presente (vem do `[**P]`), então a cobertura de AST é
mantida. O bug **3** permanece uma limitação real do `recpython3` para recursões
que **genuinamente** precisem repassar argumentos variádicos a si mesmas.
