# encoding: utf-8

from collections import namedtuple

from marrow.util.compat import binary, unicode, IO, parse_qsl
from marrow.util.bunch import Bunch, MultiBunch
from marrow.util.insensitive import CaseInsensitiveDict
from marrow.util.object import NoDefault

from marrow.wsgi.objects.adapters import *


log = __import__('logging').getLogger(__name__)
__all__ = ['Response']


WSGIData = namedtuple('WSGIData', ['status', 'headers', 'body'])



class Response(object):
    """A WSGI application representing a standard response.
    
    This conforms to the WSGI 2.0 draft specification.
    
    For more information, see:
        http://wsgi.org/wsgi/WSGI_2.0
    
    """
    
    status = Status()
    # body = RequestBody()
    conditional = False
    
    defaults = Bunch(status=200, mime='text/html')
    
    mime = ContentType('Content-Type')
    encoding = Charset('Content-Type')
    disposition = ReaderWriter('Content-Disposition', rfc='14.11')
    pragma = ReaderWriter('Pragma', rfc='14.32')
    server = ReaderWriter('Server', rfc='14.38')
    
    cookies = []
    
    location = ReaderWriter('Location')
    language = ReaderWriter('Content-Language')
    
    # date = Date('Date', rfc='14.18')
    age = Int('Age', rfc='14.6')
    # cache = CacheControl('Cache-Control', rfc='14.9')
    # expires = Date('Expires', rfc='14.21')
    # modified = Date('Last-Modified', rfc='14.29')
    # etag = ETag('ETag', rfc='14.19')
    # retry = TimeDelta('Retry-After', rfc='14.37')
    
    allow = List('Allow', rfc='14.7')
    vary = List('Vary', rfc='14.44')
    
    # language = List('Content-Language', rfc='14.12')
    location = ReaderWriter('Content-Location', rfc='14.14')
    hash = ContentMD5('Content-MD5', rfc='14.16')
    # ranges = AcceptRanges('Accept-Ranges', rfc='14.16')
    # range = ContentRange('Content-Range', rfc='14.16')
    length = ContentLength('Content-Length', rfc='14.17')
    
    def __init__(self, request=None, **kw):
        self.headers = CaseInsensitiveDict()
        
        self.status = self.defaults.status
        self.mime = self.defaults.mime
        self.encoding = self.defaults.encoding
        
        self.body = None
        
        if hasattr(request, 'environ'):
            self.environ = request.environ
            self.request = request
        
        else:
            self.environ = request
            self.request = None
        
        for name, value in kw.iteritems():
            if not hasattr(self, name):
                raise AttributeError('Unknown attribute %r.' % (name, ))
            setattr(self, name, value)
        
        super(Response, self).__init__()
    
    def __repr__(self):
        return '<%s at 0x%x %s>' % (
            self.__class__.__name__,
            abs(id(self)),
            self.status)
    
    def __getitem__(self, name):
        return self.headers[name]
    
    def __setitem__(self, name, value):
        self.headers[name] = value
    
    def __delitem__(self, name):
        del self.headers[name]
    
    _final = False
    
    @property
    def final(self):
        """I'm the 'x' property."""
        return self._final
    
    @final.setter
    def final(self, value):
        self._final = self._final or bool(value)
    
    @x.deleter
    def final(self):
        return
    
    @property
    def wsgi(self):
        body = self.body
        
        if isinstance(body, binary): body = [body]
        elif isinstance(body, unicode): body = [body.encode(self.encoding)]
        elif isinstance(body, IO):
            def generator(body):
                data = body.read(1024)
                while data:
                    yield data
                    data = body.read(1024)
            
            body = generator(body)
        
        return WSGIData(binary(self.status), [(n, v) for n, v in self.headers.iteritems()], body)
    
    def __call__(self, environ=None, start_response=None):
        """Process the headers and content body and return a 3-tuple of status, header list, and iterable body.
        
        Alternatively, pass the status and header list to the provided start_response callable and return an iterable body.
        
        start_response is included to support WSGI 1, and is not required for WSGI 2.
        """
        
        if environ is None:
            environ = self.environ
        
        status, headers, body = self.wsgi
        
        # We support WSGI 1.0.
        if hasattr(start_response, '__call__'):
            start_response(status, headers)
            return body
        
        return status, headers, body

