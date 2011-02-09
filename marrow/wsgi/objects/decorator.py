# encoding: utf-8

from marrow.wsgi.objects.request import Request, LocalRequest
from marrow.wsgi.objects.response import Response
from marrow.wsgi import exceptions as exc

from marrow.util.compat import exception


__all__ = ['wsgify']




class wsgify(object):
    """Decorate callable to act as a WSGI1/WSGI2 application."""
    
    def __init__(self, func=None, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw
    
    def __repr__(self):
        return ""
    
    def __get__(self, obj, type=None):
        if hasattr(self.func, '__get__'):
            return self.clone(self.func.__get__(obj, type))
        else:
            return self
    
    def __call__(self, environ, start_response=None):
        req = Request(environ)
        req.response = Response(req)
        
        try:
            resp = self.call(req, *self.args, **self.kw)
        
        except exc.HTTPException:
            resp = exception().exception
        
        if resp is None:
            return req.response(environ, start_response)
        
        # Handle None
        # Handle byte string
        # Handle unicode string
        # Handle file handle
        # Handle iterable
        # Handle exception
        # Handle response
        
        return resp(environ, start_response)
    
    def get(self, url, **kw):
        kw.setdefault('method', 'GET')
        req = LocalRequest(None, url, **kw)
        return self(req)
    
    def post(self, url, POST=None, **kw):
        kw.setdefault('method', 'POST')
        req = LocalRequest(None, url, POST=POST, **kw)
        return self(req)
    
    def request(self, url, **kw):
        req = LocalRequest(url, **kw)
        return self(req)
    
    def call(self, req, *args, **kw):
        return self.func(req, *args, **kw)
    
    @property
    def undecorated(self):
        return self.func
