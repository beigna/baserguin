# -*- coding: utf-8 -*-

import pycurl
import cStringIO
from urlparse import urlparse
from urllib import urlencode

class BasicHttpError(Exception): pass
class UnsupportedScheme(BasicHttpError): pass
class InvalidResponse(BasicHttpError): pass

class BasicHttp(object):
    __slots__ = ('_url', '_url_parsed', '_status', '_header', '_body', '_curl')

    def __init__(self, url, *args, **kwargs):
        """
        Test Init

        >>> a = BasicHttp('ftp://www.google.com/')
        Traceback (most recent call last):
        ...
        UnsupportedScheme: Unsupported scheme: ftp

        >>> a = BasicHttp('http://www.google.com/')
        """

        self._url = url
        self._url_parsed = urlparse(url)

        if self._url_parsed.scheme != 'http':
            raise UnsupportedScheme('Unsupported scheme: %s' % (
                self._url_parsed.scheme))

        self._status = 0
        self._header = cStringIO.StringIO()
        self._body = cStringIO.StringIO()

        self._curl = pycurl.Curl()
        self._curl.setopt(pycurl.URL, self._url)

        self._curl.setopt(pycurl.WRITEFUNCTION, self._body.write)
        self._curl.setopt(pycurl.HEADERFUNCTION, self._header.write)

        self._curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self._curl.setopt(pycurl.MAXREDIRS, 5)

    def authenticate(self, username, password):
        """
        Test authenticate

        >>> a = BasicHttp('http://handle.library.cornell.edu/' \
            'control/authBasic/authTest/')
        >>> a.authenticate('test', 'this')
        >>> response = a.request()
        >>> response['status'] == 200
        True

        >>> a = BasicHttp('http://handle.library.cornell.edu/' \
            'control/authBasic/authTest/')
        >>> a.authenticate('', '')
        >>> response = a.request()
        >>> response['status'] == 401
        True
        """

        self._curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        self._curl.setopt(pycurl.USERPWD, '%s:%s' % (username, password))

    def _request(self, method='GET', data=None, headers={}, wanted_status=None):

        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = 'Cyclelogic BasicHTTP Lib 0.2'

        headers = ['%s: %s' % (k, v) for k, v in headers.iteritems()]
        self._curl.setopt(pycurl.HTTPHEADER, headers)

        if isinstance(data, dict):
            data = urlencode(data)

        if method == 'POST':
            self._curl.setopt(pycurl.POST, 1)
            self._curl.setopt(pycurl.POSTFIELDS, data)

        elif method == 'PUT':
            self._curl.setopt(pycurl.PUT, 1)
            self._curl.setopt(pycurl.POSTFIELDS, data)

        elif method == 'HEAD':
            self._curl.setopt(pycurl.HEADER, 1)
            self._curl.setopt(pycurl.NOBODY, 1)

        self._curl.perform()
        self._status = self._curl.getinfo(pycurl.HTTP_CODE)

        if isinstance(wanted_status, list):
            if self._status not in wanted_status:
                raise InvalidResponse('Wanted Status: %d Response ' \
                    'Status: %d' % (wanted_status, self._status))

        data = {
            'status': self._status,
            'headers': self._header.getvalue(),
            'body': self._body.getvalue()
        }
        return data

    def GET(self, data=None, headers={}, wanted_status=None):
        return self._request('GET', data, headers, wanted_status)

    def POST(self, data=None, headers={}, wanted_status=None):
        return self._request('POST', data, headers, wanted_status)

    def HEAD(self, data=None, headers={}, wanted_status=None):
        return self._request('HEAD', data, headers, wanted_status)

    def PUT(self, data=None, headers={}, wanted_status=None):
        return self._request('POST', data, headers, wanted_status)

