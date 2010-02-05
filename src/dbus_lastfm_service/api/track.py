"""
    DBus based API - Track
    @author: jldupont
"""
import dbus.service

from dbus_lastfm_service.mbus import Bus


class DbusApiTrack(dbus.service.Object):
    """
    API - mixin pattern
    """
    def __init__(self):
        bus_name = dbus.service.BusName('fm.lastfm.api', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/track')
        self._cache={}
        
    ## ================================================================ Bus interface
    def _snif_user_params(self, _, user_params):
        """
        "Snif" the user parameters transported on the Bus
        """
        self._cache.update(user_params)
        self._enable=(self._cache.get("dbus_enable", False) == "True")
        
    def gatePublish(self, *pa):
        if self._enable:
            Bus.publish(self, *pa)        

    ## ================================================================ DBus API        
        
    @dbus.service.method('fm.last.api.track', 
                         in_signature="ss", out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def getTags(self, artist, track, _callback, _errback):
        self.gatePublish("method_call", {"method":"track.getTags","artist":artist, "track":track}, 
                                    {"c":_callback, "e":_errback})
        

    @dbus.service.method('fm.last.api.track', 
                         in_signature="ssas", out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def addTags(self, artist, track, tags, _callback, _errback):
        self.gatePublish("method_call", {"method":"track.addTags",  
                                    "artist":artist, "track":track, "tags":tags},
                                    {"c":_callback, "e":_errback})

    @dbus.service.method('fm.last.api.track', 
                         in_signature="sss", out_signature="v", 
                         async_callbacks=("_callback", "_errback"))
    def removeTag(self, artist, track, tag, _callback, _errback):
        self.gatePublish("method_call", {"method":"track.removeTag",  
                                    "artist":artist, "track":track, "tag":tag},
                                    {"c":_callback, "e":_errback})

    
api=DbusApiTrack()
Bus.subscribe("user_params", api._snif_user_params)
