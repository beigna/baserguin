# -*- coding: utf-8 -*-

from lib.constants import STRING, NUMBER
from lib.basic_types import Boolean, String, Integer, DateTime

class News(object):
    __slots__ = (
        '_attachments',
        '_enhanced_message',
        '_enhanced_title',
        '_id', #R
        '_is_extra', #R
        '_publish_at', #R
        '_short_message',
        '_short_title',
        '_title',
        '_wap_push_title',
        '_wap_push_url',
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.is_extra = kwargs.get('is_extra')
        self.publish_at = kwargs.get('publish_at')

        self.enhanced_message = kwargs.get('enhanced_message', '')
        self.enhanced_title = kwargs.get('enhanced_title', '')
        self.short_message = kwargs.get('short_message', '')
        self.short_title = kwargs.get('short_title', '')
        self.title = kwargs.get('title', '')
        self.wap_push_title = kwargs.get('wap_push_title', '')
        self.wap_push_url = kwargs.get('wap_push_url', '')

    def __str__(self):
        return 'News ID# %d %s' % (self.id, self.short_title or
            self.enhanced_title or self.wap_push_title)

    def get_wap_push_url(self):
        return self._wap_push_url.value
    def set_wap_push_url(self, value):
        self._wap_push_url = String(value)

    wap_push_url = property(get_wap_push_url, set_wap_push_url)
    #
    def get_wap_push_title(self):
        return self._wap_push_title.value
    def set_wap_push_title(self, value):
        self._wap_push_title = String(value)
    wap_push_title = property(get_wap_push_title, set_wap_push_title)
    #
    def get_title(self):
        return self._title.value
    def set_title(self, value):
        self._title = String(value)
    title = property(get_title, set_title)
    #
    def get_short_title(self):
        return self._short_title.value
    def set_short_title(self, value):
        self._short_title = String(value)
    short_title = property(get_short_title, set_short_title)
    #
    def get_short_message(self):
        return self._short_message.value
    def set_short_message(self, value):
        self._short_message = String(value)
    short_message = property(get_short_message, set_short_message)
    #
    def get_publish_at(self):
        return self._publish_at.value
    def set_publish_at(self, value):
        self._publish_at = DateTime(value)

    publish_at = property(get_publish_at, set_publish_at)
    #
    def get_is_extra(self):
        return self._is_extra.value
    def set_is_extra(self, value):
        self._is_extra = Boolean(value)
    is_extra = property(get_is_extra, set_is_extra)
    #
    def get_id(self):
        return self._id.value
    def set_id(self, value):
        self._id = Integer(value)
    id = property(get_id, set_id)
    #
    def get_enhanced_title(self):
        return self._enhanced_title.value
    def set_enhanced_title(self, value):
        self._enhanced_title = String(value)
    enhanced_title = property(get_enhanced_title, set_enhanced_title)
    #
    def get_enhanced_message(self):
        return self._enhanced_message.value
    def set_enhanced_message(self, value):
        self._enhanced_message = String(value)
    enhanced_message = property(get_enhanced_message, set_enhanced_message)
    #
    def get_attachments(self):
        return self._attachments

    def set_attachments(self, value):
        if not value:
            raise ValueError('attachments must be positive integer.')
        self._attachments = value

    attachments = property(get_attachments, set_attachments)
    #
