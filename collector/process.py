from time import time
from datetime import datetime

from amqplib.client_0_8 import Message
import msgpack

from lib.cco import CCOProfile
from lib.sct import AsyncCharge
from lib.rabbit_handler import RabbitHandler


class CollectorProcess(object):

    def __init__(self, *args, **kwargs):
        self._logger = kwargs['logger']
        self._rabbit_cfg = kwargs['rabbit_cfg']
        self._rabbit_sc_cfg = kwargs['rabbit_sc_cfg']
        self._dispatch_info = kwargs['dispatch_info']
        self._cco = kwargs['cco_profile']
        self._dispatch_content = kwargs.get('dispatch_content', None)

    def cco_charge(self):
        self._cco_charge = CCOProfile(
            brand_id=self._cco['brand_id'],
            partner_id=self._cco['partner_id'],
            product_id=self._cco['product_id'],
            application_id=self._cco['application_id'],
            is_sync=self._cco['is_sync'],
            username=self._cco['username'],
            password=self._cco['password'],
            url=self._cco['url']
        )

        self.msisdn = self._cco['destination']['msisdn']
        self.subscription_id = self._cco['destination']['id']

        self._logger.info('[%s] Charging Brand %s; ANI: %s; Product ID: %s' % (
            self._cco['charge_id'], self._cco['brand_id'], self.msisdn,
            self._cco['product_id']))

        start_time = time()
        self._cco_result = self._cco_charge.charge(self.msisdn,
            self.subscription_id)
        request_lenght = time() - start_time

        self._logger.info('[%s] Charge request time: [%.2fs]; %s Resp: %s' % (
            self._cco['charge_id'], request_lenght, self._cco['brand_id'],
            self._cco_result['response']))

    def report_charge(self):
        try:
            data = msgpack.dumps({
                'charge_id': self._cco['charge_id'],
                'cco_transaction_id': self._cco_result['transaction'],
                'cco_response': self._cco_result['response'],
                'cco_ws_response_date': datetime.utcnow().strftime(
                    '%Y-%m-%d %H:%M:%S')
            })

            rabbit = RabbitHandler(**self._rabbit_sc_cfg)
            rabbit.put(data=data, exchange='x', routing_key='charesp')
            rabbit.disconnect()

        except Exception, e:
            self._logger.exception('[%s] Error on make report.' % (
                self._cco['charge_id']))

    def is_cco_charge_ok(self):
        return self._cco_result['response'] == 0

    def club_notify(self):
        self._logger.warning('[%s] progr a menme!!!!' % (
            self._cco['charge_id']))

    def is_async_fallbackeable(self):
        return self._cco['is_sync'] and self._cco['async_fallback']

    def sct_async_charge(self):
        fallback_product_id = self._cco['product_id']

        if self._cco['fallback_product_id']:
            fallback_product_id = self._cco['fallback_product_id']

        async_charge = AsyncCharge(
            brand_id = self._cco['brand_id'],
            partner_id = self._cco['partner_id'],
            product_id = fallback_product_id,
            application_id = self._cco['application_id'],
            msisdn = self.msisdn,
            subscription_id = self.subscription_id,
            is_sync = False,
            username = self._cco['username'],
            password = self._cco['password'],
            url = self._cco['url'],
            service_id = self._cco['service_id']
        )

        self._logger.info('[%s] Making async charge fallback Product ' \
            'ID: %s' % (self._cco['charge_id'], fallback_product_id))
        async_charge.charge()

    def ignore_charge_result(self):
        return self._cco['ignore_charge_result']

    def is_dispatch_sendeable(self):
        return not self.ignore_charge_result() and self.is_cco_charge_ok()

    def enable_dispatch_delivery(self):
        self._logger.info('[%s] Delivering dispatch' % (
            self._cco['charge_id']))

        data = {
            'dispatch_info': self._dispatch_info,
            'dispatch_content': self._dispatch_content
        }

        rabbit = RabbitHandler(**self._rabbit_cfg)
        rabbit.put(data=data, exchange='x', routing_key='putter')
        rabbit.disconnect()

