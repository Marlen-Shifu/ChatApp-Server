import socket
import asyncio

from routes import route_request


class Server:

    def __init__(self):

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.bind(
            ('localhost', 5000)
        )

        self.server_socket.listen()
        print('Server starting')

        self.connected_sockets = []
        self.connected_users = []


        self.main_loop = asyncio.get_event_loop()


    async def send_data(self, data):
        data = data+'\n'.encode('utf-8')
        for client in self.clients:

            await self.main_loop.sock_sendall(client, data)


    async def send_data_to_user(self, data, user):
        data = data+'\n'.encode('utf-8')

        await self.main_loop.sock_sendall(user.socket, data)


    async def accept_connections(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.server_socket)
            print(user_socket)

            self.connected_sockets.append(user_socket)

            user_socket.send('You connected\n'.encode('utf-8'))


            self.main_loop.create_task(self.listen_client(user_socket))


    async def listen_client(self, client_socket = None):
        if not client_socket:
            return

        while True:
            data = await self.main_loop.sock_recv(client_socket, 2048)

            if len(data) == 0:
                print('Client disconnected')
                self.clients.remove(client_socket)
                return

            else:
                await route_request(data, client_socket, self)

            print(f'Sent: {data}')


    def add_login_user(self, user):
        self.connected_users.append(user)


    def start(self):
        self.main_loop.run_until_complete(self.accept_connections())



if __name__ == '__main__':
    server = Server()
    server.start()