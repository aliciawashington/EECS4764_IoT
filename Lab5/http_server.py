from machine import Pin
import socket
import time
import sys
from  _thread import *
import network

ssid = 'Columbia University' #'Verizon_JSVC7Z'
password = ''                #'noisy6-hist-pod'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())


def proxy_server(webserver, port, conn, addr, message):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((webserver, port))
        server.sendall(message)
        while True:
            reply = server.recv(1024)

            if len(reply) > 0:
                conn.sendall(reply)
                print(f' Request done: {addr[0]}, {webserver}')
            else:
                break
        client.close()
    except socket.error as err:
        print(err)
        server.close()
        client.close()

def clientReq(client, addr, message):

    getreq = message.splitlines()[0]
    url = str(getreq.split()[1])

    lhttp_pos = url.find("://")
    if (lhttp_pos == -1):
        ltemp = url
    else:
        ltemp = url[(lhttp_pos + 3):]
    lport_pos = ltemp.find(":")
    lwebserver_pos = ltemp.find("/")
    if lwebserver_pos == -1:
        lwebserver_pos = len(ltemp)
    webserver = ""
    port = -1
    if (lport_pos == -1 or lwebserver_pos < lport_pos):
        port = 80
        webserver = ltemp[:lwebserver_pos]
    else:
        port = int((ltemp[(lport_pos + 1):])[:lwebserver_pos - lport_pos - 1])
        webserver = ltemp[:lport_pos]
    
    proxy_server(webserver, port, client, addr, message)


def main():
    try:
        host = ''
        port = 8080
        maxtime = 60
        timeout = time.time() + maxtime

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print(f'Now Listening on port {port}')

        while True:
            client, addr = server.accept()
            print('client connected from', addr)
            # Get the client request
            message = client.recv(1024)
            print(f'Client Request: {message}')
            if not message or time.time()>=timeout:
                print(f'Closing connection to Client: {addr}')
                client.close()
            else:
                start_new_thread(clientReq, (client, addr, message, ))
    except KeyboardInterrupt:
        print('Caught key interruption')
        print('Proxy Server stopped ...')
    finally:
        # Close server socket
        print("Closing Server Socket ...")
        server.close()

            



if __name__ == "__main__":
    main()
