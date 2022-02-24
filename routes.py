import json

from user import User

from db import *


def read_data(data):
    json_data = json.loads(data)

    return json_data


def get_connected_user(server, username = None, socket = None):

    if username == None and socket == None:
        raise Exception("Must be given username or socket")

    if username != None:
        for user in server.connected_users:
            if user.username == username:
                return user
        return None

    elif socket != None:
        for user in server.connected_users:
            if user.socket == socket:
                return user
        return None

async def route_request(request, socket, server):

    data = read_data(request)

    #-----------------------------------------------------------
    if data['oper'] == "login":
        user = User(socket, data['username'])
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

    #---------------------------------------------------------------
    if data['oper'] == "reg":

        s = get_session()

        new_user = UserDB(username = data['username'], password = data['password'])
        s.add(new_user)
        s.flush()

        user_data = json.dumps(new_user.to_object())

        await server.send_data_to_socket(user_data.encode("utf-8"), socket)
        s.commit()

    # ---------------------------------------------------------------
    if data['oper'] == "create-chat":

        s = get_session()

        new_chat = Chat(title = data['title'])
        s.add(new_chat)
        s.flush()

        chat_data = json.dumps(new_chat.to_object())

        await server.send_data_to_socket(chat_data.encode("utf-8"), socket)
        s.commit()

    # ---------------------------------------------------------------
    if data['oper'] == "join-chat":

        s = get_session()

        new_chat_member = ChatMember(user_id = data['id'], chat_id = data['chat_id'])
        s.add(new_chat_member)
        s.flush()

        data = json.dumps(new_chat_member.to_object())

        await server.send_data_to_socket(data.encode("utf-8"), socket)
        s.commit()

        # print(s.query(Chat).all())

    # ---------------------------------------------------------------
    if data['oper'] == "send-message":

        s = get_session()

        new_object = Message(sender_id = data['id'], chat_id = data['chat_id'], text = data['text'])
        s.add(new_object)
        s.flush()

        data_to = json.dumps(new_object.to_object())

        await server.send_data_to_socket(data_to.encode("utf-8"), socket)
        s.commit()

        chat_users = s.query(ChatMember).filter_by(chat_id = int(data['chat_id'])).all()
        print(chat_users)

        for user in chat_users:
            userdb = s.query(UserDB).filter_by(id = user.user_id).first()
            print(userdb.username)

            connected_user = get_connected_user(server, username=userdb.username)
            print(connected_user)

            if connected_user != None:
                await server.send_data_to_socket(data_to.encode("utf-8"), connected_user.socket)

    print(data)
