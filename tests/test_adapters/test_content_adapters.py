# encoding: utf-8

from __future__ import unicode_literals, division, print_function, absolute_import

try:  # This to handle Python 2.6 which is missing a lot.
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from marrow.wsgi.objects.adapters.content import ContentType, ContentEncoding
from helpers import MockObject


class TestContentType(TestCase):
    class Mock(MockObject):
        mime = ContentType('CONTENT_TYPE', None)
    
    def setUp(self):
        self.inst = self.Mock()
    
    def test_empty(self):
        self.assertEquals(None, self.inst.mime)
    
    def test_default(self):
        class Mock(MockObject):
            mime = ContentType('CONTENT_TYPE', b"text/html")
        
        inst = Mock()
        self.assertEquals(b"text/html", inst.mime)
    
    def test_assignment(self):
        self.assertEquals(None, self.inst.mime)
        
        __import__('pprint').pprint(self.inst)
        self.inst.mime = "text/html"
        self.assertEquals(b"text/html", self.inst.mime)
    
    def test_assignment_with_charset(self):
        self.inst['CONTENT_TYPE'] = b'text/html; charset=utf8'
        self.assertEquals(b"text/html", self.inst.mime)
        
        self.inst.mime = "text/plain"
        self.assertEquals(b'text/plain; charset=utf8', self.inst['CONTENT_TYPE'])


class TestContentEncoding(TestCase):
    class Mock(MockObject):
        encoding = ContentEncoding('CONTENT_TYPE')
    
    def setUp(self):
        self.inst = self.Mock()
    
    def test_default(self):
        self.assertEquals("utf8", self.inst.encoding)
    
    def test_default_with_mime(self):
        self.inst['CONTENT_TYPE'] = b"text/html"
        self.assertEquals(None, self.inst.encoding)
    
    def test_assignment(self):
        self.inst.encoding = "latin1"
        self.assertEquals(b'; charset=latin1', self.inst['CONTENT_TYPE'])
        
        self.inst['CONTENT_TYPE'] = b"text/html"
        self.inst.encoding = "latin1"
        self.assertEquals(b'text/html; charset=latin1', self.inst['CONTENT_TYPE'])
    
    def test_removal(self):
        self.inst.encoding = "latin1"
        self.assertEquals(b'; charset=latin1', self.inst['CONTENT_TYPE'])
        
        self.inst.encoding = None
        self.assertEquals(b'', self.inst['CONTENT_TYPE'])
        
        self.inst.encoding = "latin1"
        del self.inst.encoding
        self.assertEquals(b'', self.inst['CONTENT_TYPE'])
