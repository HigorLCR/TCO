import ast

with open('teste.py') as file:
    source_code = file.read()
    
    tree = ast.parse(source_code)

    print("Código fonte: ", source_code)

    print("Dados convertidos: ", ast.dump(tree, indent=4))