"""
    WebService Method
    
    @author: jldupont
    
    Helpers for creating "Method Calls" to Last.fm Web Service
    
    Signing: 
    api_keyxxxxxxxxxxmethodauth.getSessiontokenyyyyyy
    api signature = md5("api_keyxxxxxxxxxxmethodauth.getSessiontokenyyyyyyilovecher")
    
"""
from mbus import Bus

_wsMethod={
    ## ================================================= TRACK
     "track.addTags":       {"w":True,  "s":True}
    ,"track.getTags":       {"w":False, "s":True}
    ,"track.removeTag":     {"w":True,  "s":True}
    
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
    
    def __init__(self, method, write, session, **kwa):
        self.method=method
        self.params=kwa
        
        self.url=None
        self.body=None
        
        self._process()

    def _process(self):
        """
        """
        

class WsMethodHandler(object):
    """
    """
    def __init__(self):
        pass
    
    def h_umethod_call(self, _, (mdic, udic)):
        """
        @param mdic: method_call dictionary
        @param udic: user parameters dictionary
        """
        pass

    def h_auth_url(self, _):
        pass


wsh=WsMethodHandler()
Bus.subscribe("umethod_call", wsh.h_umethod_call)
Bus.subscribe("auth_url",     wsh.h_auth_url)

    