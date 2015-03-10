# -*- coding: utf-8 -*-
import SocketServer
from datetime import datetime
import json

History={}
Names=[]
class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.logged_in=0
        self.username=' '
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            try:
                received_string = self.connection.recv(4096)
                received_data=json.loads(received_string)
                request=received_data['request'];
                content=received_data['content'];
                if request=='login':
                    self.handleLoginRequest(content)
                elif request =='logout':
                    self.handleLogoutRequest()
                elif request=='msg':
                    self.handlemsgRequest(content)
                elif request=='names':
                     self.handleNamesRequest()
                elif request=='help':
                     self.handleHelpRequest()
                else:
                     self.sendError('Invalid request')
            except ValueError:
                    pass
                   

            #print received_data
            

            



            
            # TODO: Add handling of received payload from client
    def handleLoginRequest(self,data):
        if self.logged_in==1:
            self.sendError('You are already logged in')
        else:
            self.logged_in=1
            self.username=data
            Names.append(self.username)
            print self.username + ' logged in'
            self.sendHistory()
    def handleLogoutRequest(self):
        if self.logged_in==1:
            self.logged_in=0
            Names.remove(self.username)
            print self.username + ' logged out'
            self.connection.shutdown(1)
            
    def handlemsgRequest(self,data):
        if self.logged_in==1:
            self.sendMessage(data)
        else:
            self.sendError('You must be logged in, you can only request login or help')
    def handleNamesRequest(self):
        if self.logged_in==1:
            self.sendMessage(Names)
        else:
            self.sendError('You must be logged in, you can only request login or help')
    def handleHelpRequest(self):
        self.sendInfo('No help for you')


    def sendError(self, error):
        self.sendResponse('error', error,0)
    def sendInfo(self, info):
        self.sendResponse('info', info,0)
    def sendHistory(self):
        self.sendResponse('history',History,0)
    def sendMessage(self, message):
        self.sendResponse('message', message,1)

    def sendResponse(self,response, content,broadcast):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #timestampLine = "'timestamp:'" + '<' currentTime + '>' + ',\n'
        #senderLine = "'sender':" + '<' + username + '>' + ',\n'
        #responseLine = "'resopnse':" + '<' + response + '>' + ',\n'
        #contentLine = "'content':" + '<' + content + '>'
        message = {'timestamp':currentTime,'sender':self.username,'response':response,'content':content} #timestampLine + senderLine + responeLine + contentLine
        data = json.dumps(message)
        if content=='message':
            addHistory=self.username+'currentTime'
            History[addHistory]=data
        if broadcast==1:
            self.connection.sendall(data)
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
    HOST, PORT = '78.91.75.91', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
