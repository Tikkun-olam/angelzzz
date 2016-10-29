import binascii
import os
import os.path
import struct
import numpy
import time
import gzip
import sys
import traceback
import bluetooth
from timeout import timeout, TimeoutError

debug = 'DEBUG' in os.environ and os.environ['DEBUG'] == "on"

class ProtocolError(Exception):
    pass


class BedditConnection(object):

    def __init__(self, connection):
        self.connection = connection

    def open_connection(self):
        self.connection.send("OK\n".encode())
        time.sleep(0.2)

        response_to_ok = self._receive(3)

        if response_to_ok != 'OK\n':
            raise ProtocolError("Got {} after OK".format(repr(response_to_ok)))

    def start_streaming(self):
        self.connection.send("START\n".encode())

    def stop_streaming(self):
        self.connection.send("STOP\n".encode())

    def disconnect(self):
        self.connection.close()

    def _receive(self, packet_size, timeout_max=1):
        data = None
        with timeout(timeout_max):
            data = self.connection.recv(packet_size)
            while len(data) < packet_size:
                if debug:
                    print("receiving " + str(len(data)) + "/" + packet_size)
                data = data + self.connection.recv(packet_size - len(data))

        return data

    def _read_packet(self):
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

        sample_array = numpy.fromstring(payload, "uint16")

        channel1 = sample_array[0::2]
        channel2 = sample_array[1::2]

        return (packet_number, channel1, channel2)

def get_beddit_mac():
    beddit_mac = None
    PATH = os.path.dirname(os.path.realpath(__file__))
    with open (os.path.join(PATH, "beddit_mac.txt"), "r") as mac_file:
        beddit_mac=mac_file.readlines()[0].strip()
    return str(beddit_mac)

class BedditStreamer:
    def __init__(self):
        self.port = 1
        try:
            with timeout(10):
                ser = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                ser.connect((get_beddit_mac(), self.port))
        except TimeoutError as e:
            print("connection timeout")
            self.port += 1
            ser.close()
            raise e
        self.conn = BedditConnection(ser)
        try:
        
            self.conn.open_connection()
            self.conn.start_streaming()
        
        except Exception as e:
            print("beddit dissconnect")
            self.conn.stop_streaming()
            self.conn.disconnect()
            raise e
        
    def get_reading(self):
        chan1 = []
        chan2 = []

        packet_number, channel1, channel2 = self.conn.read_sample_packet()
        for i in channel1:
            chan1.append(i)
        for i in channel2:
            chan2.append(i)
        return [chan1, chan2]
    def close(self):
        self.conn.stop_streaming()
        self.conn.disconnect()


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
                
                

    
