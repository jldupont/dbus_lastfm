"""
    WebService Method
    
    @author: jldupont
    
    Helpers for creating "Method Calls" to Last.fm Web Service
    
"""
from hashlib import md5
from mbus import Bus
from ws import make_ws_request
import urllib
import dbus

_wsMethod={
    ## ================================================= AUTHEN
    "auth.getToken":        {"w":False, "s":False}
    ,"auth.getSession":     {"w":False, "s":False}
    
    ## ================================================= TRACK
    ,"track.addTags":       {"w":True,  "s":True}
    ,"track.getTags":       {"w":False, "s":True}
    ,"track.removeTag":     {"w":True,  "s":True}
    
    ## ================================================= USER
    ,"user.getLovedTracks":  {"w":False, "s":False}
    ,"user.getRecentTracks": {"w":False, "s":False}
    ,"user.getTopAlbums":    {"w":False, "s":False}
    ,"user.getTopArtists":   {"w":False, "s":False}
    ,"user.getTopTracks":    {"w":False, "s":False}
}

_wsMethodChecks = {
    "track.addTags": { "_tocheck": ["tags"], "tags":{"type": dbus.Array, "max_count":10} }
}

class WsMethod(object):
    """
    Prepares a Last.fm API method
    """
    API="http://ws.audioscrobbler.com/2.0/"
    HOST="ws.audioscrobbler.com"
    
    def __init__(self, mdic, udic):
        """
        @param wmethod: "write" method
        @param ression: session required True/False 
        """
        self.method=None
        self.wmethod=False
        self.srequired=False
        self.token=False
        self.mdic=mdic
        self.udic=udic
        self._error=False
        
        self.url=None
        self.body=None
        
        self._preprocess()
        if self._error:
            return
        
        if not self._performChecks():
            return
        
        self._process()

    def _performChecks(self):
        """
        Performs access checks e.g. maximum number of items in list
        
        """
        lcheck=_wsMethodChecks.get(self.method, None)
        if not lcheck:
            return True
        
        pcheck=lcheck["_tocheck"]
        for pkey in pcheck:
            pvalue=self.mdic.get(pkey, None)
            if not pvalue:
                self._error=["missing_parameter", "parameter(%s)" % pkey]
                return False
            ## checks associated with a method parameter
            kcheck=lcheck[pkey]
            t=kcheck["type"]
            if type(pvalue) != t:
                self._error=["wrong_type", "parameter(%s) expected to be of type(%s)" % (pkey, str(t))]
                return False
            if t==dbus.Array:
                maxcount=kcheck["max_count"]
                if len(pvalue) > maxcount:
                    self._error=["too_long", "parameter(%s) expected to be shorter than %s" % (pkey, maxcount)]
                    return False
        return True

    def session_required(self):
        """
        Returns True if a session is required
        but isn't available 
        """
        if self.srequired:
            if not self.token:
                return True
        return False

    def get_error(self):
        return self._error

    def is_error(self):
        return self._error

    def _preprocess(self):
        """
        Actually builds the URL used for making
        the API method call
        
        If the method_call requires authentication (i.e. a "session"),
        'api_sig' is generated.
        """
        self.method=self.mdic.get("method", {})
        mdetails=_wsMethod.get(self.method, None)
        if not mdetails:
            self._error="unsupported_method"
            return
        
        self.wmethod=mdetails.get("w", False)
        self.srequired=mdetails.get("s", False)
        
        if self.wmethod:
            self.http_method="POST"
        else:
            self.http_method="GET"

        self.token=self.udic.get("token", "")
        
    def _process(self):
        dic=self.mdic
        if self.method=="auth.getSession":
            dic["token"]=self.udic.get("auth_token", "MISSING_AUTH_TOKEN")
        else:
            if self.srequired:
                dic["sk"]=self.udic.get("token", "MISSING_SESSION_TOKEN")
        
        dic["api_key"]=self.udic.get("api_key","")
        
        ## Signing
        tsign=""
        if self.srequired or self.method=="auth.getSession":
            secret=self.udic.get("secret_key", "")  
            keys=sorted(dic.keys())
            for key in keys:
                value=self.mdic[key]
                if type(value)==dbus.Array:
                    liste=""
                    for item in value:
                        liste=item+","
                    value=liste.strip(",")
                tsign += key+value
            tsign+=secret.strip()
            m=md5()
            m.update(tsign)
            api_sig=m.hexdigest()
            Bus.publish(self, "log", "tosign(%s)" % tsign)
            
        ## URL formatting / POST body formatting
        fragment=""
        for key in dic:
            value=dic[key]
            if type(value) == dbus.Array:
                liste=""
                for item in value:
                    liste=str(item)+","
                value=liste.strip(",")
                
            fragment+=key+"="+urllib.quote(value)+"&"
            
        if self.srequired or self.method=="auth.getSession":
            fragment+="api_sig="+str(api_sig)
        fragment=fragment.strip("&")
                        
        ## We do not want to update 'dic' with 'api_sig'
        ## Do not add keys which would pollute unneccessarily
        ## --------------------------------------------------
        if self.wmethod:
            self.url=self.API
            self.body=fragment
        else:
            self.url=self.API+"?"+fragment
            self.body=None
        

class WsMethodHandler(object):
    """
    Handler for API requests that need
    to be sent off to Last.fm
    """
    
    def h_umethod_call(self, _, (mdic, cdic, udic)):
        """
        @param mdic: method_call dictionary
        @param cdic: callback dictionary
        @param udic: user parameters dictionary
        """
        ws_method=WsMethod(mdic, udic)
        #Bus.publish(self, "log", "h_umethod_call: method(%s) http_method(%s) body(%s)" % 
        #            (ws_method.method, ws_method.http_method, ws_method.body))
        
        if not ws_method.is_error():
            if not ws_method.method=="auth.getSession":
                if ws_method.session_required():
                    self._session_required_flow(mdic, cdic, udic)
                    return
        
        if ws_method.is_error():
            cdic["e"](["error", ws_method.get_error()])
            return       
        
        ctx=(ws_method.method, cdic, udic)        
        make_ws_request(ctx, ws_method.url, http_method=ws_method.http_method, postdata=ws_method.body)        
        
    def _session_required_flow(self, mdic, cdic, udic):
        """
        A session must be authenticated before calling the method
        
        We need to have a "token" as starting point 
        """
        #Bus.publish(self, "log", "_session_required_flow: mdic(%s)" % mdic)
        
        auth_token=udic.get("auth_token", "")
        if not auth_token: 
            cdic["e"](["error", "session_required"])
            return
        
        cdic.update({"original_mdic":mdic})
        Bus.publish(self, "method_call", {"method":"auth.getSession"}, cdic)


wsh=WsMethodHandler()
Bus.subscribe("umethod_call", wsh.h_umethod_call)

## Test string for 'track.getTags'
#"depeche mode", "little 15"
