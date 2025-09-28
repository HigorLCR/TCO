class Node:
    """A node in a binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def find_min_element(node):
    _P = []
    _P.append((node, None, None, None, None, 0))
    while len(_P) > 0:
        node, left_min, right_min, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            '\n    Recursively finds the minimum element in a binary tree.\n\n    Args:\n        node: The root node of the binary tree.\n\n    Returns:\n        The minimum value in the tree.\n    '
        if _s in [] or (_s == 0 and node is None):
            if _s == 0:
                _r = float('inf')
                _s = -1
        if _s == 0:
            _P.append((node, left_min, right_min, _r1, _r2, 1))
            _P.append((node.left, None, None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            left_min = _r1
        if _s == 0:
            _P.append((node, left_min, right_min, _r1, _r2, 2))
            _P.append((node.right, None, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            right_min = _r2
        if _s == 0:
            _r = min(node.value, left_min, right_min)
            _s = -1
    return _r
root = Node(4)
root.left = Node(2)
root.right = Node(6)
root.left.left = Node(1)
root.left.right = Node(3)
root.right.left = Node(5)
root.right.right = Node(7)
root.right.right.right = Node(0)
minimum_value = find_min_element(root)
print(f'The minimum element in the binary tree is: {minimum_value}')