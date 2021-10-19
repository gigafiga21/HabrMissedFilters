from urllib.parse import quote_plus as encodeURL

def getSearchPageURL(query):
    return "https://habr.com/ru/search/?q=" + encodeURL(query) + "&target_type=posts&order=relevance"
