#pvxjsonformatter
import json
import logging
import subprocess
import time


class JSONFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__()

        self._ignore_keys = {"msg", "args"}

    def format(self, record: logging.LogRecord) -> str:
        #message = record.__dict__.copy()
        message={}
        message['timestamp']=self.fmttime( record.created )
        message['level'] = record.levelname
        message['label'] = record.name
        message['ahostname'] = subprocess.getoutput("hostname")
        message["message"] = record.getMessage()        
        message['ausername'] = None
        
        if record.levelname == "ERROR":
            if record.stack_info:
                message["stack_info"] = self.formatStack(record.stack_info)
            if record.pathname:
                message["stack_info"] = record.pathname
            if record.filename:
                message["filename"] = record.filename   
            if record.lineno:
                message["lineno"] = record.lineno
            if record.exc_text:
                message["exc_text"] = record.exc_text
            if record.exc_info:
                message["exc_info"] = record.exc_info
            if record.module:
                message["module"] = record.module
        return json.dumps(message)
    
    def fmttime( self,  logtime ):
        tmformat="%Y-%m-%dT%H:%M:%S.%sZ"
        tmformatv1="%Y-%m-%dT%H:%M:%S +0000"
         
        gmttimestamp=time.gmtime( logtime )
        strgmtime=time.strftime( tmformat, gmttimestamp)
        return strgmtime
