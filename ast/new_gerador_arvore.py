import ast

def is_tail_recursive(func):
    print("FUNC: ", ast.dump(func, indent=4))
    if not isinstance(func, ast.FunctionDef):
        return False
    if not func.body:
        return False
    #melhorar abrangência de casos identificados como recursivos de cauda
    last_stmt = func.body[-1]
    return isinstance(last_stmt, ast.Return) and isinstance(last_stmt.value, ast.Call) and last_stmt.value.func.id == func.name

def optimize_tail_recursive(func): 

    new_body = []
    for stmt in func.body[:-1]:
        new_body.append(stmt)
    last_stmt = func.body[-1]
    if isinstance(last_stmt, ast.Return):
        new_body.append(ast.Return(value=last_stmt.value))
    return ast.FunctionDef(name=func.name, args=func.args, body=new_body, decorator_list=func.decorator_list)


def tail_call_optimization(tree):
    if is_tail_recursive(tree.body[0]):
        optimized_func = optimize_tail_recursive(tree.body[0])

        return optimized_func
    else:
        return tree


with open('../recursive_functions/tail/factorial.py') as file: #/code_templates/assign.py
    source_code = file.read()

    tree = ast.parse(source_code)

    #print("\nCÓDIGO ORIGINAL: \n", ast.unparse(tree))

    #print("\nESTRUTURA ARVORE: \n", ast.dump(tree, indent=4))
    optimized_tree = tail_call_optimization(tree)

    #print("\nCÓDIGO OTIMIZADO: \n", ast.unparse(optimized_tree))