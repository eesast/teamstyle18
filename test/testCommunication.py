#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from src import communication
from nose.tools import assert_equals
import socket


def test_serialize_python():
    # 测试communication.py中的serialize()函数是否正确编码（如果没理解错函数用途的话）待发送数据
    tcp_server = communication.main_tcp_server
    assert_equals(tcp_server.serialize(), None)


def test_recv():
    #
    # 建立socket连接python端通信服务器，测试接收是否正常
    tcp_server = communication.MainServer(host)
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_socket.connect((host, port))
    while 1:
        data = receive_socket.recv(1024)
        assert_equals(data, None)


def test_decode():
    # 测试传至python端数据是否被正确解码
    pass
