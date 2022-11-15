import json


from functionality import check_all_http_requests, check_is_request


"""
Function get N strings and determine whether they are links and which http request are accessible 
All necessary input values are requested from console
"""


def read_from_console():
    try:
        n = int(input("Enter N: "))
    except ValueError:
        print("N must be int")

        return None

    res = {}

    while n > 0:
        n -= 1
        string_from_user = input("Enter string: ")

        if check_is_request(string_from_user):
            res[string_from_user] = check_all_http_requests(string_from_user)
        else:
            print(f"String \"{string_from_user}\" is not a link!")

    return res


"""
Function get N strings and determine whether they are links and which http request are accessible 
All necessary input values are requested from file
"""


def read_from_file(input_filename, result_filename):
    with open(input_filename, 'r') as file_read, open(result_filename, 'w') as file_write:
        try:
            n = int(file_read.readline())
        except ValueError:
            file_write.write("N must be int")

            return None

        res = {}

        while n > 0:
            n -= 1

            string_from_user = str(file_read.readline())
            string_from_user = string_from_user.replace('\n', '')

            if check_is_request(string_from_user):
                res[string_from_user] = check_all_http_requests(string_from_user)
            else:
                print(f"String \"{string_from_user}\" is not a link!")

        file_write.writelines(json.dumps(res))

    return res


if __name__ == '__main__':
    print(read_from_console())
    print(read_from_file("input.txt", "output.txt"))

