import json

from user import User

from db import *

# SEPARATOR = "<separator>"
# EQUALITION = ":===:"

# def read_data(data):
#     spliteds = data.decode("utf-8").split(SEPARATOR)
#
#     print(spliteds)
#
#     for_return = {}
#     for splited in spliteds:
#         print(splited)
#         data = splited.split(EQUALITION)
#         for_return[data[0]] = data[1]
#
#     return for_return


def read_data(data):
    json_data = json.loads(data)

    return json_data


async def route_request(request, socket, server):

    data = read_data(request)

    if data['oper'] == "login":
        user = User(socket, "User")
        server.add_login_user(user)

        chats_data = json.dumps(
            {'chats':
                 [
                     {
                         "name": "chat_1",
                         "id": 1
                     },

                     {
                         "name": "chat_2",
                         "id": 2
                     }
                ]
            }
        )

        await server.send_data_to_user(chats_data.encode("utf-8"), user)
        print(server.connected_users)

    if data['oper'] == "reg":

        s = get_session()

        new_user = UserDB(username = data['username'], password = data['password'])
        s.add(new_user)
        s.flush()

        user_data = json.dumps(new_user.to_object())

        await server.send_data_to_socket(user_data.encode("utf-8"), socket)
        s.commit()


    print(data)
