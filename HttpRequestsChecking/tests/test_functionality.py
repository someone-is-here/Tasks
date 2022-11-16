import pytest
from functionality import check_http_request, check_all_http_requests, check_is_request


@pytest.fixture
def get_url():
    return "https://google.com"


def test_check_is_request_false():
    assert check_is_request("4") == False


def test_check_is_request_true(get_url):
    assert check_is_request(get_url) == True


def test_check_http_request_true(get_url):
    assert check_http_request(get_url, "GET") == (True, 200)


def test_check_http_request_false(get_url):
    assert check_http_request(get_url, "PUT") == (False, 405)


def test_check_all_http_request():
    assert check_all_http_requests("https://facebook.com/") == \
           {"GET": 200, "POST": 200, "PUT": 200, "PATCH": 200, "HEAD": 200, "DELETE": 200, "OPTIONS": 200}
