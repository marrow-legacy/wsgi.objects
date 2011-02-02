# encoding: utf-8

import cgi

from marrow.util.bunch import MultiBunch
from marrow.util.object import NoDefault
from marrow.util.path import Path as PathObj

from marrow.wsgi.objects.adapters.base import *


__all__ = ['Path', 'RoutingArgs', 'RoutingKwargs']



class Path(ReaderWriter):
    def __get__(self, obj, cls):
        return PathObj(super(Path, self).__get__(obj, cls))
    
    def __set__(self, obj, value):
        super(Path, self).__set__(obj, str(value))
    
    def __del__(self, obj):
        super(Path, self).__set__(obj, '')


def _args_kwargs_default(self, obj):
    """Parse PATH_INFO, the response body, and QUERY_STRING to produce args and kwargs."""
    
    args = tuple(obj.remainder)
    
    kwargs = MultiBunch()
    
    # Process QUERY_STRING arguments.
    
    # Process HTTP body arguments, if available.
    
    if obj.method in ('POST', 'PUT') and obj.mime in ('', None, 'application/x-www-form-urlencoded', 'multipart/form-data'):
        fs_environ = obj.copy()
        fs_environ.setdefault('CONTENT_LENGTH', '0')
        fs_environ['QUERY_STRING'] = ''
        
        fs = cgi.FieldStorage(fp=obj.body, environ=fs_environ, keep_blank_values=True)
        
        if fs.list:
            for field in fs.list:
                if field in kwargs: del kwargs[field]
                
                kwargs[field] = field if field.filename else field.value
    
    return (args, kwargs)


class RoutingArgs(ReaderWriter):
    """Return the positional arguments for this request.

    For more information, see: http://wsgi.org/wsgi/Specifications/routing_args
    """

    default = _args_kwargs_default

    def __get__(self, obj, cls):
        return super(RoutingArgs, self).__get__(obj, cls)[0]

    def __set__(self, obj, value):
        super(RoutingArgs, self).__set__(obj, (value, obj.kwargs))

    def __delete__(self, obj):
        if not self.__get__(obj, None):
            return super(RoutingArgs, self).__delete__(obj)

        obj['wsgiorg.routing_args'] = ((), obj.kwargs)


class RoutingKwargs(ReaderWriter):
    """Return the named arguments for this request.
    
    For more information, see: http://wsgi.org/wsgi/Specifications/routing_args
    """
    
    default = _args_kwargs_default
    
    def __get__(self, obj, cls):
        return super(RoutingKwargs, self).__get__(obj, cls)[1]

    def __set__(self, obj, value):
        super(RoutingKwargs, self).__set__(obj, (obj.args, value))

    def __delete__(self, obj):
        if not self.__get__(obj, None):
            super(RoutingKwargs, self).__delete__(obj)
        
        obj['wsgiorg.routing_args'] = (obj.args, MultiBunch())

