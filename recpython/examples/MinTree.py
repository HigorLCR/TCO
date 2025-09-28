class Node:
    """A node in a binary tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def find_min_element(node):
    """
    Recursively finds the minimum element in a binary tree.

    Args:
        node: The root node of the binary tree.

    Returns:
        The minimum value in the tree.
    """
    if node is None:
        return float('inf') # Return a very large value for an empty subtree

    # Recursively find the minimum in the left and right subtrees
    left_min = find_min_element(node.left)
    right_min = find_min_element(node.right)

    # Compare the current node's value with the minimums from the subtrees
    return min(node.value, left_min, right_min)

# Example usage:
# Create a sample binary tree
root = Node(4)
root.left = Node(2)
root.right = Node(6)
root.left.left = Node(1)
root.left.right = Node(3)
root.right.left = Node(5)
root.right.right = Node(7)
root.right.right.right = Node(0)

# Find the minimum element
minimum_value = find_min_element(root)
print(f"The minimum element in the binary tree is: {minimum_value}")