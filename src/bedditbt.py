import serial
import binascii
import struct
import numpy
import time
import gzip
import sys
import traceback

class ProtocolError(Exception):
    pass


class BedditConnection(object):

    def __init__(self, connection):
        self.connection = connection

    def open_connection(self):
        self.connection.write("OK\n")

        response_to_ok = self.connection.readline()

        if response_to_ok != 'OK\n':
            raise ProtocolError("Got {} after OK".format(repr(response_to_ok)))

    def start_streaming(self):
        self.connection.write("START\n")

    def stop_streaming(self):
        self.connection.write("STOP\n")

    def disconnect(self):
        self.connection.close()

    def _read_packet(self):
        header = self.connection.read(6)

        if len(header) != 6:
            raise ProtocolError()

        packet_number = struct.unpack('I', header[:4])[0]
        payload_length = struct.unpack('H', header[4:])[0]

        payload = self.connection.read(payload_length)

        crc = struct.unpack('I', self.connection.read(4))[0]

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

class BedditStreamer:
    def __init__(self):
        device = '/dev/rfcomm0'

        ser = serial.Serial()
        ser.port = device
        ser.open()
        self.conn = BedditConnection(ser)
        
        try:
            self.conn.open_connection()
            self.conn.start_streaming()
        
        except:
            self.conn.stop_streaming()
            self.conn.disconnect()
        
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
        
                    

def main():
    device = '/dev/rfcomm0'

    ser = serial.Serial()
    ser.port = device
    ser.open()

    conn = BedditConnection(ser)

    try:
        conn.open_connection()
        conn.start_streaming()

        while True:
            packet_number, channel1, channel2 = conn.read_sample_packet()
            for i in channel1:
                print i

    finally:
        conn.stop_streaming()
        conn.disconnect()


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
                
                

    
