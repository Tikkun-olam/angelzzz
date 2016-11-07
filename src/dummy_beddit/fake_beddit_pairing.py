
import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

data = client_sock.recv(1024)
print "received [%s]" % data
client_sock.send("OK\n".encode())
data = client_sock.recv(1024)
print "received [%s]" % data
client_sock.send("INFO VERSION: 1.0; CHANNELS: normal, gained; SAMPLERATE: 140.0; SERIAL: 00:07:80:17:bd:e8; BUILD: 037d7f8\n".encode())
#data = client_sock.recv(1024)
#print "received [%s]" % data



client_sock.close()
server_sock.close()