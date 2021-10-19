import Modules.Page as Page
import Modules.Habr.HabrURL as HabrURL 

def getURL(postDom):
    link = postDom.find(class_="tm-article-snippet__title-link")
    try:
        return Page.completeURL(link['href'], HabrURL.DOMAIN)
    except:
        return None
