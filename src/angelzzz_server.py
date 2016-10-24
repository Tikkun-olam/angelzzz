import argparse
from bedditbt import BedditStreamer 
import time
import traceback
import os.path
import os
from sqlalchemy import  create_engine

from Database import AngelzzzDB, Base

RFCOMM_DEV = "/dev/rfcomm0"
DB_PATH = "sqlite:////home/pi/angelzzz.sql"

def avg(l):
    return sum(l) / float(len(l))

def init_db(engine):
    Base.metadata.create_all(engine)

def inser_to_db(engine, time, beddit, channel1, channel2):
    connection = engine.connect()
    sql = "insert into " + AngelzzzDB.__tablename__ + " values (?,?,?,?)"
    variables = (time, beddit, channel1, channel2)
    connection.execute(sql,variables)
    connection.close()
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
            inser_to_db(engine, time.time(), "beddit",avg(channel1), avg(channel2))
            # print(data)
        except Exception:
            connected = False
            time.sleep(1)
            print("except " + str(time.time()))
            print(traceback.format_exc())
    
if __name__ == "__main__":
    PATH = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isfile(""):
        os.system(os.path.join(PATH, "connect.sh"))
        
    
    run_server_forever()

    
