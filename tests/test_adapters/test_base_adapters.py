# encoding: utf-8

from __future__ import unicode_literals, division, print_function, absolute_import

try:  # This to handle Python 2.6 which is missing a lot.
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from marrow.wsgi.objects.adapters.base import ReaderWriter, Int
from helpers import MockObject


class TestReaderWriter(TestCase):
    class Mock(MockObject):
        plain = ReaderWriter('foo')
        defaulted = ReaderWriter('bar', b"BAR")
        callback = ReaderWriter('baz', lambda o: b"BAZ")
        readonly = ReaderWriter('foo', rw=False)
    
    def setUp(self):
        self.inst = self.Mock()
    
    def test_direct_access(self):
        self.assertIsInstance(self.Mock.plain, ReaderWriter)
        
        self.assertEquals('ReaderWriter("foo")', repr(self.Mock.plain))
    
    def test_plain(self):
        with self.assertRaises(AttributeError):
            self.inst.plain
        
        self.inst['foo'] = b"FOO"
        self.assertEquals(b"FOO", self.inst.plain)
        
        self.inst.plain = b"OTHER"
        self.assertEquals(b"OTHER", self.inst['foo'])
        self.assertEquals(b"OTHER", self.inst.plain)
    
    def test_default(self):
        self.assertEquals(b"BAR", self.inst.defaulted)
        
        self.inst.defaulted = b"OTHER"
        self.assertEquals(b"OTHER", self.inst.defaulted)
    
    def test_callback(self):
        self.assertEquals(b"BAZ", self.inst.callback)
    
    def test_readonly(self):
        self.inst['foo'] = b"FOO"
        self.assertEquals(b"FOO", self.inst.readonly)
        
        with self.assertRaises(AttributeError):
            self.inst.readonly = b"OTHER"
        
        self.inst.final = True
        
        with self.assertRaises(AttributeError):
            self.inst.plain = b"OTHER"
    
    def test_deletion(self):
        self.inst['foo'] = b"FOO"
        
        del self.inst.plain
        self.assertNotIn('foo', self.inst)
        
        self.inst['foo'] = b"FOO"
        self.inst.plain = None
        self.assertNotIn('foo', self.inst)
        
        self.inst['foo'] = b"FOO"
        self.inst.final = True
        
        with self.assertRaises(AttributeError):
            del self.inst.plain


class TestIntReaderWriter(TestCase):
    class Mock(MockObject):
        numeric = Int('diz')
    
    def setUp(self):
        self.inst = self.Mock()
    
    def test_int_read(self):
        self.assertEquals(None, self.inst.numeric)
        
        self.inst['diz'] = b"27"
        self.assertEquals(27, self.inst.numeric)
        
        self.inst['diz'] = b"bad"
        self.assertEquals(None, self.inst.numeric)
    
    def test_int_write(self):
        self.inst.numeric = 42
        self.assertEquals(b"42", self.inst['diz'])
