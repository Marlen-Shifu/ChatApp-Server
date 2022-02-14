from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///db.sqlite", echo=False)

Base = declarative_base()


class User(Base):
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


class ChatMember(Base):
    __tablename__ = 'chat_member'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)
    chat_id = Column(Integer)


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)

    sender_id = Column(Integer)
    chat_id = Column(Integer)
    send_time = Column(DateTime, server_default=func.now())
    text = Column(String)


Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



if __name__ == '__main__':
    s = get_session()

    test_user = User(username = 'testuser', password = '123456')
    s.add(test_user)
    s.flush()

    test_chat = Chat(title = 'Chat1')
    s.add(test_chat)
    s.flush()

    test_chat_member = ChatMember(user_id = test_user.id, chat_id = test_chat.id)
    s.add(test_chat_member)

    message = Message(sender_id = test_user.id, chat_id = test_chat.id, text = "QWERTYUIOP{{}KJHGFCVBN")
    s.add(message)

    s.commit()