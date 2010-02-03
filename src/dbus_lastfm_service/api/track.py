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

    
api=DbusApiTrack()
