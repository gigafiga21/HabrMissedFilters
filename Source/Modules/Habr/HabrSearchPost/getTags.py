def getTags(postDom):
    tags = postDom.findAll(class_="tm-article-snippet__hubs-item")
    return list(map(lambda tag: tag.getText(), tags))
