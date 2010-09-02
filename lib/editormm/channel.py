# -*- coding: utf-8 -*-

from lib.basic_types import Boolean, String, Integer

class Channel(object):
    __slots__ = (
        '_expiration_days',
        '_extra_sm_enabled',
        '_extra_sm_length',
        '_id',
        '_is_autoload',
        '_name',
        '_scheduled_sm_enabled',
        '_scheduled_sm_length'
    )

    def __unicode__(self):
        return u'ID# %d %s' % (self.id, self.name)

    def __str__(self):
        return 'ID# %d %s' % (self.id, self.name.encode('utf-8'))

    def __init__(self, *args, **kwargs):
        self.expiration_days = kwargs.get('expiration_days', -1)
        self.extra_sm_enabled = kwargs.get('extra_sm_enabled', False)
        self.extra_sm_length = kwargs.get('extra_sm_length', 0)

        self._id = None
        if kwargs.get('id'):
            self.id = kwargs.get('id')

        self.is_autoload = kwargs.get('is_autoload', False)
        self.name = kwargs.get('name', '')
        self.scheduled_sm_enabled = kwargs.get('scheduled_sm_enabled', False)
        self.scheduled_sm_length = kwargs.get('scheduled_sm_length', 0)


    def get_scheduled_sm_length(self):
        return self._scheduled_sm_length.value
    def set_scheduled_sm_length(self, value):
        self._scheduled_sm_length = Integer(value)
    scheduled_sm_length = property(get_scheduled_sm_length,
        set_scheduled_sm_length)
    #
    def get_scheduled_sm_enabled(self):
        return self._scheduled_sm_enabled.value
    def set_scheduled_sm_enabled(self, value):
        self._scheduled_sm_enabled = Boolean(value)
    scheduled_sm_enabled = property(get_scheduled_sm_enabled,
        set_scheduled_sm_enabled)
    #
    def get_name(self):
        return self._name.value
    def set_name(self, value):
        self._name = String(value)

    name = property(get_name, set_name)
    #
    def get_is_autoload(self):
        return self._is_autoload.value
    def set_is_autoload(self, value):
        self._is_autoload = Boolean(value)

    is_autoload = property(get_is_autoload, set_is_autoload)
    #
    def get_id(self):
        return self._id.value
    def set_id(self, value):
        self._id = Integer(value)
    id = property(get_id, set_id)
    #
    def get_extra_sm_length(self):
        return self._extra_sm_length.value
    def set_extra_sm_length(self, value):
        self._extra_sm_length = Integer(value)
    extra_sm_length = property(get_extra_sm_length, set_extra_sm_length)
    #
    def get_extra_sm_enabled(self):
        return self._extra_sm_enabled.value
    def set_extra_sm_enabled(self, value):
        self._extra_sm_enabled = Boolean(value)
    extra_sm_enabled = property(get_extra_sm_enabled, set_extra_sm_enabled)
    #
    def get_expiration_days(self):
        return self._expiration_days.value
    def set_expiration_days(self, value):
        self._expiration_days = Integer(value)
    expiration_days = property(get_expiration_days, set_expiration_days)
    #
