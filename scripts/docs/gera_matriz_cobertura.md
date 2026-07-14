# `gera_matriz_cobertura.py` — gera `node_matrix.txt`

## Papel

Produtor de dados da cobertura: gera a matriz **nós AST × arquivos-fonte**
(`arquivos/txt/node_matrix.txt`), que alimenta a planilha de cobertura
(`planilha_cobertura.py`). É a fonte oficial de "quem cobre o quê".

## Uso

```
python scripts/gera_matriz_cobertura.py
```

Sem parâmetros — caminhos fixos no script.

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `recursive_functions/benchmark/*.py`, **excluindo** `*_nonrec.py` e `output_*` (35 arquivos) |
| Saída | `arquivos/txt/node_matrix.txt` |

## Formato do arquivo gerado

Preservado do arquivo original do projeto:

- codificação **UTF-16-LE com BOM** (`﻿`);
- separador `|` (sem espaços);
- quebras de linha **CRLF**;
- primeira célula do cabeçalho: `NO`;
- linhas = tipos de nó (ordenados alfabeticamente), colunas = arquivos
  (ordenados), célula `X` se o nó aparece naquele arquivo, `.` caso contrário.

```
NO|binary_search.py|conta.py|...
Add|X|X|...
Assign|X|X|...
...
```

## Como funciona

1. **Coleta estática:** para cada arquivo-fonte, `ast.parse` (parse padrão,
   sem `type_comments`) + `ast.walk` → conjunto dos tipos de nó presentes.
   Arquivos com `SyntaxError` são logados e contam como conjunto vazio.

2. **Cobertura demonstrativa (`manipula_no_*`):** quatro nós **nunca** aparecem
   num parse estático padrão:
   - `Interactive`, `Expression`, `FunctionType` — raízes *mod* de outros modos
     de parse (`mode="single"/"eval"/"func_type"`);
   - `TypeIgnore` — só existe com `type_comments=True`, em
     `Module.type_ignores`.

   Cada arquivo `manipula_no_<no>.py` cobre seu nó-alvo **em runtime**
   (constrói/manipula o nó de fato). O gerador deduz o alvo pelo sufixo do
   nome, casando com o catálogo `dir(ast)` em minúsculas
   (`manipula_no_typeignore.py` → `TypeIgnore`), e injeta o nó no conjunto do
   arquivo. Sufixo que não casa com nó nenhum gera `[AVISO]`.

3. **Escrita:** união de todos os nós → linhas; grava no formato descrito
   acima (criando `arquivos/txt/` se preciso).

4. **Resumo no console:** nº de arquivos/nós, tabela da cobertura
   demonstrativa aplicada e contagem de nós distintos por arquivo.

## Relação com os outros scripts de cobertura

```
fontes .py ──→ gera_matriz_cobertura.py ──→ node_matrix.txt ──→ planilha_cobertura.py ──→ xlsx
fontes .py ──→ printa_cobertura.py ──→ relatório no terminal (ramo independente, sem arquivo)
```

- O `printa_cobertura.py` faz a **mesma análise estática**, mas só imprime e
  **não** aplica a cobertura demonstrativa (lá esses 4 nós constam como
  faltantes).
- O `planilha_cobertura.py` **não parseia Python** — herda toda a informação
  desta matriz. Se o benchmark mudou, regenere a matriz antes de regenerar a
  planilha.
