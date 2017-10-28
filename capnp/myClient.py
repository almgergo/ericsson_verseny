import socket
import sys
import capnp
import Bugfix_capnp
import Request_capnp
import Response_capnp
import numpy as np

HOST, PORT = "ecovpn.dyndns.org", 11223


def getLoginMessage():
    request = Request_capnp.Request.new_message()

    login = request.init('login')
    login.team = '42'
    login.hash = 'r06176kpltk360ooeamvb6eauq1uu1taw9qh'
    return request

def fixBugMessage(bugId):
    request = Request_capnp.Request.new_message()
    bugfix = request.init('bugfix')
    bugfix.bugs = 1
    bugfix.message = 'Fixed'
    return request

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    print(getLoginMessage().to_bytes())
    sock.connect((HOST, PORT))
    sock.sendall(getLoginMessage().to_bytes())

    # Receive data from the server and shut down
    response = Response_capnp.Response.from_bytes(sock.recv(2048))
    print (response)

    bugCount = response.bugfix.bugs
    for i in range(0,1):
        print('i: ' + str(i))
        sock.sendall(fixBugMessage(10).to_bytes())
        

    print(bugCount)

    response = Response_capnp.Response.from_bytes(sock.recv(2048))
    print (response)
    