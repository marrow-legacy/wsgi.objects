#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

from pprint import pformat

from marrow.server.http import HTTPServer
from marrow.wsgi.objects.decorator import wsgify


@wsgify
def hello(request):
    resp = request.response
    resp.mime = "text/plain"
    resp.body = "%r\n\n%s\n\n%s" % (request, request, pformat(request.__dict__))


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    HTTPServer(None, 8080, application=hello).start()
