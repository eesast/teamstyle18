__author__ = 'Administrator'
import communication
import unit
import threading
import asyncore
from time import sleep
BASE = 0
INFANTRY = 1
VEHICLE = 2
AIRCRAFT = 3
BUILDING = 4

FLAG_0 = 0
FLAG_1 = 1
ai_id0=0
ai_id1=1
test_buff = {
    FLAG_0: {
        INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                   'shot_range_buff': 0.0},
        VEHICLE: {'health_buff': 0.5, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                  'shot_range_buff': 0.0},
        AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                        'shot_range_buff': 0.0},
        BUILDING: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                        'shot_range_buff': 0.0}
    },
    FLAG_1: {
        INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                   'shot_range_buff': 0.0},
        VEHICLE: {'health_buff': 0.6, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                  'shot_range_buff': 0.0},
        AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                        'shot_range_buff': 0.0},
        BUILDING: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                        'shot_range_buff': 0.0}
    }
}
resource = {ai_id0: {"tech": 1000, "money": 1000, "remain_people": 1000000},
                         ai_id1: {"tech": 1000, "money": 1000, "remain_people": 1000000}}
tank = unit.UnitObject(1, 1, 'nuke_tank', (22, 33), test_buff)
u_list=[tank]
a=communication.MainServer(('127.0.0.1',18223))
def action():
    global a
    while True:
        u_list.append(tank)
        a.send_to_player(u_list)
        #a.send_to_player(resource)
        #a.send_to_player(test_buff)
        sleep(0.5)

t=threading.Thread(target=asyncore.loop)
t.start()
while not a.gamestart:
    sleep(1)
action()

