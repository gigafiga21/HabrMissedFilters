from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

import Modules.Log

def load(url):
    try:
        return urlopen(url)
    except HTTPError as e:
        Log.out("The server returned an HTTP error", "ERROR")
        return None
    except URLError as e:
        Log.out("The server could not be found!", "ERROR")
        return None
    except:
        Log.out("Failed to open page\n URL: " + url, "ERROR")
        return None
