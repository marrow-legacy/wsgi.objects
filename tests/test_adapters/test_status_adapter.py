# encoding: utf-8

from __future__ import unicode_literals, division, print_function, absolute_import

try:  # This to handle Python 2.6 which is missing a lot.
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from marrow.wsgi.objects.adapters.status import StatusValue, Status
from marrow.util.compat import bytes, unicode


class TestStatusValue(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inst = StatusValue(200, "OK")
    
    def test_attrs(self):
        self.assertEquals(200, self.inst.numeric)
        self.assertEquals("OK", self.inst.text)
    
    def test_repr(self):
        self.assertEquals("Status(200, 'OK')", repr(self.inst))
    
    def test_representation_core(self):
        self.assertEquals("200 OK", self.inst.string)
        self.assertEquals(b"200 OK", self.inst.binary)
    
    def test_coersion(self):
        self.assertEquals(200, int(self.inst))
        self.assertEquals("200 OK", unicode(self.inst))
        self.assertEquals(b"200 OK", bytes(self.inst))
    
    def test_binary(self):
        inst = StatusValue(200, b"OK")
        self.assertEquals("OK", inst.text)


class TestStatus(TestCase):
    class Mock(object):
        status = Status(200)
    
    def setUp(self):
        self.inst = self.Mock()
    
    def test_default(self):
        self.assertEquals(200, int(self.inst.status))
        self.assertEquals("200 OK", unicode(self.inst.status))
    
    def test_numeric_assignment(self):
        self.assertEquals(200, int(self.inst.status))
        
        self.inst.status = 404
        self.assertEquals(404, int(self.inst.status))
        self.assertEquals("404 Not Found", unicode(self.inst.status))
        
        self.inst.status = "500"
        self.assertEquals(500, int(self.inst.status))
        self.assertEquals("500 Internal Server Error", unicode(self.inst.status))
        
        with self.assertRaises(ValueError):
            self.inst.status = "742" # A Kitten Dies
    
    def test_text_assignment(self):
        self.assertEquals(200, int(self.inst.status))
        
        self.inst.status = "Not Found"
        self.assertEquals(404, int(self.inst.status))
        self.assertEquals("404 Not Found", unicode(self.inst.status))
        
        with self.assertRaises(ValueError):
            self.inst.status = "I don't always test my code, but when I do I do it in production"
    
    def test_binary_assignment(self):
        self.assertEquals(200, int(self.inst.status))
        
        self.inst.status = b"Not Found"
        self.assertEquals(404, int(self.inst.status))
        self.assertEquals("404 Not Found", unicode(self.inst.status))
    
    def test_full_assignment(self):
        self.assertEquals(200, int(self.inst.status))
        
        self.inst.status = "768 Accidentally Took Sleeping Pills Instead Of Migraine Pills During Crunch Week"
        self.assertEquals(768, int(self.inst.status))
        self.assertEquals("768 Accidentally Took Sleeping Pills Instead Of Migraine Pills During Crunch Week", unicode(self.inst.status))
    
    def test_descriptor_access(self):
        self.assertIsInstance(self.Mock.status, Status)
    
    def test_no_default(self):
        class Mock(object):
            status = Status()
        
        self.assertEquals(None, Mock().status)
    
    def test_set_none(self):
        self.assertEquals(200, int(self.inst.status))
        
        self.inst.status = None
        self.assertEquals(None, self.inst.status)
    
    def test_set_tuple(self):
        self.assertEquals(200, int(self.inst.status))
        
        self.inst.status = (748, "Confounded by Ponies")
        self.assertEquals(748, int(self.inst.status))
        self.assertEquals("748 Confounded by Ponies", unicode(self.inst.status))
