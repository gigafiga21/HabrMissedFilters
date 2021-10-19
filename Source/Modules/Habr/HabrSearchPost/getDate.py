from dateutil.parser import parse

def getDate(postDom):
    return parse(postDom.find("time")['datetime']).timestamp()
