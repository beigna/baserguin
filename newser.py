#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.logger import get_logger
from lib.newser import Newser
from lib.snoopy_daemon import Daemon

log = get_logger('snoopy-newser')
log.info('I\'m standding up, Sir!')

cfg = get_newser_settings()

daemon = Scheduler('/var/run/snoopy/dnewser.pid', cfg, log)
daemon.start()
