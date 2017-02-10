from sqlalchemy import create_engine
from sqlalchemy.sql import select, desc
from Database import AngelzzzDB, Base
from common import DB_PATH
from flask import Flask, send_file, render_template, after_this_request, request
import StringIO
from flask_bootstrap import Bootstrap
import gzip
import functools
import time

app = Flask("angelzzz")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH

Bootstrap(app)

@app.route("/")
def root():
    readout=print_select_result(lambda: select([AngelzzzDB]).where(AngelzzzDB.__table__.c.time >= time.time() - 60).order_by(desc(AngelzzzDB.time)).limit(1))
    return render_template("index.jinja2", readout=readout)
    
    
def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or
                'Content-Encoding' in response.headers):
                return response
            gzip_buffer = StringIO.StringIO()
            gzip_file = gzip.GzipFile(mode='wb', 
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func


def get_select_result(select_data):
    engine = create_engine(DB_PATH)
    conn = engine.connect()
    s = select_data()
    result = conn.execute(s)
    return_value = StringIO.StringIO()
    
    for row in result:
        return_value.write(str(row["time"]) + "," + str(row["channel1"]) + "," +  str(row["channel2"]) + "\n")
        
    return_value.seek(0)
    
    return send_file(return_value,
                     attachment_filename="testing.csv",
                     mimetype='text/csv',
                     as_attachment=True)

def print_select_result(select_data):
    engine = create_engine(DB_PATH)
    conn = engine.connect()
    s = select_data()
    result = conn.execute(s)
    return_value = ""
    for row in result:
        return_value += str(row["time"]) + "," + str(row["channel1"]) + "," +  str(row["channel2"]) + "\n"
    return return_value

    

@app.route("/download/all")
@gzipped
def download_all():
    return get_select_result(lambda: select([AngelzzzDB]))

@app.route("/download/last_day")
@gzipped
def last_day():
    return get_select_result(lambda: select([AngelzzzDB]).where(AngelzzzDB.__table__.c.time >= time.time() - 24*60*60))

@app.route("/hello")
def hello():
    return "Hello World!"
