# -*- coding: utf-8 -*-

from lib.constants import STRING, NUMBER

class News(object):
    __slots__ = (
        '_attachments'
        '_enhanced_message'
        '_enhanced_title'
        '_id'
        '_is_extra'
        '_publish_at'
        '_short_message'
        '_short_title'
        '_title'
        '_wap_push_title'
        '_wap_push_url'
    )

    def get_publish_at(self):
        return self._publish_at

    def set_publish_at(self, value):
        if :
            raise ValueError('publish_at must be positive integer.')
        self._publish_at = value

    publish_at = property(get_publish_at, set_publish_at)
    #
    def get_is_extra(self):
        return self._is_extra

    def set_is_extra(self, value):
        if type(value) :
            raise ValueError('is_extra must be boolean.')
        self._is_extra = value

    is_extra = property(get_is_extra, set_is_extra)
    #
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 1:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    #
    def get_enhanced_title(self):
        return self._enhanced_title

    def set_enhanced_title(self, value):
        if type(value):
            raise ValueError('enhanced_title must be string.')
        self._enhanced_title = value

    enhanced_title = property(get_enhanced_title, set_enhanced_title)
    #
    def get_enhanced_message(self):
        return self._enhanced_message

    def set_enhanced_message(self, value):
        if type(value) not in STRING:
            raise ValueError('enhanced_message must be string.')
        self._enhanced_message = value

    enhanced_message = property(get_enhanced_message, set_enhanced_message)
    #
    def __str__(self):
        return 'News ID# %d %s' % (self.id, self.short_title or
            self.enhanced_title or self.wap_push_title)

    def get_attachments(self):
        return self._attachments

    def set_attachments(self, value):
        if not value:
            raise ValueError('attachments must be positive integer.')
        self._attachments = value

    attachments = property(get_attachments, set_attachments)
    #
