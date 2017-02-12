#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import queue
import time
import pickle
from src import gamemain
from src import unit

'''
start thread RunLogger in gamemain
RunLogger.write() to save data on the map
RepManager.get_message() to get infomation from .rpy file: [turn_num, [dict(unit1), dict(unit2), ...], list(resource)]
'''

MAX_SIZE = 5

class RunLogger(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        if not filename:
            filename = 'ts18_' + time.strftime('%m%d%H%M%S') + '.rpy'
        self._filename = filename
        self._fp = open(self._filename, 'wb')
        self.sig = queue.Queue()

        # self.turn_num = 0

    def run(self):
        while 1:
            q = self.sig.get(block=True)
            if q == -1:
                self._fp.close()
                break
            pickle.dump(q, self._fp, 4)

    def write(self, GameMain_obj):
        if not isinstance(GameMain_obj, gamemain.GameMain):
            return

        unit_obj = []
        for i in GameMain_obj.units:
            unit_obj.append(GameMain_obj.units[i])

        message = [GameMain_obj.turn_num, unit_obj, GameMain_obj.resource,
                              GameMain_obj.skill_instr_0, GameMain_obj.skill_instr_1]
        self.sig.put(message)

    def exit(self):
        self.sig.put(-1)

class RepManager:
    def __init__(self, filename):
        if filename:
            self._filename = filename
            self._fp = open(self._filename, 'rb')
        self.sig = queue.Queue()

    def get_message(self, turn_num):
        message = pickle.load(self._fp)
        if not message:
            return 0

        if message[0] > turn_num:
            self._fp.seek(0)
            message = pickle.load(self._fp)
            if not message:
                return 0

        while message[0] < turn_num:
            _message = pickle.load(self._fp)
            if not message:
                return 0

        return message

# test

A = gamemain.GameMain()
B = RunLogger('test.rpy')
B.start()

tank = unit.UnitObject(1, 1, 'nuke_tank', (22, 33), A.buff)
fuck = unit.UnitObject(2, 0, 'battle_tank', (22, 32), A.buff)
eagle = unit.UnitObject(3, 1, 'eagle', (22, 33), A.buff)
base = unit.UnitObject(4, 0, 'base', (21, 32), A.buff)
A.hqs.append(base)

A.units[1] = tank
A.units[2] = fuck
A.units[3] = eagle
order = [['nuke_tank_skill2', 1, (22, 31)], ['nuke_tank_skill1', 1, 2], ['eagle_skill1', 3, (21, 32)],
         ['eagle_skill2', 3, (21, 32), (22, 32)]]

A.skill_phase(order)

B.write(A)

B.exit()

time.sleep(1)

C = RepManager('test.rpy')
message = C.get_message(0)
print(message)
print(message[1][4].health_now)
