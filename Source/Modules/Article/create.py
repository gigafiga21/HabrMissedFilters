class ArticleTitleError(Exception):
    pass

class ArticleURLError(Exception):
    pass

def create(title, url, tags, date, rating, source):
    if not isinstance(url, str):
        raise ArticleURLError
    if not isinstance(title, str):
        raise ArticleTitleError
    return {
        'title': title,
        'url': url,
        'tags': tags if isinstance(tags, list) else [],
        'date': date,
        'rating': rating if isinstance(rating, int) else None,
        'source': source
    }
