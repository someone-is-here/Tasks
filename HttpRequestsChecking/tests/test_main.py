import pytest
import mock

from main import read_from_file, read_from_console


def test_read_from_file_n_not_int():
    print(read_from_file("tests/input_for_test2.txt", "output.txt"))
    assert read_from_file("tests/input_for_test2.txt", "output.txt") == \
           {'https://wrongsite.com': {'PATCH': 403, 'PUT': 403,
                                      'DELETE': 403, 'GET': 200,
                                      'HEAD': 200, 'POST': 200,
                                      'OPTIONS': 200},
            'https://google.com': {'HEAD': 200, 'GET': 200},
            'https://facebook.com': {'GET': 200, 'DELETE': 200,
                                     'OPTIONS': 200, 'POST': 200,
                                     'HEAD': 200, 'PATCH': 200,
                                     'PUT': 200},
            'https://yandex.com': {'OPTIONS': 200, 'PUT': 200,
                                   'HEAD': 200, 'POST': 200,
                                   'DELETE': 200, 'GET': 200,
                                   'PATCH': 200}}


def test_read_from_file():
    assert read_from_file("tests/input_for_test.txt", "output.txt") == {
        "https://google.com/": {"GET": 200, "HEAD": 200},
        "https://facebook.com/": {"GET": 200, "POST": 200,
                                  "PUT": 200, "PATCH": 200,
                                  "HEAD": 200, "DELETE": 200,
                                  "OPTIONS": 200},
        "https://stackoverflow.com": {"GET": 200, "POST": 200,
                                      "PUT": 200, "PATCH": 200,
                                      "HEAD": 200, "DELETE": 200,
                                      "OPTIONS": 200}
    }


def test_read_from_console_empty_string(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert read_from_console() == {}


def test_read_from_console_not_empty(monkeypatch):
    inputs = iter(["https://google.com/", "https://facebook.com/", "5", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert read_from_console() == {
        "https://google.com/": {"GET": 200, "HEAD": 200},
        "https://facebook.com/": {"GET": 200, "POST": 200,
                                  "PUT": 200, "PATCH": 200,
                                  "HEAD": 200, "DELETE": 200,
                                  "OPTIONS": 200}}
