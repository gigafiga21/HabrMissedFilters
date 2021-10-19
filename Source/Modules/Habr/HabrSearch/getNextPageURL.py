import Modules.Page as Page
import Modules.Habr.HabrURL as HabrURL 

def getNextPageURL(dom):
    links = dom.findAll(class_="tm-pagination__navigation-link")
    try:
        return Page.completeURL(links[1]['href'], HabrURL.DOMAIN)
    except:
        return None
