import socket
from threading import Thread

from type_msg import *
from jim import f_encode, f_decode


class CClient:
    def __init__(self, name):
        self.name = name

    def send_msg(self, serv_sock):
        to = 'Fox'  # input('Кому: ')
        msg = f_msg(to, self.name, input('Текст: '))
        bj_msg = f_encode(msg)
        serv_sock.send(bj_msg)

    def recv_msg(self, serv_sock):
        while True:
            bj_msg = serv_sock.recv(1024)
            msg = f_decode(bj_msg)
            print('От {}: {}'.format(msg['from'], msg['message']))

    def meeting(self, serv_sock):
        msg = f_presence(self.name)
        bj_msg = f_encode(msg)
        serv_sock.send(bj_msg)


if __name__ == '__main__':
    with socket.socket() as sock:
        sock.connect(('127.0.0.1', 7777))
        cli = CClient('Alex')
        cli.meeting(sock)
        thr = Thread(target=cli.recv_msg, args=(sock, ), daemon=True)
        thr.start()
        while True:
            cli.send_msg(sock)
