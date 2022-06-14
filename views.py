import json
import time

from user import User

from db import *


def get_connected_user(server, username=None, socket=None):
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


async def login(request, socket, server, data):

    if data['username'] == 'admin' and data['password'] == 'admin':

        user = User(socket, data['username'])
        server.add_login_user(user)

        s = get_session()

        chats_db = s.query(Chat).all()

        data = {
            'oper': 'login',
            'ok': True,
            'chats':[]}

        for chat_db in chats_db:
            data['chats'].append(chat_db.to_object())

    else:
        data = {"ok":False}

    chats_data = json.dumps(data)

    await server.send_data_to_socket(chats_data.encode("utf-8"), socket)


async def register(request, socket, server, data):

    s = get_session()

    new_user = UserDB(username=data['username'], password=data['password'])
    s.add(new_user)
    s.flush()

    user_data = json.dumps(new_user.to_object())

    await server.send_data_to_socket(user_data.encode("utf-8"), socket)
    s.commit()


async def create_chat(request, socket, server, data):
    s = get_session()

    new_chat = Chat(title=data['title'])
    s.add(new_chat)
    s.flush()

    chat_data = json.dumps(new_chat.to_object())

    await server.send_data_to_socket(chat_data.encode("utf-8"), socket)
    s.commit()


async def join_chat(request, socket, server, data):
    s = get_session()

    new_chat_member = ChatMember(user_id=data['id'], chat_id=data['chat_id'])
    s.add(new_chat_member)
    s.flush()

    data = json.dumps(new_chat_member.to_object())

    await server.send_data_to_socket(data.encode("utf-8"), socket)
    s.commit()

    # print(s.query(Chat).all())


async def messages(request, socket, server, data):

    if 'chat_id' in data:

        s = get_session()

        messages_db = s.query(Message).filter(Message.chat_id == data['chat_id'])

        data = {
            'oper': 'messages',
            'ok': True,
            'messages':[]}

        for message in messages_db:
            data['messages'].append(message.to_object())

    else:
        data = {"ok":False, "message": "Require chat_id"}

    chats_data = json.dumps(data)

    await server.send_data_to_socket(chats_data.encode("utf-8"), socket)

    for i in range (3):
        time.sleep(3)

        message_data = json.dumps({
                "ok": True,
                "oper": "new_message",
                "message": {'sender': "USER",
                            'id': 6 + i,
                            'sender_id': "3",
                            'chat': "wqwq",
                            'chat_id': "1",
                            'send_time': "23:33",
                            'text': f"message{i}"
                            }
        })

        await server.send_data_to_socket(message_data.encode("utf-8"), socket)


async def send_message(request, socket, server, data):

    s = get_session()

    new_object = Message(sender_id=data['id'], chat_id=data['chat_id'], text=data['text'])
    s.add(new_object)
    s.flush()

    data_to = json.dumps(new_object.to_object())

    await server.send_data_to_socket(data_to.encode("utf-8"), socket)
    s.commit()

    chat_users = s.query(ChatMember).filter_by(chat_id=int(data['chat_id'])).all()
    print(chat_users)

    for user in chat_users:
        userdb = s.query(UserDB).filter_by(id=user.user_id).first()
        print(userdb.username)

        connected_user = get_connected_user(server, username=userdb.username)
        print(connected_user)

        if connected_user != None:
            await server.send_data_to_socket(data_to.encode("utf-8"), connected_user.socket)

