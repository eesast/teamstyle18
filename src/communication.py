import threading
import socketserver
import socket
import queue
import select

class IO_Thread(threading.Thread):
    def __init__(self):
        self.send_queue=queue.Queue()
        self.player_dict={}
        threading.Thread.__init__(self)
    def run(self):
        #Test code
        #Test code

class Main_Handler(socketserver.BaseRequestHandler):
    def handler(self):
        message_queue=queue.Queue()
        self.player_dict[message_queue]=self.request

class Main_Tcp_Server(socketserver.TCPServer):
    def __init__(self, server_address, handler):
        self.send=[]
        self.io=IO_Thread()
        self.io.start()
        socket.TCPServer.__init__(self, server_address, handler)
    def serialize(non_string_object):
        pass
    def send_message_to_players(non_string_object,player_no):
        #self.send[player_no].send_queue.put(serialize(non_string_object))
        pass
    def add_order_to_game_main():
        pass
