# encoding: utf-8

"""Adapters specific to requests."""

from __future__ import unicode_literals, division, print_function, absolute_import


class RequestHeaderProxy(object):
    __slots__ = ('source', )
    
    def __init__(self, source):
        self.source = source
    
    @staticmethod
    def _norm_to_env(name):
        return 'HTTP_' + name.replace(' ', '_').replace('-', '_').upper()
    
    @staticmethod
    def _norm_to_natural(name):
        if name.startswith('HTTP_'):
            name = name[5:]
        
        return name.replace('_', ' ').replace('-', ' ').title().replace(' ', '-')
    
    def get(self, name, default=None):
        name = self._norm_to_env(name)
        
        if name not in self.source:
            return default
        
        return self.source[name]
    
    def clear(self):
        for name in list(self):
            del self[name]
    
    def __getitem__(self, name):
        return self.source[self._norm_to_env(name)]
    
    def __setitem__(self, name, value):
        self.source[self._norm_to_env(name)] = value
    
    def __delitem__(self, name):
        del self.source[self._norm_to_env(name)]
    
    def __iter__(self):
        for name in sorted(self.source):
            if name.startswith('HTTP_'):
                yield self._norm_to_natural(name)
    
    def __contains__(self, name):
        return self._norm_to_env(name) in self.source



class RequestHeaders(object):
    def __get__(self, obj, cls):
        if obj is None:
            return self
        
        return RequestHeaderProxy(obj)
    
    def __set__(self, obj, value):
        proxy = RequestHeaderProxy(obj)
        proxy.clear()
        
        if not value:
            return
        
        for name, value in dict(value).items():
            proxy[name] = value
    
    def __delete__(self, obj):
        proxy = RequestHeaderProxy(obj)
        proxy.clear()
