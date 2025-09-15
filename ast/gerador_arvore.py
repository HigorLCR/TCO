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

def convert_tail_recursive_to_loop(tree, func_name):
    recursive_if = find_recursive_if_block(tree, func_name)

    #arguments da função
    signature_args = find_signature_args(tree, func_name)

    #argumentos passados na recursão
    recursion_args = find_recursion_args(recursive_if["recursive_block"], func_name)

    # Extrai a condição do if
    condition = recursive_if["stop_condition"]
    
    # Extrai o corpo do if (bloco verdadeiro)
    stop_condition_block = recursive_if["stop_condition_block"]
    
    # Extrai o corpo do else (bloco falso), se existir
    false_block = recursive_if["recursive_block"]

    last_stmt = false_block[-1]
    if (
        isinstance(last_stmt, ast.Return) and 
        isinstance(last_stmt.value, ast.Call) and 
        isinstance(last_stmt.value.func, ast.Name) and
        last_stmt.value.func.id == func_name
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
                            ast.Name(id=signature_args.args[0].arg, ctx=ast.Store()),
                            ast.Name(id=signature_args.args[1].arg, ctx=ast.Store())
                        ],
                        ctx=ast.Store()
                    )],
                    value=ast.Tuple(
                        elts=[
                            recursion_args[0],
                            recursion_args[1]
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
    return tree

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

def find_recursion_args(nodes, func_name):
    for stmt in nodes:
        if isinstance(stmt, ast.Return):
            for arg in ast.walk(stmt):
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                    if arg.func.id == func_name:
                        return arg.args
    return None

def find_signature_args(nodes, func_name):
    for stmt in nodes:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == func_name:
            return stmt.args
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
                    "recursive_block": stmt.body, 
                    "stop_condition_block": stmt.orelse, 
                    "stop_condition": stmt.test 
                }
            elif is_false_block_recursive:  
                return { 
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


    