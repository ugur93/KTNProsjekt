# -*- coding: utf-8 -*-
import socket
import sys
from time import sleep
from threading import *
from Tkinter import *
#from MessageReceiver import *


from threading import Thread
class MessageReceiver(Thread):
    def __init__(self, clientstr, connectionstr):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        while(1):
            sleep(1)
            Client.receive_message(client, 'Hey you')


class Client:
    def __init__(self, host, server_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        
        receiver = MessageReceiver('client', 'connection')
        receiver.setName('receiverThread')
        receiver.start()

    def run(self):
        self.root = Tk()
        self.root.title('KTN Chat')
        self.root.geometry('{}x{}'.format(400, 300))
        self.send_var = StringVar()

        self.b_login = Button(self.root, text='Log in', command=self.open_chat)
        self.b_logout = Button(self.root, text='Log out', command=self.open_chat)
        self.b_names = Button(self.root, text='List names', command=self.open_chat)
        self.b_chat = Button(self.root, text='Open chat', command=self.open_chat)
        self.b_help = Button(self.root, text='Help', command=self.open_chat)
        self.b_quit = Button(self.root, text='Quit', command=self.quit)

        self.w_text_frame = Frame(self.root, height=280, width=400, bg='Black')
        self.w_text_frame.pack_propagate(False)
        self.w_write_frame = Frame(self.root, height=20, width=400)
        self.w_write_frame.pack_propagate(False)
        self.w_text_scrollbar = Scrollbar(self.w_text_frame)

        self.w_text = Text(self.w_text_frame, font=('Helvetica', 10), bg='Black', fg='Green') #, textvariable=self.recv_var
        self.w_text.config(yscrollcommand=self.w_text_scrollbar.set)
        self.w_text_scrollbar.config(command=self.w_text.yview)
        self.w_text.insert(END, 'Welcome to KTN Chat\nType \quit to exit\n')

        self.w_write = Entry(self.w_write_frame, textvariable=self.send_var, width=400)
        self.w_write.bind('<Return>', self.send_payload)

        self.open_menu()

        self.root.mainloop()


    def disconnect(self):
        # TODO: Handle disconnection
        #self.connection.close()
        pass

    def receive_message(self, message):
        try:
            self.w_text.insert(END, message + '\n')
            self.w_text.yview(END)
        except:
            pass
        

    def send_payload(self, event):
        
        send_var = self.w_write.get()
        if send_var == '\quit':
            self.open_menu()
        else:
            print send_var #for debugging
            # use json on data
            #self.connection.send(data)
        self.w_write.delete(0, END)

    def open_menu(self):
        self.w_text_frame.pack_forget()
        self.w_write_frame.pack_forget()
        self.w_text_scrollbar.pack_forget()
        
        self.w_text.pack_forget()
        self.w_write.pack_forget()

        self.b_login.pack()
        self.b_logout.pack()
        self.b_names.pack()
        self.b_chat.pack()
        self.b_help.pack()
        self.b_quit.pack()

    def open_chat(self):
        self.b_login.pack_forget()
        self.b_logout.pack_forget()
        self.b_names.pack_forget()
        self.b_chat.pack_forget()
        self.b_help.pack_forget()
        self.b_quit.pack_forget()

        self.w_text_frame.pack(side=TOP)
        self.w_write_frame.pack(side=BOTTOM)
        self.w_text_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.w_text.pack()
        self.w_write.pack()

    def quit(self):
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

