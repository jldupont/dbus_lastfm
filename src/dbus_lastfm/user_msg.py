"""
    @author: jldupont

    Created on 2010-02-04
"""
import pynotify #@UnresolvedImport

from dbus_lastfm_service.mbus import Bus

class UserMessenger(object):
    """
    
    """
    _msgs={"api_access_error":"Error whilst accessing Last.FM web api. <br/>Is the service authentified?"
           ,"conn_error":"Connection error. <br/>Is Internet access functional?"
           ,"unknown":"Unknown error!"
           }
    
    def h_error(self, _, errorType, *pa, **kwa):
        errmsg=self._msgs.get(errorType, None)
        if not errmsg:
            errmsg=self._msgs.get("unknown")
        self._doNotify("DBus Last.fm - Error", errmsg)
        
    def _doNotify(self, summary, msg):
        pynotify.init("DBus Last.fm")
        n=pynotify.Notification(summary, msg)
        n.show()
    

usermsg=UserMessenger()
Bus.subscribe("error", usermsg.h_error)




if __name__=="__main__":
    u=UserMessenger()
    u.h_error("", "api_access_error")
    #u.h_error("", "conn_error")
    #u.h_error("", "foo")