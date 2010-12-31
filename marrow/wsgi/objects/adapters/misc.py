# encoding: utf-8

from marrow.wsgi.objects.adapters.base import *


__all__ = ['Host']



class Host(ReaderWriter):
    """Host name provided in HTTP_HOST, if present, SERVER_NAME otherwise."""
    
    def default(self, obj):
        return obj.host if obj.host else (obj.server + ':' + obj.port)
