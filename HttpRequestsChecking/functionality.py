import requests
import threading
import urlextract

extractor = urlextract.URLExtract()


def check_is_request(url):
    """
    Function gets string for checking and monitors if it is a link
    """
    if len(extractor.find_urls(url)) == 0:
        return False

    try:
        requests.head(url, verify=False, timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False


def check_http_request(url, http_request):
    """
    Function gets string for checking(url) and http request then checks if the request is available
    Returns tuple with (Boolean(if request is available), status_code)
    """
    result = requests.request(http_request, url)

    if result.status_code != 405:
        return True, result.status_code

    return False, 405


def check_all_http_requests(str_for_check):
    """
    Function gets string for checking and checks all http request
    Returns dict with requests and codes if request where available
    """
    list_with_requests = ["GET", "POST",
                          "PUT", "PATCH",
                          "HEAD", "DELETE",
                          "OPTIONS"]

    list_with_thread = []
    list_with_results = []

    for item in list_with_requests:
        thread = threading.Thread(target=lambda list_with_res, name, url, http_request:
        list_with_res.append((name, check_http_request(url, http_request))),
                                  args=(list_with_results, item, str_for_check, item))
        thread.start()
        list_with_thread.append(thread)

    for thread in list_with_thread:
        thread.join()

    result_of_checking = {key: value[1] for key, value in dict(list_with_results).items() if value[0]}

    return result_of_checking
