# -*- coding: utf-8 -*-
from threading import Thread
from time import sleep
from Client import *
import json
import socket

class MessageReceiver(Thread):
    def __init__(self, client, connection):
        Thread.__init__(self)
        self.daemon = True
        self.connect = connection
        self.client = client 

    def run(self):
        while(1):
        	received_string = self.connect.recv(4096)
        	if received_string:
                    received_data=json.loads(received_string)
                    msgType = received_data['response']
                    message = received_data['content']
                    self.client.receive_message(msgType, message)        
