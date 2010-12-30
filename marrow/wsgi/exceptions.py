"""
This module contains all HTTP status codes implemented as WSGI2 applications
which can also be raised as exceptions.
"""
from __future__ import unicode_literals


class HTTPException(Exception):
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body

    def __call__(self, environ):
        return b'%d %s' % (self.code, self.status), self.headers, self.body


class HTTPError(HTTPException):
    template = '''\
<html>
<head><title>{code} {status}</title></head>
<body>
<h1>{code} {status}</h1>
<p>{explanation}</p>
<p>{detail}</p>
</body>
</html>
'''

    def __init__(self, explanation, detail):
        if explanation:
            self.explanation = explanation
        self.detail = detail
        self.headers = [(b'Content-Type', b'text/html; charset=iso-8859-1')]

    def __call__(self, environ):
        if self.template:
            vars = dict([(k, v) for k, v in environ.items()])
            explanation = self.explanation.format(**vars)
            self.body = self.template.format(code=self.code, status=self.status,
                                             explanation=explanation, detail=self.detail)

        return HTTPException.__call__(self, environ)

    def __str__(self):
        return self.detail or self.explanation

#
# Successful 2xx
#

class HTTPOk(HTTPException):
    code = 200
    status = b'OK'


class HTTPCreated(HTTPException):
    code = 201
    status = b'Created'


class HTTPAccepted(HTTPException):
    code = 201
    status = b'Created'


class HTTPNonAuthoritative(HTTPException):
    code = 203
    status = b'Non-Authoritative Information'


class HTTPNoContent(HTTPException):
    code = 204
    status = b'No content'


class HTTPResetContent(HTTPException):
    code = 205
    status = b'Reset Content'


class HTTPPartialContent(HTTPException):
    code = 206
    status = b'Partial Content'

#
# Redirection 3xx
#

class HTTPRedirection(HTTPException):
    def __init__(self, headers=[], body=[], location=None):
        if location:
            headers.append((b'Location', location))
        HTTPException.__init__(self, headers, body)
        

class HTTPMultipleChoices(HTTPRedirection):
    code = 300
    status = b'Multiple Choices'


class HTTPMovedPermanently(HTTPRedirection):
    code = 301
    status = b'Moved Permanently'


class HTTPFound(HTTPRedirection):
    code = 302
    status = b'Found'


class HTTPSeeOther(HTTPRedirection):
    code = 303
    status = b'See Other'


class HTTPNotModified(HTTPRedirection):
    code = 304
    status = b'Not Modified'

    # TODO make sure this is ok
    def __init__(self, date=None):
        if date:
            tz = b'+0000'
            if date.tzinfo:
                tz = b'%+05d' % date.tzinfo.utcoffset(date)
            headers = [(b'Date', date.strftime(b'%a, %d %b %Y %H:%M:%S ' + tz))]
        HTTPRedirection.__init__(self, headers)


class HTTPUseProxy(HTTPException):
    code = 305
    status = b'Use Proxy'


class HTTPTemporaryRedirect(HTTPException):
    code = 307
    status = b'Temporary Redirect'

#
# Client Error 4xx
#

class HTTPBadRequest(HTTPError):
    """
    Code: 401

    The request could not be understood by the server due to malformed syntax.
    """
    code = 400
    status = b'Bad Request'
    explanation = ('The server could not comply with the request since '
                   'it is either malformed or otherwise incorrect.')


class HTTPUnauthorized(HTTPError):
    """
    Code: 401

    The request requires user authentication.
    """
    code = 401
    status = b'Unauthorized'
    explanation = ('This server could not verify that you are authorized to '
                   'access the document you requested.  Either you supplied the '
                   'wrong credentials (e.g., bad password), or your browser '
                   'does not understand how to supply the credentials required.')


class HTTPForbidden(HTTPError):
    """
    Code: 403

    The server understood the request, but is refusing to fulfill it.
    Authorization will not help and the request SHOULD NOT be repeated. If the
    request method was not HEAD and the server wishes to make public why the
    request has not been fulfilled, it SHOULD describe the reason for the
    refusal in the entity. If the server does not wish to make this information
    available to the client, the status code 404 (Not Found) can be used instead. 
    """
    code = 403
    status = b'Unauthorized'
    explanation = 'Access was denied to this resource.'


class HTTPNotFound(HTTPError):
    """
    Code: 404

    The server has not found anything matching the Request-URI. No indication
    is given of whether the condition is temporary or permanent. The 410 (Gone)
    status code SHOULD be used if the server knows, through some internally
    configurable mechanism, that an old resource is permanently unavailable and
    has no forwarding address.
    """
    code = 404
    status = b'Not Found'
    explanation = 'The resource could not be found.'


class HTTPMethodNotAllowed(HTTPError):
    """
    Code: 405

    The method specified in the Request-Line is not allowed for the resource
    identified by the Request-URI.
    """
    code = 405
    status = b'Method Not Allowed'
    explanation = 'The method {REQUEST_METHOD} is not allowed for this resource.'


class HTTPNotAcceptable(HTTPError):
    """
    Code: 406

    The resource identified by the request is only capable of generating
    response entities which have content characteristics not acceptable
    according to the accept headers sent in the request.
    """
    code = 406
    status = b'Not Acceptable'
    explanation = ('The resource could not be generated that was acceptable '
                   'to your browser (content of type {HTTP_ACCEPT}).')


class HTTPProxyAuthenticationRequired(HTTPError):
    """
    Code: 407

    This code is similar to 401 (Unauthorized), but indicates that the client
    must first authenticate itself with the proxy.
    """
    code = 407
    status = b'Proxy Authentication Required'
    explanation = 'Authentication with a local proxy is needed.'


