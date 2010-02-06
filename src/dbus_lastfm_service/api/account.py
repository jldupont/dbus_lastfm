"""
    DBus based API - Account
    @author: jldupont
"""
import dbus.service

from dbus_lastfm_service.mbus import Bus


class DbusApiAccount(dbus.service.Object):
    """
    API - mixin pattern
    """
    def __init__(self):
        bus_name = dbus.service.BusName('fm.lastfm.api', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/account')
        self._cache={}
        self._enable=False
        Bus.publish(self, "user_params?")
        
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
        
    ## ================================================================ Account interface
        
    @dbus.service.method('fm.last.api.account', out_signature="s")
    def getUsername(self):
        self.gatePublish("user_params?")
        return self._cache.get("username", "")

    @dbus.service.method('fm.last.api.account', in_signature="s")
    def setUsername(self, username):
        self.gatePublish("user_params", {"username":username})
        
    @dbus.service.method('fm.last.api.account', in_signature="s")
    def setApiKey(self, api_key):
        self.gatePublish("user_params", {"api_key":api_key})
        
    @dbus.service.method('fm.last.api.account', in_signature="s")
    def setSecretKey(self, secret_key):
        self.gatePublish("user_params", {"secret_key":secret_key})

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
        self.gatePublish("method_call", {"method":"auth.getToken"}, 
                    {"c":_callback, "e":_errback})

    @dbus.service.method('fm.last.api.account') 
    def clearSession(self):
        """
        Clears all session related user parameters
        """
        self.gatePublish("user_params", {"auth_token":"", "token":""})


    
api=DbusApiAccount()
Bus.subscribe("user_params", api._snif_user_params)
