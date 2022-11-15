import pytest
import mock

from main import read_from_file, read_from_console


def test_read_from_file_n_not_int():
    assert read_from_file("tests/input_for_test2.txt", "output.txt") == None


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


def test_read_from_console_empty(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "0")
    assert read_from_console() == {}


def test_read_from_console_not_int(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "smth")
    assert read_from_console() == None


def test_read_from_console_not_empty(monkeypatch):
    inputs = iter(['3', 'https://google.com/', "https://facebook.com/", '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert read_from_console() == {
        "https://google.com/": {"GET": 200, "HEAD": 200},
        "https://facebook.com/": {"GET": 200, "POST": 200,
                                  "PUT": 200, "PATCH": 200,
                                  "HEAD": 200, "DELETE": 200,
                                  "OPTIONS": 200}}
