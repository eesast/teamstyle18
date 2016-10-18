#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import socket
import queue
import asyncore
import struct


class IOHandler(asyncore.dispatcher):
    send_list=[]    #Things to send
    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        self.info_queue = queue.Queue()

    def handle_read(self):
        instruction = str(self.recv(8192))
        if instruction:
            self.add_to_gamemain(instruction)

    def handle_write(self):
        obj_list=self.info_queue.get()
        byte_message_list=self.serializer(obj_list)
        for byte_message in byte_message_list:
            self.send(byte_message)

    def writable(self):
        return not self.info_queue.empty()

    def serializer(self, object_list):
        byte_message_list=[]
        for obj in object_list:
            args=[]
            pack_header=""
            for name, value in vars(obj).items():
                if name in send_list:
                    pack_header+="f" if type(value)==int or type(value)==float else str(len(value))+"s"
                    args.append(value if type(value)!=str else bytes(value.encode('utf-8')))
            byte_message_list.append(struct.pack(pack_header,*args))
        return byte_message_list
    def add_to_gamemain(self, instruction):
        pass


class MainServer(asyncore.dispatcher):

    def __init__(self, host_addr):
        asyncore.dispatcher.__init__(self)
        self.conn_list = []
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(host_addr)
        self.listen(5)
        print('Server initialized')

    def handle_accept(self):
        pair = self.accept()
        print("Accept")
        if pair is not None:
            handler = IOHandler(pair[0])
            self.conn_list.append(handler)

    def send_to_player(self, obj_list, ai_id):
        # Put info into corresponding conn's queue
        self.conn_list[ai_id].info_queue.put(obj_list)
