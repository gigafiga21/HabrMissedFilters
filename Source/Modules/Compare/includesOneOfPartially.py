def includesOneOfPartially(array, toFind):
    if len(toFind) == 0:
        return True

    for query in toFind:
        if len([s for s in array if query in s]) > 0:
            return True

    return False
