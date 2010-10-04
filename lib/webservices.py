# -*- coding: utf-8 -*-
import httplib
import socket

from base64 import encodestring
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError
from urlparse import urlparse
from xml.dom import minidom

import simplejson
import yaml

from lib.email import snoopy_email
from lib.settings import get_lib_ws_settings

cfg = get_lib_ws_settings()


class RestRequestError(Exception):
    pass


class GetFromWSError(Exception):
    pass


class PlataformError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return repr(self._message)


class MasError(PlataformError):
    def __init__(self, message):
        super(MasError, self).__init__(message)


class WmpError(PlataformError):
    def __init__(self, message):
        super(WmpError, self).__init__(message)


# ButterFly - Begin
def post_bf_consume(schedule_id, credit_to_consume, date):
    url = '%s/schedules/%d/edit/' % (cfg['butterfly']['url'], schedule_id)
    data = {
        'schedule_id': schedule_id,
        'credit_to_consume': credit_to_consume,
        'date': date
    }

    return rest_request(url, 'PUT', simplejson.dumps(data))

def set_bt_reserved_credit(schedule_id, credit_to_reserve):
    url = '%s/schedules/%d/edit/' % (cfg['butterfly']['url'], schedule_id)
    data = {
        'schedule_id': schedule_id,
        'credit_to_reserve': credit_to_reserve
    }

    return rest_request(url, 'PUT', simplejson.dumps(data))

def get_bf_ad_default(partner_id):
    url = '%s/ad_default/?partner_id=%d' % (
        cfg['butterfly']['url'], partner_id)

    ad_default = get_from_ws(url, cfg['butterfly']['format'],
        cfg['butterfly']['user'], cfg['butterfly']['pass'])

    return ad_default

def get_bf_available_credit(schedule_id):
    url = '%s/schedules/%d/detail/' % (cfg['butterfly']['url'], schedule_id)

    schedule_detail = get_from_ws(url, cfg['butterfly']['format'],
        cfg['butterfly']['user'], cfg['butterfly']['pass'])

    return int(schedule_detail['available_credit'])

def get_bf_active_zones(service_id, distribution_type):
    if distribution_type == 'province':
        agrupation = 'city'
    elif distribution_type == 'location':
        agrupation = 'area'

    url = '%s../stats/totalized/%d/?agrupation=%s' % (
        cfg['subman']['url'],
        service_id,
        agrupation
    )

    return get_from_ws(url, cfg['subman']['format'],
        cfg['subman']['user'], cfg['subman']['pass'])

def get_bf_ads(partner_id, service_id, news_id=0):
    url = '%s/ads/?service_id=%d&partner_id=%d' % (
        cfg['butterfly']['url'], service_id, partner_id
    )

    if news_id:
        url = '%s&news_id=%d' % (url, news_id)

    return get_from_ws(url, cfg['butterfly']['format'],
        cfg['butterfly']['user'], cfg['butterfly']['pass'])

def get_bf_campaign(partner_id):
    url = '%s/campaigns/?partner_id=%d' % (
        cfg['butterfly']['url'], partner_id
    )

    return get_from_ws(url, cfg['butterfly']['format'],
        cfg['butterfly']['user'], cfg['butterfly']['pass'])

def get_bf_subscriptions(service_id, carrier, distribution_type, zone_id):
    url = '%s%d/subscriptions/?subscriber__carrier=%s'\
        % (cfg['subman']['url'], service_id, carrier)

    if distribution_type == 'province':
        url = '%s&subscriber__area__city=%d' % (url, zone_id)

    elif distribution_type == 'location':
        url = '%s&subscriber__area=%d' % (url, zone_id)

    return get_from_ws(url, cfg['subman']['format'],
        cfg['subman']['user'], cfg['subman']['pass'])

# ButterFly - End

# Subman

def get_consumes(subscription_id, url):
    url = url % (subscription_id)
    data = get_from_ws(url, 'json')

    return data

