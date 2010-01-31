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
    """
    params=("username"
            ,"api_key"
            ,"secret_key"
            )
    def _getParams(self, dic={}):
        account=Account()
        for key in self.params:
            dic[key]=account[key]
        return dic
        
    
    def h_method_call(self, _, cdic):
        """
        Listens for "method_call" messages and
        fills "cdic" with the missing parameters
        """
        dic=self._getParams()
        cdic.update(dic)
        Bus.publish(self, "umethod_call", cdic)
        
    def q_user_params(self, _):
        """
        Responder for the question "user_params?"
        """
        dic=self._getParams()          
        Bus.publish(self, "user_params", dic)
    
    def a_user_params(self, _, params):
        """
        Updates the user params
        """
        account=Account()
        account.update(params)
    
user=User()
Bus.subscribe("user_params?", user.q_user_params)
Bus.subscribe("user_params",  user.a_user_params)
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
    