# encoding: utf-8

import re
import sys
import urllib
import urlparse
import cgi

from weakref import proxy

from marrow.util.compat import binary, unicode, IO, parse_qsl
from marrow.util.object import NoDefault
from marrow.util.insensitive import CaseInsensitiveDict

from marrow.wsgi.objects.adapters import *


log = __import__('logging').getLogger(__name__)
__all__ = ['Request', 'LocalRequest']

SCHEME_RE = re.compile(r'^[a-z]+:', re.I)


class Request(object):
    _decode_param_names = False
    _body_limit = 10*1024
    
    # body = RequestBody('wsgi.input')
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
    
    parameters = ReaderWriter('PARAMETERS')
    query = ReaderWriter('QUERY_STRING')
    args = RoutingArgs('wsgiorg.routing_args')
    kwargs = RoutingKwargs('wsgiorg.routing_args')
    fragment = ReaderWriter('FRAGMENT')
    
    class __metaclass__(type):
        def __call__(cls, environ, *args, **kw):
            if not isinstance(environ, dict):
                # environ object is request-local pack
                environ = environ.environ
            
            if 'marrow.request' not in environ:
                environ['marrow.request'] = type.__call__(cls, environ, *args, **kw) #proxy(type.__call__(cls, environ, *args, **kw))
            
            return environ['marrow.request']
    
    def __init__(self, environ, **kw):
        super(Request, self).__init__()
        
        self.environ = environ
        
        for name, value in kw.iteritems():
            setattr(self, name, value)
    
    
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
    
    
    def __getitem__(self, name):
        return self.environ[name]
    
    def __setitem__(self, name, value):
        self.environ[name] = value
    
    def __delitem__(self, name):
        del self.environ[name]
    
    
    @property
    def url(self):
        """The full request URL including QUERY_STRING."""
        
        url = [self.scheme, '://']
        
        # TODO: HTTP Basic authentication username.
        # if self.user:
        #     pass
        
        if self.host: url.append(self.host)
        else: url.extend([self.server, ':', self.port])
        
        url.append(str(self.path))
        url.append(str(self.remainder))
        
        if self.parameters:
            url.extend([';', self.parameters])
        
        if self.query:
            url.extend(['?', self.query])
        
        if self.fragment:
            url.extend(['#', self.fragment])
        
        return ''.join(url)
    
    
    _ = '''

    
    @property
    def host_url(self):
        """The URL excluding SCRIPT_NAME, PATH_INFO, and QUERY_STRING."""
        
        url = self.scheme + '://' + self.host
        
        if ':' not in self.host:
            url += ':' + ('443' if self.scheme == 'https' else '80')
        
        return url
    
    @property
    def application_url(self):
        """The URL excluding PATH_INFO and QUERY_STRING."""
        return self.host_url + urllib.quote(self.name)
    
    @property
    def path_url(self):
        """The URL excluding QUERY_STRING."""
        return self.application_url + urllib.quote(self.path_info)
    
    @property
    def path(self):
        """The query path excluding QUERY_STRING."""
        return urllib.quote(self.name + self.path_info)
    
    @property
    def path_qs(self):
        """The query path including QUERY_STRING."""
        return self.path + ('?' + self.query_string) if self.query_string else ''
    
    @property
    def is_xhr(self):
        """Returns a boolean if X-Requested-With is "XMLHttpRequest".
    
        The presence of this value is JavaScript library-dependant. Both Prototype and jQuery are known to work.
        """
        return self.get('HTTP_X_REQUESTED_WITH', '') == 'XMLHttpRequest'
    
    def relative_url(self, other, narrow=False):
        """Resolve a relative path.
        
        If narrow is True use only SCRIPT_NAME when resolving.
        """
        
        if narrow:
            return urlparse.urljoin(self.applicaiton_url + ('' if self.applicaiton_url.endswith('/') else '/'), other)
        
        return urlparse.urljoin(self.path_url, other)
    
    def path_info_pop(self):
        """Pop a segment from PATH_INFO and push it onto SCRIPT_NAME.
        
        Returns None if there are no segments left.  Will not return empty segments.
        """
        pass
    
    def path_info_peek(self):
        """Return the next segment from PATH_INFO, or None."""
        pass
    
    '''


    
class LocalRequest(Request):
    """A blank request environment suitable for automated testing."""
    
    def __init__(self, environ=None, path=binary('/'), POST=None, **kw):
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

        path = urllib.unquote(path)
        
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
                'wsgi.input': IO(''),
                # 'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                # 'wsgi.run_once': False,
            }

        if POST is not None:
            env['REQUEST_METHOD'] = 'POST'
            body = urllib.urlencode(POST.items() if hasattr(POST, 'items') else POST)
            env['wsgi.input'] = IO(body)
            env['CONTENT_LENGTH'] = binary(len(body))
            env['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'

        if environ:
            env.update(environ)

        super(LocalRequest, self).__init__(env, **kw)
