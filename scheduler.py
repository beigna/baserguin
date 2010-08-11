#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.editormm import EditorMM, Schedule
from lib.scheduler import Scheduler
from lib.snoopy_types import SnoopySchedule

from lib.logger import get_logger
from lib.pidlocks import lock_pid

class SnoopySchedulerError(Exception):
    pass

log = get_logger('snoopy-scheduler')
log.info('Initializing...')

scheduler = Scheduler(log)
try:
    scheduler.load_settings()
except:
    log.exception('Failed while load settings.')
    raise SnoopySchedulerError('mama mia!')

try:
    if lock_pid(scheduler.pid_path) == False:
        raise SnoopySchedulerError('mama mia!')
except:
    log.exception('Pid file exists. The schedules is already running?')
    raise SnoopySchedulerError('mama mia!')

try:
    schedules.load_brands_profiles()
    schedules.load_custom_partners()
except:
    log.exception('Failed while load brands or custom partners.')
    raise SnoopySchedulerError('mama mia!')

# LESTO

try:
    scheduler.load_last_activity()
    scheduler.load_history()

    log.info('Looking for schedules between %s and %s' % (
        scheduler.last_activity, scheduler.start_time)

    editormm = EditorMM()
    editormm.load_settings()

    fail_flag = False

    for brand_profile in scheduler.brands_profiles:
        log.info('Looking for %s - %d [%s]' % (brand_profile['brand'],
            brand_profile['partner_id'],
            brand_profile['distribution_channel']))

        extra_dispatches = editormm.get_extras()

        scheduled_dispatches = editormm.get_schedules(brand_profile,
            scheduler.last_activity, scheduler.start_time)

        for dispatch in scheduled_dispatches:
            if scheduler.is_schedule_in_history(dispatch):
                log.warning('Schedule ID %d has been already processed.' % (
                    dispatch.id))

            else:
                log.info('Saving Schedule ID %d ...' % (dispatch.id))
                try:
                    schedule_dispatch = \
                        SnoopySchedule(schedule=dispatch.as_dict())

                    schedule_dispatch.since = scheduler.last_activity
                    schedule_dispatch.under = scheduler.start_time
                    scheduler.check_news_outlet(schedule_dispatch)

                    scheduler.inject_to_queue(schedule_dispatch)
                    scheduler.add_schedule_to_history(schedule_dispatch)
                    scheduler.report(schedule_dispatch)

                except:
                    log.exception('Unknow error.')
                    fail_flag = True

    if fail_flag == False:
        scheduler.save_last_activity()
        scheduler.save_last_status('ok')

except:
    scheduler.save_last_status('fail')

finally:
    log.info('Updating Scheduler history.')
    scheduler.save_history()

    try:
        os.unlink(scheduler.pid_path)
    except:
        log.exception('Failed at remove pid file. You manual '
            'removes it while the scripts is under execution?')

    log.info('Done.')

