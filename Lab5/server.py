import socket
import sys
import time

if len(sys.argv) <= 1:
    print('Not enough arguments passed. Enter server port number')
    sys.exit(2)

host = ''
port = int(sys.argv[1])


# Create a server socket and bind it.
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind((host, port))
try:
    while 1:
        # Listen on the bound socket and accept a connection if it comes in.
        print('\nReady to serve...')
        serv_sock.listen()
        cli_sock, addr = serv_sock.accept()
        print('Received a connection from: ', addr)

        message = cli_sock.recv(1024)
        print(message)

        getreq = message.splitlines()[0]
        print(getreq)

        url = getreq.split('')[1]
        print(str.encode(url))

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

        # Get the filename from the message.
        filename = message.split()[1].partition("/")[2]
        print(filename)

        fileExist = False
        filetouse = "/" + filename
        print(filetouse)


        try:
            # Find if the file exists in the cache or not.
            f = open(filetouse[1:], "r")
            outputdata = f.readlines()
            fileExist = True
            # Cache Hit
            cli_sock.send(b"HTTP/1.1 200 OK\r\n")
            cli_sock.send(b"Content-Type:text/html\r\n")
            # Read rest of the file from cache
            for i in range(0, len(outputdata)):
                cli_sock.send(outputdata[i])
            print('Read from cache')
            f.close()

        # Cache miss
        except IOError:
            if fileExist == False:
                # File does not exist in cache create a new socket to get the new page
                host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Hostname: "+webserver)
                try:
                    host_sock.connect((webserver, 80))
                    fileobj = host_sock.makefile('r', 0)
                    fileobj.write("GET" + "http://" + filename + "HTTP/1.1\n\n")
                    buffer = fileobj.readlines()
                    temp_file = open("./" + filename, "wb")
                    for line in buffer:
                        temp_file.write(str.encode(line))
                        cli_sock.send(str.encode(line))
                    temp_file.write(cs_header + str.encode(str(time.time())))
                    cli_sock.send(cs_header + str.encode(str(time.time())))
                    temp_file.write(b"X-Forwarded-For: " + str.encode(addr))
                    cli_sock.send(b"X-Forwarded-For: " + str.encode(addr))

                except:
                    print("Unknown request")
            else:
                # File was not found by host
                cli_sock.send(b"HTTP/1.0 404 File Not Found\r\n")
                cli_sock.send(b"Content-Type:text/html\r\n")
                cli_sock.send(b"\r\n")

        cli_sock.close()
except KeyboardInterrupt:
    print('Caught key interruption')
    print('Proxy Server stopped ...')
finally:
    print("Closing Server Socket ...")
    serv_sock.close()
