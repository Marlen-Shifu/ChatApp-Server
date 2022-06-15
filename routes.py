import json


from views import *

routes = [
    {"req": "login", "func": login},
    {"req": "register", "func": register},
    {"req": "create-chat", "func": create_chat},
    {"req": "join-chat", "func": join_chat},
    {"req": "messages", "func": messages},
    {"req": "send_message", "func": new_message_recieve},
]


def read_data(data):
    json_data = json.loads(data)

    return json_data

async def route_request(request, socket, server):

    data = read_data(request)

    for route in routes:

        oper, func = route.values()

        if oper == data['oper']:
            await func(request, socket, server, data)

