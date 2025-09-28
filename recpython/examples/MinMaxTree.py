class Node:
    """A node in a binary tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def maxmin(T):
    """
    Finds the minimum and maximum elements in a binary tree T.

    Args:
        T: The root node of the binary tree.

    Returns:
        A tuple (min_val, max_val) representing the minimum and maximum
        elements in the tree. Returns (None, None) if the tree is empty.
    """
    if T is None:
        return (None, None)

    # Initialize min and max with the root's value
    min_val = T.value
    max_val = T.value

    # Recursively find min and max in the left and right subtrees
    left_min, left_max = maxmin(T.left)
    right_min, right_max = maxmin(T.right)

    # Update min_val with the minimum from the left subtree
    if left_min is not None:
        min_val = min(min_val, left_min)

    # Update max_val with the maximum from the left subtree
    if left_max is not None:
        max_val = max(max_val, left_max)

    # Update min_val with the minimum from the right subtree
    if right_min is not None:
        min_val = min(min_val, right_min)

    # Update max_val with the maximum from the right subtree
    if right_max is not None:
        max_val = max(max_val, right_max)

    return (min_val, max_val)

# Example Usage:
# Create a sample binary tree
# Nível 1 - Raiz da árvore
root = Node(10)

# Nível 2 - Filhos diretos da raiz
root.left = Node(5)      # Subárvore esquerda
root.right = Node(15)    # Subárvore direita

# Nível 3 - Netos da raiz
root.left.left = Node(3)     # Extremidade esquerda
root.left.right = Node(7)    # Centro esquerdo
root.right.left = Node(12)   # Centro direito
root.right.right = Node(18)  # Extremidade direita

# Nível 4 - Bisnetos da raiz
root.right.right.right = Node(20)  # Extremidade direita superior
root.right.right.left = Node(20)   # Extremidade direita inferior
root.right.left.right = Node(23)   # Centro direito superior
root.right.left.left = Node(23)    # Centro direito inferior
root.left.right.left = Node(30)    # Centro esquerdo superior
root.left.right.right = Node(30)   # Centro esquerdo inferior
root.left.left.right = Node(40)    # Extremidade esquerda superior
root.left.left.left = Node(40)     # Extremidade esquerda inferior
root.right.right.right.left = Node(1)  # Nó especial esquerdo
root.right.right.right.right = Node(1) # Nó especial direito

# Nível 5 - Primeira expansão
root.left.left.left.left = Node(45)  # Extremidade esquerda superior
root.left.left.left.right = Node(50) # Extremidade esquerda central
root.left.left.right.left = Node(55) # Centro esquerdo superior
root.left.left.right.right = Node(60) # Centro esquerdo inferior
root.right.right.right.right.right = Node(25) # Extremidade direita superior
root.right.right.right.right.left = Node(35)  # Extremidade direita central
root.right.right.right.left.right = Node(70)  # Centro direito superior
root.right.right.right.left.left = Node(80)   # Centro direito inferior

# Nível 6 - Segunda expansão
root.left.right.left.left = Node(90)    # Centro esquerdo superior
root.left.right.left.right = Node(95)   # Centro esquerdo central
root.right.left.right.left = Node(105)  # Centro direito superior
root.right.left.right.right = Node(110) # Centro direito inferior

# Nível 7 - Terceira expansão
root.left.left.left.left.left = Node(45)  # Extremidade esquerda superior
root.left.left.left.left.right = Node(50) # Extremidade esquerda central
root.left.left.left.right.left = Node(55) # Centro esquerdo superior
root.left.left.left.right.right = Node(60) # Centro esquerdo inferior
root.left.left.right.left.left = Node(65) # Extremidade esquerda superior
root.left.left.right.left.right = Node(70) # Extremidade esquerda central
root.left.left.right.right.left = Node(75) # Centro esquerdo superior
root.left.left.right.right.right = Node(80) # Centro esquerdo inferior

# Nível 8 - Quarta expansão
root.right.right.right.right.right.right = Node(25) # Extremidade direita superior
root.right.right.right.right.right.left = Node(35)  # Extremidade direita central
root.right.right.right.right.right.right = Node(85) # Extremidade direita superior
root.right.right.right.right.right.left = Node(90)  # Extremidade direita central
root.right.right.right.right.right.right = Node(95) # Extremidade direita superior
root.right.right.right.right.right.left = Node(100) # Extremidade direita central
root.right.right.right.right.right.right = Node(105) # Extremidade direita superior
root.right.right.right.right.right.left = Node(110) # Extremidade direita central

# Nível 9 - Quinta expansão
root.left.right.left.left.left = Node(115)  # Extremidade esquerda superior
root.left.right.left.left.right = Node(120) # Extremidade esquerda central
root.left.right.left.right.left = Node(125) # Centro esquerdo superior
root.left.right.left.right.right = Node(130) # Centro esquerdo inferior
root.right.left.right.left.left = Node(135)  # Extremidade direita superior
root.right.left.right.left.right = Node(140) # Extremidade direita central
root.right.left.right.right.left = Node(145) # Centro direito superior
root.right.left.right.right.right = Node(150) # Centro direito inferior

# Nível 10 - Sexta expansão
root.left.left.left.left.left.left = Node(155)  # Extremidade esquerda superior
root.left.left.left.left.left.right = Node(160) # Extremidade esquerda central
root.left.left.left.left.right.left = Node(165) # Centro esquerdo superior
root.left.left.left.left.right.right = Node(170) # Centro esquerdo inferior
root.right.right.right.right.right.right.right = Node(175) # Extremidade direita superior
root.right.right.right.right.right.right.left = Node(180) # Extremidade direita central
root.right.right.right.right.right.right.right = Node(185) # Extremidade direita superior
root.right.right.right.right.right.right.left = Node(190) # Extremidade direita central

# Nível 11 - Sétima expansão
root.left.left.left.left.left.left.left = Node(195)  # Extremidade esquerda superior
root.left.left.left.left.left.left.right = Node(200) # Extremidade esquerda central
root.left.left.left.left.left.right.left = Node(205) # Centro esquerdo superior
root.left.left.left.left.left.right.right = Node(210) # Centro esquerdo inferior
root.right.right.right.right.right.right.right.right = Node(215) # Extremidade direita superior
root.right.right.right.right.right.right.right.left = Node(220) # Extremidade direita central
root.right.right.right.right.right.right.right.right = Node(225) # Extremidade direita superior
root.right.right.right.right.right.right.right.left = Node(230) # Extremidade direita central

# Nível 12 - Oitava expansão
root.left.left.left.left.left.left.left.left = Node(235)  # Extremidade esquerda superior
root.left.left.left.left.left.left.left.right = Node(240) # Extremidade esquerda central
root.left.left.left.left.left.left.right.left = Node(245) # Centro esquerdo superior
root.left.left.left.left.left.left.right.right = Node(250) # Centro esquerdo inferior
root.left.left.left.left.left.right.left.left = Node(255) # Extremidade esquerda superior
root.left.left.left.left.left.right.left.right = Node(260) # Extremidade esquerda central
root.left.left.left.left.left.right.right.left = Node(265) # Centro esquerdo superior
root.left.left.left.left.left.right.right.right = Node(270) # Centro esquerdo inferior

# Nível 13 - Nona expansão
root.right.right.right.right.right.right.right.right.right = Node(275) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.left = Node(280) # Extremidade direita central
root.right.right.right.right.right.right.right.right.right = Node(285) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.left = Node(290) # Extremidade direita central
root.right.right.right.right.right.right.right.right.right = Node(295) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.left = Node(300) # Extremidade direita central
root.right.right.right.right.right.right.right.right.right = Node(305) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.left = Node(310) # Extremidade direita central

# Nível 14 - Décima expansão
root.left.right.left.left.left.left = Node(315)  # Extremidade esquerda superior
root.left.right.left.left.left.right = Node(320) # Extremidade esquerda central
root.left.right.left.left.right.left = Node(325) # Centro esquerdo superior
root.left.right.left.left.right.right = Node(330) # Centro esquerdo inferior
root.right.left.right.left.left.left = Node(335)  # Extremidade direita superior
root.right.left.right.left.left.right = Node(340) # Extremidade direita central
root.right.left.right.left.right.left = Node(345) # Centro direito superior
root.right.left.right.left.right.right = Node(350) # Centro direito inferior

# Nível 15 - Décima primeira expansão
root.left.left.left.left.left.left.left.left.left = Node(355)  # Extremidade esquerda superior
root.left.left.left.left.left.left.left.left.right = Node(360) # Extremidade esquerda central
root.left.left.left.left.left.left.left.right.left = Node(365) # Centro esquerdo superior
root.left.left.left.left.left.left.left.right.right = Node(370) # Centro esquerdo inferior
root.right.right.right.right.right.right.right.right.right.right = Node(375) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.right.left = Node(380) # Extremidade direita central
root.right.right.right.right.right.right.right.right.right.right = Node(385) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.right.left = Node(390) # Extremidade direita central

# Nível 16 - Décima segunda expansão
root.left.left.left.left.left.left.left.left.left.left = Node(395)  # Extremidade esquerda superior
root.left.left.left.left.left.left.left.left.left.right = Node(400) # Extremidade esquerda central
root.left.left.left.left.left.left.left.left.right.left = Node(405) # Centro esquerdo superior
root.left.left.left.left.left.left.left.left.right.right = Node(410) # Centro esquerdo inferior
root.right.right.right.right.right.right.right.right.right.right.right = Node(415) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.right.right.left = Node(420) # Extremidade direita central
root.right.right.right.right.right.right.right.right.right.right.right = Node(425) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.right.right.left = Node(430) # Extremidade direita central

# Nível 17 - Décima terceira expansão
root.left.left.left.left.left.left.left.left.left.left.left = Node(435)  # Extremidade esquerda superior
root.left.left.left.left.left.left.left.left.left.left.right = Node(440) # Extremidade esquerda central
root.left.left.left.left.left.left.left.left.left.right.left = Node(445) # Centro esquerdo superior
root.left.left.left.left.left.left.left.left.left.right.right = Node(450) # Centro esquerdo inferior
root.right.right.right.right.right.right.right.right.right.right.right.right = Node(455) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.right.right.right.left = Node(460) # Extremidade direita central
root.right.right.right.right.right.right.right.right.right.right.right.right = Node(465) # Extremidade direita superior
root.right.right.right.right.right.right.right.right.right.right.right.left = Node(470) # Extremidade direita central


# Find the min and max elements
min_val, max_val = maxmin(root)
print(f"The minimum element is: {min_val}")
print(f"The maximum element is: {max_val}")

# Example with a single node
single_node_tree = Node(100)
min_val_single, max_val_single = maxmin(single_node_tree)
print(f"The minimum element in single node tree is: {min_val_single}")
print(f"The maximum element in single node tree is: {max_val_single}")

# Example with an empty tree
empty_tree = None
min_val_empty, max_val_empty = maxmin(empty_tree)
print(f"The minimum element in an empty tree is: {min_val_empty}")
print(f"The maximum element in an empty tree is: {max_val_empty}")