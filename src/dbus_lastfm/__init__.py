#!/usr/bin/env python
"""
    @author: Jean-Lou Dupont
"""
import os
import sys

import pygtk
import gtk      #@UnresolvedImport
import gobject  #@UnresolvedImport

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
        self._dowiring()
        self.builder.connect_signals(self.window, self.window)
        self.window.builder = self.builder
        
        self.window.bapply       = self.builder.get_object("bapply")
        
        self.window.wusername    = self.builder.get_object("eusername")
        self.window.wapi_key     = self.builder.get_object("eapi_key")
        self.window.wsecret_key  = self.builder.get_object("esecret_key")
        
        self.window.username_changed   = False
        self.window.api_key_changed    = False
        self.window.secret_key_changed = False
        
        

    def _find_file(self, file):
        cpath=os.path.dirname(__file__)
        return cpath+os.path.sep+file

    def _dowiring(self):
        """
        Wires the GTK dialog to the signal handlers
        provided in this class
        """
        for name, m in self.__class__.__dict__.items():               
            if name.startswith("on_"):
                self.window.__dict__[name]=m
                
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
                wgt=getattr(self.window, "w%s" % param)
                wgt.set_text(value)
            
                
    ## ================================================ API
    def show(self):
        Bus.publish(self, "user_params?")
        self.window.bapply.props.sensitive=True 
        self.window.present()
        
        
    def hide(self):
        self.window.hide()

    ## ================================================ Handlers
    def on_bapply_clicked(self, window):
        print "toggled"
        return True
    
    def on_bauth_clicked(self, window):
        #text=self.wusername.get_text()
        #Bus.publish(self, "log", "username: %s" % text)
        #toplevel=self.get_toplevel()
        #builder=toplevel.builder
        #wusername=builder.get_object("eusername")
        print window.wusername.get_text()

        return True
    
    def on_bclose_clicked(self, window):
        self.window.hide()
        return True
    
    def on_eusername_changed(self, window):
        window.username_changed=True
        return True

    def on_eapi_key_changed(self, window):
        window.api_key_changed=True
        return True

    def on_esecret_key_changed(self, window):
        window.secret_key_changed=True
        return True


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

