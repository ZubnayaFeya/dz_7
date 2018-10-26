import servers_d.db.declarative as dba
from system_d.config import *


names = ['Bob', 'Bill', 'Bakki', 'Bella', 'Megan', 'Olia', 'Vanessa', 'Kitti', 'Margaret', 'Liz', 'Barry']
client_w = 'Alex'
names.append(client_w)

for name in names:
    new_user = dba.User(name, fullname=name, password='123')
    dba.session.add(new_user)
dba.session.commit()
dba.session.close()
