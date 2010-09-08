# -*- coding: utf-8 -*-

from lib.constants import STRING, NUMBER

class Package(object):
    __slots__ = (
        '_channels', #R
        '_cross_selling',
        '_default_smil',
        '_description',
        '_distribution_channel', #R
        '_has_fixed_image',
        '_id', #R
        '_mms_header'
        '_mms_title',
        '_name', #R
        '_partner_id', #R
        '_partner_name', #R
    )

    def __init__(self, *args, **kwargs):
        self.channels = kwargs.get('channels')
        self.distribution_channel = kwargs.get('distribution_channel_id')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.parter_id = kwargs.get('parter_id')
        self.partner_name = kwargs.get('partner_name')

        self._cross_selling = None
        if kwargs.get('cross_selling'):
            self.cross_selling = kwargs.get('cross_selling')

        self._default_smil = None
        if kwargs.get('default_smil'):
            self.default_smil = kwargs.get('default_smil')

        self._description = None
        if kwargs.get('description'):
            self.description = kwargs.get('description')

        self._has_fidex_image = None
        if kwargs.get('has_fidex_image'):
            self.has_fidex_image = kwargs.get('has_fidex_image')

        self._mms_header = None
        if kwargs.get('mms_header'):
            self.mms_header = kwargs.get('mms_header')

        self._mms_title = None
        if kwargs.get('mms_title'):
            self.mms_title = kwargs.get('mms_title')

    #
    def get_channels(self):
        return self._channels

    def set_channels(self, value):
        if not isinstance(value, list):
            raise ValueError('channels must be list.')
        self._channels = value

    channels = property(get_channels, set_channels)
    #
    def get_cross_selling(self):
        return self._cross_selling

    def set_cross_selling(self, value):
        if type(value) not in STRING:
            raise ValueError('cross_selling must be string.')

        if isinstance(value, str):
            value = value.decode('utf-8')

        self._cross_selling = value

    cross_selling = property(get_cross_selling, set_cross_selling)
    #
    def get_default_smil(self):
        return self._default_smil

    def set_default_smil(self, value):
        if type(value) not in NUMBER:
            raise ValueError('default_smil must be integer.')
        self._default_smil = value

    default_smil = property(get_default_smil, set_default_smil)
    #
    def get_description(self):
        return self._description

    def set_description(self, value):
        if type(value) not in STRING:
            raise ValueError('description must be string.')

        if isinstance(value, str):
            value = value.decode('utf-8')

        self._description = value

    description = property(get_description, set_description)
    #
    def get_distribution_channel(self):
        return self._distribution_channel

    def set_distribution_channel(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('distribution_channel must be positive integer.')
        self._distribution_channel = value

    distribution_channel = property(get_distribution_channel,
        set_distribution_channel)
    #
    def get_has_fixed_image(self):
        return self._has_fixed_image

    def set_has_fixed_image(self, value):
        if value not in (0, 1):
            if not isinstance(value, bool):
                raise ValueError('has_fixed_image must be boolean.')

        self._has_fixed_image = bool(value)

    has_fixed_image = property(get_has_fixed_image, set_has_fixed_image)
    #
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    #
    def get_mms_header(self):
        return self._mms_header

    def set_mms_header(self, value):
        if type(value) not in STRING:
            raise ValueError('mms_header must be string.')

        if isinstance(value, str):
            value = value.decode('utf-8')

        self._mms_header = value

    mms_header = property(get_mms_header, set_mms_header)
    #
    def get_mms_title(self):
        return self._mms_title

    def set_mms_title(self, value):
        if type(value) not in STRING:
            raise ValueError('mms_title must be string.')

        if isinstance(value, str):
            value = value.decode('utf-8')

        self._mms_title = value

    mms_title = property(get_mms_title, set_mms_title)
    #
    def get_name(self):
        return self._name

    def set_name(self, value):
        if type(value) not in STRING:
            raise ValueError('name must be string.')

        if isinstance(value, str):
            value = value.decode('utf-8')

        self._name = value

    name = property(get_name, set_name)
    #
    def get_partner_id(self):
        return self._partner_id

    def set_partner_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('partner_id must be positive integer.')
        self._partner_id = value

    partner_id = property(get_partner_id, set_partner_id)
    #
    def get_partner_name(self):
        return self._partner_name

    def set_partner_name(self, value):
        if type(value) not in STRING:
            raise ValueError('partner_name must be string.')

        if isinstance(value, str):
            value = value.decode('utf-8')

        self._partner_name = value

    partner_name = property(get_partner_name, set_partner_name)
    #
