import argparse
from bedditbt import BedditStreamer 
import time
import traceback
import os.path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database import AngelzzzDB, Base
from timeout import timeout

DB_PATH = "sqlite:////home/pi/angelzzz.sql"

def avg(l):
    return sum(l) / float(len(l))

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
    a = None
    engine = create_engine(DB_PATH)
    init_db(engine)
    
    connected = False
    while True:
        try:
            if not connected:
                print("Connecting")
                connected = True
                a = BedditStreamer()
                print("Connected")
            channel1, channel2 = a.get_reading()
            data = [ time.time(),avg(channel1), avg(channel2)]
            insert_to_db(engine, time.time(), "beddit",avg(channel1), avg(channel2))
            # print(data)
        except Exception:
            time.sleep(1)
            print("except " + str(time.time()))
            print(traceback.format_exc())
    
if __name__ == "__main__":
    PATH = os.path.dirname(os.path.realpath(__file__))
    
    run_server_forever()

    
