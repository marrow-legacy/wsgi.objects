# encoding: utf-8

"""This module contains all HTTP status codes implemented as WSGI 2 applications which can also be raised as exceptions."""

from __future__ import unicode_literals


__all__ = []



class HTTPException(Exception):
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body
    
    def __call__(self, environ):
        return b'%d %s' % (self.code, self.status), self.headers, self.body


class HTTPError(HTTPException):
    template = '''<html>
<head><title>{code} {status}</title></head>
<body>
<h1>{code} {status}</h1>
<p>{explanation}</p>
<div>{detail}</div>
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
            self.body = self.template.format(
                    code = self.code,
                    status = self.status,
                    explanation = explanation,
                    detail = self.detail
                )
        
        return super(HTTPError, self).__call__(environ)
    
    def __str__(self):
        return self.detail or self.explanation



# Informational - 1xx

class HTTPInformational(HTTPException):
    """The base class from which HTTP 1xx status code exceptions are derived.
    
    This class of status code indicates a provisional response, consisting
    only of the Status-Line and optional headers, and is terminated by an
    empty line. There are no required headers for this class of status code.
    Since HTTP/1.0 did not define any 1xx status codes, servers MUST NOT send
    a 1xx response to an HTTP/1.0 client except under experimental conditions.
    
    For information, see RFC 2616 §10.1:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1
    """
    pass


class HTTPContinue(HTTPInformational):
    """100 Continue
    
    The client SHOULD continue with its request. This interim response
    is used to inform the client that the initial part of the request
    has been received and has not yet been rejected by the server. The
    client SHOULD continue by sending the remainder of the request or,
    if the request has already been completed, ignore this response.
    The server MUST send a final response after the request has been
    completed.
    
    For information, see RFC 2616 §10.1.1:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.1
    """
    
    code = 100
    status = b'Continue'


class HTTPSwitchingProtocols(HTTPInformational):
    """101 Switching Protocols
    
    The server understands and is willing to comply with the client's
    request, via the Upgrade message header field (section 14.42), for
    a change in the application protocol being used on this connection.
    The server will switch protocols to those defined by the response's
    Upgrade header field immediately after the empty line which
    terminates the 101 response.
    
    The protocol SHOULD be switched only when it is advantageous to do
    so. For example, switching to a newer version of HTTP is
    advantageous over older versions, and switching to a real-time,
    synchronous protocol might be advantageous when delivering
    resources that use such features.
    
    For information, see RFC 2616 §10.1.2:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.2
    """
    
    code = 101
    status = b'Switching Protocols'



# Successful - 2xx

class HTTPSuccess(HTTPException):
    """The base class from which HTTP 2xx status code exceptions are derived.
    
    This class of status code indicates that the client's request was
    successfully received, understood, and accepted.
    
    For information, see RFC 2616 §10.2:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2
    """
    pass


class HTTPOk(HTTPSuccess):
    """200 OK
    
    The request has succeeded. The information returned with the response is
    dependent on the method used in the request.
    
    For information, see RFC 2616 §10.2.1:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    
    code = 200
    status = b'OK'


class HTTPCreated(HTTPSuccess):
    """201 Created
    
    The request has been fulfilled and resulted in a new resource being
    created. The newly created resource can be referenced by the URI(s)
    returned in the entity of the response, with the most specific URI for the
    resource given by a Location header field. The response SHOULD include an
    entity containing a list of resource characteristics and location(s) from
    which the user or user agent can choose the one most appropriate. The
    entity format is specified by the media type given in the Content-Type
    header field. The origin server MUST create the resource before returning
    the 201 status code. If the action cannot be carried out immediately, the
    server SHOULD respond with 202 (Accepted) response instead.
    
    A 201 response MAY contain an ETag response header field indicating the
    current value of the entity tag for the requested variant just created.
    
    For information, see RFC 2616 §10.2.2:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.2
    """
    
    code = 201
    status = b'Created'


class HTTPAccepted(HTTPSuccess):
    """202 Accepted
    
    The request has been accepted for processing, but the processing has not been completed. The request might or might not eventually be acted upon, as it might be disallowed when processing actually takes place. There is no facility for re-sending a status code from an asynchronous operation such as this.
    
    The 202 response is intentionally non-committal. Its purpose is to allow a server to accept a request for some other process (perhaps a batch-oriented process that is only run once per day) without requiring that the user agent's connection to the server persist until the process is completed. The entity returned with this response SHOULD include an indication of the request's current status and either a pointer to a status monitor or some estimate of when the user can expect the request to be fulfilled.
    
    For information, see RFC 2616 §10.2.3:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.3
    """
    
    code = 202
    status = b'Created'


class HTTPNonAuthoritative(HTTPSuccess):
    """203 Non-Authoritative Information
    
    The returned metainformation in the entity-header is not the definitive
    set as available from the origin server, but is gathered from a local or a
    third-party copy. The set presented MAY be a subset or superset of the
    original version. For example, including local annotation information
    about the resource might result in a superset of the metainformation known
    by the origin server. Use of this response code is not required and is
    only appropriate when the response would otherwise be 200 (OK).
    
    For information, see RFC 2616 §10.2.4:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.4
    """
    
    code = 203
    status = b'Non-Authoritative Information'


class HTTPNoContent(HTTPSuccess):
    """204 No Content
    
    The server has fulfilled the request but does not need to return an
    entity-body, and might want to return updated metainformation. The
    response MAY include new or updated metainformation in the form of
    entity-headers, which if present SHOULD be associated with the requested
    variant.
    
    If the client is a user agent, it SHOULD NOT change its document view from
    that which caused the request to be sent. This response is primarily
    intended to allow input for actions to take place without causing a change
    to the user agent's active document view, although any new or updated
    metainformation SHOULD be applied to the document currently in the user
    agent's active view.
    
    The 204 response MUST NOT include a message-body, and thus is always
    terminated by the first empty line after the header fields.
    
    For information, see RFC 2616 §10.2.5:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.5
    """
    
    code = 204
    status = b'No content'


class HTTPResetContent(HTTPSuccess):
    """205 Reset Content
    
    The server has fulfilled the request and the user agent SHOULD reset the
    document view which caused the request to be sent. This response is
    primarily intended to allow input for actions to take place via user
    input, followed by a clearing of the form in which the input is given so
    that the user can easily initiate another input action. The response MUST
    NOT include an entity.
    
    For information, see RFC 2616 §10.2.6:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.6
    """
    
    code = 205
    status = b'Reset Content'


class HTTPPartialContent(HTTPSuccess):
    """206 Partial Content
    
    The server has fulfilled the partial GET request for the resource.
    
    This status code should be used with caution, as there are a number of
    specific requirements for its use.
    
    For information, see RFC 2616 §10.2.7:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.7
    """
    
    code = 206
    status = b'Partial Content'



# Redirection 3xx

class HTTPRedirection(HTTPException):
    """The base class from which HTTP 3xx status code exceptions are derived.
    
    This class of status code indicates that further action needs to be taken
    by the user agent in order to fulfill the request. The action required MAY
    be carried out by the user agent without interaction with the user if and
    only if the method used in the second request is GET or HEAD. A client
    SHOULD detect infinite redirection loops, since such loops generate
    network traffic for each redirection.
    
    For information, see RFC 2616 §10.3:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3
    """
    
    def __init__(self, headers=[], body=[], location=None):
        if location:
            headers.append((b'Location', location))
        HTTPException.__init__(self, headers, body)


class HTTPMultipleChoices(HTTPRedirection):
    """300 Multiple Choices
    
    The requested resource corresponds to any one of a set of representations,
    each with its own specific location, and agent-driven negotiation
    information is being provided so that the user (or user agent) can select
    a preferred representation and redirect its request to that location.
    
    Unless it was a HEAD request, the response SHOULD include an entity
    containing a list of resource characteristics and location(s) from which
    the user or user agent can choose the one most appropriate. The entity
    format is specified by the media type given in the Content-Type header
    field. Depending upon the format and the capabilities of the user agent,
    selection of the most appropriate choice MAY be performed automatically.
    
    If the server has a preferred choice of representation, it SHOULD include
    the specific URI for that representation in the Location field; user
    agents MAY use the Location field value for automatic redirection. This
    response is cacheable unless indicated otherwise.
    
    For information, see RFC 2616 §10.3.1:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.1
    """
    
    code = 300
    status = b'Multiple Choices'


class HTTPMovedPermanently(HTTPRedirection):
    """301 Moved Permanently
    
    The requested resource has been assigned a new permanent URI and any
    future references to this resource SHOULD use one of the returned URIs.
    Clients with link editing capabilities ought to automatically re-link
    references to the Request-URI to one or more of the new references
    returned by the server, where possible. This response is cacheable unless
    indicated otherwise.
    
    The new permanent URI SHOULD be given by the Location field in the
    response. Unless the request method was HEAD, the entity of the response
    SHOULD contain a short hypertext note with a hyperlink to the new URI(s).
    
    If the 301 status code is received in response to a request other than GET
    or HEAD, the user agent MUST NOT automatically redirect the request unless
    it can be confirmed by the user, since this might change the conditions
    under which the request was issued.
    
          Note: When automatically redirecting a POST request after
          receiving a 301 status code, some existing HTTP/1.0 user agents
          will erroneously change it into a GET request.
    
    For information, see RFC 2616 §10.3.2:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.2
    """
    
    code = 301
    status = b'Moved Permanently'


class HTTPFound(HTTPRedirection):
    """302 Found
    
    The requested resource resides temporarily under a different URI. Since
    the redirection might be altered on occasion, the client SHOULD continue
    to use the Request-URI for future requests. This response is only
    cacheable if indicated by a Cache-Control or Expires header field.
    
    The temporary URI SHOULD be given by the Location field in the response.
    Unless the request method was HEAD, the entity of the response SHOULD
    contain a short hypertext note with a hyperlink to the new URI(s).
    
    If the 302 status code is received in response to a request other than GET
    or HEAD, the user agent MUST NOT automatically redirect the request unless
    it can be confirmed by the user, since this might change the conditions
    under which the request was issued.
    
          Note: RFC 1945 and RFC 2068 specify that the client is not allowed
          to change the method on the redirected request.  However, most
          existing user agent implementations treat 302 as if it were a 303
          response, performing a GET on the Location field-value regardless
          of the original request method. The status codes 303 and 307 have
          been added for servers that wish to make unambiguously clear which
          kind of reaction is expected of the client.
    
    For information, see RFC 2616 §10.3.3:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.3
    """
    
    code = 302
    status = b'Found'


class HTTPSeeOther(HTTPRedirection):
    """303 See Other
    
    The response to the request can be found under a different URI and SHOULD
    be retrieved using a GET method on that resource. This method exists
    primarily to allow the output of a POST-activated script to redirect the
    user agent to a selected resource. The new URI is not a substitute
    reference for the originally requested resource. The 303 response MUST NOT
    be cached, but the response to the second (redirected) request might be
    cacheable.
    
    The different URI SHOULD be given by the Location field in the response.
    Unless the request method was HEAD, the entity of the response SHOULD
    contain a short hypertext note with a hyperlink to the new URI(s).
    
          Note: Many pre-HTTP/1.1 user agents do not understand the 303
          status. When interoperability with such clients is a concern, the
          302 status code may be used instead, since most user agents react
          to a 302 response as described here for 303.
    
    For information, see RFC 2616 §10.3.4:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.4
    """
    
    code = 303
    status = b'See Other'


class HTTPNotModified(HTTPRedirection):
    """304 Not Modified
    
    If the client has performed a conditional GET request and access is
    allowed, but the document has not been modified, the server SHOULD respond
    with this status code. The 304 response MUST NOT contain a message-body,
    and thus is always terminated by the first empty line after the header
    fields.
    
    This status code should be used with caution, as there are a number of
    specific requirements for its use.
    
    For information, see RFC 2616 §10.3.5:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.5
    """
    
    code = 304
    status = b'Not Modified'


class HTTPUseProxy(HTTPRedirection):
    """305 Use Proxy
    
    The requested resource MUST be accessed through the proxy given by the
    Location field. The Location field gives the URI of the proxy. The
    recipient is expected to repeat this single request via the proxy. 305
    responses MUST only be generated by origin servers.
    
    For information, see RFC 2616 §10.3.6:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.6
    """
    
    code = 305
    status = b'Use Proxy'


class HTTPTemporaryRedirect(HTTPRedirection):
    """307 Temporary Redirect
    
    The requested resource resides temporarily under a different URI. Since
    the redirection MAY be altered on occasion, the client SHOULD continue to
    use the Request-URI for future requests. This response is only cacheable
    if indicated by a Cache-Control or Expires header field.
    
    The temporary URI SHOULD be given by the Location field in the response.
    Unless the request method was HEAD, the entity of the response SHOULD
    contain a short hypertext note with a hyperlink to the new URI(s), since
    many pre-HTTP/1.1 user agents do not understand the 307 status. Therefore,
    the note SHOULD contain the information necessary for a user to repeat the
    original request on the new URI.
    
    If the 307 status code is received in response to a request other than GET
    or HEAD, the user agent MUST NOT automatically redirect the request unless
    it can be confirmed by the user, since this might change the conditions
    under which the request was issued.
    
    For information, see RFC 2616 §10.3.8:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.8
    """
    
    code = 307
    status = b'Temporary Redirect'



# Client Error 4xx

class HTTPClientError(HTTPError):
    """"""
    pass

class HTTPBadRequest(HTTPClientError):
    """
    Code: 401
    
    The request could not be understood by the server due to malformed syntax.
    """
    code = 400
    status = b'Bad Request'
    explanation = ('The server could not comply with the request since '
                   'it is either malformed or otherwise incorrect.')


class HTTPUnauthorized(HTTPClientError):
    """
    Code: 401
    
    The request requires user authentication.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 401
    status = b'Unauthorized'
    explanation = ('This server could not verify that you are authorized to '
                   'access the document you requested.  Either you supplied the '
                   'wrong credentials (e.g., bad password), or your browser '
                   'does not understand how to supply the credentials required.')


class HTTPForbidden(HTTPClientError):
    """
    Code: 403
    
    The server understood the request, but is refusing to fulfill it.
    Authorization will not help and the request SHOULD NOT be repeated. If the
    request method was not HEAD and the server wishes to make public why the
    request has not been fulfilled, it SHOULD describe the reason for the
    refusal in the entity. If the server does not wish to make this information
    available to the client, the status code 404 (Not Found) can be used instead. 
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 403
    status = b'Unauthorized'
    explanation = 'Access was denied to this resource.'


class HTTPNotFound(HTTPClientError):
    """
    Code: 404
    
    The server has not found anything matching the Request-URI. No indication
    is given of whether the condition is temporary or permanent. The 410 (Gone)
    status code SHOULD be used if the server knows, through some internally
    configurable mechanism, that an old resource is permanently unavailable and
    has no forwarding address.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 404
    status = b'Not Found'
    explanation = 'The resource could not be found.'


class HTTPMethodNotAllowed(HTTPClientError):
    """
    Code: 405
    
    The method specified in the Request-Line is not allowed for the resource
    identified by the Request-URI.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 405
    status = b'Method Not Allowed'
    explanation = 'The method {REQUEST_METHOD} is not allowed for this resource.'


class HTTPNotAcceptable(HTTPClientError):
    """
    Code: 406
    
    The resource identified by the request is only capable of generating
    response entities which have content characteristics not acceptable
    according to the accept headers sent in the request.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 406
    status = b'Not Acceptable'
    explanation = ('The resource could not be generated that was acceptable '
                   'to your browser (content of type {HTTP_ACCEPT}).')


class HTTPProxyAuthenticationRequired(HTTPClientError):
    """
    Code: 407
    
    This code is similar to 401 (Unauthorized), but indicates that the client
    must first authenticate itself with the proxy.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 407
    status = b'Proxy Authentication Required'
    explanation = 'Authentication with a local proxy is needed.'


class HTTPRequestTimeout(HTTPClientError):
    """
    Code: 408
    
    The client did not produce a request within the time that the server was
    prepared to wait.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 408
    status = b'Request Timeout'
    explanation = 'The server has waited too long for the request to be sent by the client.'


class HTTPConflict(HTTPClientError):
    """
    Code: 409
    
    The request could not be completed due to a conflict with the current state
    of the resource.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 409
    status = b'Conflict'
    explanation = 'There was a conflict when trying to complete your request.'


class HTTPGone(HTTPClientError):
    """
    Code: 410
    
    The requested resource is no longer available at the server and no
    forwarding address is known. This condition is expected to be considered
    permanent.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 410
    status = b'Gone'
    explanation = 'This resource is no longer available. No forwarding address is given.'


class HTTPLengthRequired(HTTPClientError):
    """
    Code: 411
    
    The server refuses to accept the request without a defined Content-Length.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 411
    status = b'Length Required'
    explanation = 'Content-Length header required.'


class HTTPPreconditionFailed(HTTPClientError):
    """
    Code: 412
    
    The precondition given in one or more of the request-header fields
    evaluated to false when it was tested on the server. This response code
    allows the client to place preconditions on the current resource
    metainformation (header field data) and thus prevent the requested method
    from being applied to a resource other than the one intended. 
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 412
    status = b'Precondition Failed'
    explanation = 'Request precondition failed.'


class HTTPRequestEntityTooLarge(HTTPClientError):
    """
    Code: 413
    
    The server is refusing to process a request because the request entity is
    larger than the server is willing or able to process.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 413
    status = b'Request Entity Too Large'
    explanation = 'The body of your request was too large for this server.'


class HTTPRequestURITooLong(HTTPClientError):
    """
    Code: 414
    
    The server is refusing to service the request because the Request-URI is
    longer than the server is willing to interpret.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 414
    status = b'Request-URI Too Long'
    explanation = 'The request URI was too long for this server.'


class HTTPUnsupportedMediaType(HTTPClientError):
    """
    Code: 415
    
    The server is refusing to service the request because the entity of the
    request is in a format not supported by the requested resource for the
    requested method.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 415
    status = b'Unsupported Media Type'
    explanation = 'The request media type is not supported by this server.'


class HTTPRequestedRangeNotSatisfiable(HTTPClientError):
    """
    Code: 416
    
    The server is refusing to service the request because the entity of the
    request is in a format not supported by the requested resource for the
    requested method.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 416
    status = b'Requested Range Not Satisfiable'
    explanation = 'The Range requested is not available.'


class HTTPExpectationFailed(HTTPClientError):
    """
    Code: 417
    
    The expectation given in an Expect request-header field could not be met by
    this server, or, if the server is a proxy, the server has unambiguous
    evidence that the request could not be met by the next-hop server. 
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 417
    status = b'Expectation Failed'
    explanation = 'Expectation failed.'



# Server Error 5xx

class HTTPServerError(HTTPError):
    """"""
    pass


class HTTPInternalServerError(HTTPServerError):
    """
    Code: 500
    
    The server encountered an unexpected condition which prevented it from
    fulfilling the request.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 500
    status = b'Internal Server Error'
    explanation = (
        'The server has either erred or is incapable of performing the '
        'requested operation.')


class HTTPNotImplemented(HTTPServerError):
    """
    Code: 501
    
    The server does not support the functionality required to fulfill the request.
    This is the appropriate response when the server does not recognize the request
    method and is not capable of supporting it for any resource.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 501
    status = b'Not Implemented'
    explanation = 'The request method {REQUEST_METHOD} is not implemented for this server.'


class HTTPBadGateway(HTTPServerError):
    """
    Code: 502
    
    The server, while acting as a gateway or proxy, received an invalid response
    from the upstream server it accessed in attempting to fulfill the request. 
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 502
    status = b'Bad Gateway'
    explanation = 'The upstream server is currently unavailable.'


class HTTPServiceUnavailable(HTTPServerError):
    """
    Code: 503
    
    The server is currently unable to handle the request due to a temporary
    overloading or maintenance of the server.
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 503
    status = b'Service Unavailable'
    explanation = 'The server is currently unavailable. Please try again at a later time.'


class HTTPGatewayTimeout(HTTPServerError):
    """
    Code: 504
    
    The server, while acting as a gateway or proxy, did not receive a timely
    response from the upstream server specified by the URI (e.g. HTTP, FTP, LDAP)
    or some other auxiliary server (e.g. DNS) it needed to access in attempting
    to complete the request. 
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 504
    status = b'Gateway Timeout'
    explanation = 'The gateway has timed out.'


class HTTPVersionNotSupported(HTTPServerError):
    """
    Code: 505
    
    The server does not support, or refuses to support, the HTTP protocol
    version that was used in the request message. 
    
    For information, see RFC 2616 §10.:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
    """
    code = 505
    status = b'HTTP Version Not Supported'
    explanation = 'The HTTP version is not supported.'

#
# WebDAV exceptions (RFC 2518)


class WebDAVException(Exception):
    pass


class HTTPUnprocessableEntity(HTTPClientError, WebDAVException):
    """
    Code: 422; Only for WebDAV
    
    The 422 (Unprocessable Entity) status code means the server understands the
    content type of the request entity, and the syntax of the request entity is
    correct but was unable to process the contained instructions.
    
    For information, see RFC 2518 §10.:
    http://tools.ietf.org/html/rfc2518
    """
    code = 422
    status = 'Unprocessable Entity'
    explanation = 'Unable to process the contained instructions'


class HTTPLocked(HTTPClientError, WebDAVException):
    """
    Code: 423; Only for WebDAV
    
    The 423 (Locked) status code means the source or destination resource of a
    method is locked.
    
    For information, see RFC 2518 §10.:
    http://tools.ietf.org/html/rfc2518
    """
    code = 423
    status = 'Locked'
    explanation = 'The resource is locked'


class HTTPFailedDependency(HTTPClientError, WebDAVException):
    """
    Code: 424; Only for WebDAV
    
    The 424 (Failed Dependency) status code means that the method could not be
    performed on the resource because the requested action depended on another
    action and that action failed.
    
    For information, see RFC 2518 §10.:
    http://tools.ietf.org/html/rfc2518
    """
    code = 424
    status = 'Failed Dependency'
    explanation = ('The method could not be performed because the requested '
                   'action dependended on another action and that action failed')


class HTTPInsufficientStorage(HTTPServerError, WebDAVException):
    """
    Code: 507; Only for WebDAV
    
    The 507 (Insufficient Storage) status code means the method could not be
    performed on the resource because the server is unable to store the
    representation needed to successfully complete the request.
    
    For information, see RFC 2518 §10.:
    http://tools.ietf.org/html/rfc2518
    """
    code = 507
    status = b'Insufficient Storage'
    explanation = 'There was not enough space to save the resource.'
