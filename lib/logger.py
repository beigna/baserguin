from logging.handlers import SysLogHandler
import logging
import os

def get_logger(name='no_name'):
    logger = logging.getLogger('%s[%s]' % (name, os.getpid()))
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(name)s: %(levelname)8s - %(message)s'
    )

    handler = SysLogHandler(address='/dev/log')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


