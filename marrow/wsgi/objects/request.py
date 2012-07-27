# encoding: utf-8

import re

try:
    import urlparse
    from urllib import unquote, urlencode
except ImportError:
    from urllib import parse as urlparse
    from urllib.parse import unquote, urlencode

#from weakref import proxy

from marrow.util.compat import binary, IO
from marrow.util.object import NoDefault
#from marrow.util.insensitive import CaseInsensitiveDict

from marrow.wsgi.objects.adapters import *


log = __import__('logging').getLogger(__name__)
__all__ = ['Request', 'LocalRequest']

SCHEME_RE = re.compile(r'^[a-z]+:', re.I)


class Request(object):
    _decode_param_names = False
    _body_limit = 10*1024
    
    rw = True
    final = False
    
    body = RequestBody('wsgi.input')
    length = Int('CONTENT_LENGTH', None, rfc='14.13')
    mime = ContentType('CONTENT_TYPE', None)
    charset = Charset('CONTENT_TYPE')
    
    protocol = ReaderWriter('SERVER_PROTOCOL')
    method = ReaderWriter('REQUEST_METHOD')
    scheme = ReaderWriter('wsgi.url_scheme')
    path = Path('SCRIPT_NAME', default='')
    remainder = Path('PATH_INFO', default='')
    
    host = Host('HTTP_HOST', rfc='14.23')
    server = ReaderWriter('SERVER_NAME')
    port = Int('SERVER_PORT')
    
    user = ReaderWriter('REMOTE_USER', default=None) # TODO: abstract this out to remote.user and remote.addr
    address = ReaderWriter('REMOTE_ADDR', default=None)
    
    parameters = ReaderWriter('PARAMETERS', default='')
    query = ReaderWriter('QUERY_STRING', default='')
    args = RoutingArgs('wsgiorg.routing_args')
    kwargs = RoutingKwargs('wsgiorg.routing_args')
    fragment = ReaderWriter('FRAGMENT')
    
    def __init__(self, environ, **kw):
        super(Request, self).__init__()
        
        self.environ = environ
        
        for name in kw:
            setattr(self, name, kw[name])
    
    def __repr__(self):
        try:
            name = self.method + ' ' + str(self.path + self.remainder)
        
        except KeyError:
            name = '(invalid WSGI environ)'
        
        return '<' + self.__class__.__name__ + ' ' + name + '>'
    
    def __str__(self, skip_body=False):
        parts = [' '.join([self.method, self.url, self.protocol])]
        
        if self.method in ('PUT', 'POST'):
            parts += ['', self.body]
        
        return '\n'.join(parts)
    
    
    def get(self, name, default=NoDefault):
        try:
            value = self.environ[name]
        
        except:
            if default is NoDefault:
                raise
            
            value = default
        
        return value
    
    def __getitem__(self, name):
        return self.environ[name]
    
    def __setitem__(self, name, value):
        self.environ[name] = value
    
    def __delitem__(self, name):
        del self.environ[name]
    
    
    @property
    def url(self):
        """The full request URL including QUERY_STRING."""
        
        return self.urlize()
    
    def urlize(self, scheme=True, host=True, path=True, remainder=True, parameters=True, query=True, fragment=True):
        url = [self.scheme, '://'] if scheme else []
        
        # TODO: HTTP Basic authentication username.
        # if self.user:
        #     pass
        
        if host:
            if self.host: url.append(self.host)
            else: url.extend([self.server, ':', self.port])
        
        if path:
            url.append(str(self.path))
            
            if remainder:
                url.append(str(self.remainder))
        
        if parameters and self.parameters:
            url.extend([';', self.parameters])
        
        if query and self.query:
            url.extend(['?', self.query])
        
        if fragment and self.fragment:
            url.extend(['#', self.fragment])
        
        return ''.join(url)
    
    # These might not stick around, since they're easy to implement using urlize directly.
    # ... and I hate underscores.  -_-;
    host_url = property(lambda self: self.urlize(True, True, False, False, False, False))
    application_url = property(lambda self: self.urlize(True, True, True, False, False, False, False))
    path_url = property(lambda self: self.urlize(True, True, True, True, False, False, False))
    
    @property
    def xhr(self):
        """Returns a boolean if X-Requested-With is "XMLHttpRequest".
        
        The presence of this value is JavaScript library-dependant. Both Prototype and jQuery are known to work.
        """
        
        return self.get('HTTP_X_REQUESTED_WITH', '') == 'XMLHttpRequest'


class LocalRequest(Request):
    """A blank request environment suitable for automated testing."""
    
    def __init__(self, environ=None, path='/', POST=None, **kw):
        """Initialize a blank environment.
        
        The path argument may be a full URL or simple urlencoded path.

        If you pass a dictionary as environ, your keys will take prescedence.
        """
        
        scheme = 'http'
        netloc = 'localhost:80'
        query_string = ''

        if SCHEME_RE.search(path):
            scheme, netloc, path, query_string, fragment = urlparse.urlsplit(path)

            if ':' not in netloc:
                netloc += dict(http=':80', https=':443')[scheme]

        elif path and '?' in path:
            path, query_string = path.split('?', 1)

        path = unquote(path)
        
        # TODO: Update this to better conform to PEP 444.
        env = {
                'REQUEST_METHOD': 'GET',
                'SCRIPT_NAME': '',
                'PATH_INFO': path,
                'QUERY_STRING': query_string,
                'SERVER_NAME': netloc.split(':')[0],
                'SERVER_PORT': netloc.split(':')[1],
                'HTTP_HOST': netloc,
                'SERVER_PROTOCOL': 'HTTP/1.0',
                'CONTENT_LENGTH': '0',
                'wsgi.version': (2, 0),
                'wsgi.url_scheme': scheme,
                'wsgi.input': IO(),
                # 'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': True,
            }

        if POST is not None:
            env['REQUEST_METHOD'] = 'POST'
            body = urlencode(POST if isinstance(POST, dict) else POST).encode('utf8')
            env['wsgi.input'] = IO(body)
            env['CONTENT_LENGTH'] = binary(len(body))
            env['CONTENT_TYPE'] = b'application/x-www-form-urlencoded'

        if environ:
            env.update(environ)

        super(LocalRequest, self).__init__(env, **kw)
