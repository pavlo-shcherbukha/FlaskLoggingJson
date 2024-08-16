from datetime import datetime
from operator import truediv
from flask import Flask, render_template, request, jsonify, Response
import json
import logging
#import sh_app.jsonlogger
#from sh_app.jsonlogger import CustomFormatter
#import json_logging

##import json_log_formatter
##import sh_app.jformatter

### pvx
import sh_app.pvxjsonformatter 

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





logging.basicConfig(filename='myapp.log', level=logging.DEBUG)


# USE  package json-logging
# import json_logging
#json_logging.init_flask(enable_json=True)
#json_logging.init_request_instrument(application)
#logger = logging.getLogger("test-logger")
#logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.StreamHandler(sys.stdout))
#def log( a_msg='NoMessage', a_label='logger' ):
#    logger.info("test log statement")


#===================================================
# Функція внутрішнього логера
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===================================================
#logger = logging.getLogger()
#logHandler = logging.StreamHandler()
#formatterdef = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#formatter= CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logHandler.setFormatter(formatter)
#logger.addHandler(logHandler)



#def log( a_msg='NoMessage', a_label='logger' ):
#	dttm = datetime.datetime.now()#
#	ls_dttm = dttm.strftime('%d-%m-%y %I:%M:%S %p')
#	logger.info(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)
#	print(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)


# =============================================
#formatter = json_log_formatter.JSONFormatter()

#formatter = sh_app.jformatter.CustomisedJSONFormatter()

#json_handler = logging.StreamHandler()
#json_handler.setFormatter(formatter)

#logger = logging.getLogger('my_json')
#logger.addHandler(json_handler)
#logger.setLevel(logging.DEBUG)

#def log( a_msg='NoMessage', a_label='logger' ):
#	dttm = datetime.datetime.now()
#	ls_dttm = dttm.strftime('%d-%m-%y %I:%M:%S %p')
#	logger.info(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)
#	#print(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)


# ===========================================================================
# https://aminalaee.dev/posts/2022/python-json-logging/
# https://docs.python.org/3/library/logging.html#logrecord-attributes
# http://web.archive.org/web/20201130054012/https://wtanaka.com/node/8201
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Будемо використовувати свій власний форматтре логів
# ==========================================================================

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(sh_app.pvxjsonformatter.JSONFormatter())

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
        log('Health check' , 'health')
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

    log('Відправляю результат: ', label)
    return json.dumps( result ), 200, {'Content-Type':'application/json'}
    






