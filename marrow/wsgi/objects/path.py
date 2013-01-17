# encoding: utf-8

from __future__ import unicode_literals

import sys
import collections

from marrow.util.compat import basestring, binary, unicode, unicodestr

try:
    from urlparse import urlparse
    from urllib import quote_plus, unquote_plus

except ImportError:
    from urllib.parse import urlparse, quote_plus, unquote_plus


__all__ = ['Path']



class Path(object):
    """An object representing the path component of a URL/URI.

    The Uniform Resource Locator (URI) RFC defines a path as:

        path          = path-abempty    ; begins with "/" or is empty
                      / path-absolute   ; begins with "/" but not "//"
                      / path-noscheme   ; begins with a non-colon segment
                      / path-rootless   ; begins with a segment
                      / path-empty      ; zero characters

        path-abempty  = *( "/" segment )
        path-absolute = "/" [ segment-nz *( "/" segment ) ]
        path-noscheme = segment-nz-nc *( "/" segment )
        path-rootless = segment-nz *( "/" segment )
        path-empty    = 0<pchar>

        segment       = *pchar
        segment-nz    = 1*pchar
        segment-nz-nc = 1*( unreserved / pct-encoded / sub-delims / "@" )
                      ; non-zero-length segment without any colon ":"

        pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"

    The full text of the RFC can be found here:

        http://pretty-rfc.herokuapp.com/RFC3986
    """


    def __init__(self, value=None, separator='/', encoded=False, encoding='utf8'):
        self.components = []
        self.separator = unicode(separator)
        self.encoded = encoded
        self.encoding = encoding

        if value is not None:
            self.replace(value)

    def __set__(self, obj, value):
        self.replace(value)
    
    def __unicode__(self):
        if self[:1] == [self.separator]:
            return self.separator + self.separator.join((quote_plus(i) if self.encoded else i) for i in self[1:])
        
        return self.separator.join((quote_plus(i) if self.encoded else i) for i in self)

    def __bytes__(self):
        if self[:1] == [self.separator]:
            sep = self.separator.encode('ascii')
            return sep + sep.join((quote_plus(i.encode(self.encoding)) if self.encoded else i) for i in self[1:])
        
        return self.separator.encode('ascii').join((quote_plus(i.encode(self.encoding)) if self.encoded else i.encode(self.encoding)) for i in self)

    if sys.version_info[0] == 2:
        __str__ = __bytes__
    else:
        __str__ = __unicode__
    
    def __add__(self, other):
        return self.copy().extend(other)

    def __repr__(self):
        return "<Path {0}>".format(self)

    def __eq__(self, other):
        if isinstance(other, basestring):
            return unicode(self) == unicode(other)

        return self.components == list(other)

    def __getitem__(self, i):
        return Path(self.components[i])

    def __abs__(self):
        if self[:1] == [self.separator]:
            return self.copy()
        
        return Path(self.separator, self.separator, self.encoded, self.encoding) + self

    def __len__(self):
        return len(self.components)

    def __setitem__(self, key, value):
        self.components[key] = value

    def __delitem__(self, key):
        del self.components[key]
    
    def __iter__(self):
        return iter(self.components)

    def replace(self, value, encoded=None, encoding=None):
        self.encoded = encoded if encoded is not None else self.encoded
        self.encoding = encoding if encoding is not None else self.encoding

        self.clear()

        if not value:
            return self

        self.extend(value)
        return self

    def clear(self):
        self.components = []
        return self

    def extend(self, value):
        if not isinstance(value, basestring):
            self.components.extend(value)
            return self
        
        encoded = self.encoded
        encoding = self.encoding
        separator = self.separator
        
        value = value.strip()
        
        rooted = value and value[0] == self.separator
        if rooted:
            if not self.components:
                self.components.append(self.separator)
            value = value[1:]
        
        if not value:
            return self
        
        self.components.extend((unquote_plus(i) if encoded else i) for i in unicodestr(value, encoding).split(separator))
        return self
    
    def append(self, value):
        self.components.append(value)
        return self
    
    def insert(self, i, x):
        self.components.insert(i, x)
        return self
    
    def remove(self, x):
        self.components.remove(x)
        return self
    
    def copy(self):
        return self.__class__(unicode(self), self.separator, self.encoded, self.encoding)
    
    def pop(self, i=-1):
        return self.components.pop(i)
    
    def consume(self):
        return self.components.pop(0)
