class Node:
    """A node in a binary tree."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def maxmin(T):
    _P = []
    _P.append((T, None, None, None, None, None, None, None, None, 0))
    while len(_P) > 0:
        T, min_val, max_val, left_min, left_max, right_min, right_max, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            '\n    Finds the minimum and maximum elements in a binary tree T.\n\n    Args:\n        T: The root node of the binary tree.\n\n    Returns:\n        A tuple (min_val, max_val) representing the minimum and maximum\n        elements in the tree. Returns (None, None) if the tree is empty.\n    '
        if _s in [] or (_s == 0 and T is None):
            if _s == 0:
                _r = (None, None)
                _s = -1
        if _s == 0:
            min_val = T.value
        if _s == 0:
            max_val = T.value
        if _s == 0:
            _P.append((T, min_val, max_val, left_min, left_max, right_min, right_max, _r1, _r2, 1))
            _P.append((T.left, None, None, None, None, None, None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            left_min, left_max = _r1
        if _s == 0:
            _P.append((T, min_val, max_val, left_min, left_max, right_min, right_max, _r1, _r2, 2))
            _P.append((T.right, None, None, None, None, None, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            right_min, right_max = _r2
        if _s in [] or (_s == 0 and left_min is not None):
            if _s == 0:
                min_val = min(min_val, left_min)
        if _s in [] or (_s == 0 and left_max is not None):
            if _s == 0:
                max_val = max(max_val, left_max)
        if _s in [] or (_s == 0 and right_min is not None):
            if _s == 0:
                min_val = min(min_val, right_min)
        if _s in [] or (_s == 0 and right_max is not None):
            if _s == 0:
                max_val = max(max_val, right_max)
        if _s == 0:
            _r = (min_val, max_val)
            _s = -1
    return _r
root = Node(10)
root.left = Node(5)
root.right = Node(15)
root.left.left = Node(3)
root.left.right = Node(7)
root.right.left = Node(12)
root.right.right = Node(18)
root.right.right.right = Node(20)
root.right.right.left = Node(20)
root.right.left.right = Node(23)
root.right.left.left = Node(23)
root.left.right.left = Node(30)
root.left.right.right = Node(30)
root.left.left.right = Node(40)
root.left.left.left = Node(40)
root.right.right.right.left = Node(1)
root.right.right.right.right = Node(1)
root.left.left.left.left = Node(45)
root.left.left.left.right = Node(50)
root.left.left.right.left = Node(55)
root.left.left.right.right = Node(60)
root.right.right.right.right.right = Node(25)
root.right.right.right.right.left = Node(35)
root.right.right.right.left.right = Node(70)
root.right.right.right.left.left = Node(80)
root.left.right.left.left = Node(90)
root.left.right.left.right = Node(95)
root.right.left.right.left = Node(105)
root.right.left.right.right = Node(110)
root.left.left.left.left.left = Node(45)
root.left.left.left.left.right = Node(50)
root.left.left.left.right.left = Node(55)
root.left.left.left.right.right = Node(60)
root.left.left.right.left.left = Node(65)
root.left.left.right.left.right = Node(70)
root.left.left.right.right.left = Node(75)
root.left.left.right.right.right = Node(80)
root.right.right.right.right.right.right = Node(25)
root.right.right.right.right.right.left = Node(35)
root.right.right.right.right.right.right = Node(85)
root.right.right.right.right.right.left = Node(90)
root.right.right.right.right.right.right = Node(95)
root.right.right.right.right.right.left = Node(100)
root.right.right.right.right.right.right = Node(105)
root.right.right.right.right.right.left = Node(110)
root.left.right.left.left.left = Node(115)
root.left.right.left.left.right = Node(120)
root.left.right.left.right.left = Node(125)
root.left.right.left.right.right = Node(130)
root.right.left.right.left.left = Node(135)
root.right.left.right.left.right = Node(140)
root.right.left.right.right.left = Node(145)
root.right.left.right.right.right = Node(150)
root.left.left.left.left.left.left = Node(155)
root.left.left.left.left.left.right = Node(160)
root.left.left.left.left.right.left = Node(165)
root.left.left.left.left.right.right = Node(170)
root.right.right.right.right.right.right.right = Node(175)
root.right.right.right.right.right.right.left = Node(180)
root.right.right.right.right.right.right.right = Node(185)
root.right.right.right.right.right.right.left = Node(190)
root.left.left.left.left.left.left.left = Node(195)
root.left.left.left.left.left.left.right = Node(200)
root.left.left.left.left.left.right.left = Node(205)
root.left.left.left.left.left.right.right = Node(210)
root.right.right.right.right.right.right.right.right = Node(215)
root.right.right.right.right.right.right.right.left = Node(220)
root.right.right.right.right.right.right.right.right = Node(225)
root.right.right.right.right.right.right.right.left = Node(230)
root.left.left.left.left.left.left.left.left = Node(235)
root.left.left.left.left.left.left.left.right = Node(240)
root.left.left.left.left.left.left.right.left = Node(245)
root.left.left.left.left.left.left.right.right = Node(250)
root.left.left.left.left.left.right.left.left = Node(255)
root.left.left.left.left.left.right.left.right = Node(260)
root.left.left.left.left.left.right.right.left = Node(265)
root.left.left.left.left.left.right.right.right = Node(270)
root.right.right.right.right.right.right.right.right.right = Node(275)
root.right.right.right.right.right.right.right.right.left = Node(280)
root.right.right.right.right.right.right.right.right.right = Node(285)
root.right.right.right.right.right.right.right.right.left = Node(290)
root.right.right.right.right.right.right.right.right.right = Node(295)
root.right.right.right.right.right.right.right.right.left = Node(300)
root.right.right.right.right.right.right.right.right.right = Node(305)
root.right.right.right.right.right.right.right.right.left = Node(310)
root.left.right.left.left.left.left = Node(315)
root.left.right.left.left.left.right = Node(320)
root.left.right.left.left.right.left = Node(325)
root.left.right.left.left.right.right = Node(330)
root.right.left.right.left.left.left = Node(335)
root.right.left.right.left.left.right = Node(340)
root.right.left.right.left.right.left = Node(345)
root.right.left.right.left.right.right = Node(350)
root.left.left.left.left.left.left.left.left.left = Node(355)
root.left.left.left.left.left.left.left.left.right = Node(360)
root.left.left.left.left.left.left.left.right.left = Node(365)
root.left.left.left.left.left.left.left.right.right = Node(370)
root.right.right.right.right.right.right.right.right.right.right = Node(375)
root.right.right.right.right.right.right.right.right.right.left = Node(380)
root.right.right.right.right.right.right.right.right.right.right = Node(385)
root.right.right.right.right.right.right.right.right.right.left = Node(390)
root.left.left.left.left.left.left.left.left.left.left = Node(395)
root.left.left.left.left.left.left.left.left.left.right = Node(400)
root.left.left.left.left.left.left.left.left.right.left = Node(405)
root.left.left.left.left.left.left.left.left.right.right = Node(410)
root.right.right.right.right.right.right.right.right.right.right.right = Node(415)
root.right.right.right.right.right.right.right.right.right.right.left = Node(420)
root.right.right.right.right.right.right.right.right.right.right.right = Node(425)
root.right.right.right.right.right.right.right.right.right.right.left = Node(430)
root.left.left.left.left.left.left.left.left.left.left.left = Node(435)
root.left.left.left.left.left.left.left.left.left.left.right = Node(440)
root.left.left.left.left.left.left.left.left.left.right.left = Node(445)
root.left.left.left.left.left.left.left.left.left.right.right = Node(450)
root.right.right.right.right.right.right.right.right.right.right.right.right = Node(455)
root.right.right.right.right.right.right.right.right.right.right.right.left = Node(460)
root.right.right.right.right.right.right.right.right.right.right.right.right = Node(465)
root.right.right.right.right.right.right.right.right.right.right.right.left = Node(470)
min_val, max_val = maxmin(root)
print(f'The minimum element is: {min_val}')
print(f'The maximum element is: {max_val}')
single_node_tree = Node(100)
min_val_single, max_val_single = maxmin(single_node_tree)
print(f'The minimum element in single node tree is: {min_val_single}')
print(f'The maximum element in single node tree is: {max_val_single}')
empty_tree = None
min_val_empty, max_val_empty = maxmin(empty_tree)
print(f'The minimum element in an empty tree is: {min_val_empty}')
print(f'The maximum element in an empty tree is: {max_val_empty}')