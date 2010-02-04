"""
    Last.fm Web Service
    
    @author: jldupont
    
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/protocols/basic.py
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/web/client.py
    http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/web/http.py
    
"""

from twisted.web.client import HTTPPageGetter, HTTPClientFactory
from twisted.internet import reactor
from mbus import Bus

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
        (self.method, self.cdic, _) = ctx
        self.eback=self.cdic["e"]
        ##self.cback=self.cdic["c"]
        
    ## ==================================================  callbacks from WsProtocol
    def noPage(self, failure):
        if self.finished:
            return
        self.finished=True        
        self.eback(["error", "no_page", "no page for method(%s), HTTP status(%s)" % (self.method, self.status)])
        Bus.publish(self, "error", ["api_access_error", {"status":self.status}])
    
    def page(self, response):
        if self.finished:
            return       
        self.finished=True
        Bus.publish(self, "ws_response", (self.status, self.response_headers, self._ctx, response))
    
    def clientConnectionFailed(self, _, reason):
        self.eback(["error", "conn_error", "connection to Last.fm API failed"])
        Bus.publish(self, "error", ["conn_error", {"reason":reason, "status":self.status}])
            
            
def make_ws_request(ctx, url, http_method="GET", postdata=None):
    """
    Makes a request
    @param ctx: context of request - parameter useful for processing a Response
    @param url: URL for making the request
    @param http_method: HTTP method e.g. GET, POST
    """
    #Bus.publish(None, "log", "make_ws_request: http_method(%s) postdata(%s)" % (http_method, postdata))
    headers={}
    if http_method=="POST":
        headers={"Content-Type":"application/x-www-form-urlencoded"}        

    reactor.connectTCP("ws.audioscrobbler.com", 80, WsFactory(ctx, str(url), method=http_method, postdata=postdata, headers=headers)) #@UndefinedVariable


## ============ Test ===============

if __name__=="__main__":

    reactor.connectTCP("www.google.ca", 80, WsFactory(None, "http://www.google.ca/")) #@UndefinedVariable
    reactor.run() #@UndefinedVariable
    