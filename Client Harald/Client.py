# -*- coding: utf-8 -*-
import socket
import sys
from time import sleep
from threading import *
from MessageReceiver import *

#from threading import Thread


class Client:
    def __init__(self, host, server_port):
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        

        # TODO: Finish init process with necessary code
        receiver = MessageReceiver('client', 'connection')
        receiver.setName('receiverThread')
        receiver.start()
        writer = writeWindow()
        writer.setName('writerThread')
        writer.start()

        #self.run()

    def run(self):
        # Initiate the connection to the server
        #self.connection.connect((self.host, self.server_port))

        while(1):
            print 'running', activeCount(), 'threads'
            sleep(2)
            pass

    def disconnect(self):
        # TODO: Handle disconnection
        #self.connection.close()
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print message

    def send_payload(self, data):
        print data
        # use json on data
        #self.connection.send(data)
    
    def quit():
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        client = Client('localhost', 9998)
        client.run()
    elif len(sys.argv) == 2:
        client = Client(sys.argv[1], 9998)
        client.run()
    else:
        print 'Too many input arguments'
        sys.exit()

    #subprocess.popen([sys.executable, 'MessageReceiver.py'], 
    #           creationflags = subprocess.CREATE_NEW_CONSOLE)
