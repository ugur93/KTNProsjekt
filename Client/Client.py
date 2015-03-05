# -*- coding: utf-8 -*-
import socket
import sys
from MessageReceiver.py import MessageReceiver

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

        # TODO: Finish init process with necessary code
        receiver = MessageReceiver()
        receiver.start()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        print message

    def send_payload(self, data):
        while 1:
            message = raw_input()
            if message == '\quit':
                break
            send_payload(message)


if __name__ == '__main__':
    client = Client(sys.argv[1], 9998)
