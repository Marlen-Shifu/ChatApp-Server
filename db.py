import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///db.sqlite", echo=False)

Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(12))

    def to_object(self):
        return {
            'id': self.id,
            'username': self.username
        }


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))

    def to_object(self):
        return {
            'id': self.id,
            'title': self.title
        }


class ChatMember(Base):
    __tablename__ = 'chat_member'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)
    chat_id = Column(Integer)


    def to_object(self):
        return get_session().query(Chat).filter_by(id = self.chat_id).first().to_object()


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)

    sender_id = Column(Integer)
    chat_id = Column(Integer)
    send_time = Column(DateTime, server_default=func.now())
    text = Column(String)

    def to_object(self):

        s = get_session()

        sender = s.query(UserDB).filter(UserDB.id == self.sender_id).first()

        chat = s.query(Chat).filter(Chat.id == self.chat_id).first()

        return {
            'id': self.id,
            'sender': sender.username,
            'sender_id': self.sender_id,
            'chat': chat.title,
            'chat_id': self.chat_id,
            'send_time': f"{self.send_time.hour}:{self.send_time.minute}",
            'text': self.text
        }


Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



# if __name__ == '__main__':
#     s = get_session()
#
#     test_user = User(username = 'testuser', password = '123456')
#     s.add(test_user)
#     s.flush()
#
#     test_chat = Chat(title = 'Chat1')
#     s.add(test_chat)
#     s.flush()
#
#     test_chat_member = ChatMember(user_id = test_user.id, chat_id = test_chat.id)
#     s.add(test_chat_member)
#
#     message = Message(sender_id = test_user.id, chat_id = test_chat.id, text = "QWERTYUIOP{{}KJHGFCVBN")
#     s.add(message)
#
#     s.commit()