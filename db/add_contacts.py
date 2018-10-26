from random import randint

import servers_d.db.declarative as dba
from system_d.config import *


for id in range(1, 13):
    a = []
    id2 = []
    for _ in range(randint(1, 5)):
        a.append(randint(1, 13))
    i = list(set(a))
    for id2 in i:
        if id2 != id:
            new_contact = dba.Contacts(id, id2)
            dba.session.add(new_contact)
dba.session.commit()
dba.session.close()
