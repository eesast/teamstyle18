import threading
import socketserver
import socket
import queue
import select

class recv_thread(threading.Thread):
    def __init__(self):
        self.request_list=[]
        #Access gamemain instrction queue directly?
        self.order_list_0=queue.Queue()
        self.order_list_1=queue.Queue()
        threading.Thread.__init__(self)
    def run(self):
        pass
class send_thread(threading.Thread):
    def __init__(self, request):
        self.send_queue=queue.Queue()
        self.request=request
        threading.Thread.__init__(self)
    def run(self):
        pass

class main_handler(socketserver.BaseRequestHandler):
    def handler(self):
        send=send_thread(self.request)
        send.daemon=True
        send.append(self.send)
        recv.request_list.append(self.request)
        send.start

class main_tcp_server(socketserver.TCPServer):
    def __init__(self, server_address, handler):
        self.send=[]
        self.recv=recv_thread
        socket.TCPServer.__init__(self, server_address, handler)
    def serialize(non_string_object):
        pass
    def send_message_to_players(non_string_object,player_no):
        self.send[player_no].send_queue.put(serialize(non_string_object))
    def add_order_to_game_main():
        pass
