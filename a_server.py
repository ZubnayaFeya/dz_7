import asyncio
import jim
from conf import *
from type_msg import *


class CServer(asyncio.Protocol):
    def __init__(self, connections):
        self.connections = connections
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        if isinstance(exc, ConnectionResetError):
            print('Обрыв соединения')
            del self.connections[self.transport]
        else:
            print(f'Ошибка при отключении клиента: {exc}')

    def data_received(self, data):
        if data:
            message = jim.f_decode(data)
            print(f'Входящее сообщение: {message}')
            self.message_handle_router(message)

    def message_handle_router(self, message):
        action = message['action']
        if action == 'presence':
            self.presence_handle(message)
        elif action == 'msg':
            self.new_msg_handle(message)
        elif action == 'get_contact':
            pass
        elif action == 'add_contact':
            pass
        elif action == 'del_contact':
            pass
        else:
            self.send_error_message('400')

    def send_error_message(self, num_error):
        response = f_error(num_error, code[num_error])
        self.transport.write(jim.f_encode(response))

    def presence_handle(self, message):
        account_name = message['user']['account_name']
        response = f_alert('200', code['200'])
        self.transport.write(jim.f_encode(response))
        self.connections[self.transport] = account_name

    def is_client_online(self, account_name):
        if account_name in self.connections.values():
            return True
        else:
            return False

    def new_msg_handle(self, message):
        to = message['to']
        if self.is_client_online(to):
            for transport, account_name in self.connections.items():
                if account_name == to:
                    transport.write(jim.f_encode(message))
        else:
            response = f_error('410', code['410'])
            self.transport.write(jim.f_encode(response))


if __name__ == '__main__':
    server_connections = {}

    loop = asyncio. get_event_loop()
    coro = loop.create_server(lambda: CServer(server_connections), HOST, PORT)
    server = loop.run_until_complete(coro)
    loop.run_forever()
