import requests

def good_request(req):
    """Prints the status code if it is not ok"""
    if req.status_code != 200:
        print(req.status_code)
        return False
    else:
        return True

def none_check(something, congress, year):
    if something is None:
        print("Error on "+str(congress)+"-"+str(year)+", aborting")
        return True
    else:
        return False

