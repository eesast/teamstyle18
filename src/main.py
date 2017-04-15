__author__ = 'Administrator'
from gamemain import GameMain
from communication import MainServer
import communication
from time import sleep
import unit
import time
import threading
import asyncore
import os
import sys
#
lines=[]
connection_port=18223
host='127.0.0.1'
if os.path.exists('settings.ini'):
    with open('settings.ini','r')as f:
        lines=f.readlines()
if len(lines)>0:
    for x in lines:
        if "port" in x.replace(" ",""):
            connection_port=int(x.replace(" ","").split('=')[1])
        if "host" in x.replace(" ",""):
            host =x.replace(" ", "").replace("\n", "").replace("\r", "").split('=')[1]
filename = 'ts18_' + time.strftime('%m%d%H%M%S') + '.rpy'

if (len(sys.argv)>1):
    filename = sys.argv[1]
comm_server=MainServer((host,connection_port))
game=GameMain()
server_thread=threading.Thread(target=asyncore.loop)
server_thread.start()
while not comm_server.gamestart:
    pass
print ('start')
file =[]
while (game.is_end==False):
    changed_building=set()
    other_unit=[]
    if game.turn_num==0:
        communication.c_unit_num = len(game.units)
        comm_server.send_to_player(list(game.units.values()))
    else:
        for unit in game.units.values():
            if unit.Get_unit_type()!=4 or  unit.Get_type_name()==16 or  unit.Get_type_name()==17 or  unit.Get_type_name()==18 or  unit.Get_type_name()==19:
                other_unit.append(unit)
            else:
                changed_building.add((unit.unit_id,unit.flag,unit.Get_type_name(),unit.position[0],unit.position[1]))
        communication.c_unit_num=len(game.units)
        comm_server.send_to_player(other_unit)
        comm_server.send_to_player(changed_building)

    comm_server.send_to_player(game.resource)
    comm_server.send_to_player(game.buff)
    #print(game.buff)
    #print(game.resource)
    while((comm_server.conn_list[0].patient==False and comm_server.conn_list[0].patient_time<=220000)or(comm_server.conn_list[1].patient == False and comm_server.conn_list[1].patient_time<=220000)):
        comm_server.conn_list[0].patient_time+=1
        comm_server.conn_list[1].patient_time += 1
        #print("slower main timer")
        #sleep(0.001)

    game.produce_instr_0=comm_server.conn_list[0].produce_instr
    game.move_instr_0=comm_server.conn_list[0].move_instr
    game.capture_instr_0 = comm_server.conn_list[0].capture_instr
    game.skill_instr_0 = comm_server.conn_list[0].skill_instr
    comm_server.conn_list[0].dump()

        #sleep(0.01)
    game.produce_instr_1=comm_server.conn_list[1].produce_instr
    game.move_instr_1=comm_server.conn_list[1].move_instr
    game.capture_instr_1 = comm_server.conn_list[1].capture_instr
    game.skill_instr_1 = comm_server.conn_list[1].skill_instr
    comm_server.conn_list[1].dump()
    print ("server turns:", game.turn_num)

    file.append(communication.u_serializer(list(game.units.values())))
    file.append(communication.r_serializer(game.resource))
    file.append(communication.b_serializer(game.buff))
    file.append(communication.instr_serializer(set(comm_server.conn_list[0].instruction + comm_server.conn_list[1].instruction)))
    game.next_tick()
    comm_server.conn_list[0].patient = False
    comm_server.conn_list[1].patient = False
    comm_server.conn_list[0].patient_time = 0
    comm_server.conn_list[1].patient_time = 0
    #sleep(0.05)

f = open(filename, 'ab')
for b in file:
    f.write(b)
f.write(communication.e_serializer(game.check_winner+300))
f.close()
comm_server.send_to_player(game.check_winner)
sleep(0.2)
os._exit(0)
