# -*- coding: utf8
#! /usr/bin/python3

from time import time


def f_presence(account_name, status='online'):
    presence = {
        'action': 'presence',
        'time': time(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status
        }
    }
    return presence


def f_reg(name, password):
    reg_message = {
        'action': 'registration',
        'time': time(),
        'user': {
            'account_name': name,
            'password': password
        }
    }
    return reg_message


def f_auth(name, password):
    auth_message = {
        'action': 'authenticate',
        'time': time(),
        'user': {
            'account_name': name,
            'password': password
        }
    }
    return auth_message


def f_msg(to_name, from_name, text):
    msg = {
        'action': 'msg',
        'time': time(),
        'to': to_name,
        'from': from_name,
        'encoding': 'utf-8',
        'message': text
    }
    return msg


def f_join():
    join_chat = {
        'action': 'join',
        'time': time(),
        'room': '#room_name'
    }
    return join_chat


def f_leave():
    leave_chat = {
        'action': 'leave',
        'time': time(),
        'room': '#room_name'
    }
    return leave_chat


def f_quit():
    quit = {
        'action': 'quit'
    }
    return quit


def f_probe():
    probe = {
        'action': 'probe',
        'time': time()
    }
    return probe


def f_alert(number, text):
    alert = {
        'response': number,
        'time': time(),
        'alert': text
    }
    return alert


def f_error(number, text):
    error = {
        'response': number,
        'time': time(),
        'error': text
    }
    return error


code = {
    '100': 'based notification',
    '101': 'important notice',
    '200': 'OK',
    '201': 'created',
    '202': 'accepted',

    '400': 'incorrect json object',
    '401': 'not authorized',
    '402': 'incorrect login or password',
    '403': 'user forbidden',
    '404': 'user or chat not found in server',
    '409': 'conflict! login is already in use',
    '410': 'user offline',
    '500': 'server error'
}

'''
Шпаргалка по созданию алертов и эрроров
a = '200'
a = f_alert(a, code[a])
'''