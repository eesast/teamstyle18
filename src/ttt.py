import socket,struct
from time import sleep
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',18223))
sleep(1)
s.recv(4)
while(1):
    buff=s.recv(8)
    n=struct.unpack('ii',buff)[1]
    print (n)
    buff=s.recv(n*19*4)
    print (struct.unpack(n*'iiiffiiiififfiifiii',buff))
