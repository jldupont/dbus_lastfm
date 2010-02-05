"""
    Authorization Agent
    Looks after the "authorization" flow

    @author: jldupont

    Created on 2010-02-04
"""
import webbrowser

from dbus_lastfm_service.mbus import Bus


class AuthResponseAgent(object):
    
    _msgTable={"method_failed":     "auth_error"
               ,"invalid_response": "api_error"
               ,"token_missing":    "api_error"
               ,"no_page":          "auth_error"
               }
    
    def h_apicb(self, response):
        """
        API response callback
        
        If a valid 'url' is received, open a browser tab
        for the user to 'authorize' the application
        """
        _status, url=response
        webbrowser.open_new_tab(url)
        
    def h_apieb(self, response):
        """
        API response errback
        """
        _,code, msg=response
        tcode=self._msgTable.get(code, "unknown")
        Bus.publish(self, "error", tcode)
        Bus.publish(self, "log", "Authorization error, code(%s) msg(%s)" % (code, msg))
    

class AuthorizeAgent(object):
    
    def h_authorize(self, _):
        """
        Bus message handler
        """
        ahandler=AuthResponseAgent()
        Bus.publish(self, "method_call", {"method":"auth.getToken"}, 
                    {"c":ahandler.h_apicb, "e":ahandler.h_apieb})

    
aagent=AuthorizeAgent()
Bus.subscribe("authorize", aagent.h_authorize)
