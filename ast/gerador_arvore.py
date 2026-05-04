import ast
import argparse

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

#Classe para visitar todos os nós da árvore de maneira completa
class FullVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []

    def print_type(self, node):
        print("Visiting node:", type(node))
        super().print_type(node)

    def generic_visit(self, node):
        self.nodes.append(node)
        super().generic_visit(node)

    def clear_nodes(self):
        self.nodes = []

    def get_nodes(self):
        return self.nodes

def flatten_elif_chain(recursive_block, func_name):
    conditions = []
    base_blocks = []
    current = recursive_block

    while True:
        if len(current) == 1 and isinstance(current[0], ast.If):
            node = current[0]
            false_recursive = any(is_function_recursive(n, func_name) for n in node.orelse)
            true_recursive = any(is_function_recursive(n, func_name) for n in node.body)

            if false_recursive:
                conditions.append(node.test)
                base_blocks.append(node.body)
                current = node.orelse
            elif true_recursive:
                conditions.append(ast.UnaryOp(op=ast.Not(), operand=node.test))
                base_blocks.append(node.orelse)
                current = node.body
            else:
                return conditions, base_blocks, None, []
        else:
            args = find_recursion_args(current, func_name)
            prefix = [s for s in current if not isinstance(s, ast.Return)]
            return conditions, base_blocks, args, prefix

def build_post_loop_block(conditions, base_blocks):
    if len(conditions) == 1:
        return base_blocks[0]
    orelse = base_blocks[-1]
    for cond, block in zip(reversed(conditions[:-1]), reversed(base_blocks[:-1])):
        orelse = [ast.If(test=cond, body=block, orelse=orelse)]
    return orelse

def convert_tail_recursive_to_loop(tree, func_name):
    recursive_if = find_recursive_if_block(tree, func_name)
    initial_block = find_initial_block(tree, recursive_if, func_name)
    signature = find_signature(tree, func_name)

    false_block = recursive_if["recursive_block"]
    first_condition = recursive_if["stop_condition"]
    first_base_block = recursive_if["stop_condition_block"]

    elif_conditions, elif_base_blocks, recursion_args, prefix = flatten_elif_chain(false_block, func_name)

    if recursion_args is None:
        return tree

    all_conditions = [first_condition] + elif_conditions
    all_base_blocks = [first_base_block] + elif_base_blocks

    if len(all_conditions) == 1:
        while_test = ast.UnaryOp(op=ast.Not(), operand=all_conditions[0])
    else:
        while_test = ast.UnaryOp(
            op=ast.Not(),
            operand=ast.BoolOp(op=ast.Or(), values=all_conditions)
        )

    while_loop = ast.While(
        test=while_test,
        body=[
            *initial_block,
            *prefix,
            ast.Assign(
                targets=[ast.Tuple(
                    elts=[ast.Name(arg.arg, ctx=ast.Store()) for arg in signature.args.args],
                    ctx=ast.Store()
                )],
                value=ast.Tuple(
                    elts=list(recursion_args),
                    ctx=ast.Load()
                )
            )
        ],
        orelse=[]
    )

    post_loop = build_post_loop_block(all_conditions, all_base_blocks)
    signature.body = [*initial_block, while_loop, *post_loop]
    return ast.Module(body=[signature], type_ignores=[])

def is_function_tail_recursive(func_node, func_name=None):
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
def is_function_recursive(func_node, func_name=None):
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

def find_initial_block(nodes, recursive_if, func_name):
    initial_block = []
    for node in nodes:
        if isinstance(node, ast.Module):
            for  stmt_1 in node.body:
                if isinstance(stmt_1, ast.FunctionDef) and stmt_1.name == func_name:
                    for stmt_2 in stmt_1.body:
                        if ast.dump(recursive_if['if'], include_attributes=True) != ast.dump(stmt_2, include_attributes=True):
                            initial_block.append(stmt_2)
    return initial_block

def find_recursion_args(nodes, func_name):
    for stmt in nodes:
        if isinstance(stmt, ast.Return):
            for arg in ast.walk(stmt):
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                    if arg.func.id == func_name:
                        return arg.args
    return None

def find_signature(nodes, func_name):
    for stmt in nodes:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == func_name:
            return stmt
    return None

def find_recursive_if_block(nodes, func_name):
    for stmt in nodes:
        if isinstance(stmt, ast.If):
            is_true_block_recursive = False 
            is_false_block_recursive = False

            for node in stmt.body:
                if is_function_recursive(node, func_name):
                    is_true_block_recursive = True
            for node in stmt.orelse:
                if is_function_recursive(node, func_name):
                    is_false_block_recursive = True
            
            if is_true_block_recursive:
                return { 
                    "if": stmt,
                    "recursive_block": stmt.body, 
                    "stop_condition_block": stmt.orelse, 
                    "stop_condition": stmt.test 
                }
            elif is_false_block_recursive:  
                return { 
                    "if": stmt,
                    "recursive_block": stmt.orelse, 
                    "stop_condition_block": stmt.body, 
                    "stop_condition": stmt.test 
                }
    return None

    
parser = argparse.ArgumentParser()
parser.add_argument('arquivo', help='Nome do arquivo de código fonte (dentro da pasta tail)')
parser.add_argument('nome_funcao', help='Nome da função a ser analisada')
parser.add_argument('-dump', action='store_true', help='Exibe detalhes da análise')
parser.add_argument('-nt', action='store_true', help='Indica que a função não é de cauda')
args = parser.parse_args()

source_code = ""
with open(f'../recursive_functions/{'non_tail' if args.nt else 'tail'}/{args.arquivo}') as file:
    source_code = file.read()
    tree = ast.parse(source_code)
    visitor = FullVisitor()

    #coleta todos os nós da árvore e armazena em nodes
    visitor.generic_visit(tree)
    nodes = visitor.get_nodes()
    visitor.clear_nodes()

    func_name = args.nome_funcao
    
    isRecursive = is_function_recursive(tree, func_name)
    isTail = is_function_tail_recursive(tree, func_name)


    new_code = convert_tail_recursive_to_loop(nodes, func_name)
    ast.fix_missing_locations(new_code)

    if args.dump:
        print("Código original: \n", ast.unparse(tree))

        print("\nNovo código: \n", ast.unparse(new_code))

        print("\nÁrvore sintática: \n", ast.dump(tree, indent=4)) 
        
        print("\nNova árvore sintática: \n", ast.dump(new_code, indent=4))

with open(f'output_{args.arquivo}', 'w') as file:
    file.write(ast.unparse(new_code))