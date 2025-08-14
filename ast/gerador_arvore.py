import ast

#pesquisar se instanciação pos-modificação é possivel ou é necessario criar um "clone" da arvore

def converter_condicional_recursao_cauda(stmt, func):
    if isinstance(stmt, ast.If):
        # Extrai a condição do if
        condition = stmt.test
        
        # Extrai o corpo do if (bloco verdadeiro)
        true_block = stmt.body
        
        # Extrai o corpo do else (bloco falso), se existir
        false_block = stmt.orelse if stmt.orelse else []
        last_stmt = false_block[-1]
        if (
            isinstance(last_stmt, ast.Return) and 
            isinstance(last_stmt.value, ast.Call) and 
            isinstance(last_stmt.value.func, ast.Name) and
            last_stmt.value.func.id == func.name
        ):
            while_loop = ast.While(
                test=ast.UnaryOp(
                    op = ast.Not(),
                    operand=condition
                ),
                body=[
                    false_block[:-1], 
                    ast.Assign(
                        targets=[ast.Tuple(
                            elts=[
                                ast.Name(id=func.args.args[0].arg, ctx=ast.Store()),
                                ast.Name(id=func.args.args[1].arg, ctx=ast.Store())
                            ],
                            ctx=ast.Store()
                        )],
                        value=ast.Tuple(
                            elts=[
                                false_block[-1].value.args[0],
                                false_block[-1].value.args[1]
                            ],
                            ctx=ast.Load()
                        )
                    )
                ],
                orelse=[] #false_block
            )

            return ast.Module(
                body=[while_loop, true_block],
                type_ignores=[]
            )
        
        # Cria a estrutura de atribuição para o bloco verdadeiro
    

        # Cria a estrutura while com a condição e o corpo verdadeiro
    return stmt

#Criar função que detecta se uma recursão é de cauda
def is_tail_recursive(func_node):
    """
    Detecta se uma função é recursiva de cauda.
    :param func_node: ast.FunctionDef
    :return: bool
    """
    func_name = func_node.name
    for stmt in func_node.body:
        print("STMT: ", stmt)
        # Procura por um return no final do corpo da função
        if isinstance(stmt, ast.Return):
            # Verifica se o return é uma chamada à própria função
            if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name):
                if stmt.value.func.id == func_name:
                    return True
    return False

class UpperCaseFunctionNames(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.name = node.name+"_tco"
        self.generic_visit(node)
        return node
    
    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node.value = node.value.upper()
        return node
    
    def visit_Return(self, node):
        node.value = ast.Constant(value="teste")
        return node

def encontrar_condicao_parada(node):
    if isinstance(node, ast.If):
        return node.test
    return None

with open('../recursive_functions/tail/factorial.py') as file:
    source_code = file.read()
    
    tree = ast.parse(source_code)
    print(ast.unparse(tree))
    # is_tail = is_tail_recursive(tree.body[0])

    # print("É recursiva? ", is_tail, tree.body[0])

    #print("Árvore sintática: ", ast.dump(tree, indent=4))
    new_code = converter_condicional_recursao_cauda(tree.body[0].body[0], tree.body[0])
    ast.fix_missing_locations(new_code)
    print("Novo código: ", ast.unparse(new_code))
    
    #print("BODY 1: ", tree.body[1].orelse)

    #condicao_parada=encontrar_condicao_parada(tree.body[0].body[0])

    #estrutura_while = ast.While(
    #    test=condicao_parada,
    #    body=[
    #        ast.Break()
    #    ],
    #    orelse=[]
    #)

    # transformer = UpperCaseFunctionNames()
    # tree = transformer.visit(tree)

    # print("Código fonte: ", source_code)
    # print("____________________________")
    #print("Árvore sintática: ", ast.dump(tree, indent=4))
    # print("____________________________")
    # print("Dados convertidos: ", ast.unparse(tree))
    