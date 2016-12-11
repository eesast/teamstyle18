if __name__ == '__main__':  
    import socket  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('localhost', 8192))  
    import time
    while 1:
        time.sleep(2)  
        #sock.send('1')  
        print sock.recv(1024)  
    sock.close()  
