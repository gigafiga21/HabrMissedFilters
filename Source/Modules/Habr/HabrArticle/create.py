import Modules.Article as Article

def create(*articleArgs):
    return Article.create(*articleArgs, 'Habrahabr')
