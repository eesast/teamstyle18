#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import socket
import queue
import asyncore
import struct
'''
使用asyncore().loop启动服务器，选手端发起连接请求，接受请求后会向选手端发送ai_id
发送数据: MainServer.send_to_player(data)
接收数据：MainServer.conn_list[ai_id].dump,返回(skill_instr,produce_instr,move_instr,capture_instr)
'''

class IOHandler(asyncore.dispatcher):
    def __init__(self, sock, ai_id, main_server, is_unity=False):
        asyncore.dispatcher.__init__(self, sock)
        self.info_queue = queue.Queue()
        self.ai_id=ai_id
        self.send(struct.pack('i',self.ai_id))
        self.skill_instr=[]
        self.produce_instr=[]
        self.move_instr=[]
        self.capture_instr=[]
        self.last_units=[]
        self.is_unity=is_unity
        self.main_server=main_server

    def handle_read(self):
        instruction = self.recv(8192)
        if instruction:
            print ('received instruction，length:',len(instruction))
            self.unpack_instrs(instruction)


    def handle_write(self):
        data=self.info_queue.get()
        if type(data)is list:
            byte_message=self.unit_serializer(data)
            if self.is_unity:                                   #Also send dead unit list to unity side
                dead=[unit for unit in self.last_units if unit not in data]
                self.send(bytes(3)+self.unit_serializer(dead))
        elif type(data)is dict and 1 in data[0]:
            byte_message=self.buff_serializer(data)
        else:
            byte_message=self.resource_serializer(data)
        self.send(byte_message)

    def writable(self):
        return True

    def readable(self):
        return True

    def unit_serializer(self, object_list):
        pack_header="ii"
        args=[0,len(object_list)]
        for obj in object_list:
            for name, value in sorted(vars(obj).items(), key=lambda t: t[0]):
                if (name[0]=='_') and name!='_UnitObject__unit_type' and name!='_UnitObject__type_name':
                    continue
                elif (name=='_UnitObject__unit_type' or name == '_UnitObject__type_name'):
                    name=name[-9:]
                if value is None:
                    pack_header+="i"
                    args.append(0)
                    continue
                if type(value)==tuple or type(value)==list:
                    for sub in value:
                        pack_header+= "i" if type(sub)==int else (("15s") if type(sub)==str else 'f')
                        args.append(sub if type(sub)!=str else (sub+str((15-len(sub))*' ').encode('utf-8')))
                    continue
                pack_header+="i" if type(value)==int or type(value)==bool else (str(len(value))+("s") if type(value)==str else 'f')
                args.append(value if type(value)!=str else value.encode('utf-8'))
        #print(pack_header)
        return struct.pack(pack_header,*args)

    def resource_serializer(self,object_dict):
        header="i"
        args=[2]
        for name, value in sorted(object_dict.items(),key=lambda t:t[0]):
            for name, value in sorted(value.items(),key=lambda t:t[0]):
                header+="i"
                args.append(value if type(value)!=str else value.encode('utf-8'))
        return struct.pack(header,*args)

    def buff_serializer(self,object_dict):
        header="i"
        args=[1]
        for name, value in sorted(object_dict.items(),key=lambda t:t[0]):
            for name, value in sorted(value.items(),key=lambda t:t[0]):
                for name, value in sorted(value.items(),key=lambda t:t[0]):
                    header+="i" if type(value)==int else ((str(len(value))+"s") if type(value)==str else 'f')
                    args.append(value if type(value)!=str else value.encode('utf-8'))
        return struct.pack(header,*args)

    def unpack_instrs(self, instruction):
        num=int(len(instruction)/(28))
        for i in range(0,num):
            itype,uid,bid,pos1x,pos1y,po2x,pos2y=(struct.unpack('iiiiiii',instruction[28*i:28*i+28]))
            #print(struct.unpack('iiiiiii',instruction[28*i:28*i+28]))
            if itype is 1 or itype is 2:
                if bid is -1:
                    self.skill_instr.append([itype,uid,pos1x,pos1y])
                else:
                    self.skill_instr.append([itype,uid,bid])
            elif itype is 3:
                self.produce_instr.append(bid)
            elif itype is 4:
                self.move_instr.append([uid,pos1x,pos1y])
            elif itype is 5:
                self.capture_instr.append([uid,bid])
        #print(len(self.produce_instr))

    def dump(self):
        instr_pack=(self.skill_instr,self.produce_instr,self.move_instr,self.capture_instr)
        self.skill_instr=[]
        self.produce_instr=[]
        self.move_instr=[]
        self.capture_instr=[]
        return instr_pack


class MainServer(asyncore.dispatcher):

    def __init__(self, host_addr):
        asyncore.dispatcher.__init__(self)
        self.conn_list = []
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(host_addr)
        self.listen(5)
        self.gamestart=False
        print('Server initialized')

    def handle_accept(self):
        conn,cli = self.accept()
        ai_id=0
        if conn is not None:
            self.conn_list.append(IOHandler(conn, ai_id, self, ai_id is 2))
            ai_id+=1
        if len(self.conn_list) is 1:
            print ("Both ai and unity connected")
            self.gamestart=True

    def send_to_player(self, data):
        for conn in self.conn_list:
            conn.info_queue.put(data)