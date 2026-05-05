def woodcutter(t, wood, lower, upper):
    middle_h = (lower + upper) // 2
    wood_collected = sum(max(0, tree - middle_h) for tree in t)

    if wood_collected == wood or lower == upper:
        return middle_h
    elif lower == upper - 1:
        if sum(max(0, tree - upper) for tree in t) >= wood:
            return upper
        else:
            return lower
    elif wood_collected > wood:
        return woodcutter(t, wood, middle_h, upper)
    else:
        return woodcutter(t, wood, lower, middle_h - 1)
