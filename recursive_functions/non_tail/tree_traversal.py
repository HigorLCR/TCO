"""
Funções recursivas não-tail para percorrer árvores binárias
"""

class TreeNode:
    """Nó de uma árvore binária"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def inorder_traversal(root, result=None):
    """
    Percorrimento in-order (esquerda, raiz, direita) não-tail.
    
    Args:
        root: nó raiz da árvore
        result: lista para armazenar os valores (inicializada automaticamente)
    
    Returns:
        Lista com os valores em ordem in-order
    """
    if result is None:
        result = []
    
    if root is not None:
        # Recursão não-tail: as operações acontecem após as chamadas recursivas
        inorder_traversal(root.left, result)
        result.append(root.value)
        inorder_traversal(root.right, result)
    
    return result

def preorder_traversal(root, result=None):
    """
    Percorrimento pre-order (raiz, esquerda, direita) não-tail.
    
    Args:
        root: nó raiz da árvore
        result: lista para armazenar os valores (inicializada automaticamente)
    
    Returns:
        Lista com os valores em ordem pre-order
    """
    if result is None:
        result = []
    
    if root is not None:
        # Recursão não-tail: as operações acontecem após as chamadas recursivas
        result.append(root.value)
        preorder_traversal(root.left, result)
        preorder_traversal(root.right, result)
    
    return result

def postorder_traversal(root, result=None):
    """
    Percorrimento post-order (esquerda, direita, raiz) não-tail.
    
    Args:
        root: nó raiz da árvore
        result: lista para armazenar os valores (inicializada automaticamente)
    
    Returns:
        Lista com os valores em ordem post-order
    """
    if result is None:
        result = []
    
    if root is not None:
        # Recursão não-tail: as operações acontecem após as chamadas recursivas
        postorder_traversal(root.left, result)
        postorder_traversal(root.right, result)
        result.append(root.value)
    
    return result

def tree_height(root):
    """
    Calcula a altura de uma árvore binária.
    
    Args:
        root: nó raiz da árvore
    
    Returns:
        Altura da árvore (número de níveis - 1)
    """
    if root is None:
        return -1  # Árvore vazia tem altura -1
    else:
        # Recursão não-tail: a operação max acontece após as chamadas recursivas
        return 1 + max(tree_height(root.left), tree_height(root.right))

# Teste das funções
if __name__ == "__main__":
    # Criar uma árvore binária de exemplo
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print("Testando percorrimentos de árvore:")
    print(f"Árvore criada:")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \\")
    print("    4   5")
    print()
    
    print(f"In-order: {inorder_traversal(root)}")
    print(f"Pre-order: {preorder_traversal(root)}")
    print(f"Post-order: {postorder_traversal(root)}")
    print(f"Altura da árvore: {tree_height(root)}")
    
    # Teste com árvore maior
    #        10
    #       /  \
    #      5    15
    #     / \   / \
    #    3   7 12 20
    #   /
    #  1
    big_root = TreeNode(10)
    big_root.left = TreeNode(5)
    big_root.right = TreeNode(15)
    big_root.left.left = TreeNode(3)
    big_root.left.right = TreeNode(7)
    big_root.right.left = TreeNode(12)
    big_root.right.right = TreeNode(20)
    big_root.left.left.left = TreeNode(1)
    
    print(f"\nÁrvore maior:")
    print(f"Altura: {tree_height(big_root)}")
    print(f"In-order: {inorder_traversal(big_root)}")
