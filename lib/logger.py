# -*- coding: utf-8 -*-

import logging
from logging.handlers import SysLogHandler

def get_logger(name='root'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s: %(levelname)-8s%(message)s',
        '%Y-%m-%d %H:%M:%S')

    handler = SysLogHandler(address='/dev/log')
    #handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    if not len(logger.handlers):
        logger.addHandler(handler)

    return logger
