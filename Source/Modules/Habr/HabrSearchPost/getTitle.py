def getTitle(postDom):
    return postDom.find(class_="tm-article-snippet__title").getText()
