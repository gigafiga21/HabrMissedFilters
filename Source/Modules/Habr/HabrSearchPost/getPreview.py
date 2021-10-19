def getPreview(postDom):
    return postDom.find(class_="article-formatted-body").getText()
