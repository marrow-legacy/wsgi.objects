# encoding: utf-8

from __future__ import unicode_literals, division, print_function, absolute_import

try:  # This to handle Python 2.6 which is missing a lot.
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from marrow.wsgi.objects.request import BareRequest


class TestBareRequest(TestCase):
    def new(self, environ, **kw):
        return environ, BareRequest(environ, **kw)
    
    def test_plain_creation(self):
        environ, request = self.new(dict(HTTP_HOST=b"example.com"))
        self.assertTrue(environ is request.environ, "environ and request.environ are not the same object")
    
    def test_environ_access(self):
        environ, request = self.new(dict(HTTP_HOST=b"example.com"))
        
        self.assertEquals(b"example.com", request['HTTP_HOST'])
        self.assertEquals(b"example.com", request.get('HTTP_HOST'))
        self.assertEquals(None, request.get('foo'))
        self.assertEquals(27, request.get('bar', 27))
        
        with self.assertRaises(KeyError):
            request['baz']
    
    def test_environ_assignment(self):
        environ, request = self.new(dict(HTTP_HOST=b"example.com"))
        
        self.assertEquals(None, request.get('foo'))
        request['foo'] = 27
        self.assertEquals(27, request['foo'])
    
    def test_environ_deletion(self):
        environ, request = self.new(dict(HTTP_HOST=b"example.com"))
        self.assertEquals(b"example.com", request['HTTP_HOST'])
        
        del request['HTTP_HOST']
        
        with self.assertRaises(KeyError):
            request['HTTP_HOST']
        
        self.assertEquals(None, request.get('HTTP_HOST'))
    
    def test_representation(self):
        environ, request = self.new(dict(HTTP_HOST=b"example.com"))
        
        self.assertEquals("<BareRequest", repr(request).partition(' ')[0])
        self.assertEquals(">", repr(request)[-1])
