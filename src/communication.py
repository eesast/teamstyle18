#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import socket
import queue
import asyncore


class IOHandler(asyncore.dispatcher):

    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)
        self.info_queue = queue.Queue()

    def handle_read(self):
        instruction = str(self.recv(8192))
        if instruction:
            self.add_to_gamemain(instruction.decode('utf-8'))

    def handle_write(self):
        self.send(self.info_queue.get().encode('utf-8'))

    def writable(self):
        return not self.info_queue.empty()

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
            handler = IO_Handler(pair[0])
            self.conn_list.append(handler)

    def send_to_player(self, info):
        # Put info into corresponding conn's queue
        pass
