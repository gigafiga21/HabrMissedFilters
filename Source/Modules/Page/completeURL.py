from re import match

def completeURL(url, domain):
    if match("^https?://", url):
        return url
    elif url[0] == "/":
        return domain + url
    else:
        return None
