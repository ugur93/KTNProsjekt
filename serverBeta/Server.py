# -*- coding: utf-8 -*-
import SocketServer
from datetime import datetime
import json
import socket
import sys
#import threading

""" 
Important: 
- A client shoud be assigned a TCP connection when it is running, independent of login/logouts. Managed in Sockets
- The users logged in are managed in Names, and logged_in boolean
- Chat history is stored in History 

"""

History = []
Names = []         
Sockets = []
class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    #def __init__(self,lock):

    
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.logged_in = 0
        self.username = ' '
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request # So that a client program gets a TCP connection when it is run
        print 'Client ' + str(self.ip) + ':' + str(self.port) + ' connected'
        #self.lock.acquire()
        Sockets.append(self.connection)
        #self.lock.release()
        
        # Loop that listens for messages from the client
        while True:
                try:
                    received_string = self.connection.recv(4096)
                         #if error==errno.WSAECONNRESET:
                         #       print "error"
                         #Sockets.remove(self.connection)
                         #self.connection.close()
                    if len(received_string) != 0:
                        received_data = json.loads(received_string)
                        request = received_data['request'];
                        content = received_data['content'];
                        if request == 'login':
                            self.handleLoginRequest(content)
                        elif request =='logout':
                            self.handleLogoutRequest()
                        elif request == 'msg':
                            self.handlemsgRequest(content)
                        elif request == 'names':
                             self.handleNamesRequest()
                        elif request == 'help':
                             self.handleHelpRequest()
                        else:
                             self.sendError('Invalid request')
                except Exception as error:
                     print error
                     break; 
            #print received_data            
            # TODO: Add handling of received payload from client

    def handleLoginRequest(self,data):
        if self.logged_in == 1:
            self.sendError('You are already logged in')
        else:
            if data in Names:
                self.sendError('The username is already in use!')
            else:
                self.username = data
                Names.append(self.username)
                self.sendMessage(self.username + ' logged in')
                print self.username + ' logged in'
                self.logged_in = 1
                self.sendHistory()
        #print 'logged in: ' + str(self.logged_in)

    def handleLogoutRequest(self):
        if self.logged_in == 1:
            Names.remove(self.username)
            #Sockets.remove(self.connection) # Moved to handlemsgRequest()
            self.sendMessage(self.username + ' logged out')
            print self.username + ' logged out'
            #self.connection.close()
            self.logged_in = 0
        elif self.logged_in == 0:
            print 'Some dude that is not logged in tried to log out :-$'
        #print 'logged in: ' + str(self.logged_in)    

    def handlemsgRequest(self,data):
        if self.logged_in == 1:
            self.sendMessage(self.username +' said: ' + data)
            print self.username + ' said: ' + data
        else:
            if data == 'closingTCPConn': # So that a client program can notify the server when it is about to terminate and close its TCP connection
                Sockets.remove(self.connection)
                print 'Client ' + str(self.ip) + ':' + str(self.port) + ' disconnected'
            else:
                self.sendError('You must be logged in, you can only request login or help')

    def handleNamesRequest(self):
        if self.logged_in == 1:
            Names_string = 'You are talking with:\n'
            for i in Names:
                Names_string = Names_string + i + '\n'
            self.sendInfo(Names_string)
        else:
            self.sendError('You must be logged in, you can only request login or help')
    def handleHelpRequest(self):
        self.sendInfo('No help for you')


    def sendError(self, error):
        self.sendResponse('error', error, 0)
    def sendInfo(self, info):
        self.sendResponse('info', info, 0)
    def sendHistory(self):
        History_string=' '
        for i in History:
            History_string = History_string + i + '\n'
        self.sendResponse('history', History_string, 0)
    def sendMessage(self, message):
        self.sendResponse('message',message,1)

    def sendResponse(self, response, content, broadcast):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = {'timestamp':currentTime, 'sender':self.username, 'response':response, 'content':content} #timestampLine + senderLine + responeLine + contentLine
        data = json.dumps(message)
        if content == 'message':
            addHistory=self.username+' said: '+content
            History.append(addHistory)
        if broadcast == 1:
            for socket_n in Sockets:
                socket_n.send(data)       
        else:
            self.connection.send(data)
        

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True
    
if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    #lock=threading.Lock();
    #HOST, PORT = '192.168.0.110', 9998
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 9998 # Resolves automaticly the server host's IP address
    print 'Server running on ' + str(HOST) + ':' + str(PORT)

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
