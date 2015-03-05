# -*- coding: utf-8 -*-
from threading import Thread
from time import sleep
from Client import *

class MessageReceiver(Thread):
    def __init__(self, clientstr, connectionstr):

        

        Thread.__init__(self)

        self.daemon = True
        #self.start()

        print 'test'
        #Client.send_payload(client, 'test')

    def run(self):
        while(1):
            sleep(1)
            Client.send_payload(client, 'Hello')

class writeWindow(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        #self.start()

    def run(self):
        while 1:
            message = raw_input()
            if message == '\quit':
                quit()
            Client.send_payload(client, message)
