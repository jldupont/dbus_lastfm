"""
    Web Service - Helpers

    @author: Jean-Lou Dupont
    
    NOTE: this module is *not* used at the moment.
    ====
"""
__all__=["msession", "mwrite", "WsMethodBase"]

def msession(method):
    """
    Decorates a "web service method" as requiring 
    "session level" authentication
    """
    def decorated(that, *pa, **kwa):
        that.session_required=True
        return method(that, *pa, **kwa)
        
    return decorated

def mwrite(method):
    """
    Decorates a "web service method" as being a "write" method 
    """
    def decorated(that, *pa, **kwa):
        that.write_required=True
        return method(that, *pa, **kwa)
        
    return decorated



class WsMethodBase(type):
    """
    Metaclass for WsMethod
    
    Uses an AOP-like technique to insert a
    "before" and "after" method calls wrapping a method 
    """
    def __init__(cls, name, bases, ns):
        from types import FunctionType
        updatesDict={}
        for k in cls.__dict__:
            v=cls.__dict__[k]
            if v.__class__ == FunctionType:
                if not v.__name__.startswith("__"):
                    updatesDict[k]= v
                    
        for mname, func in updatesDict.iteritems():
            def _(self, *pa, **kwa):
                cls._before()
                ret=func(self, *pa, **kwa)
                cls._after(ret, *pa, **kwa)
                return ret
            setattr(cls, mname, _)

        cls.__init__ = cls.cls_init

    def _before(self, *pa, **kwa):
        print "_before!"
        
    def _after(self, *pa, **kwa):
        print "_after!"

    def cls_init(self):
        """
        Provides a default initialization method
        """
        self.write_required=False
        self.session_required=False
        

class WsMethod(object):
    """
    WebService method 
    """
    __metaclass__= WsMethodBase
    
    API="http://ws.audioscrobbler.com/"
            
    @mwrite
    @msession
    def track_addTags(self, artist, track, tags):
        print "track_addTags, session_required: %s" % self.session_required
        print "track_addTags, write_required: %s" % self.write_required
        #print self.API

        
        
if __name__=="__main__":
    wsm=WsMethod()
    assert not wsm.write_required
    assert not wsm.session_required
    
    wsm.track_addTags("Mind.in.a.Box", "amnesia", "electronica")
    assert wsm.session_required
    assert wsm.write_required
    
