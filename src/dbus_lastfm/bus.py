""" 
    GObject message Bus
    
    @author: jldupont
"""

import gobject #@UnresolvedImport

class Signals(gobject.GObject):
    """
    List of the application level signals
    """
    __gsignals__ = {
                    
        ## Announces changes in the user's Last.fm properties
        "lastfm_username_changed":     (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,)) 
        ,"lastfm_api_key_changed":     (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
        ,"lastfm_secret_key_changed":  (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
        
        ,"lastfm_secret_key_changed":  (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
    }

    def __init__(self):
        gobject.GObject.__init__(self)
        
        
class Bus(object):
    """
    Message Bus
    
    Borg Pattern
    """
    _signals=Signals()

    @classmethod
    def emit(cls, name, *pa, **kwa):
        cls._signals.emit(name, *pa, **kwa)

    @classmethod
    def add_emission_hook(cls, name, callback):
        gobject.add_emission_hook(cls._signals, name, callback)
    
mbus=Bus()


## =============================================================== Tests


if __name__=="__main__":

    def callback(signal, data):
        print "callback: signal=%s, data=%s" % (signal, data)
    
    Bus.add_emission_hook("lastfm_username_changed", callback)
    
    Bus.emit("lastfm_username_changed", "jldupont")
    