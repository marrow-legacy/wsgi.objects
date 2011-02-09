#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from pprint import pformat

from marrow.server.http import HTTPServer
from marrow.wsgi.objects.request import Request



def hello(request):
    request = Request(request)
    
    response = ("%r\n\n%s\n\n%s" % (request, request, pformat(request.__dict__))).encode('utf8')
    
    return b'200 OK', [(b'Content-Type', b'text/plain; encoding=utf8')], [response]


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    HTTPServer(None, 8080, application=hello).start()
