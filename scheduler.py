#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from lib.constants import DATETIME_FORMAT
from lib.editormm.editormm import EditorMM
from lib.logger import get_logger
from lib.pidlocks import lock_pid
from lib.scheduler import Scheduler
from lib.snoopy_types import SnoopyDispatch


class SnoopySchedulerError(Exception):
    pass


class PidFileExists(Exception):
    pass


log = get_logger('snoopy-scheduler')
log.info('Initializing...')

scheduler = Scheduler(log)
scheduler.load_settings()

try:
    if lock_pid(scheduler.pid_path) == False:
        raise PidFileExists('Pid file %s exists. The scheduler is running?' %
            (scheduler.pid_path))

except Exception, e:
    log.exception('Error locking pid.')
    raise e

scheduler.load_brands_profiles()
scheduler.load_custom_partners()

# LESTO

scheduler.load_last_activity()
scheduler.load_history()

dc = {1: 'SMS', 3: 'MMS', 5: 'WAP'}

try:
    log.info('Looking for dispatches between %s and %s' % (
        scheduler.last_activity.strftime(DATETIME_FORMAT),
        scheduler.start_time.strftime(DATETIME_FORMAT)
    ))

    editormm = EditorMM(log)
    editormm.load_settings()

    fail_flag = False

    log.info('Looking for extras...')
    dispatches = editormm.get_extras(scheduler.last_activity,
        scheduler.start_time)

    for i, dispatch in enumerate(dispatches):
        if not scheduler.can_be_send(dispatch):
            log.warning('%s is not supported by Scheduler\'s brands '\
                'profiles.' % (dispatch))
            del(dispatches[i])

    for brand_profile in scheduler.brands_profiles:
        log.info('Looking for schedules %s - %d [%s]'\
            % (brand_profile['brand'], brand_profile['partner_id'],
            dc[brand_profile['distribution_channel']]))

        dispatches.extend(editormm.get_schedules(brand_profile,
            scheduler.last_activity, scheduler.start_time))

    for dispatch in dispatches:
        if dispatch.is_extra:
            log.info('  Processing [Extra] %s' % (dispatch))
        else:
            log.info('  Processing [Scheduled] %s' % (dispatch))

        if scheduler.is_dispatch_in_history(dispatch):
            log.warning('   Dispatch has been already processed.')

        else:
            log.info('   Saving dispatch ...')
            try:
                schedule_dispatch = \
                    SnoopyDispatch(schedule=dispatch.as_dict())

                schedule_dispatch.since = scheduler.last_activity
                schedule_dispatch.until = scheduler.start_time
                scheduler.check_news_outlet(schedule_dispatch)

                scheduler.inject_to_queue(schedule_dispatch)

            except:
                log.exception('   Unknow error.')
                log.debug(schedule_dispatch.as_dict())
                fail_flag = True

            else:
                scheduler.add_dispatch_to_history(schedule_dispatch)

                os.rename(schedule_dispatch.outlet_file,
                    schedule_dispatch.outlet_file.replace('.tmp', '.go'))

                try:
                    scheduler.report(schedule_dispatch)
                except:
                    log.exception('Fail while reporting...')

    if fail_flag == False:
        scheduler.save_last_activity()
        scheduler.save_last_status('ok')

except:
    scheduler.save_last_status('fail')
    log.exception('Unknow error.')

finally:
    log.info('Updating Scheduler history.')
    scheduler.save_history()

    try:
        os.unlink(scheduler.pid_path)
    except:
        log.exception('Failed at remove pid file. You manual '
            'removes it while the scripts is under execution?')

    log.info('Done. Fail flag: %s' % (fail_flag))
