
from basic_http import BasicHttp


class AsyncCharge(object):
    def __init__(self, *args, **kwargs):
        self._brand_id = kwargs['brand_id']
        self._partner_id = kwargs['partner_id']
        self._product_id = kwargs['product_id']
        self._application_id = kwargs['application_id']
        self._msisdn = kwargs['msisdn']
        self._is_sync = kwargs['is_sync']
        self._username = kwargs['username']
        self._password = kwargs['password']
        self._url = kwargs['url']
        self._service_id = kwargs['service_id']

    def charge(self):
        data = {
            'brand_id': self._brand_id,
            'partner_id': self._partner_id,
            'product_id': self._product_id,
            'application_id': self._application_id,
            'msisdn': self._msisdn,
            'is_sync': self._is_sync,
            'username': self._username,
            'password': self._password,
            'url': self._url,
            'service_id': self._service_id
        }

        req = BasicHttp('http://sct.cyclelogic.com/tracker/cco_async_charge/')
        req.POST(data=data, headers={'User-Agent': 'SnoopyOO'})
