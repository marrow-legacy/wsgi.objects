# encoding: utf-8

import re

from marrow.wsgi.objects.adapters.args import *
from marrow.wsgi.objects.adapters.base import *
from marrow.wsgi.objects.adapters.body import *
from marrow.wsgi.objects.adapters.content import *
from marrow.wsgi.objects.adapters.misc import *


__all__ = [
        'Path', 'RoutingArgs', 'RoutingKwargs', # args
        'ReaderWriter', 'Int', # base
        'RequestBody', # body
        'ContentLength', 'ContentMD5', 'ContentType', 'Charset', # content
        'Host', # misc
        
        'QUOTES_RE',
    ]

QUOTES_RE = re.compile('"(.*)"')
