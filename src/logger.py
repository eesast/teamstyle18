#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import gzip
import queue
import time
import json
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
        self._fp = gzip.open(self._filename, 'wt', encoding='utf-8')
        self.sig = queue.Queue()

        # self.turn_num = 0

    def run(self):
        while 1:
            q = self.sig.get(block=True)
            if q == 0:
                self._fp.close()
                break
            self._fp.write(q)
            self._fp.write('\n')

    def write(self, GameMain_obj):
        if not isinstance(GameMain_obj, gamemain.GameMain):
            return

        unit_obj = []
        for i in GameMain_obj.units:
            pr = {}
            for name in dir(GameMain_obj.units[i]):
                value = getattr(GameMain_obj.units[i], name)
                if not name.startswith('__') and not callable(value):
                    pr[name] = value
            unit_obj.append(pr)

        message = json.dumps([GameMain_obj.turn_num, unit_obj, GameMain_obj.resource])
        self.sig.put(message)

    # def test_write(self):
    #     message = json.dumps([self.turn_num, [1,2,3,4,5], [1,2], [1,2,3], [1,2,3]])
    #     self.turn_num += 1
    #     self.sig.put(message)

    def exit(self):
        self.sig.put(0)

class RepManager:
    def __init__(self, filename):
        if filename:
            self._filename = filename
            self.fp = gzip.open(self._filename, 'rt', encoding = 'utf-8')
        self.sig = queue.Queue()

    def get_message(self, turn_num):
        _get = self.fp.readline()
        message = json.loads(_get)
        if not message:
            return 0

        if message[0] > turn_num:
            self.fp.seek(0)
            _get = self.fp.readline()
            if not _get:
                return 0
            message = json.loads(_get)

        while message[0] < turn_num:
            _get = self.fp.readline()
            if not _get:
                return 0
            message = json.loads(_get)

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

B.write(A)
# B.write()
# B.write()
B.exit()

time.sleep(1)

C = RepManager('test.rpy')
message = C.get_message(0)
print(message)
# message = C.get_message(1)
# print(message)
# message = C.get_message(0)
# print(message)
# message = C.get_message(4)
# print(message)
