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
    """
    protocol=HTTPPageGetter
    agent="dbus_lastfm"
    
    def __init__(self, *p, **k):
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
        
    ## ==================================================  callbacks from WsProtocol
    def noPage(self, failure):
        if self.finished:
            return
        print ">>> Factory noPage"
        self.finished=True
    
    def page(self, response):
        if self.finished:
            return       
        self.finished=True
        print ">>> Factory page: %s" % ""
        print self.response_headers
    
    def clientConnectionFailed(self, _, reason):
        print ">>> clientConnectionFailed, reason: "+str(reason)
            
## ============ Test ===============

if __name__=="__main__":
    from twisted.internet import reactor
    reactor.connectTCP("www.google.ca2", 80, WsFactory("http://www.google.ca/")) #@UndefinedVariable

    reactor.run() #@UndefinedVariable