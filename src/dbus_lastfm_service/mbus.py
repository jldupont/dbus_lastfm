"""
    Simple "Bus" based message publish/subscribe

    Created on 2010-01-28

    @author: jldupont
"""

__all__=["Bus"]

class Bus(object):
    """
    Simple publish/subscribe "message bus"
    with configurable error reporting
    
    Message delivery is "synchronous i.e. the caller of
    the "publish" method blocks until all the subscribers
    of the message have been "called-back".
    
    Any "callback" can return "True" for stopping the
    calling chain.
    """
    debug=False
    logger=None
    ftable={}

    @classmethod
    def _maybeLog(cls, msgType, msg):
        """
        Private - Logging helper
        """
        if msgType=="log":
            return
        
        if cls.logger:
            cls.logger(msg)
    
    @classmethod
    def subscribe(cls, msgType, callback):
        """
        Subscribe to a Message Type
        
        @param msgType: string, unique message-type identifier
        @param callback: callable instance which will be called upon message delivery  
        """
        try:
            cls._maybeLog(msgType, "subscribe: subscriber(%s) msgType(%s)" % (callback.__self__, msgType))
            subs=cls.ftable.get(msgType, [])
            subs.append((callback.__self__, callback))
            cls.ftable[msgType]=subs
        except Exception, e:
            cls._maybeLog("Exception: subscribe: %s" % str(e))
        
    @classmethod
    def publish(cls, caller, msgType, *pa, **kwa):
        """
        Publish a message from a specific type on the bus
        
        @param msgType: string, message-type
        @param *pa:   positional arguments
        @param **kwa: keyword based arguments
        """
        if cls.debug:
            cls._maybeLog(msgType, "publish: caller(%s) type(%s) pa(%s) kwa(%s)" % (caller, msgType, pa, kwa))
        subs=cls.ftable.get(msgType, [])
        for (sub, cb) in subs:
            if sub==caller:  ## don't send to self
                continue
            try:
                stop_chain=cb(msgType, *pa, **kwa)
            except Exception, e:
                stop_chain=True    
                if cls.logger:
                    cls.logger("Exception: msgType(%s): %s" %( msgType, str(e)))
            if stop_chain:
                return
                    

## =========================================================== TESTS

if __name__ == '__main__':
    class Logger(object):
        def __call__(self, msg):
            print msg
    
    class Cback(object):
        def handler(self, msgType, *pa, **kwa):
            print "cb: msgType(%s) pa(%s) kwa(%s)" % (msgType, pa, kwa)
        
    Bus.logger=Logger()
    Bus.debug=True
    
    cb=Cback()
    cb2=Cback()
    
    Bus.subscribe("test", cb.handler)
    
    Bus.publish(cb2, "test",  p1="v1", p2="v2")
    Bus.publish(cb2, "test2", p1="v1", p2="v2")
    
    Bus.subscribe("test", None)
    Bus.publish(cb2, "test",  p2="v2", p3="v3")
    
    Bus.logger=None
    Bus.publish(cb2, "test",  p2="v2", p3="v3")

    Bus.publish(cb, "test", whatever="don't care")
