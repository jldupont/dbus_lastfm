"""
    WebService Method
    
    @author: jldupont
    
    Helpers for creating "Method Calls" to Last.fm Web Service
    
"""
from hashlib import md5
from mbus import Bus
from ws import make_ws_request

_wsMethod={
    ## ================================================= AUTHEN
    "auth.gettoken":        {"w":False, "s":False}
    
    ## ================================================= TRACK
    ,"track.addtags":       {"w":True,  "s":True}
    ,"track.gettags":       {"w":False, "s":True}
    ,"track.removetag":     {"w":True,  "s":True}
    
    ## ================================================= USER
    ,"user.getLovedTracks":  {"w":False, "s":False}
    ,"user.getRecentTracks": {"w":False, "s":False}
    ,"user.getTopAlbums":    {"w":False, "s":False}
    ,"user.getTopArtists":   {"w":False, "s":False}
    ,"user.getTopTracks":    {"w":False, "s":False}
}


class WsMethod(object):
    """
    Prepares a Last.fm API method
    """
    API="http://ws.audioscrobbler.com/2.0/"
    HOST="ws.audioscrobbler.com"
    
    def __init__(self, wmethod, rsession, mdic, udic):
        """
        @param wmethod: "write" method
        @param ression: session required True/False 
        """
        self.wmethod=wmethod
        self.rsession=rsession
        self.mdic=mdic
        self.udic=udic
        
        if wmethod:
            self.http_method="POST"
        else:
            self.http_method="GET"
        self.url=None
        self.body=None
        
        self._process()

    def _process(self):
        """
        Actually builds the URL used for making
        the API method call
        
        If the method_call requires authentication (i.e. a "session"),
        'api_sig' is generated.
        """
        dic=self.mdic
        dic["api_key"]=self.udic.get("api_key","")
        if self.rsession:
            session=self.udic.get("session", "")
            secret=self.udic.get("secret_key", "")  
            tsign=""
            keys=sorted(dic.keys())
            for key in keys:
                tsign += key+self.mdic[key]
                tsign+=session.strip()
                tsign+=secret.strip()
            api_sig=md5(tsign)
            dic["api_sig"]=api_sig
        self.url=self.API+"?"
        for key in dic:
            self.url+=key+"="+dic[key]+"&"
        self.url=self.url.strip("&")
        #Bus.publish(self, "log", "url: %s" % self.url)
        
        

class WsMethodHandler(object):
    """
    Handler for API requests that need
    to be sent off to Last.fm
    """
    def __init__(self):
        pass
    
    def h_umethod_call(self, _, (mdic, cdic, udic)):
        """
        @param mdic: method_call dictionary
        @param cdic: callback dictionary
        @param udic: user parameters dictionary
        """
        method=mdic.get("method", "")
        mdetails=_wsMethod.get(method, None)
        if not mdetails:
            errback=cdic["e"]
            errback(["error", "unsupported_method", "unknown method: %s" + method])
            return
        wmethod=mdetails.get("w", False)
        srequired=mdetails.get("s", False)
       
        ws_method=WsMethod(wmethod, srequired, {"method":method}, udic)
        ctx=(method, cdic, udic)        
        make_ws_request(ctx, ws_method.url, http_method=ws_method.http_method)        
        


wsh=WsMethodHandler()
Bus.subscribe("umethod_call", wsh.h_umethod_call)

    