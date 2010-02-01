"""
    Last.fm Web Service
    
    @author: jldupont
    
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/protocols/basic.py
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/web/client.py
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/web/http.py
    
"""

from twisted.web.client import HTTPPageGetter, HTTPClientFactory


class WsFactory(HTTPClientFactory):
    """
    Single use - cannot be shared / reused

    This Factory creates a single WsProtocol instance and
    must not be recycled. This behaviour is required because
    of a limitation stemming from HTTPClientFactory.
    
    The Response Headers are accessible 
    through "response_headers".
    
    The HTTP status code is "status".
    """
    protocol=HTTPPageGetter
    agent="dbus_lastfm"
    
    def __init__(self, ctx, *p, **k):
        """
        @param url
        @param method
        @param postdata
        @param headers
        @param timeout
        @param cookies
        @param followRedirect
        @param redirectLimit
        """
        HTTPClientFactory.__init__(self, *p, agent=self.agent, **k)
        self.finished=False
        self._ctx=ctx
        
    ## ==================================================  callbacks from WsProtocol
    def noPage(self, failure):
        if self.finished:
            return
        self.finished=True        
        print ">>> Factory noPage"

    
    def page(self, response):
        if self.finished:
            return       
        self.finished=True
        print ">>> Factory page: %s" % ""
        print "status: %s" % self.status
    
    def clientConnectionFailed(self, _, reason):
        print ">>> clientConnectionFailed, reason: "+str(reason)
            
            
def make_request(ctx, url, method, postdata=None):
    """
    Makes a request
    """
    reactor.connectTCP("ws.audioscrobbler.com", 80, WsFactory(ctx, url, method=method, postdata=postdata)) #@UndefinedVariable


## ============ Test ===============

if __name__=="__main__":
    from twisted.internet import reactor
    reactor.connectTCP("www.google.ca", 80, WsFactory(None, "http://www.google.ca/")) #@UndefinedVariable

    reactor.run() #@UndefinedVariable