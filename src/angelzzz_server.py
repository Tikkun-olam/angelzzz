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
from common import avg

from Database import AngelzzzDB, Base
from timeout import timeout, TimeoutError


PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = "sqlite:///" + os.path.join(PATH, "angelzzz.sql")


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
    
    engine = create_engine(DB_PATH)
    init_db(engine)
    def log_db(measure_time, beddit, chan1, chan2):
        insert_to_db(engine, time.time(), "beddit", avg(channel1), avg(channel2))
    
        
    run_logging_server(log_db)
    


    
if __name__ == "__main__":
    
    run_server_forever()

    