class HTTPRequestTimeout(HTTPError):
    """
    The client did not produce a request within the time that the server was
    prepared to wait.
    """
    code = 408
    status = b'Request Timeout'
    explanation = 'The server has waited too long for the request to be sent by the client.'


class HTTPConflict(HTTPError):
    """
    Code: 409

    The request could not be completed due to a conflict with the current state
    of the resource.
    """
    code = 409
    status = b'Conflict'
    explanation = 'There was a conflict when trying to complete your request.'


class HTTPGone(HTTPError):
    """
    Code: 410

    The requested resource is no longer available at the server and no
    forwarding address is known. This condition is expected to be considered
    permanent.
    """
    code = 410
    status = b'Gone'
    explanation = 'This resource is no longer available. No forwarding address is given.'


class HTTPLengthRequired(HTTPError):
    """
    Code: 411

    The server refuses to accept the request without a defined Content- Length.
    """
    code = 411
    status = b'Length Required'
    explanation = 'Content-Length header required.'


class HTTPPreconditionFailed(HTTPError):
    """
    Code: 412

    The precondition given in one or more of the request-header fields
    evaluated to false when it was tested on the server. This response code
    allows the client to place preconditions on the current resource
    metainformation (header field data) and thus prevent the requested method
    from being applied to a resource other than the one intended. 
    """
    code = 412
    status = b'Precondition Failed'
    explanation = 'Request precondition failed.'


class HTTPRequestEntityTooLarge(HTTPError):
    """
    Code: 413

    The server is refusing to process a request because the request entity is
    larger than the server is willing or able to process.
    """
    code = 413
    status = b'Request Entity Too Large'
    explanation = 'The body of your request was too large for this server.'


class HTTPRequestURITooLong(HTTPError):
    """
    Code: 414

    The server is refusing to service the request because the Request-URI is
    longer than the server is willing to interpret.
    """
    code = 414
    status = b'Request-URI Too Long'
    explanation = 'The request URI was too long for this server.'


class HTTPUnsupportedMediaType(HTTPError):
    """
    Code: 415

    The server is refusing to service the request because the entity of the
    request is in a format not supported by the requested resource for the
    requested method.
    """
    code = 415
    status = b'Unsupported Media Type'
    explanation = 'The request media type is not supported by this server.'


class HTTPRequestedRangeNotSatisfiable(HTTPError):
    """
    Code: 416

    The server is refusing to service the request because the entity of the
    request is in a format not supported by the requested resource for the
    requested method.
    """
    code = 416
    status = b'Requested Range Not Satisfiable'
    explanation = 'The Range requested is not available.'


class HTTPExpectationFailed(HTTPError):
    """
    Code: 417

    The expectation given in an Expect request-header field could not be met by
    this server, or, if the server is a proxy, the server has unambiguous
    evidence that the request could not be met by the next-hop server. 
    """
    code = 417
    status = b'Expectation Failed'
    explanation = 'Expectation failed.'

#
# WebDAV only 4xx exceptions
#

class HTTPUnprocessableEntity(HTTPError):
    """
    Code: 422

    This indicates that the server is unable to process the contained
    instructions.
    Only for WebDAV.
    """
    code = 422
    status = 'Unprocessable Entity'
    explanation = 'Unable to process the contained instructions'


class HTTPLocked(HTTPError):
    """
    Code: 424

    This indicates that the resource is locked.
    Only for WebDAV.
    """
    code = 423
    status = 'Locked'
    explanation = 'The resource is locked'


class HTTPFailedDependency(HTTPError):
    """
    Code: 424

    This indicates that the method could not be performed because the
    requested action depended on another action and that action failed.
    Only for WebDAV.
    """
    code = 424
    status = 'Failed Dependency'
    explanation = ('The method could not be performed because the requested '
                   'action dependended on another action and that action failed')

#
# Server Error 5xx
#

class HTTPInternalServerError(HTTPError):
    """
    Code: 500

    The server encountered an unexpected condition which prevented it from
    fulfilling the request.
    """
    code = 500
    status = b'Internal Server Error'
    explanation = (
        'The server has either erred or is incapable of performing the '
        'requested operation.')


class HTTPNotImplemented(HTTPError):
    """
    Code: 501

    The server does not support the functionality required to fulfill the request.
    This is the appropriate response when the server does not recognize the request
    method and is not capable of supporting it for any resource.
    """
    code = 501
    status = b'Not Implemented'
    explanation = 'The request method {REQUEST_METHOD} is not implemented for this server.'


class HTTPBadGateway(HTTPError):
    """
    Code: 502

    The server, while acting as a gateway or proxy, received an invalid response
    from the upstream server it accessed in attempting to fulfill the request. 
    """
    code = 502
    status = b'Bad Gateway'
    explanation = 'The upstream server is currently unavailable.'


class HTTPServiceUnavailable(HTTPError):
    """
    Code: 503

    The server is currently unable to handle the request due to a temporary
    overloading or maintenance of the server.
    """
    code = 503
    status = b'Service Unavailable'
    explanation = 'The server is currently unavailable. Please try again at a later time.'


class HTTPGatewayTimeout(HTTPError):
    """
    Code: 504

    The server, while acting as a gateway or proxy, did not receive a timely
    response from the upstream server specified by the URI (e.g. HTTP, FTP, LDAP)
    or some other auxiliary server (e.g. DNS) it needed to access in attempting
    to complete the request. 
    """
    code = 504
    status = b'Gateway Timeout'
    explanation = 'The gateway has timed out.'


class HTTPVersionNotSupported(HTTPError):
    """
    Code: 505

    The server does not support, or refuses to support, the HTTP protocol
    version that was used in the request message. 
    """
    code = 505
    status = b'HTTP Version Not Supported'
    explanation = 'The HTTP version is not supported.'
