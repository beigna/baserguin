# -*- coding: utf-8 -*-

from lib.constants import STRING, NUMBER

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
        return self._content

    def set_content(self, value):
        if type(value) not in STRING:
            raise ValueError('content must be string.')
        self._content = value

    content = property(get_content, set_content)
    #
    def get_content_type(self):
        return self._content_type

    def set_content_type(self, value):
        if type(value) not in STRING:
            raise ValueError('content_type must be string.')
        self._content_type = value

    content_type = property(get_content_type, set_content_type)
    #
    def get_filename(self):
        return self._filename

    def set_filename(self, value):
        if type(value) not in STRING:
            raise ValueError('filename must be string.')
        self._filename = value

    filename = property(get_filename, set_filename)
    #
    def get_id(self):
        return self._id

    def set_id(self, value):
        if type(value) not in NUMBER or value < 0:
            raise ValueError('id must be positive integer.')
        self._id = value

    id = property(get_id, set_id)
    #
