import bluetooth
import struct
from threading import Thread
import os.path
import os
import time

def get_beddit_mac():
    beddit_mac = None
    PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    with open (os.path.join(PATH, "beddit_mac.txt"), "r") as mac_file:
        beddit_mac=mac_file.readlines()[0].strip()
        
    return str(beddit_mac)





class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return


server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

phone,address = server_sock.accept()
print "Accepted connection from ",address

ser = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print("connecting to: " + str(get_beddit_mac()))
ser.connect((get_beddit_mac(), 1))
print("Connected")


def receive_and_pass(source, dest, logger, log_time=False):
    while True:
        #sbuffer = []
        data = source.recv(1)
        #sbuffer.append(data)
        
        #print(data, )
        logger.write(data)
        if log_time and data == "\n":
            logger.write(str(time.time()))
        logger.flush()
        dest.send(data)
        
        
        #if data == "\n":
        #    dest.send("".join(data))
        #    sbuffer = []
        
    
    
    
    

running = True

os.system("rm /tmp/file_phone_to_beddit.log")
os.system("rm /tmp/file_beddit_to_phone.log")
with open("/tmp/file_phone_to_beddit.log", 'w') as file_phone_to_beddit:
    with open("/tmp/file_beddit_to_phone.log", 'w') as file_beddit_to_phone:
        
        ser_phone = ThreadWithReturnValue(target=receive_and_pass, args=(ser, phone, file_beddit_to_phone))
        phone_ser = ThreadWithReturnValue(target=receive_and_pass, args=(phone, ser, file_phone_to_beddit, True))

        phone_ser.daemon=True
        ser_phone.daemon=True

        try:
            ser_phone.start()
            phone_ser.start()
            while running:
                time.sleep(1)

        except KeyboardInterrupt as e:
            print("Kill received")
            ser_phone.kill_received = True
            phone_ser.kill_received = True
            running = False
            raise e
    
