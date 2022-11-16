import json
from functionality import check_all_http_requests, check_is_request


def read_from_console():
    """
    Function get N strings and determine whether they are links and which http request are accessible
    All necessary input values are requested from console
    """
    res = {}
    string_from_user = input("Enter string: ")

    while len(string_from_user) > 0:
        if check_is_request(string_from_user):
            res[string_from_user] = check_all_http_requests(string_from_user)
        else:
            print(f"String \"{string_from_user}\" is not a link!")

        string_from_user = input("Enter string: ")

    return res


def read_from_file(input_filename, result_filename):
    """
    Function get N strings and determine whether they are links and which http request are accessible
    All necessary input values are requested from file
    """
    with open(input_filename, 'r') as file_read, open(result_filename, 'w') as file_write:
        res = {}

        strings_from_user = str(file_read.read())
        list_with_input = strings_from_user.split()

        for string_from_user in list_with_input:
            if check_is_request(string_from_user):
                res[string_from_user] = check_all_http_requests(string_from_user)
            else:
                print(f"String \"{string_from_user}\" is not a link!")

        file_write.writelines(json.dumps(res))

    return res


if __name__ == "__main__":
    # print(read_from_console())
    print(read_from_file("tests/input_for_test2.txt", "output.txt"))

