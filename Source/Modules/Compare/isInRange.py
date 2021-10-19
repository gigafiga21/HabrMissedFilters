def isInRange(checking, min, max):
    if checking == None:
        return False
    return (min == None or min <= checking) and (max == None or max >= checking)
