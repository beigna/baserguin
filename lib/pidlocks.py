# -*- coding: utf-8 -*-
import os

def lock_pid(pid_path):
    if os.path.exists(pid_path):
        return False

    open(pid_path, 'w').write(str(os.getpid()))
    return True
