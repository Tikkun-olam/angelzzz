#!/usr/bin/env python
import argparse
from bedditbt import run_logging_server 
import time
import traceback
import os.path
import os
import sys
import bluetooth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database import AngelzzzDB, Base
from timeout import timeout, TimeoutError
import multiprocessing
from common import DB_PATH, init_log
from webserver import app
debug = 'DEBUG' in os.environ and os.environ['DEBUG'] == "on"


def init_db(engine):
    Base.metadata.create_all(engine)

def insert_to_db(engine, time, beddit, channel1, channel2):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    entry = AngelzzzDB(time=time, beddit=beddit, channel1=channel1, channel2=channel2)
    session.add(entry)
    session.commit()
    return
    
def run_server_forever():
    
    init_log()
    engine = create_engine(DB_PATH)
    init_db(engine)
    def log_db(measure_time, beddit, channel1, channel2):
        insert_to_db(engine, time.time(), "beddit",channel1, channel2)
    
    
    p_logger = multiprocessing.Process(target=run_logging_server, args=(log_db, ))
    web_logger = multiprocessing.Process(target=app.run, kwargs=dict(debug=debug, host='0.0.0.0'))
    
    p_logger.start()
    web_logger.start()
    
    while True:
        print("running")
        time.sleep(100)
    


    
if __name__ == "__main__":
    
    run_server_forever()

    
