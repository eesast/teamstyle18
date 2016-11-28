#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import gzip
import queue
import time

class RunLogger(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        if not filename:
            filename = 'ts18_' + time.strftime('%m%d%H%M%S') + '.rpy'
        self._filename = filename
        self._fp = gzip.open(self._filename, 'wt', encoding='utf-8')
        self.sig = queue.Queue()

    def run(self):
        while 1:
            q = self.sig.get(block=True)
            if q == 0:
                self._fp.close()
                break
            self._fp.write(q)
            self._fp.write('\n')

    def exit(self):
        self.sig.put(0)
