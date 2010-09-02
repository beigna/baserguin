# -*- coding: utf-8 -*-

from lib.basic_types import String, Integer

class Attachment(object):
    __slots__ = (
        '_id',
        '_filename',
        '_content_type',
        '_content'
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.filename = kwargs.get('filename')
        self.content_type = kwargs.get('content_type')
        self.content = kwargs.get('content')

    def __str__(self):
        return '%s %s' % (self.filename, self.content_type)
    #
    def get_content(self):
        return self._content.value
    def set_content(self, value):
        self._content = String(value)
    content = property(get_content, set_content)
    #
    def get_content_type(self):
        return self._content_type.value
    def set_content_type(self, value):
        self._content_type = String(value)
    content_type = property(get_content_type, set_content_type)
    #
    def get_filename(self):
        return self._filename.value
    def set_filename(self, value):
        self._filename = String(value)
    filename = property(get_filename, set_filename)
    #
    def get_id(self):
        return self._id.value
    def set_id(self, value):
        self._id = Integer(value)
    id = property(get_id, set_id)
    #
