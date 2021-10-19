import Modules.Habr.HabrArticle as HabrArticle
import Modules.Habr.HabrSearchPost as HabrSearchPost

def fromDom(postDom):
    title = HabrSearchPost.getTitle(postDom)
    url = HabrSearchPost.getURL(postDom)
    tags = HabrSearchPost.getTags(postDom)
    date = HabrSearchPost.getDate(postDom)
    rating = HabrSearchPost.getRating(postDom)
    return HabrArticle.create(title, url, tags, date, rating)
