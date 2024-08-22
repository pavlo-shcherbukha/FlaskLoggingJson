from datetime import datetime
from operator import truediv
from flask import Flask, render_template, request, jsonify, Response, has_request_context
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



#logging.basicConfig(filename='myapp.log', level=logging.DEBUG)



logger = logging.getLogger(__name__)
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

logger.info("INFO ...... ......MESSAGE", extra={"label": "lblblblblbl"} )

#=================================================
# Головна сторінка
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/")
def home():
    #log("render home.html" )
    logger=logging.getLogger(__name__).getChild("home_rout")
    logger.info("Hoem page logger")
    return render_template("home.html")


#=================================================
# Про програму
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/about/")
def about():
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
    title="Remote debug demo"
    label="health"
    result={}
    log('Health check', label)
    try:
        result= {}
        result["message"]= title
        result["ok"]=True
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
    






