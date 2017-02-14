__author__ = 'Administrator'
from gamemain import GameMain
from communication import MainServer
from time import sleep
import unit
import runner
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

while (game.is_end==False):
    comm_server.send_to_player(game.resource)
    comm_server.send_to_player(game.buff)
    comm_server.send_to_player(list(game.units.values()))
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
    print (len(game.units.values()),"turns:", game.turn_num,game.resource)
    comm_server.send_to_unity(set(comm_server.conn_list[0].instruction+comm_server.conn_list[1].instruction))
    game.next_tick()
    comm_server.conn_list[0].patient = False
    comm_server.conn_list[1].patient = False
    comm_server.conn_list[0].patient_time = 0
    comm_server.conn_list[1].patient_time = 0
    #runner.make_pip(game.units)
    #sleep(0.1)
comm_server.send_to_player(game.check_winner)
sleep(0.2)
os._exit(0)