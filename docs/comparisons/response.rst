===========================
 Response Comparison Table
===========================

b=WebOb
z=Werkzeug
y=WebOb & Werkzeug
m=Marrow WSGI Objects
w=WebOb & Marrow
k=Werkzeug & Marrow
x=all
 =none

WEBOB NAME                         write  read  WERKZEUG NAME                       MARROW NAME                         NOTES
=================================  =====  ====  ==================================  ==================================  ==================================================================
default_content_type                 x      x   default_mimetype                    defaults.mime                       wb/wc default: "text/html", wz: "text/plain"
default_charset                      w      w                                       defaults.encoding                   wz uses class var default for charset
charset                              x      x   charset                             encoding                            
unicode_errors                       b      b                                                                           
default_conditional_response         b      b                                                                           
from_file() (classmethod)            b      b                                       factory() (classmethod)             wc detects file-like, str, unicode
copy                                 b      b                                                                           wc defines __copy__
status (string)                      x      x   status                              status                              wc uses a rich object that defines __str__ and __int__
status_int                           x      x   status_code                         status                              
                                     m      k   default_status                      defaults.status                     
headers                              w      w                                       headers                             wc acts as a dictlike object accessing the headers
body                                 w      w                                       body                                wc uses duck-typing to determine written type, returning original
unicode_body                         x      x   data                                body                                
body_file                            m      b                                       body                                File-like obj returned is writeable
app_iter                             w      x   get_app_iter()                      body                                
                                            z   iter_encoded()                                                          
allow                                w      x   allow                               allow                               
vary                                 w      x   vary                                vary                                
content_type                         y      y   content_type                                                            
content_type_params                  y      y   mime_type_params                                                        
                                     k      k   mime_type                           mime                                content_type str wo parameters
content_length                       x      x   content_length                      length                              
content_encoding                     x      x   content_encoding                    encoding                            
content_language                     w      x   content_language                    language                            
content_location                     x      x   content_location                    location                            
content_md5                          x      x   content_md5                         hash                                
content_disposition                  w      w                                       disposition                         
accept_ranges                        w      w                                       ranges                              
content_range                        w      w                                       range                               
date                                 x      x   date                                date                                
expires                              x      x   expires                             expires                             
last_modified                        x      x   last_modified                       modified                            
cache_control                        w      k   cache_control                       cache                               
cache_expires (dwim)                 w      w                                       expires                             
conditional_response (bool)          b      x   make_conditional()                  conditional                         
etag                                 b      x   add_etag()                          etag                                
etag                                 b      x   get_etag()                          etag                                
etag                                 b      x   set_etag()                          etag                                
                                            z   freeze()                                                                
location                             x      x   location                            location                            
pragma                               b      b                                       pragma                              
age                                  x      x   age                                 age                                 
retry_after                          x      x   retry_after                         retry                               
server                               b      b                                       server                              
www_authenticate                     b      z   www_authenticate                    authenticate                        
                                     x      x   date                                date                                
set_cookie()                                    set_cookie()                        cookies                             wc uses a combined dict- and list-like object of named tuples
delete_cookie()                                 delete_cookie()                     cookies                             
unset_cookie()                                                                      cookies                             
                                            z   is_streamed                                                             
                                            z   is_sequence                                                             
body_file                                   x   stream                              body                                
                                                close()                                                                 
                                                get_wsgi_headers()                  wsgi (property)                     wc returns a 3-tuple of status, headers, body_iter
                                                get_wsgi_response()                 wsgi (property)                     
__call__()                                      __call__()                          __call__()                          
