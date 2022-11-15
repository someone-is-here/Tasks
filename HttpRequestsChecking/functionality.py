import urlextract
import requests

extractor = urlextract.URLExtract()

"""
Function gets string for checking and monitors if it is a link
"""


def check_is_request(url):
    try:
        r = requests.head(url, verify=False, timeout=5)
        return True
    except:
        return False


"""
Function gets string for checking(url) and http request then checks if the request is available
Returns tuple with (Boolean(if request is available), status_code)
"""


def check_http_request(url, http_request):
    result = requests.request(http_request, url)

    if result.status_code != 405:
        return True, result.status_code

    return False, 405


"""
Function gets string for checking and checks all http request
Returns dict with requests and codes if request where available
"""


def check_all_http_requests(str_for_check):
    result_of_checking = {}

    list_with_requests = ["GET", "POST",
                          "PUT", "PATCH",
                          "HEAD", "DELETE",
                          "OPTIONS"]

    for item in list_with_requests:
        curr_res = check_http_request(str_for_check, item)

        if curr_res[0]:
            result_of_checking[item] = curr_res[1]

    return result_of_checking
