__author__ = 'Administrator'
from gamemain import GameMain
from communication import MainServer
from time import sleep
import unit
import threading
import asyncore

comm_server=MainServer(('127.0.0.1',18223))
game=GameMain()
server_thread=threading.Thread(target=asyncore.loop)
server_thread.start()
while not comm_server.gamestart:
    pass
print ('start')
while (game.is_end==False):
    #print (game.resource,game.buff,game.units.values())
    comm_server.send_to_player(game.resource)
    #comm_server.send_to_player(game.buff)
    comm_server.send_to_player(list(game.units.values()))
    print (len(game.units.values()),"turns:", game.turn_num,game.resource)
    game.produce_instr_0=comm_server.conn_list[0].produce_instr
    game.move_instr_0=comm_server.conn_list[0].move_instr
    game.capture_instr_0 = comm_server.conn_list[0].capture_instr
    game.skill_instr_0 = comm_server.conn_list[0].skill_instr
    comm_server.conn_list[0].dump()
    game.next_tick()
    sleep(0.3)