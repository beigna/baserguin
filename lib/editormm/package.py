# -*- coding: utf-8 -*-

from lib.constants import STRING, NUMBER
from lib.basic_types import Boolean, String, Integer, DateTime

class Package(object):
    __slots__ = (
        '_channels', #R
        '_cross_selling',
        '_default_smil',
        '_description',
        '_distribution_channel', #R
        '_has_fixed_image',
        '_id', #R
        '_mms_header',
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
        self.partner_id = kwargs.get('partner_id')
        self.partner_name = kwargs.get('partner_name')

        self.has_fixed_image = kwargs.get('has_fixed_image', False)
        self.cross_selling = kwargs.get('cross_selling', '')
        self.default_smil = kwargs.get('default_smil', 0)
        self.description = kwargs.get('description', '')
        self.mms_header = kwargs.get('mms_header', '')
        self.mms_title = kwargs.get('mms_title', '')

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
        return self._cross_selling.value

    def set_cross_selling(self, value):
        self._cross_selling = String(value)

    cross_selling = property(get_cross_selling, set_cross_selling)
    #
    def get_default_smil(self):
        return self._default_smil.value

    def set_default_smil(self, value):
        self._default_smil = Integer(value)

    default_smil = property(get_default_smil, set_default_smil)
    #
    def get_description(self):
        return self._description.value

    def set_description(self, value):
        self._description = String(value)

    description = property(get_description, set_description)
    #
    def get_distribution_channel(self):
        return self._distribution_channel.value

    def set_distribution_channel(self, value):
        self._distribution_channel = Integer(value)

    distribution_channel = property(get_distribution_channel,
        set_distribution_channel)
    #
    def get_has_fixed_image(self):
        return self._has_fixed_image.value

    def set_has_fixed_image(self, value):
        self._has_fixed_image = Boolean(value)

    has_fixed_image = property(get_has_fixed_image, set_has_fixed_image)
    #
    def get_id(self):
        return self._id.value

    def set_id(self, value):
        self._id = Integer(value)

    id = property(get_id, set_id)
    #
    def get_mms_header(self):
        return self._mms_header

    def set_mms_header(self, value):
        if type(value) != str:
            raise ValueError('mms_header must be string.')

        self._mms_header = value

    mms_header = property(get_mms_header, set_mms_header)
    #
    def get_mms_title(self):
        return self._mms_title.value

    def set_mms_title(self, value):
        self._mms_title = String(value)

    mms_title = property(get_mms_title, set_mms_title)
    #
    def get_name(self):
        return self._name.value

    def set_name(self, value):
        self._name = String(value)

    name = property(get_name, set_name)
    #
    def get_partner_id(self):
        return self._partner_id.value

    def set_partner_id(self, value):
        self._partner_id = Integer(value)

    partner_id = property(get_partner_id, set_partner_id)
    #
    def get_partner_name(self):
        return self._partner_name.value

    def set_partner_name(self, value):
        self._partner_name = String(value)

    partner_name = property(get_partner_name, set_partner_name)
    #
