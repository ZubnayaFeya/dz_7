import json


def f_decode(bjmessage):
    try:
        jmessage = bjmessage.decode('utf-8')
        message = json.loads(jmessage)
    except ValueError:
        message = None
    return message


def f_encode(message):
    jmessage = json.dumps(message)
    bjmessage = jmessage.encode('utf-8')
    return bjmessage