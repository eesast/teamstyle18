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
        byte_message=self.serializer(obj_list)
        self.send(byte_message)

    def writable(self):
        return not self.info_queue.empty()

    def object_serializer(self, object_list):
        byte_message=b""
        byte_message+=(struct.pack('i',len(object_list)))
        pack_header="!"
        args=[]
        for obj in object_list:
            for name, value in sorted(vars(obj).items(), key=lambda t: t[0]):
                if value is None:
                    pack_header+="4s"
                    args.append("none".encode('utf-8'))
                    continue
                if type(value)==tuple or type(value)==list:
                    for sub in value:
                        pack_header+= "i" if type(sub)==int else ((str(len(sub))+"s") if type(sub)==str else 'f')
                        args.append(sub if type(sub)!=str else sub.encode('utf-8'))
                    continue
                pack_header+="i" if type(value)==int else ((str(len(value))+"s") if type(value)==str else 'f')
                args.append(value if type(value)!=str else value.encode('utf-8'))
            print (pack_header,args)
            byte_message+=(struct.pack(pack_header,*args))
        return byte_message

    def dict_serializer(self,object_dict):
        header=""
        arg=[]
        for value in dict.values():
            header+="i" if type(value)==int else ((str(len(value))+"s") if type(value)==str else 'f')
            args.append(value if type(value)!=str else value.encode('utf-8'))
        return struct.pack(header,*arg)

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
