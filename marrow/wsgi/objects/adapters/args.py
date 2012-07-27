# encoding: utf-8

import cgi

try:
    from urllib import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl

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
    
    encoding = obj.charset or "utf-8"
    
    kwargs.update(parse_qsl(obj.parameters, True, False, encoding))
    kwargs.update(parse_qsl(obj.query, True, False, encoding))
    
    # TODO: THIS IS INSECURE AND BAD AND FULL OF BADNESS
    # But cgi.FieldStorage sucks zombies.
    if obj.method in ('POST', 'PUT') and obj.mime in ('', None, 'application/x-www-form-urlencoded'):  # , 'multipart/form-data'
        print("ADA")
        obj.body.seek(0)
        kwargs.update(parse_qsl(obj.body.read().decode(encoding), True, False, encoding))
    
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

        # remainder

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

