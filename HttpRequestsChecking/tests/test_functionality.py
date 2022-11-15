import pytest

from functionality import check_http_request, check_all_http_requests, check_is_request


def test_check_is_request_false():
    assert check_is_request("4") == False


def test_check_is_request_true():
    assert check_is_request("https://google.com") == True


def test_check_http_request_true():
    assert check_http_request("https://google.com", "GET") == (True, 200)


def test_check_http_request_false():
    assert check_http_request("https://google.com", "PUT") == (False, 405)


def test_check_all_http_request():
    assert check_all_http_requests("https://facebook.com/") == \
           {'GET': 200, 'POST': 200, 'PUT': 200, 'PATCH': 200, 'HEAD': 200, 'DELETE': 200, 'OPTIONS': 200}