def put_consumes(subscription_id, charge, url):
    url = url % (subscription_id)

    xml = u'''<?xml version="1.0" encoding="utf-8"?>
<Subscription>
    <Subscriber Consumes="%d" />
</Subscription>''' % (charge)

    return rest_request(url, 'PUT', xml)

# Subman

def report_put(uuid, date):
    url = '%s/%s/puts/' % (cfg['abanico']['url'], uuid)
    data = {
        'uuid': uuid,
        'date': date
    }

    return rest_request(url, 'PUT', yaml.safe_dump(data))

def report_subscriptors(uuid, subscriptors, files, notified_at):
    url = '%s/%s/subscriptors/' % (cfg['abanico']['url'], uuid)
    data = {
        'subscriptors_total': subscriptors,
        'files_total': files,
        'subscriptors_notified_at': notified_at
    }

    return rest_request(url, 'PUT', yaml.safe_dump(data))

def report_news(uuid, id, notified_at):
    url = '%s/%s/news/' % (cfg['abanico']['url'], uuid)
    data = {
        'news_id': id,
        'news_notified_at': notified_at
    }

    return rest_request(url, 'PUT', yaml.safe_dump(data))

def report_schedule(uuid, id, partner, is_extra, date, notified_at):
    url = '%s/' % (cfg['abanico']['url'])
    data = {
        'uuid': uuid,
        'schedule_id': id,
        'schedule_partner': partner,
        'schedule_is_extra': is_extra,
        'schedule_date': date,
        'schedule_notified_at': notified_at
    }

    return rest_request(url, 'POST', yaml.safe_dump(data))

def report_butterfly(uuid, carrier_id, partner_id,
        service_id, campaign_id, advertiser_id, ad_id, ad_content,
        ad_is_default, location_id, agrupation_id, schedule_id, schedule_date,
        quantity, notified_at):

    url = '%s/../stats/ws/' % (cfg['butterfly']['url'])
    data = {
        'uuid': uuid,
        'carrier_id': carrier_id,
        'partner_id': partner_id,
        'service_id': service_id,
        'campaign_id': campaign_id,
        'advertiser_id': advertiser_id,
        'ad_id': ad_id,
        'ad_content': ad_content,
        'ad_is_default': ad_is_default,
        'location_id': location_id,
        'agrupation_id': agrupation_id,
        'schedule_id': schedule_id,
        'schedule_date': schedule_date,
        'quantity': quantity,
        'notified_at': notified_at
    }

    return rest_request(url, 'POST', yaml.safe_dump(data))

def rest_request(url, method='GET', body='', headers={}):
    socket.setdefaulttimeout(20)
    original_url = url
    url = urlparse(url)
    if url.scheme == 'http':
        req = httplib.HTTPConnection(url.netloc)
        req.request(method, url.path, body, headers)

        res = req.getresponse()

        data = {'status': res.status, 'body': res.read(), 'url': original_url}

        req.close()
        res.close()

        status = str(data['status'])
        if status.startswith('4') or status.startswith('5'):
            raise RestRequestError(simplejson.dumps(data))

        return data

    else:
        raise RestRequestError('Invalid scheme')

def post_to_wap(url, data):
    socket.setdefaulttimeout(20)
    headers = {
        'Content-Type': 'multipart/form-data; ' \
            'boundary=----------ThIs_Is_tHe_bouNdaRY_$',
        'Content-Length': len(str(data))
    }

    req = Request(url, headers=headers)
    try:
        res = urlopen(req, data=data).read()
    except HTTPError, e:
        if e.code == httplib.ACCEPTED:
            return True
        return e.read()

def post_to_wmp(url, data, username, password):
    socket.setdefaulttimeout(20)
    headers = {
        'Content-Type': 'text/xml',
        'id': username,
        'pwd': password,
    }

    req = Request(url, headers=headers)
    wmp_res = urlopen(req, data=data).read()

    res = {'status': 500, 'message': u'Invalid XML document'}
    try:
        doc = minidom.parseString(wmp_res)
        for item in doc.childNodes:
            if item.nodeName == u'Submit-Response':
                res = {
                    'status': int(item.getAttribute('Status')),
                    'message': item.getAttribute('Message')
                }
    except:
        # el WMP da una respuesta inesperada
        raise WmpError('Unexpected error in WMP\'s response: %s' % (wmp_res))

    if res['status'] != 0 or res['message'] != u'OK':
        raise WmpError('WMP Status: %d | Message: %s' % (
            res['status'], res['message']))


