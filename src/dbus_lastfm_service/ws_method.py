"""
    WebService Method
    
    @author: jldupont
    
    Helpers for creating "Method Calls" to Last.fm Web Service
    
    Signing: 
    api_keyxxxxxxxxxxmethodauth.getSessiontokenyyyyyy
    api signature = md5("api_keyxxxxxxxxxxmethodauth.getSessiontokenyyyyyyilovecher")
    
"""
from hashlib import md5
from mbus import Bus
from ws import make_ws_request

_wsMethod={
    ## ================================================= TRACK
     "track.addtags":       {"w":True,  "s":True}
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
        
        self.url=None
        self.body=None
        
        self._process()

    def _process(self):
        """
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
        Bus.publish(self, "log", "url: %s" % self.url)
        
        

class WsMethodHandler(object):
    """
    """
    def __init__(self):
        pass
    
    def h_umethod_call(self, _, (mdic, cdic, udic)):
        """
        @param mdic: method_call dictionary
        @param cdic: callback dictionary
        @param udic: user parameters dictionary
        """
        method=mdic.get("method", None)
        mdetails=_wsMethod.get(method, None)
        if not mdetails:
            errback=cdic["e"]
            errback("unknown method: %s" + method)
            return
        

    def h_uauth_url(self, _, (cdic, udic)):
        """
        Start an authentication flow - clear any existing session
        
        @param cdic: context dictionary i.e. callback & errback
        @param udic: user parameters dictionary
        """
        Bus.publish(self, "user_params", {"token":None, "session":None})
        method=WsMethod("auth.gettoken", False, {"method":"auth.gettoken"}, udic)
        ctx=("auth_url", cdic, udic)
        make_ws_request(ctx, method.url, http_method="GET")
        


wsh=WsMethodHandler()
Bus.subscribe("umethod_call", wsh.h_umethod_call)
Bus.subscribe("uauth_url",    wsh.h_uauth_url)

    