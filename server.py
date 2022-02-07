import socket
import threading

HOST = '127.0.0.1' #Can find IP adrress using ipconfig if using an online server
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []    #Empty list of clients
nicknames = []  #Empty list of nicknames

#broadcast function that sends one messege to all connected clients

def broadcast(message):
    for client in clients:
        client.send(message)

#Need our handle function before the receive function since it takes clients as a parameter
#handle function that handles individual client connections
def handle(client):
    while True:
        try:
            #Want to recieve a message from client up to 1024 bytes
            message = client.recv(1024)

            #Tells us which index in the client's list it is then takes that index and gives that nickname
            print(f"{nicknames[clients.index(client)]} says {message}")

            #Broadcasts message if received successfully
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            #We need a break statement to end the while True loop
            break


#receive function that accepts new connections

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!") #Using formatted strings

        client.send("NICK".encode('utf-8')) #Using utf-8 for our unicode
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))  #Letting client know they're connected

        thread = threading.Thread(target = handle, args = (client,)) #Created a tuple by adding that comma at the end
        thread.start()

#We use the receive method because it calls the handle method, which calls the broadcast method.
#In other words, it runs everything.
print("Server Running...")
receive()