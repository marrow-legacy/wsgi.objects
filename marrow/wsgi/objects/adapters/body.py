# encoding: utf-8

from marrow.util.compat import binary, bytestring, unicode
from marrow.wsgi.objects.adapters.base import ReaderWriter


__all__ = ['RequestBody']



class RequestBody(ReaderWriter):
    """Access the request body (wsgi.input) as a binary file-like object.
    
    Assigning a value (or deleting it) will set the corresponding CONTENT_LENGTH header.
    
     * Sets CONTENT_LENGTH to the length of the binary (or encoded unicode) value.
     * Sets CONTENT_LENGTH to -1 if you assign a non-binary or non-unicode value.
     * Sets CONTENT_LENGTH to 0 if you delete the value.
    """
    
    def __set__(self, obj, value):
        if isinstance(value, binary):
            obj.length = len(value)
            super(RequestBody, self).__set__(obj, IO(value))
            return
        
        if isinstance(value, unicode):
            if not isinstance(obj.encoding, binary):
                raise TypeError("When assigning a unicode body an encoding must be defined.")
            
            value = value.encode(obj.encoding)
            obj.length = len(value)
            super(RequestBody, self).__set__(obj, IO(value))
            return
        
        obj.length = -1
        
        if hasattr(body, "__iter__"):
            value = flatten(value)
        
        super(RequestBody, self).__set__(obj, value)
        return
    
    def __delete__(self, obj):
        del obj.length
        self.__set__(obj, binary())
