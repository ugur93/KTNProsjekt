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

        # the window
        self.root = Tk()
        self.root.title('KTN Chat')
        self.root.geometry('{}x{}'.format(400, 300))

        # user input
        self.send_var   = StringVar()
        self.user_name  = StringVar()

        # frames
        self.b_login_frame = Frame(self.root, height=30, width=100)
        self.b_login_frame.pack_propagate(False)
        self.b_login_frame.place(x=40, y=20)
        self.b_logout_frame = Frame(self.root, height=30, width=100)
        self.b_logout_frame.pack_propagate(False)
        self.b_logout_frame.place(x=40, y=60)
        self.b_names_frame = Frame(self.root, height=30, width=100)
        self.b_names_frame.pack_propagate(False)
        self.b_names_frame.place(x=40, y=100)
        self.b_chat_frame = Frame(self.root, height=30, width=100)
        self.b_chat_frame.pack_propagate(False)
        self.b_chat_frame.place(x=40, y=140)
        self.b_help_frame = Frame(self.root, height=30, width=100)
        self.b_help_frame.pack_propagate(False)
        self.b_help_frame.place(x=40, y=180)
        self.b_quit_frame = Frame(self.root, height=30, width=100)
        self.b_quit_frame.pack_propagate(False)
        self.b_quit_frame.place(x=40, y=220)

        self.w_text_frame = Frame(self.root, height=280, width=400, bg='Black')
        self.w_text_frame.pack_propagate(False)
        self.w_text_scrollbar = Scrollbar(self.w_text_frame)

        self.w_write_frame = Frame(self.root, height=20, width=400)
        self.w_write_frame.pack_propagate(False)

        #self.w_login_frame = Frame(self.root, height=20, width=40)
        #self.w_login_frame.pack_propagate(False)
        
        # buttons
        self.b_login    = Button(self.b_login_frame,    text='Log in'   , command=self.login_button)
        self.b_logout   = Button(self.b_logout_frame,   text='Log out'  , command=self.logout)
        self.b_names    = Button(self.b_names_frame,    text='List names', command=self.list_names)
        self.b_chat     = Button(self.b_chat_frame,     text='Open chat', command=self.open_chat)
        self.b_help     = Button(self.b_help_frame,     text='Help'     , command=self.help)
        self.b_quit     = Button(self.b_quit_frame,     text='Quit'     , command=self.quit)

        # text fields
        self.w_text = Text(self.w_text_frame, font=('Helvetica', 10), bg='Black', fg='Green')
        self.w_text.config(yscrollcommand=self.w_text_scrollbar.set)
        self.w_text_scrollbar.config(command=self.w_text.yview)
        self.w_text.insert(END, 'Welcome to KTN Chat\nType \quit to exit\n')

        self.w_write = Entry(self.w_write_frame, textvariable=self.send_var, width=400)
        self.w_write.bind('<Return>', self.read_input)

        self.w_login = Entry(self.b_login_frame, textvariable=self.user_name, width=400)
        self.w_login.bind('<Return>', self.login)
        self.user_name.set('username')


    def run(self):
        self.open_menu()

        self.root.mainloop()

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

    def login_button(self):
        self.b_login.pack_forget()
        self.w_login.pack()
    def login(self, event):
        self.send_payload('login ' + self.w_login.get())
        self.w_login.pack_forget()
        self.b_login.pack()

    def logout(self):
        pass
    def list_names(self):
        pass

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

    def help(self):
        pass
    def quit(self):
        self.disconnect()
        sys.exit()

    def receive_message(self, message):
        try:
            self.w_text.insert(END, message + '\n')
            self.w_text.yview(END)
        except:
            pass

    def read_input(self, event):
        send_var = self.w_write.get()
        if send_var == '\quit':
            self.open_menu()
        else:
            self.send_payload(send_var)
        self.w_write.delete(0, END)

    def send_payload(self, data):
        print data #for debugging
        # use json on data
        #self.connection.send(data)

    def disconnect(self):
        # TODO: Handle disconnection
        #self.connection.close()
        pass

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

