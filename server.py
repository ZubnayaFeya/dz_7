import socket
from queue import Queue
from threading import Thread

from jim import f_encode, f_decode


class CServer:
    def __init__(self):
        self.addr = '127.0.0.1'
        self.port = 7777
        self.in_msg = Queue()    # обычная очередь сообщений
        self.conn_msg = Queue()  # сообщения до авторизации
        self.out_msg = Queue()   # сообщения для отправки
        self.clients = {}        # авторизованные клиенты
        self.cl_sock = []        # сокеты авторизованных клиентов
        self.revert_client = {}

    def create_sock(self):
        # Создаём серверный сокет
        sock = socket.socket()
        sock.bind((self.addr, self.port))
        sock.listen(15)
        sock.settimeout(0.2)
        return sock

    def disconnect_cl(self, sock_cl, addr):
        # отключение клиентского сокета
        sock_cl.close()
        print('{} не прислал корректный пресенс и был отключен'.format(addr))

    def recv_conn(self, sock_cl, addr):
        # получение сообщения
        sock_cl.settimeout(0.2)
        try:
            data = sock_cl.recv(1024)
        except socket.timeout:
            self.disconnect_cl(sock_cl, addr)
            return None
        else:
            msg = f_decode(data)
            return msg

    def meeting(self, sock_cl, addr):
        # знакомство клиента с сервером
        msg = self.recv_conn(sock_cl, addr)
        if msg is not None:
            if msg['action'] == 'presence':
                self.clients[msg['user']['account_name']] = sock_cl
                self.revert_client[sock_cl] = msg['user']['account_name']
                self.cl_sock.append(sock_cl)
                print('{} успешно подключился'.format(msg['user']['account_name']))
            else:
                self.disconnect_cl(sock_cl, addr)

    def check_cl_is_online(self, cl_sock):
        # удаление клиентского сокета из списков если он отвалился
        self.cl_sock.remove(cl_sock)
        name = self.revert_client[cl_sock]
        self.clients.pop(name)
        self.revert_client.pop(cl_sock)

    def recv_msg(self):
        # получение сообщения
        while True:
            for sock_cl in self.cl_sock[:]:
                sock_cl.settimeout(0.1)
                try:
                    data = sock_cl.recv(1024)
                except socket.timeout:
                    pass
                else:
                    if data == b'' and sock_cl.fileno() == 5:
                        print(sock_cl.fileno())
                        self.check_cl_is_online(sock_cl)
                        break
                    try:
                        msg = f_decode(data)
                        self.in_msg.put(msg)
                    except Exception as e:
                        print(e)
                        self.check_cl_is_online(sock_cl)

    def prep_responce(self):
        # если адресат онлайн то сообщение переходит в очередь на отправку
        msg = self.in_msg.get()
        if msg['to'] in self.clients:
            sock_out = self.clients[msg['to']]
            self.out_msg.put({sock_out: msg})

    def send_msg(self):
        # отправка сообщений из очереди
        while True:
            data = self.out_msg.get()
            sock_cl, msg = data.popitem()
            bj_data = f_encode(msg)
            sock_cl.send(bj_data)

    def loop_connect(self, sock_serv):
        # цикл ожидающий подключение новых клиентов
        while True:
            try:
                conn, addr = sock_serv.accept()
            except socket.timeout:
                pass
            else:
                self.meeting(conn, addr)


if __name__ == '__main__':
    srv = CServer()
    sock_s = srv.create_sock()

    thr_recv = Thread(target=srv.recv_msg, daemon=True)
    thr_recv.start()

    thr_conn = Thread(target=srv.loop_connect, args=(sock_s,), daemon=True)
    thr_conn.start()

    thr_send = Thread(target=srv.send_msg, daemon=True)
    thr_send.start()

    while True:
        srv.prep_responce()
