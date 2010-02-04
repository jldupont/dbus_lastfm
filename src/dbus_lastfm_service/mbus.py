"""
    Simple "Bus" based message publish/subscribe

    Created on 2010-01-28

    @author: jldupont
"""

__all__=["Bus"]

class sQueue(object):
    """
    Simple Queue class
    """
    def __init__(self):
        self.queue=[]
        
    def push(self, el):
        self.queue.append(el)
        return self
    
    def pop(self):
        try:     el=self.queue.pop(0)
        except:  el=None
        return el


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
    incall=False
    q=sQueue()

    @classmethod
    def _maybeLog(cls, msgType, msg):
        """
        Private - Logging helper
        """
        if not cls.debug:
            return
        
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
            cls._maybeLog(msgType, "Exception: subscribe: %s" % str(e))
        
    @classmethod
    def publish(cls, caller, msgType, *pa, **kwa):
        """
        Publish a message from a specific type on the bus
        
        @param msgType: string, message-type
        @param *pa:   positional arguments
        @param **kwa: keyword based arguments
        """
        if cls.incall:
            #cls._maybeLog(msgType, "BUS: publish: INCALL - caller(%s) type(%s) pa(%s) kwa(%s)" % (caller, msgType, pa, kwa))
            cls._maybeLog(msgType, "BUS: publish: QUEUING - caller(%s) type(%s)" % (caller, msgType))            
            cls.q.push((caller, msgType, pa, kwa))
            return           
        cls.incall=True

        cls._maybeLog(msgType, "BUS: publish:BEGIN - Queue processing")
        while True:
            cls._maybeLog(msgType, "BUS: publish: caller(%s) type(%s) pa(%s) kwa(%s)" % (caller, msgType, pa, kwa))
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
                    break

            msg=cls.q.pop()
            if not msg:
                break
            caller, msgType, pa, kwa = msg

        cls._maybeLog(msgType, "BUS: publish:END - Queue processing")
        cls.incall=False
        

## =========================================================== TESTS

if __name__ == '__main__':
    class Logger(object):
        def __call__(self, msg):
            print "LOGGER: %s" % msg
    
    class Cback(object):
        def handler(self, msgType, *pa, **kwa):
            print "cb: msgType(%s) pa(%s) kwa(%s)" % (msgType, pa, kwa)
        
    Bus.logger=Logger()
    Bus.debug=True
    
    def test1(self):
    
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

## =========== Queue test
    print "BEGIN QUEUE test"
    
    class Test(object):
        def __init__(self, name, msg):
            self.name=name
            self.msg=msg
            
        def handler1(self, msgtype, *pa, **kwa):
            print "handler1: name(%s) msgtype(%s)" % (self.name, msgtype)
            
        def handler2(self, msgtype, *pa, **kwa):
            print "handler2: name(%s) msgtype(%s)" % (self.name, msgtype)
            Bus.publish(self, self.msg)
            Bus.publish(self, self.msg)
            
    
    x=Test("X", "msgX")
    y=Test("Y", "msgY")
    
    Bus.subscribe("msgX", y.handler2)
    Bus.subscribe("msgY", x.handler1)
    
    Bus.publish(x, "msgX")
    
    Bus.publish(x, "msgX")
