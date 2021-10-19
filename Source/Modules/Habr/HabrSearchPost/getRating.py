from re import match

def getRating(postDom):
    rating = postDom.find(class_="tm-votes-meter__value").getText()
    if match("^[\+-]?\d+$", rating):
        return int(rating)
    return None
