#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import env, get, local, put, run
import os
from time import sleep
from datetime import datetime
from tempfile import mkdtemp

FILES = []
EXT = ('py', 'conf')
NO_UPLOAD = ('fabfile.py')
PRESERVE_FILES = (
)

APP_NAME = 'snoopy_oo'
APP_PACKAGE = '%s-%s.tbz2' % (APP_NAME,
    datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S'))
APP_PATH = '/opt/cyclelogic/%s' % (APP_NAME)

all_files = os.walk('./')
for path, dirnames, filenames in all_files:
    for filename in filenames:
        if filename in NO_UPLOAD:
            continue
        else:
            file_extension = filename.split('.')[-1]
            if file_extension in EXT:
                if path[2:]:
                    FILES.append('%s/%s' % (path[2:], filename))
                else:
                    FILES.append('%s' % (filename))

def staging():
    env.hosts = ['192.168.23.240']
    env.user = 'deployer'
    env.password = 'deployer'

def production():
    env.hosts = ['192.168.149.39', '192.168.149.18']
    env.user = 'root'
    env.password = 'Password1'

def restart():
    run('sudo /etc/init.d/snoopy-collector restart')

def update(is_install=False):
    'Install the application (?)'

    # Copio el proyecto a una carpeta temporal
    tmp_dir = mkdtemp(prefix='%s_' % (APP_NAME))
    local('tar c %s | tar xC %s' % (' '.join(FILES), tmp_dir))

    # Copio desde produccion archivos importantes
    if is_install == False:
        for element in PRESERVE_FILES:
            destination = element.replace(element.split('/')[-1], '')
            destination = '%s/%s' % (tmp_dir, destination)
            if not os.path.exists(destination):
                local('mkdir -p %s' % (destination))

            get('%s/%s' % (APP_PATH, element), destination)

            try:
                local('mv %s/%s.%s %s/%s' % (tmp_dir, element, env.host,
                    tmp_dir, element))
            except:
                pass

    # Creo paquete del proyecto temporal y subo
    local('cd %s && tar cjf %s *' % (tmp_dir, APP_PACKAGE))
    put('%s/%s' % (tmp_dir, APP_PACKAGE), APP_PACKAGE)
    run('rm -rf %s/*' % (APP_PATH))
    run('tar xjf %s -C %s' % (APP_PACKAGE, APP_PATH))

    run('rm %s' % (APP_PACKAGE))

    restart()

def install():
    run('mkdir -p %s' % (APP_PATH))

    update(is_install=True)
