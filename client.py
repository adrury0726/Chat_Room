import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        #Creating the message box that will pop up for entering username/nickname
        msg = tkinter.Tk()
        msg.withdraw()

        #Asking for something, and result will be the nickname
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        #Set to say the gui is not yet built
        self.gui_done = False
        #Set to say that our connection is already running
        self.running = True

        #GUI Thread set to build/maintain the gui
        gui_thread = threading.Thread(target=self.gui_loop)
        #Receive thread set to deal with the server connection
        receive_thread = threading.Thread(target=self.receive)

        #Starting both threads
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        #Set background to be a color
        self.win.configure(bg="lightgray")

        #Set our chat box label
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)


        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        #Need set to disable so user can't change what's in text history
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        #When this button is clicked, this function will be called
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        #Whenever the window is closed, the stop function terminates the program
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        #Deletes all text from beginning to the end
        self.input_area.delete('1.0', 'end')

    #This is where we program the stop function
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')

                        #Appends message at the end
                        self.text_area.insert('end', message)

                        #Always scroll to the end with messages
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST, PORT)
