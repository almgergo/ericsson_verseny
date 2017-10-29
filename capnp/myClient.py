import socket
import sys
import capnp
import Bugfix_capnp
import Request_capnp
import Response_capnp
from time import sleep

HOST, PORT = "ecovpn.dyndns.org", 11223


def getLoginMessage():
    request = Request_capnp.Request.new_message()

    login = request.init('login')
    login.team = '42'
    login.hash = 'r06176kpltk360ooeamvb6eauq1uu1taw9qh'
    return request

def fixBugMessage(bugCount):
    request = Request_capnp.Request.new_message()
    bugfix = request.init('bugfix')
    bugfix.bugs = bugCount
    bugfix.message = 'Fixed'
    return request

def establishConnection(cnt):
# Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(getLoginMessage().to_bytes())

    # Receive data from the server and shut down
        response = Response_capnp.Response.from_bytes(sock.recv(2048))
        # print (response)
        # print (response.bugfix.bugs)

        i = response.bugfix.bugs-1
        isEnd=False
        while (not isEnd and i > -1):
            # print('bugfix cnt: ' +str(i) + '\n')            
            sock.sendall(fixBugMessage(i).to_bytes())
            response = Response_capnp.Response.from_bytes(sock.recv(2048))
            # print (response)

            which = response.which()
            # print('WHICH: ' + str(which) + (' bugs: ' + str(response.bugfix.bugs) if which=='bugfix' else  '' ))
            if (which=='end'):
                if (response.end=='true'):
                    i = -1
                    isEnd=True
                    print('DONE')
                else:
                    i -= 1
            elif (which=='bugfix'):
                if (response.bugfix.bugs > 0 ):
                    i = response.bugfix.bugs-1
                else:
                    i -= 1

        print('bugfix cnt: ' +str(cnt) + '\n')           
        sock.sendall(fixBugMessage(cnt).to_bytes())
        response = Response_capnp.Response.from_bytes(sock.recv(2048))
        print (response)

# for i in range(255,256):
    # print('fixing ' + str(i) + ' bugs')
establishConnection(255)
    # sleep(0.3)
    
    