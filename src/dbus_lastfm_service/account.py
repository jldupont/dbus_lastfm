"""
    Account module
    @author: jldupont
"""

import gconf #@UnresolvedImport

class Account(object):
    """
    Account information can be set/get two ways:
    - as a normal dictionary
    - as properties using '.' access
    """
    BASE=USERNAME="/apps/dlastfm/"
    
    def __getattr__(self, name):
        client=gconf.client_get_default()
        return client.get_string(self.BASE+str(name))

    def __setattr__(self, name, value):
        value="" if value is None else value 
        client=gconf.client_get_default()
        client.set_string(self.BASE+str(name), value)

    __getitem__=__getattr__
    __setitem__=__setattr__

    def update(self, dic):
        """
        Bulk update
        @param dic: dictionary of parameters
        """
        for k,v in dic.iteritems():
            self.__setattr__(k,v)


if __name__=="__main__":
    a=Account()
    
    print a["test"]
    a["test"]="some test value"
    print a["test"]
    
    v={"test1":"value1", "test2":"value2"}
    a.update(v)

    print a.test1
    print a.test2
