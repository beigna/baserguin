
import xmlrpclib
import socket

STRING = (str, unicode)
NUMBER = (int, long)


class CCOProfileError(Exception):
    pass


class CCOProfile(object):
    __slots__ = ('_brand_id', '_partner_id', '_product_id', '_application_id',
        '_is_sync', '_username', '_password', '_url')

    def __init__(self, *args, **kwargs):
        self._brand_id = None
        if kwargs.get('brand_id'):
            self.brand_id = kwargs.get('brand_id')

        self._partner_id = None
        if kwargs.get('partner_id'):
            self.partner_id = kwargs.get('partner_id')

        self._product_id = None
        if kwargs.get('product_id'):
            self.product_id = kwargs.get('product_id')

        self._application_id = None
        if kwargs.get('application_id'):
            self.application_id = kwargs.get('application_id')

        self._is_sync = False
        if kwargs.get('is_sync'):
            self.is_sync = kwargs.get('is_sync')

        self._username = None
        if kwargs.get('username'):
            self.username = kwargs.get('username')

        self._password = None
        if kwargs.get('password'):
            self.password = kwargs.get('password')

        self._url = None
        if kwargs.get('url'):
            self.url = kwargs.get('url')

    def charge(self, ani):
        socket.setdefaulttimeout(60)
        server = xmlrpclib.Server(self.url)

        try:
            res = server.credit.charge(self.username, self.password,
                self.product_id, self.partner_id, self.application_id,
                self.brand_id, ani, self.is_sync)

            return res

        except xmlrpclib.Fault, e:
            raise CCOProfileError('Fault code: %d | Fault message: %s' % (
                e.faultCode, e.faultString))

    ## Getters and Setters
    def get_brand_id(self):
        return self._brand_id

    def set_brand_id(self, value):
        if type(value) not in STRING or len(value) != 8 or not value.isdigit():
            raise ValueError('brand_id must be 8 digits string.')
        self._brand_id = value

    brand_id = property(get_brand_id, set_brand_id)
    #
    def get_partner_id(self):
        return self._partner_id

    def set_partner_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('partner_id must be positive integer.')
        self._partner_id = value

    partner_id = property(get_partner_id, set_partner_id)
    #
    def get_product_id(self):
        return self._product_id

    def set_product_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('product_id must be positive integer.')
        self._product_id = value

    product_id = property(get_product_id, set_product_id)
    #
    def get_application_id(self):
        return self._application_id

    def set_application_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('application_id must be positive integer.')
        self._application_id = value

    application_id = property(get_application_id, set_application_id)
    #
    def get_is_sync(self):
        return self._is_sync

    def set_is_sync(self, value):
        if type(value) in (0, 1) or type(value) != bool:
            raise ValueError('is_sync must be boolean.')
        self._is_sync = value

    is_sync = property(get_is_sync, set_is_sync)
    #
    def get_username(self):
        return self._username

    def set_username(self, value):
        if type(value) not in STRING:
            raise ValueError('username must be string.')
        self._username = value

    username = property(get_username, set_username)
    #
    def get_password(self):
        return self._password

    def set_password(self, value):
        if type(value) not in STRING:
            raise ValueError('password must be string.')
        self._password = value

    password = property(get_password, set_password)
    #
    def get_url(self):
        return self._url

    def set_url(self, value):
        if type(value) not in STRING:
            raise ValueError('url must be string.')
        self._url = value

    url = property(get_url, set_url)


