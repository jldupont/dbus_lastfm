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
        if status!='200':
            cdic["e"](["error", "method_failed", "Method Call failed (%s)" % method])
            return
        
        ## Special case for the "authentication flow"
        if method=="auth.gettoken":
            return self.h_auth_gettoken(response_headers, cdic, udic, response)
        
        Bus.publish(self, "log", "response: status: %s, text: %s" % (status, response))

    def h_auth_gettoken(self, response_headers, cdic, udic, response):
        """
        """
        if not response:
            cdic["e"](["error", "invalid_response", "Invalid response received from Last.fm"])
            return
            
        match=re.search("\<token\>(.*)\<\/token\>", response)
        if match is None:
            cdic["e"](["error", "token_missing", "Missing 'token' from Last.fm response"])
            return
        
        token=match.group(1)
        Bus.publish(self, "user_params", {"token":token})        
        
        ## No need to "ask" for the "user parameters" because
        ## if we got here in the first place that means we already
        ## grab those
        api_key=udic.get("api_key", "")
        url=self.auth_url % (api_key, token)
        cdic["c"](["ok", url])

   
   
wsrh=WsResponseHandler()
Bus.subscribe("ws_response", wsrh.h_ws_response)

