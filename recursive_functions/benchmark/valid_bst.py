import io

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class _Empty:
    pass


type NodeOrNone = TreeNode | None


def is_valid_bst(node, lo=None, hi=None):
    if node is None:
        return True
    if lo is not None and node.val <= lo:
        return False
    if hi is not None and node.val >= hi:
        return False
    return (is_valid_bst(node.left, lo, node.val) and
            is_valid_bst(node.right, node.val, hi))


def build_bst(values):
    if not values:
        return None
    mid = len(values) // 2
    node = TreeNode(values[mid])
    node.left = build_bst(values[:mid])
    node.right = build_bst(values[mid + 1:])
    return node


n = 1_000
root = build_bst(list(range(n)))

with io.StringIO() as buf:
    buf.write(f"root.val = {root.val}")

# --- benchmark ---
def chamada():
    return is_valid_bst(root)
