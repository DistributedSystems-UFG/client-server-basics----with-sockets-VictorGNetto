from socket  import *
from constCS import *

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(1024)
print(bytes.decode(data))

while True:
    cmd = input()
    if cmd == 'sair': break

    s.send(str.encode(cmd))
    data = s.recv(1024)
    print(bytes.decode(data))
    
s.close()