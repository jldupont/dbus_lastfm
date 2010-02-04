"""
    @author: jldupont

    Created on 2010-01-30
"""
from mbus import Bus
from account import Account


class User(object):
    """
    User Class - serves as proxy on the message bus
    for "questions" & "affirmations" related to 
    the user's account.
    
    Provides filling user parameters on 
    "method_call" message and produces "umethod_call"
    on the bus in return.
    
    Generates the following messages:
    ================================
    - "user_params"
    - "umethod_call"

    """
    params=("username"
            ,"api_key"
            ,"secret_key"
            ,"auth_token"
            ,"token"
            )
    
    ## Parameters that influence the validity
    ## of a user session
    rootParams = ("api_key"
                  ,"secret_key"
                  )
    ## =========================================================== HANDLERS
    
    def h_method_call(self, _, mdic, cdic):
        """
        Listens for "method_call" messages and
        adds the "user parameters" to a new message
        """
        dic=self._getParams()
        Bus.publish(self, "umethod_call", (mdic, cdic, dic))
        
    def q_user_params(self, _=None):
        """
        Responder for the question "user_params?"
        """
        dic=self._getParams()          
        Bus.publish(self, "user_params", dic)
    
    def h_user_params(self, _, params):
        """
        Updates the user params
        """
        #Bus.publish(self, "log", "h_user_params, params: %s" % params)
        self._updateParams(params)
        self._dependencyChecks(params)

    ## =========================================================== Helpers

    def _getParams(self, dic={}):
        account=Account()
        for key in self.params:
            dic[key]=account[key]
        return dic
        
    def _updateParams(self, iparams):
        account=Account()
        account.update(iparams)
        
    def _dependencyChecks(self, iparams):
        """
        Performs 'dependency checks' of the received
        parameters against the 'root parameters'
        """
        for key in iparams:
            if key in self.rootParams:
                self._updateParams({"auth_token":"", "token":""})
                self.q_user_params()
                break
            
        
    
## ========================================================== Bus Interfacing
    
user=User()
Bus.subscribe("user_params?", user.q_user_params)
Bus.subscribe("user_params",  user.h_user_params)
Bus.subscribe("method_call",  user.h_method_call)

## ========================================================== TESTS

if __name__ == '__main__':
    class Logger(object):
        def __call__(self, msgType, e):
            print "Logger: Error: msgType(%s) Exception(%s)" % (msgType, str(e))
    
    class Test(object):
        def handler(self, msgType, params):
            print params

    Bus.logger=Logger()
            
    t=Test()
    Bus.subscribe("user_params", t.handler)
    
    t2=Test()
    Bus.publish(t2, "user_params?")
    