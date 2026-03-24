def bst_search(T, key):
    if T == []:
        return None
    elif T[0] == key:
        return T[1] # return the root item
    elif key < T[0]:
        return bst_search(T[2], key) # search in left subtree
    else:
        return bst_search(T[3], key) # search in right subtree