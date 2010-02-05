"""
    Bus Agent for handling responses
    from Last.fm API method_call

    @author: jldupont

    Created on 2010-02-01
"""
import re
from mbus import Bus

class WsResponseHandler(object):
    """
    """
    auth_url="http://www.last.fm/api/auth/?api_key=%s&token=%s"
    
    def h_ws_response(self,_, (status, response_headers, ctx, response)):
        """
        Response handler
        """
        (method, cdic, udic)=ctx
        
        ## Special case for the "authentication flow"
        if method=="auth.getToken":
            return self.h_auth_gettoken(status, response_headers, cdic, udic, response)

        if method=="auth.getSession":
            return self.h_auth_getsession(status, response_headers, cdic, udic, response)
        
        if status!='200':
            cdic["e"](["error", "method_failed", "Method Call failed (%s)" % method])
            return

        ## Actually return a response to the API caller
        cdic["c"](["ok", response])
        
    def h_auth_getsession(self, status, response_headers, cdic, udic, response):
        """
        Return from "getsession" - part of authentication flow
        """
        Bus.publish(self, "log", "h_auth_getsession, status: %s" % status)
        
        if status!="200":
            cdic["e"](["error", "method_failed", "Cannot retrieve 'session token' from Last.fm"])
            return
        
        if not response:
            cdic["e"](["error", "invalid_response", "Invalid response received from Last.fm"])
            return
        
        match=re.search("\<key\>(.*)\<\/key\>", response)
        if match is None:
            cdic["e"](["error", "token_missing", "Missing 'session token' from Last.fm response"])
            return

        ## We've got a "session token" ...
        ##  Now we need to complete the original method call
        token=match.group(1)
        Bus.publish(self, "user_params", {"token":token})        
        
        orig_mdic=cdic["original_mdic"]
        
        # get rid of original_mdic in cdic
        del cdic["original_mdic"]
        Bus.publish(self, "method_call", orig_mdic, cdic) 
        

    def h_auth_gettoken(self, status, response_headers, cdic, udic, response):
        """
        Authentication flow
        
        Success:  ["ok",    url]
        Failure:  ["error", error_code, error_msg]
        """
        Bus.publish(self, "log", "h_auth_gettoken, status: %s" % status)
        
        if status!="200":
            cdic["e"](["error", "method_failed", "Cannot retrieve 'auth token' from Last.fm"])
            return
            
        if not response:
            cdic["e"](["error", "invalid_response", "Invalid response received from Last.fm"])
            return
            
        match=re.search("\<token\>(.*)\<\/token\>", response)
        if match is None:
            cdic["e"](["error", "token_missing", "Missing 'auth token' from Last.fm response"])
            return
        
        auth_token=match.group(1)
        Bus.publish(self, "user_params", {"auth_token":auth_token, "token":""})        
        
        api_key=udic.get("api_key", "")
        
        ## Return URL that must be used by the user for authentication
        ## ===========================================================
        url=self.auth_url % (api_key, auth_token)
        cdic["c"](["ok", url])

   
   
wsrh=WsResponseHandler()
Bus.subscribe("ws_response", wsrh.h_ws_response)

