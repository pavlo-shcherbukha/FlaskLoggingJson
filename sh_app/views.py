from datetime import datetime
import time
from operator import truediv
from flask import Flask, render_template, request, jsonify, Response, has_request_context, g
from flask.logging import default_handler
import json
import logging
# my own logger
import sh_app.shjsonformatter 

import datetime
import sys
import os
import traceback

if os.environ.get("APP_DEBUG") == 'DEBUG_BRK':
    import debugpy
    print("===========1-DEBUG-BREAK======")
    breakpoint() 
    print("===========2-DEBUG-BREAK======")

application = Flask(__name__)
application.logger.removeHandler(default_handler)
logging.getLogger('werkzeug').disabled = True

@application.before_request
def start_timer():
    g.start = time.time()

@application.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response


    now = time.time()
    duration = round(now - g.start, 2)
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = {
        'method': request.method, 
        'path': request.path,
        'request_content_type': request.headers.get('Content-Type'),
        'request_size': int(request.headers.get('Content-Length') or 0),
        'status': response.status_code, 
        'duration': duration, 
        'time': now,
        'ip': ip,
        'host': host,
        'params': args,
        'response_content_type': response.content_type,
        'response_size': response.calculate_content_length()

    }

    logger.info("HTTP API REQ", extra=log_params)

    return response




class InvalidAPIUsageR(Exception):
    status_code = 400

    def __init__(self, code, message, target=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code 
        if target is not None:
            self.target = target
        else:
            self.target = ""
        self.payload = payload

    def to_dict(self):
        errdsc = {}
        errdsc["code"] = self.code
        errdsc["description"] = self.message
        errdsc["target"] = self.target
        rv={}
        rv["Error"]=errdsc
        rv["Error"]["Inner"]=dict(self.payload or ())
        return rv


@application.errorhandler(InvalidAPIUsageR)
def invalid_api_usager(e):
    r=e.to_dict()
    return json.dumps(r), e.status_code, {'Content-Type':'application/json'}





class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)



logger = logging.getLogger(__name__)

apploglevel=os.environ.get("LOGLEVEL")
if apploglevel==None:
    logger.setLevel(logging.DEBUG)
elif apploglevel=='DEBUG':
    logger.setLevel(logging.DEBUG)    
elif apploglevel=='INFO':
    logger.setLevel(logging.INFO)    
elif apploglevel=='WARNING':
    logger.setLevel(logging.WARNING)    
elif apploglevel=='ERROR':    
    logger.setLevel(logging.ERROR)    
elif apploglevel=='CRITICAL':
    logger.setLevel(logging.CRITICAL)    
else:
    logger.setLevel(logging.DEBUG)  


handler = logging.StreamHandler()
handler.setFormatter(sh_app.shjsonformatter.JSONFormatter())

logger.addHandler(handler)

logger.debug("debug message")

# Найпростіші кейси для запису в лог
logger.info("INFO ...... ......MESSAGE")
try:
    logger.debug("START TEST ERROR")
    w=1/0
except Exception as e: 
    ex_type, ex_value, ex_traceback = sys.exc_info()
    trace_back = traceback.extract_tb(ex_traceback)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
    #ex_code=e.code
    ex_name=ex_type.__name__
    ex_dsc=ex_value.args[0]
    logger.error(ex_dsc)

#=================================================
# Головна сторінка
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/")
def home():
    #log("render home.html" )
    logger=logging.getLogger(__name__).getChild("home")
    logger.debug("Home page logger")
    return render_template("home.html")


#=================================================
# Про програму
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/about/")
def about():
    logger=logging.getLogger(__name__).getChild("about")
    logger.debug("About page logger")
    return render_template("about.html")





#===========================================================================
#    *********** Сервісні  АПІ ******************************
#===========================================================================

# =================================================================================
# Метод health check
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Повертає {'success':True} якщо контейнер працює
# =================================================================================
@application.route("/api/health", methods=["GET"])
def health():
    logger=logging.getLogger(__name__).getChild("health")
    title="Remote debug demo"
    label="health"
    result={}
    logger.debug('Health check')
    try:
        result= {}
        result["message"]= title
        result["ok"]=True
        logger.debug(f"Sending response {result}")
        return json.dumps( result ), 200, {'Content-Type':'application/json'}
    except Exception as e: 
            ex_type, ex_value, ex_traceback = sys.exc_info()
            trace_back = traceback.extract_tb(ex_traceback)
            stack_trace = list()
            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
            #ex_code=e.code
            ex_name=ex_type.__name__
            ex_dsc=ex_value.args[0]

            result["ok"]=False
            result["message"]= title
            result["error"]=ex_dsc
            result["errorCode"]=ex_name
            result["trace"]=stack_trace
            logger.error( ex_dsc)
            logger.error( f"ErrorResponse: {json.dumps( result )}")
            return json.dumps( result ), 422, {'Content-Type':'application/json'}



@application.route("/api/srvci", methods=["GET"])
def srvci():

    label="srvci"
    result={}
    result["DB_HOST"]=os.environ.get("DB_HOST")
    result["DB_PORT"]=os.environ.get("DB_PORT")
    result["DB_NAME"]=os.environ.get("DB_NAME")
    if result["DB_HOST"]==None:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No  ENV [DB_HOST!]", target=label,status_code=422, payload = {"code": "NoDefined ENV", "description": "Not defined env variable DB_HOST" } )
    if result["DB_PORT"]==None:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No  ENV [DB_PORT!]", target=label,status_code=422, payload = {"code": "NoDefined ENV", "description": "Not defined env variable DB_PORT" } )
    if result["DB_NAME"]==None:
        raise InvalidAPIUsageR( "InvalidAPIRequestParams",  "No  ENV [DB_NAME!]", target=label,status_code=422, payload = {"code": "NoDefined ENV", "description": "Not defined env variable DB_NAME" } )
    return json.dumps( result ), 200, {'Content-Type':'application/json'}
    






