# -*- coding: utf8
#! /usr/bin/python3

import socket
import argparse
import select

from system_d.type_msg import *
import system_d.jim as jim


class CClient():
    def __init__(self):
        self.messages = []


class CPrepareResponce():
    def __init__(self, message):
        self.message = message
        self._to = message['to']
        self._from = message['from']
        self._to_message = {}
        self._from_message = {}
        self.actions = {
            'msg': self.prep_msg,
            'presence': None
        }

    def prep_msg(self):
        if self.check_msg():
            self._to_message[self._to] = self.message
            self._from_message[self._from] = f_alert(200, code[200])
        else:
            self._to_message = None
            self._from_message[self._from] = f_error(400, code[400])

    # подготовка сообщения адресату
    def responce_to_message(self):
        return self._to_message

    # подготовка сообщения отправителю
    def responce_from_message(self):
        return self._from_message

    def main_handler(self):
        self.actions[self.message['action']]()

    def check_msg(self):
        keys = []
        values = []
        for key, value in self.message.items():
            keys.append(key)
            values.append(value)
        if keys.sort() == ['action', 'time', 'to', 'from', 'encoding', 'message'].sort():
            self.main_handler()
            return True
        else:
            print('Сообщение msg не прошло проверку')
            return False


class CServer():

    def __init__(self):
        self.all_clients = []
        self.all_user_inst = {}
        self._sock = None

    # Создание сокета
    def create_sock(self, address, port):
        self._sock = socket.socket()
        self._sock.bind((address, int(port)))
        self._sock.listen(15)
        self._sock.settimeout(10)

    # Закрытие сокета
    def kill(self):
        self._sock.close()
        print('Сокет закрыт')

    # Кодирование и отправка сообщения
    def send_message(self, cl_sock, data):
        try:
            bj_data = jim.f_encode(data)
            cl_sock.send(bj_data)
            return 'Send OK'
        except Exception as e:
            return 'При отправке возникла ошибка {}'.format(e)

    # Получение и декодирование сообщения
    def recv_message(self, cl_sock):
        bjdata = cl_sock.recv(1024)
        if bjdata:
            data = jim.f_decode(bjdata)
            return data
        else:
            pass

    # Добавление инстанса успешно подключившегося пользователя в список
    def add_user(self, name, sock):
        user_inst = CClient()
        user_inst.name = name
        user_inst.sock = sock
        self.all_user_inst[sock] = user_inst

    # Знакомство с подключившимся пользователем
    def meeting(self, sock_client, data):
        if data['action'] == 'presence':
            user_name = data['user']['account_name']
            self.add_user(user_name, sock_client)
            self.all_clients.append(sock_client)
            resp = f_alert(200, code['200'])
            self.send_message(sock_client, resp)
            return True
        else:
            resp = f_error(400, code['400'])
            self.send_message(sock_client, resp)
            return False

    # Приём входящих сообщений
    def read_requests(self, r_clients):
        # Чтение запросов из списка клиентов
        responses = {}      # Словарь ответов сервера вида {сокет: запрос}
        for sock_client in r_clients:
            try:
                data = self.recv_message(sock_client)
                responses[sock_client] = data
            except Exception as e:
                self.all_clients.remove(sock_client)
                try:
                    i = self.all_user_inst.pop(sock_client)
                    print('Клиент {} отвалился'.format(i.name))
                except KeyError:
                    pass
        return responses

    def write_responses(self, requests, w_clients):
        # отправка сообщений читателям
        for sock_client in w_clients:
            try:
                for sock_from, resp in requests.items():
                    respons = CPrepareResponce(resp)
                    respons.prep_msg()
                    if respons.responce_to_message():
                        self.send_message(sock_client, resp)
                        self.send_message(sock_from, respons.responce_from_message()[resp['from']])
                    else:
                        self.send_message(sock_from, respons.responce_from_message()[resp['from']])
            except Exception as e:                 # Сокет недоступен, клиент отключился
                sock_client.close()
                self.all_clients.remove(sock_client)
                try:
                    i = self.all_user_inst.pop(sock_client)
                    print('Клиент {} отвалился'.format(i.name))
                except KeyError:
                    pass

    # Основной цикл
    def mainloop(self):
        while True:
            try:
                conn, addr = self._sock.accept()
            except OSError as e:
                pass                            # timeout вышел
            else:
                data = self.recv_message(conn)
                self.meeting(conn, data)
                print('Поступил запрос на подключение от: {}'.format(addr))
            finally:
                wait = 0
                w, r, e = select.select(self.all_clients, self.all_clients, [], wait)

                requests = self.read_requests(w)      # Сохраним запросы клиентов
                self.write_responses(requests, r)

    @staticmethod
    def f_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port', default='7777')
        parser.add_argument('-a', '--address', default='127.0.0.1')
        return parser.parse_args()


if __name__ == '__main__':
    args = CServer.f_parser()
    serv = CServer()
    serv.create_sock(args.address, args.port)
    serv.mainloop()
    serv.kill()
