"""
    WebService Method
    
    @author: jldupont
    
    Helpers for creating "Method Calls" to Last.fm Web Service
"""

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

class WsMethodBuilder(object):
    """
    """
    def __init__(self):
        pass

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
        
    