def getAuthor(postDom):
    return postDom.find(class_="tm-user-info__username").getText()
