# encoding: utf-8

'''
try:
    from urllib.parse import urlparse, urlunparse, urljoin, urlsplit, urlencode, quote, unquote
    from urllib.request import parse_http_list
    from http import cookiejar as cookielib
    from http.cookies import Morsel

except ImportError:
    from urllib import quote, unquote, urlencode
    from urlparse import urlparse, urlunparse, urljoin, urlsplit
    from urllib2 import parse_http_list
    import cookielib
    from Cookie import Morsel
'''

from marrow.util.compat import unicode
from marrow.util.object import NoDefault



class ReaderWriter(object):
    default = NoDefault
    rw = True
    
    def __init__(self, header, default=NoDefault, rw=NoDefault, rfc=None):
        self.header = header
        
        if default is not NoDefault:
            self.default = default
        
        if rw is not NoDefault:
            self.rw = rw
        
        self.rfc = rfc
    
    def __repr__(self):
        return '{0}("{1}")'.format(self.__class__.__name__, self.header)
    
    def __get__(self, obj, cls):
        if obj is None:
            return self
        
        try:
            return obj[self.header]
        
        except KeyError:
            pass
        
        if self.default is not NoDefault:
            if hasattr(self.default, '__call__'):
                return self.default(obj)
            
            return self.default
        
        raise AttributeError('WSGI environment does not contain %s key.' % (self.header, ))
    
    def __set__(self, obj, value):
        if not self.rw or getattr(obj, 'final', False):
            raise AttributeError('%s is a read-only value.' % (self.header, ))
        
        if value is None:
            del obj[self.header]
            return
        
        obj[self.header] = value
    
    def __delete__(self, obj):
        if not self.rw or getattr(obj, 'final', False):
            raise AttributeError('%s is a read-only value.' % (self.header, ))
        
        del obj[self.header]


class Int(ReaderWriter):
    def __get__(self, obj, cls):
        if obj is None:
            return self
        
        try:
            return int(super(Int, self).__get__(obj, cls))
        except AttributeError:
            return None
        except ValueError:
            return None
    
    def __set__(self, obj, value):
        super(Int, self).__set__(obj, unicode(value).encode('ascii'))


'''
class List(ReaderWriter):
    """Parse list headers according to RFC 2068 section 2."""
    
    def __get__(self, obj, cls):
        if obj is None:
            return self
        
        result = []
        source = super(List, self).__get__(obj, cls)
        
        if not source:
            return result
        
        for item in parse_http_list(source):
            if item[:1] == item[-1:] == '"':
                item = item[1:-1].replace('\\\\', '\\').replace('\\"', '"')
            result.append(item)
        
        return result
    
    def __set__(self, obj, value):
        parts = []
        
        for part in value:
            if ' ' in part:
                parts.append('"' + part.replace('\\', '\\\\').replace('"', '\\"'))
            


class Dict(ReaderWriter):
    """Parse dictionary headers according to RFC 2068 section 2."""
    
    def __get__(self, obj, cls):
        if obj is None:
            return self
        
        result = {}
        source = super(Dict, self).__get__(obj, cls)
        
        for item in parse_http_list(source):
            if '=' not in item:
                result[item] = None
                continue
            
            name, _, value = item.partition('=')
            
            if value[:1] == value[-1:] == '"':
                value = value[1:-1].replace('\\\\', '\\').replace('\\"', '"')
            
            result[name] = value
        
        return result
    
    def __set__(self, obj, value):
        pass
'''


class Host(ReaderWriter):
    """Host name provided in HTTP_HOST, if present, SERVER_NAME otherwise."""

    def default(self, obj):
        return (obj[self.header] if self.header in obj else None) or (obj.server + ':' + obj.port)
