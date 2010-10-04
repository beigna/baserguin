# -*- coding: utf-8 -*-
import glob
import os

from multiprocessing import Process, Queue
from time import sleep

class FileQueue(Process):
    """
    """

    def __init__(self, path_pool, queue, is_running, log):
        Process.__init__(self)

        self._path_pool = path_pool
        self._queue = queue
        self._is_running = is_running
        self._log = log

    def run(self):
        while self._is_running.get():
            try:
                files_list = glob.glob('%s/*.go' % (self._path_pool))

                for file_path in files_list:
                    new_file_path = file_path.replace('.go', '.proc')
                    os.rename(file_path, new_file_path)
                    self._queue.put(new_file_path)
                sleep(1)

            except Exception, e:
                self.log.exception('#SQ General fairule.')
                continue

