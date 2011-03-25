# encoding: utf-8

from marrow.util.object import NoDefault


__all__ = ['ReaderWriter', 'Int']



class ReaderWriter(object):
    default = NoDefault
    rw = True
    
    def __init__(self, header, default=NoDefault, rw=NoDefault, rfc=None):
        self.header = header
        
        if default is not NoDefault:
            self.default = default
        
        if rw is not NoDefault:
            self.rw = rw
        
        self.rfc = rfc
    
    def __repr__(self):
        return "%s()"
    
    def __get__(self, obj, cls):
        try:
            return obj[self.header]
        
        except KeyError:
            pass
        
        if self.default is not NoDefault:
            if hasattr(self.default, '__call__'):
                value = self.default(obj)
                
                # Not sure if we really want to store the value...
                # Content-Length and Content-MD5 regeneration are useful!
                # if self.rw:
                #     obj[self.header] = value
                
                return value
            
            return self.default
        
        raise AttributeError('WSGI environment does not contain %s key.' % (self.header, ))
    
    def __set__(self, obj, value):
        if not self.rw or obj.final:
            raise AttributeError('%s is a read-only value.' % (self.header, ))
        
        if value is None:
            del obj[self.header]
            return
        
        obj[self.header] = value
    
    def __delete__(self, obj):
        if not self.rw or obj.final:
            raise AttributeError('%s is a read-only value.' % (self.header, ))
        
        del obj[self.header]


class Int(ReaderWriter):
    def __get__(self, obj, cls):
        try:
            return int(super(Int, self).__get__(obj, cls))
        except AttributeError:
            return None
        except TypeError:
            return None
    
    def __set__(self, obj, value):
        super(Int, self).__set__(obj, binary(value))