def post_to_mas(url, data, type='xml', username=None, password=None):
    socket.setdefaulttimeout(20)
    headers = {'Accept': 'application/%s' % (type), }

    if username:
        headers['Authorization'] = 'Basic %s' % (
            encodestring('%s:%s' % (username, password))[:-1]
        )

    req = Request(url, headers=headers, data=data)
    try:
        res = urlopen(req)
    except HTTPError, e:
        if e.code != httplib.ACCEPTED:
            raise MasError('HTTP Code: %d | Response: %s' % (e.code, e.read()))


def get_subscriptions(service_id, carrier, credit=0):
    url_con = cfg['subman']['url'] + '%d/' \
        'subscriptions/?parameters__consumes__gte=%d&subscriber__carrier=%s'
    url_ult = cfg['subman']['url'] + '%d/subscriptions/?subscriber__carrier=%s'

    if credit > 0:
        url = url_con % (service_id, credit, carrier)
    else:
        url = url_ult % (service_id, carrier)

    return get_from_ws(url, cfg['subman']['format'],
        cfg['subman']['user'], cfg['subman']['pass'])

def get_cross_selling(id):
    url = '%s%d/' % (cfg['packages']['url'], id)

    return get_from_ws(url, cfg['packages']['format'],
        cfg['packages']['user'], cfg['packages']['pass'])

def get_attachment(id):
    url = '%s%d/' % (cfg['attachments']['url'], id)
    data = get_from_ws(url, cfg['attachments']['format'],
        cfg['attachments']['user'], cfg['attachments']['pass'])
    return encodestring(data)

def get_channel(channel_id):
    url = '%s%d/' % (cfg['channels']['url'], channel_id)

    return get_from_ws(url, cfg['channels']['format'],
        cfg['channels']['user'], cfg['channels']['pass'])

def get_news(channel_id, is_extra, until, 
        package_id=None, since=None, limit=1):

    url = cfg['news']['url']

    params = {
        'channel_id': channel_id,
        'is_extra': is_extra,
        'until': until,
        'limit': limit
    }

    if since:
        params['since'] = since

    if is_extra:
        params['since'] = since
        params['package_id'] = package_id

    url = '%s?%s' % (url, urlencode(params))

    return get_from_ws(url, cfg['news']['format'],
        cfg['news']['user'], cfg['news']['pass'])

def get_schedules(brand, partner_id, distribution_channel,
        is_extra, weekday=None, since=None, until=None):
    url = cfg['schedules']['url']

    params = {
        'brand': brand,
        'partner_id': partner_id,
        'distribution_channel': distribution_channel,
        'is_extra': is_extra
    }

    if bool(int(is_extra)):
        params['weekday'] = weekday
    else:
        params['since'] = since
        params['until'] = until

    url = '%s?%s' % (url, urlencode(params))

    return get_from_ws(url, cfg['schedules']['format'],
        cfg['schedules']['user'], cfg['schedules']['pass'])

def get_from_ws(url, type, username=None, password=None):
    socket.setdefaulttimeout(20)
    headers = {'Accept': 'application/%s' % (type), }

    if username:
        headers['Authorization'] = 'Basic %s' % (
            encodestring('%s:%s' % (username, password))[:-1]
        )

    req = Request(url, headers=headers)
    try:
        res = urlopen(req)
    except HTTPError, e:
        raise GetFromWSError('HTTP Error %s: %s at %s' % (
            e.code, e.msg, e.url))

    if type == 'yaml':
        return yaml.load(res.read())
    elif type == 'json':
        return simplejson.loads(res.read())
    elif type == 'raw':
        return res.read()

