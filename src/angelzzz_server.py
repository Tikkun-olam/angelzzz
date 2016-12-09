import argparse
from bedditbt import BedditStreamer 
import time
import traceback
import os.path
import os
import sys
import bluetooth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from Database import AngelzzzDB, Base
from timeout import timeout, TimeoutError

from raspberrypi_gpio import restart


DB_PATH = "sqlite:////home/pi/angelzzz.sql"

PATH = os.path.dirname(os.path.realpath(__file__))


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
def get_nice_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
def run_server_forever():
    a = None
    engine = create_engine(DB_PATH)
    init_db(engine)
    
    connected = False
    last_packet_number = None
    timeout_count = 0
    packet = -1
    while True:
        try:
            if not connected:
                with timeout(15):
                    print("Connecting")
                    connected = True
                    a = BedditStreamer()
                    print("Connected")
            last_packet_number = a.last_packet_number
            with timeout(15):
                channel1, channel2 = a.get_reading()
            last_packet_number = a.last_packet_number
            #print(a.packet_number_count)
            #print("last packet: " + str(a.last_packet_number))
            data = [ time.time(),avg(channel1), avg(channel2)]
            insert_to_db(engine, time.time(), "beddit",avg(channel1), avg(channel2))
            # print(data)
        except (bluetooth.BluetoothError, TimeoutError) as e:
            print("got: " + str(e) + " at packet: " + str(last_packet_number) + " on time: " + str(get_nice_time()))
            if e.message.find("Bad file descriptor") > 0 or e.message.find("16") > 0 or type(e) == TimeoutError:
                #print("restart bluetooth power")
                #os.system(os.path.join(PATH, "restart_bluetooth_power"))
                print("sleeing 2")
                time.sleep(2)
                connected = False
                #os.system(os.path.join(PATH, "reset_device.sh")
                a.conn.disconnect()
            if type(e) == TimeoutError or e.message.find("112, 'Host is down'") > 0:
                if a is None or packet == a.last_packet_number:
                    timeout_count += 1
                    print(timeout_count)
                    if timeout_count == 5:
                        timeout_count = 0
                        restart()
                if a is not None:
                    packet = a.last_packet_number
                
            if e.message.find("Bad file descriptor"):    
                connected = False
                time.sleep(1)
        except KeyboardInterrupt:
            print("User sent termination call")
            try:
                a.conn.stop_streaming()
                a.conn.disconnect()
                sys.exit()
            except Exception:
                print(traceback.format_exc())
                sys.exit()
        except Exception as e:
            time.sleep(1)
            print("got: " + str(e) + " at packet: " + str(last_packet_number)  + " on time: " + str(get_nice_time()))
            print(traceback.format_exc())
        #except bluetooth.ProtocolError as e:
        #    print("restarting")
        #    time.sleep(1)
        #    os.execl(sys.executable,sys.executable,__file__,"restart")
    
if __name__ == "__main__":
    
    run_server_forever()

    
