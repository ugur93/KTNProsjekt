# -*- coding: utf-8 -*-
from threading import Thread
from time import sleep
from Client import *
import json

class MessageReceiver(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        while(1):
        	received_string = self.connection.recv(4096)
        	received_data=json.loads(message)
        	message = received_data['content']
        	self.client.receive_message(message)
            
            