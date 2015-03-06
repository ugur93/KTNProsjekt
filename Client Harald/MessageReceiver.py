# -*- coding: utf-8 -*-
from threading import Thread
from time import sleep
from Client import *

class MessageReceiver(Thread):
    def __init__(self, clientstr, connectionstr):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        while(1):
            sleep(1)
            Client.receive_message(client, 'Hey you')
