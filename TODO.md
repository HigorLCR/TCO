# TODO

## `ast/gerador_arvore.py`

- [ ] Adicionar `transform_recursive_calls(nodes, func_name, param_names)`: percorre recursivamente os nós AST substituindo cada `return f(args)` por uma atribuição de tupla `(params) = (args)`, mantendo returns não-recursivos e estruturas `if` intactas

- [ ] Corrigir `collect_condition_data` linha 61: quando ambos os branches são recursivos, retornar `[node]` como `recursion_prefix` em vez de `[]`, para que a etapa seguinte consiga transformar o bloco (cobre `partition_Hoare_rec`)

- [ ] Corrigir `convert_tail_recursive_to_loop`: quando `recursion_args is None` e `recursion_prefix` termina com um `ast.If`, usar `transform_recursive_calls` para construir o corpo do `while` em vez de retornar `tree` (lista) que causa o crash em `ast.fix_missing_locations` (cobre `binary_search`, `quickselect`, `partition_Hoare_rec`)

- [ ] Corrigir `convert_tail_recursive_to_loop`: mover `*initial_block` para **depois** da atribuição dos novos parâmetros no corpo do `while`, para que variáveis derivadas sejam recalculadas com os valores atualizados antes da próxima checagem da condição (cobre `linear_search_tail`)
