#!/usr/bin/env python
"""
    @author: Jean-Lou Dupont
"""
import os
import sys

import pygtk
import gtk      #@UnresolvedImport
import gobject  #@UnresolvedImport


class Config:
    
    CFILE="config.glade"
    
    def __init__(self):
        self.builder = gtk.Builder()
        glade_file=self._find_file(self.CFILE)
        self.builder.add_from_file(glade_file)
        self.window = self.builder.get_object("wconfig")
        self._dowiring()
        self.builder.connect_signals(self.window, self.window)

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
    ## ================================================ API
    def show(self):
        self.window.present()
        
    def hide(self):
        self.window.hide()

    ## ================================================ Handlers
    def on_bauth_clicked(self, _signal):
        print "auth!"
        return True
    
    def on_bclose_clicked(self, _signal):
        self.window.hide()
        return True
    
    def on_bquit_clicked(self, _signal):
        self.hide()
        gtk.main_quit()
        return True

    def on_eusername_changed(self, _signal):
        print "username: "
        return True

    def on_eapi_key_changed(self, _signal):
        print "api key: "
        return True

    def on_esecret_key_changed(self, _signal):
        print "secret key: "
        return True


cfg=Config()


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
    gtk.main()

