"""
    @author: jldupont

    Created on 2010-02-04
"""
import os
import gtk      #@UnresolvedImport

from dbus_lastfm_service.mbus import Bus

class Config:
    
    CFILE="config.glade"
    builder=None
    
    _paramsList = ["username", "api_key", "secret_key"]
    
    def __init__(self):
        self.builder = gtk.Builder()
        glade_file=self._find_file(self.CFILE)
        self.builder.add_from_file(glade_file)
        self.window = self.builder.get_object("wconfig")
        self.builder.connect_signals(self)
        self.bapply = self.builder.get_object("bapply")
        
        self.params_changed=False
        self.username_changed=False
        self.api_key_changed=False
        self.secret_key_changed=False
        
    def _find_file(self, file):
        cpath=os.path.dirname(__file__)
        return cpath+os.path.sep+file

    def h_user_params(self, _, params):
        """
        Grab the up-to-date user parameters
        
        There must be a straight mapping between
        the 'user param' in question and the widget
        used to display the parameter.
        """
        self.user_params=params
        for param in params:
            if param in self._paramsList:
                value=params[param]
                wgt=self.builder.get_object("e%s"%param)
                wgt.set_text(value)
            
                
    ## ================================================ API
    def show(self):
        Bus.publish(self, "user_params?")
        self.bapply.props.sensitive=False 
        self.window.present()
        
    def hide(self):
        self.window.hide()

    ## ================================================ Handlers
    def on_bapply_clicked(self, wbapply):
        self._publishParams()
        self._resetChanged()        
        self._applyState(False)
        return True
    
    def on_bauth_clicked(self, wbauth):
        return True
    
    def on_bclose_clicked(self, wbclose):
        self.window.hide()
        self._resetChanged()
        return True
    
    def on_eusername_changed(self, weusername):
        self.username_changed=True
        self.params_changed=True
        self._applyState(True)
        return True

    def on_eapi_key_changed(self, weapi_key):
        self.api_key_changed=True
        self.params_changed=True
        self._applyState(True)
        return True

    def on_esecret_key_changed(self, wesecret_key):
        self.secret_key_changed=True
        self.params_changed=True
        self._applyState(True)
        return True
    
    ## ========================================
    def _publishParams(self, params={}):
        """
        Publish any change
        """
        for param in self._paramsList:
            wgt=self.builder.get_object("e%s"%param)
            value=wgt.get_text()
            params[param]=value
        Bus.publish(self, "user_params", params)

    
    def _resetChanged(self):
        self.username_changed=False
        self.api_key_changed=False
        self.secret_key_changed=False
        self.params_changed=False
    
    def _applyState(self, state):
        self.bapply.props.sensitive=state
    


cfg=Config()
Bus.subscribe("user_params", cfg.h_user_params)


class App:
    def __init__(self):
        self._statusIcon=gtk.StatusIcon()
        self._statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self._statusIcon.set_visible(True)
        self._statusIcon.set_tooltip("DBus Last.fm")
        
        self._statusIcon.connect("activate", self._do_activate)
        
    def _do_activate(self, status_icon):
        cfg.show()

app=App()



def main():
    """
    Used during debugging
    """
    gtk.main()

