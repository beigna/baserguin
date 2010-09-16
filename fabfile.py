#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import env, get, local, put, run, sudo
from datetime import datetime
import os
from tempfile import mkdtemp

FILES = []
EXT = ('py', 'conf')
NO_UPLOAD = ('fabfile.py', 'newser.conf', 'putter.conf', 'scheduler.conf',
    'subscriptioner.conf', 'lib_ws.conf', 'butterfly.conf', 'statter.conf',
    'notifier.conf', 'collector.conf')

PRESERVE_FILES = (
#    'conf/newser.conf',
#    'conf/collector.conf',
#    'conf/putter.conf',
    'conf/scheduler.conf',
#    'conf/subscriptioner.conf',
#    'conf/lib_ws.conf',
#    'conf/butterfly.conf',
#    'conf/statter.conf',
#    'conf/notifier.conf'
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
            if filename.split('.')[-1] in EXT:
                if path[2:]:
                    FILES.append('%s/%s' % (path[2:], filename))
                else:
                    FILES.append('%s' % (filename))


def staging():
    env.hosts = ['192.168.23.240']
    env.user = 'deployer'
    env.password = 'deployer'


def production():
    env.hosts = ['192.168.149.95']
    env.user = 'deployer'
    env.password = 'psMwF7zdn96f'


def generate_profiles():
    '''
    Generate configs files from GS/Snoopy Consoles.
    Writes sendings profiles ;)
    '''

    sudo('/opt/cyclelogic/AppsWeb/VHosts/snoopy_consoles/' \
        'manage.py generate_profiles_files')
    sudo('/etc/init.d/snoopy-subscriptioner restart')
    sudo('/etc/init.d/snoopy-butterfly restart')


def restart():
    'Restart all %s services.' % (APP_NAME)

#    sudo('/etc/init.d/snoopy-newser restart')
#    sudo('/etc/init.d/snoopy-subscriptioner restart')
#    sudo('/etc/init.d/snoopy-butterfly restart')
#    sudo('/etc/init.d/snoopy-collector restart')
#    sudo('/etc/init.d/snoopy-putter restart')
#    sudo('/etc/init.d/snoopy-statter restart')
#    sudo('/etc/init.d/snoopy-notifier restart')


def update():
    '''
    Update the application.
    '''
    # Copio el proyecto a una carpeta temporal
    tmp_dir = mkdtemp(prefix='%s_' % (APP_NAME))
    local('tar c %s | tar xC %s' % (' '.join(FILES), tmp_dir))

    # Copio desde produccion archivos importantes
    for element in PRESERVE_FILES:
        destination = element.replace(element.split('/')[-1], '')
        destination = '%s/%s' % (tmp_dir, destination)
        if not os.path.exists(destination):
            local('mkdir -p %s' % (destination))

        get('%s/%s' % (APP_PATH, element), destination)

    # Creo paquete del proyecto temporal y subo
    local('cd %s && tar cjf %s *' % (tmp_dir, APP_PACKAGE))
    put('%s/%s' % (tmp_dir, APP_PACKAGE), APP_PACKAGE)
    sudo('rm -rf %s/*' % (APP_PATH))
    sudo('tar xjf %s -C %s' % (APP_PACKAGE, APP_PATH))
    #local('/bin/rm %s' % (APP_PACKAGE))

    restart()


def install():
    '''
    Create the directory structure, update the application files
    and generate the sendings profiles ;)
    '''

    sudo('mkdir -p %s' % (APP_PATH))

    sudo('mkdir -p /var/lib/%s' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/news_butterfly_pool' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/news_pool' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/scheduler' % (APP_NAME))
    sudo('echo \'%s\' > /var/lib/%s/scheduler/last_activity' % (
        datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), APP_NAME))
    sudo('echo \'ok\' > /var/lib/%s/scheduler/last_status' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/schedules_pool' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/charges_pool' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/sender_pool' % (APP_NAME))
    sudo('mkdir -p /var/lib/%s/stats_pool' % (APP_NAME))

    sudo('mkdir -p /var/lib/%s/_failed/sender_pool' % (APP_NAME))

    # TODO: /etc/etcetc
    sudo('mkdir -p /etc/opt/cyclelogic/%s' % (APP_NAME))

    update()
