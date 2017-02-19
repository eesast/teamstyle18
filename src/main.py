__author__ = 'Administrator'
from gamemain import GameMain
from communication import MainServer
from communication import filename
import communication
from time import sleep
import unit
import runner
import time
import threading
import asyncore
import os
comm_server=MainServer(('127.0.0.1',18223))
game=GameMain()
server_thread=threading.Thread(target=asyncore.loop)
server_thread.start()
while not comm_server.gamestart:
    pass
print ('start')
file =[]
while (game.is_end==False):
    comm_server.send_to_player(list(game.units.values()))
    comm_server.send_to_player(game.resource)
    comm_server.send_to_player(game.buff)

    while(comm_server.conn_list[0].patient==False and comm_server.conn_list[0].patient_time<=500000):
        comm_server.conn_list[0].patient_time+=1
        #print("slower main timer")
        #sleep(0.001)

    game.produce_instr_0=comm_server.conn_list[0].produce_instr
    game.move_instr_0=comm_server.conn_list[0].move_instr
    game.capture_instr_0 = comm_server.conn_list[0].capture_instr
    game.skill_instr_0 = comm_server.conn_list[0].skill_instr
    comm_server.conn_list[0].dump()
    while (comm_server.conn_list[1].patient == False and comm_server.conn_list[1].patient_time<=500000):
        comm_server.conn_list[1].patient_time += 1
    comm_server.conn_list[1].error = False

        #sleep(0.01)
    game.produce_instr_1=comm_server.conn_list[1].produce_instr
    game.move_instr_1=comm_server.conn_list[1].move_instr
    game.capture_instr_1 = comm_server.conn_list[1].capture_instr
    game.skill_instr_1 = comm_server.conn_list[1].skill_instr
    comm_server.conn_list[1].dump()
    print (len(list(game.units.values())),"turns:", game.turn_num,game.resource)

    file.append(communication.u_serializer(list(game.units.values())))
    file.append(communication.r_serializer(game.resource))
    file.append(communication.b_serializer(game.buff))
    file.append(communication.instr_serializer(set(comm_server.conn_list[0].instruction + comm_server.conn_list[1].instruction)))
    game.next_tick()
    comm_server.conn_list[0].patient = False
    comm_server.conn_list[1].patient = False
    comm_server.conn_list[0].patient_time = 0
    comm_server.conn_list[1].patient_time = 0
    #runner.make_pip(game.units)
    #sleep(0.05)

f = open(filename, 'ab')
for b in file:
    f.write(b)
f.write(communication.e_serializer(game.check_winner+300))
f.close()
comm_server.send_to_player(game.check_winner)
sleep(0.2)
os._exit(0)