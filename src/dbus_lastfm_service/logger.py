"""
    @author: jldupont

    Created on 2010-02-01
"""
from twisted.python import log
from mbus import Bus

class Logger(object):
    """
    Simple Logger
    """
    def _log(self, _, _msg):
        log.msg(_msg)

logger=Logger()
Bus.subscribe("log", logger._log)