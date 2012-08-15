# encoding: utf-8

from __future__ import unicode_literals, division, print_function, absolute_import

try:  # This to handle Python 2.6 which is missing a lot.
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from marrow.wsgi.objects.adapters.request import RequestHeaderProxy, RequestHeaders
from helpers import MockObject


class TestHeaderProxy(TestCase):
    def setUp(self):
        self.source = dict(HTTP_HOST="example.com", HTTP_CONTENT_TYPE="text/plain")
        self.proxy = RequestHeaderProxy(self.source)
    
    def test_normalization_to_environment(self):
        self.assertEquals(self.proxy._norm_to_env('Host'), 'HTTP_HOST')
        self.assertEquals(self.proxy._norm_to_env('Content-Type'), 'HTTP_CONTENT_TYPE')
        self.assertEquals(self.proxy._norm_to_env('transfer encoding'), 'HTTP_TRANSFER_ENCODING')
    
    def test_normalization_to_natural(self):
        self.assertEquals(self.proxy._norm_to_natural('HTTP_HOST'), 'Host')
        self.assertEquals(self.proxy._norm_to_natural('HTTP_CONTENT_TYPE'), 'Content-Type')
        self.assertEquals(self.proxy._norm_to_natural('HTTP_TRANSFER_ENCODING'), 'Transfer-Encoding')
        self.assertEquals(self.proxy._norm_to_natural('last modified'), 'Last-Modified')
    
    def test_get(self):
        self.assertEquals(self.proxy.get('Host'), 'example.com')
        self.assertEquals(self.proxy.get('Content-Type'), 'text/plain')
        self.assertEquals(self.proxy.get('Foo'), None)
        self.assertEquals(self.proxy.get('Bar', '27'), '27')
    
    def test_getitem(self):
        self.assertEquals(self.proxy['Host'], 'example.com')
        self.assertEquals(self.proxy['Content-Type'], 'text/plain')
        
        with self.assertRaises(KeyError):
            self.proxy['Foo']
    
    def test_clear(self):
        self.proxy.clear()
        self.assertEquals(dict(), self.source)
    
    def test_setitem(self):
        self.proxy['Host'] = 'localhost.localdomain'
        self.assertEquals('localhost.localdomain', self.source['HTTP_HOST'])
        
        self.proxy['New'] = 'foo'
        self.assertEquals('foo', self.source['HTTP_NEW'])
    
    def test_delitem(self):
        del self.proxy['host']
        self.assertNotIn('HTTP_HOST', self.source)
    
    def test_iter(self):
        self.assertEquals(list(self.proxy), ['Content-Type', 'Host'])
    
    def test_contains(self):
        self.assertIn('Content-Type', self.proxy)


class TestRequestHeaders(TestCase):
    class Mock(MockObject):
        headers = RequestHeaders()
    
    def setUp(self):
        self.inst = self.Mock()
        self.inst['HTTP_HOST'] = 'example.com'
    
    def test_bare_get(self):
        self.assertIsInstance(self.Mock.headers, RequestHeaders)
    
    def test_get(self):
        self.assertIsInstance(self.inst.headers, RequestHeaderProxy)
        self.assertEquals(self.inst.headers['host'], 'example.com')
    
    def test_set(self):
        # Yes, this should work fine.  >:D
        self.inst.headers = dict(content_type='text/plain')
        self.assertEquals(self.inst._data, dict(HTTP_CONTENT_TYPE='text/plain'))
    
    def test_set_none(self):
        self.inst.headers = None
        self.assertEquals(self.inst._data, dict())
    
    def test_del(self):
        del self.inst.headers
        self.assertEquals(self.inst._data, dict())
