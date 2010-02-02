"""
    DBus based API
    @author: jldupont
"""
import dbus.service
#from twisted.python import log

from mbus import Bus


class LastfmApi(dbus.service.Object):
    """
    API - mixin pattern
    """
    def __init__(self):
        bus_name = dbus.service.BusName('fm.lastfm.api', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/')
        self._cache={}
        
    ## ================================================================ Bus interface
    def _snif_user_params(self, _, user_params):
        """
        "Snif" the user parameters transported on the Bus
        """
        self._cache.update(user_params)        
        
    ## ================================================================ Account interface
        
    @dbus.service.method('fm.last.api.account', out_signature="s")
    def getUsername(self):
        Bus.publish(self, "user_params?")
        return self._cache.get("username", "")

    @dbus.service.method('fm.last.api.account', in_signature="s")
    def setUsername(self, username):
        Bus.publish(self, "user_params", {"username":username})
        
    @dbus.service.method('fm.last.api.account', in_signature="s")
    def setApiKey(self, api_key):
        Bus.publish(self, "user_params", {"api_key":api_key})
        
    @dbus.service.method('fm.last.api.account', in_signature="s")
    def setSecretKey(self, secret_key):
        Bus.publish(self, "user_params", {"secret_key":secret_key})

    ## ================================================================== Authentication

    @dbus.service.method('fm.last.api.account', 
                         out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def getAuthUrl(self, _callback, _errback):
        """
        Returns an URL pointing to an authorization page
        
        An "authorization token" must first be retrieved from Last.fm
        and thus the current session (if any) will be lost.
        """
        Bus.publish(self, "method_call", {"method":"auth.getToken"}, 
                    {"c":_callback, "e":_errback})

    @dbus.service.method('fm.last.api.account') 
    def clearSession(self):
        """
        Clears all session related user parameters
        """
        Bus.publish(self, "user_params", {"auth_token":"", "token":""})

    ## ================================================================== Track interface

    ## Return Response Code e.g. 200
    ## Return Response Headers 

    @dbus.service.method('fm.last.api.track', 
                         in_signature="ss", out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def getTags(self, artist, track, _callback, _errback):
        Bus.publish(self, "method_call", {"method":"track.getTags","artist":artist, "track":track}, 
                                    {"c":_callback, "e":_errback})
        

    @dbus.service.method('fm.last.api.track', 
                         in_signature="ssas", out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def addTags(self, artist, track, tags, _callback, _errback):
        Bus.publish(self, "method_call", {"method":"track.addTags",  
                                    "artist":artist, "track":track, "tags":tags},
                                    {"c":_callback, "e":_errback})

    @dbus.service.method('fm.last.api.track', 
                         in_signature="sss", out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def removeTag(self, artist, track, tag, _callback, _errback):
        Bus.publish(self, "method_call", {"method":"track.removeTag",  
                                    "artist":artist, "track":track, "tag":tag},
                                    {"c":_callback, "e":_errback})

    
api=LastfmApi()
Bus.subscribe("user_params", api._snif_user_params)
