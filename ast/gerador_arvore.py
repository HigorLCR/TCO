import ast

def converter_condicional_recursao_cauda(stmt, func):
    if isinstance(stmt, ast.If):
        # Extrai a condição do if
        condition = find_stop_condition(stmt)
        
        # Extrai o corpo do if (bloco verdadeiro)
        stop_condition_block = find_stop_condition_return(stmt)
        
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
                body=[while_loop, stop_condition_block],
                type_ignores=[]
            )
    return stmt

def is_tail_recursive(func_node, func_name=None):
    """
    Detecta se uma função é recursiva de cauda.
    :param func_node: ast.FunctionDef, func_name: str
    :return: bool
    """
    for stmt in ast.walk(func_node):
        # Procura por um return no final do corpo da função
        if isinstance(stmt, ast.Return):
            # Verifica se o return é uma chamada à própria função
            if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name):
                if stmt.value.func.id == func_name:
                    return True
    return False

#verificar consistência
def is_recursive(func_node, func_name=None):
    
    """
    Detecta se uma função é recursiva.
    :param func_node: ast.FunctionDef, func_name: str
    :return: bool
    """
    for stmt in ast.walk(func_node):
        # Procura por um return no final do corpo da função
        if isinstance(stmt, ast.Return):
            for arg in ast.walk(stmt):
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                    if arg.func.id == func_name:
                        return True
    return False

#Fazer identificação pra garantir que é a condição de parada
def find_stop_condition(node):
    for stmt in ast.walk(node):
        if isinstance(stmt, ast.If):
            return stmt.test
    return None

#Fazer identificação pra garantir que é a condição de parada
def find_stop_condition_return(node):
    for stmt in ast.walk(node):
        if isinstance(stmt, ast.Return):
            if not (isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name) and stmt.value.func.id == node.name):
                return stmt.value
    return None

#checar
def find_recursive_block(node, func_name):
    for stmt in ast.walk(node):
        if isinstance(stmt, ast.If):
            for true_block in ast.walk(stmt):
                #identifica o bloco com recursão
                is_true_block_recursive = is_recursive(true_block, func_name)
                if is_true_block_recursive:
                    return true_block
    return None

class UpperCaseFunctionNames(ast.NodeTransformer):
    #adiciona "_tco" ao nome da função
    def visit_FunctionDef(self, node):
        node.name = node.name+"_tco"
        self.generic_visit(node)
        return node
    
    #converte strings para maiúsculas
    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node.value = node.value.upper()
        return node
    
    #substitui o valor de retorno por "teste"
    def visit_Return(self, node):
        node.value = ast.Constant(value="teste")
        return node

with open('../recursive_functions/tail/factorial.py') as file:
    source_code = file.read()
    
    tree = ast.parse(source_code)
    print(ast.unparse(tree))
    
    isRecursive = is_recursive(tree, func_name=tree.body[0].name)
    isTail = is_tail_recursive(tree, func_name=tree.body[0].name)
    print("É recursiva? \n", isRecursive, "\n")
    print("É tail? \n", isTail, "\n")
    
    print("Condição de parada: \n", ast.unparse(find_stop_condition(tree)), "\n")
    print("Corpo da condição de parada: \n", ast.unparse(find_stop_condition_return(tree)), "\n")
    #print("Estrutura da árvore: \n", ast.dump(tree.body[0], indent=4), "\n")


    #trabalhar nessa função
    #condicao_parada=encontrar_condicao_parada(tree.body[0].body[0])


    #print("STMT: ", ast.unparse(tree.body[0].body[0]))
    #print("FUNC: ", ast.unparse(tree.body[0]))
    #new_code = converter_condicional_recursao_cauda(tree.body[0].body[0], tree.body[0])
    #ast.fix_missing_locations(new_code)
    #print("\nNovo código: \n", ast.unparse(new_code))


    #print("Árvore sintática: ", ast.dump(tree, indent=4)) #visualizar estrutura da árvore sintática
    # print("Dados convertidos: ", ast.unparse(tree)) #visualizar código convertido
    