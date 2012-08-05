# encoding: utf-8

from __future__ import unicode_literals, division, print_function, absolute_import

import sys

from marrow.util.compat import bytes, unicode

__all__ = ['_reasons', '_codes', 'Status']


# Blatently stolen from WebOb.
_reasons = {
        # Status Codes
        # Informational
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        
        # Successful
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi Status',
        226: 'IM Used',
        
        # Redirection
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        
        # Client Error
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Request Entity Too Large',
        414: 'Request URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Requested Range Not Satisfiable',
        417: 'Expectation Failed',
        422: 'Unprocessable Entity',
        423: 'Locked',
        424: 'Failed Dependency',
        426: 'Upgrade Required',
        
        # Server Error
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        507: 'Insufficient Storage',
        510: 'Not Extended',
    }

_codes = dict([(k, j) for j, k in _reasons.items()])



class StatusValue(object):
    __slots__ = ('numeric', 'text')
    
    def __init__(self, numeric, text):
        super(StatusValue, self).__init__()
        
        if isinstance(text, bytes):
            text = text.decode('ascii')
        
        self.numeric = numeric
        self.text = text
    
    @property
    def binary(self):
        return self.string.encode('ascii')
    
    @property
    def string(self):
        return '%d %s' % (self.numeric, self.text)
    
    def __repr__(self):
        return "Status({0}, '{1}')".format(self.numeric, self.text)
    
    def __int__(self):
        return self.numeric
    
    if sys.version_info[0] == 3: # pragma: no cover
        def __bytes__(self):
            return self.binary
        
        def __str__(self):
            return self.string
    
    else: # pragma: no cover
        def __str__(self):
            return self.binary
        
        def __unicode__(self):
            return self.string


class Status(object):
    def __init__(self, value=None):
        self.default = value
        super(Status, self).__init__()
    
    def __get__(self, obj, value):
        if obj is None:
            return self
        
        if not hasattr(obj, '_status'):
            if not self.default:
                return None
            
            self.__set__(obj, self.default)
        
        return obj._status
    
    def __set__(self, obj, value):
        if isinstance(value, int):
            obj._status = StatusValue(value, _reasons[value])
            return
        
        if not value:
            obj._status = None
            return
        
        if isinstance(value, tuple):
            obj._status = StatusValue(*value)
            return
        
        if isinstance(value, bytes):
            value = value.decode('ascii')
        
        if value.isdigit():
            value = int(value)
            if value not in _reasons:
                raise ValueError("Invalid HTTP status numer: " + unicode(value))
            obj._status = StatusValue(value, _reasons[value])
            return
        
        numeric, _, text = value.partition(' ')
        
        if numeric.isdigit():
            numeric = int(numeric)
            obj._status = StatusValue(numeric, text)
            return
        
        if value not in _codes:
            raise ValueError("Invalid HTTP status name:" + value)
        
        obj._status = StatusValue(_codes[value], value)
