import binascii
import os
import os.path
import struct
import numpy
import time
import gzip
import sys
import traceback
import shutil
import bluetooth
from common import iniToDict, avg, log
import datetime
from timeout import timeout, TimeoutError

debug = 'DEBUG' in os.environ and os.environ['DEBUG'] == "on"

PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(PATH, "config.ini")

if not os.path.isfile(CONFIG_PATH):
    shutil.copy(os.path.join(PATH, "config.ini.example"),CONFIG_PATH)

settings = iniToDict(CONFIG_PATH)


# Setup relay
if settings["beddit"]["relay"] == "dummy":
    def restart():
        return
elif settings["beddit"]["relay"] == "gpio":
    from raspberrypi_gpio import restart
else:
    raise Exception("config is invalid, please provide a relay type")


def get_nice_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

class ProtocolError(Exception):
    pass


class BedditConnection(object):

    def __init__(self, connection, timeout1=5):
        self.connection = connection
        self.read_count = 0
        self.timeout = timeout1
        self.last_cont = time.time()

    def open_connection(self):
        self.connection.send("OK\n".encode())
        time.sleep(0.2)

        response_to_ok = self._receive(3)

        if response_to_ok != 'OK\n' and response_to_ok != 'AT\n':
            raise ProtocolError("Got {} after OK".format(repr(response_to_ok)))

    def start_streaming(self):
        if self.timeout == None:
            self.connection.send("START\n".encode())
        else:
            self.connection.send("START " + str(self.timeout) + "\n".encode())
        return

    def stop_streaming(self):
        self.connection.send("STOP\n".encode())
        
    def get_info(self):
        self.connection.send("INFO\n".encode())

    def disconnect(self):
        self.connection.close()

    def _receive(self, packet_size, timeout_max=1):
        data = None
        with timeout(timeout_max):
            data = self.connection.recv(packet_size)
            while len(data) < packet_size:
                log("receiving " + str(len(data)) + "/" + str(packet_size))
                data = data + self.connection.recv(packet_size - len(data))

        return data

    def _read_packet(self):
        self.read_count += 1
        
        if self.read_count > 1000:
            log("Restarting stream")
            self.read_count = 0
            self.stop_streaming()
            self.start_streaming()
        
        header = self._receive(6)

        if len(header) != 6:
            raise ProtocolError()

        packet_number = struct.unpack('I', header[:4])[0]
        payload_length = struct.unpack('H', header[4:])[0]
        time.sleep(0.15)

        payload = self._receive(payload_length)

        crc = struct.unpack('I', self._receive(4))[0]

        computed_crc = binascii.crc32(header + payload) & 0xffffffff

        if crc != computed_crc:
            raise ProtocolError("Invalid CRC")

        return packet_number, payload

    def read_sample_packet(self):
        packet_number, payload = self._read_packet()
        now = time.time()
        if self.timeout is not None and now - self.last_cont > self.timeout - 1:
            self.connection.send("CONT\n".encode())
            self.last_cont = now

        sample_array = numpy.fromstring(payload, "uint16")

        channel1 = sample_array[0::2]
        channel2 = sample_array[1::2]

        return (packet_number, channel1, channel2)

def get_beddit_mac():
    return settings["beddit"]["mac"].strip()


class BedditStreamer:
    def __init__(self):
        self.last_packet_number = None
        self.packet_number_count = 0
        self.port = 1
        try:
            with timeout(10):
                ser = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                ser.connect((get_beddit_mac(), self.port))
                        
        except TimeoutError as e:
            log("connection timeout")
            self.port += 1
            ser.close()
            raise e
        self.conn = BedditConnection(ser)
        try:
        
            self.conn.open_connection()
            self.conn.start_streaming()
        
        except Exception as e:
            log("beddit dissconnect")
            self.conn.stop_streaming()
            self.conn.disconnect()
            raise e
        
    def get_reading(self):
        chan1 = []
        chan2 = []

        packet_number, channel1, channel2 = self.conn.read_sample_packet()
        self.last_packet_number = packet_number
        self.packet_number_count += 1
        for i in channel1:
            chan1.append(i)
        for i in channel2:
            chan2.append(i)
        return [chan1, chan2]
    def close(self):
        self.conn.stop_streaming()
        self.conn.disconnect()
        
        
        
def run_logging_server(log_callback):
    a = None
    connected = False
    last_packet_number = None
    timeout_count = 0
    packet = -1
    while True:
        try:
            if not connected:
                with timeout(15):
                    log("Connecting")
                    connected = True
                    a = BedditStreamer()
                    log("Connected")
            last_packet_number = a.last_packet_number
            with timeout(15):
                channel1, channel2 = a.get_reading()
            last_packet_number = a.last_packet_number
            data = [ time.time(),avg(channel1), avg(channel2)]
            log_callback(time.time(), "beddit",avg(channel1), avg(channel2))
            # print(data)
        except (bluetooth.BluetoothError, TimeoutError) as e:
            log("got: " + str(e) + " at packet: " + str(last_packet_number) + " on time: " + str(get_nice_time()))
            if e.message.find("Bad file descriptor") > 0 or e.message.find("16") > 0 or type(e) == TimeoutError:
                log("sleeing 2")
                time.sleep(2)
                connected = False
                a.conn.disconnect()
            if type(e) == TimeoutError or e.message.find("112, 'Host is down'") > 0:
                if a is None or packet == a.last_packet_number:
                    timeout_count += 1
                    log("times to restart: " + str(5 - timeout_count))
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
                log(traceback.format_exc())
                sys.exit()
        except Exception as e:
            time.sleep(1)
            log("got: " + str(e) + " at packet: " + str(last_packet_number)  + " on time: " + str(get_nice_time()))
            log(traceback.format_exc())
    return


if __name__ == "__main__":
    import csv
    a = None
    
    with gzip.open(sys.argv[1], 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        print("Writing to: " + sys.argv[1])
        connected = False
        while True:
            try:
                if not connected:
                    connected = True
                    a = BedditStreamer()
                channel1, channel2 = a.get_reading()
                #print(channel1, channel2)
                spamwriter.writerow([ time.time(),channel1[0], channel2[0]])
                csvfile.flush()
            except Exception:
                connected = False
                time.sleep(1)
                print("except " + str(time.time()))
                print(traceback.format_exc())
                
                

    
