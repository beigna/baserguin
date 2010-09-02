
import datetime

EMPTY_VALUES = (None, '')

class Boolean(object):
    __slots__ = ('_value',)

    def __init__(self, value):
        if value in EMPTY_VALUES:
            raise ValueError('')

        if value in (True, False):
            self._value = bool(value)
        elif value in ('t', 'True', '1'):
            self._value = True
        elif value in ('f', 'False', '0'):
            self._value = False
        else:
            raise TypeError('')

    def __repr__(self):
        return repr(self._value)

    def get(self):
        return self._value
    value = property(get)

class DateTime(object):
    __slots__ = ('_value',)

    def __init__(self, value):
        if value in EMPTY_VALUES:
            raise ValueError('')

        if isinstance(value, datetime.datetime):
            self._value = value
        elif isinstance(value, str):
            self._value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            raise TypeError('')

    def __str__(self):
        return self._value.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return repr(self._value)

    def get(self):
        return self._value
    value = property(get)

class String(object):
    __slots__ = ('_value',)

    def __init__(self, value):
        if value == None:
            raise ValueError('')

        if isinstance(value, str):
            self._value = value.decode('utf-8')
        elif isinstance(value, unicode):
            self._value = value
        else:
            raise TypeError('')

    def __unicode__(self):
        return self._value

    def __str__(self):
        return self._value.encode('utf-8')

    def __repr__(self):
        return repr(self._value)

    def get(self):
        return self._value
    value = property(get)

class Integer(object):
    __slots__ = ('_value',)

    def __init__(self, value):
        if value in EMPTY_VALUES:
            raise ValueError('')

        self._value = int(value)

    def __repr__(self):
        return repr(self._value)

    def get(self):
        return self._value
    value = property(get)

