import socket
import select
from server_classes import User, Server, Request
import nltk

'''
@author: Noah Frazier-Logue
Program that creates a netcat-based chat server. Users can chose
a username and chat with other people on the server. The server
also used NLTK to report how many nouns are used in each message
sent via the server.
'''

host = ''
port = 5000
queue = 10

server = Server(host, port, queue)

#main loop
while True:

    #use select module to find sockets that are ready to be read
    read, write, error = select.select(server.SOCKET_LIST, [], [], 0)
    
    #iterating through ready sockets
    for sock in read:
        #new connection request
        if sock == server.socket:
            client, address = server.socket.accept()
            #request that determines course of action
            req = client.recv(4096).decode('utf-8')
            #if request can be parsed into Request object,
            #then the request is from a browser
            try:
                request = Request(req)
                html = ('<h1>This is the address for a socket chat server. ' +
                       'Please use netcat to use the chat feature.</h1>' + 
                       '<br />Command: nc localhost 5000' +
                       '<br />Note: You have to press space after you make ' + 
                       'the initial request because the server uses the first request ' +
                       'to check whether or not you are using a browser.')
                client.send(bytes(html, 'utf-8'))
                continue
            #otherwise set up the chat
            except Exception as e:
                client.send(bytes("Enter the username you'd like to use:\n", 'utf-8'))
                req = client.recv(4096).decode('utf-8')
                print('nc user')
            #client.send(bytes("Enter the username you'd like to use:\n", 'utf-8'))
            #req = client.recv(4096).decode('utf-8')
            username_req = req
            #ask for valid username until it is provided
            while (not username_req) or username_req == '':
                client.send("Invalid username. Enter the username you'd like to use:\n")
                username_req = client.recv(4096)
            uname = username_req.strip('\n')
            #add new user and add socket to list
            new_user = User(client, address, uname)
            server.add_user(new_user)
            server.add_to_socket_list(client)
            #welcome message
            client.send(bytes("Welcome, " + new_user.username + "! To exit just type 'exit'.\n", 'utf-8'))
            message = uname + " HAS JOINED CHAT\n"
            server.transmit(client, message)
        #client already exists
        else:
            try:
                data = sock.recv(4096)
                #socket contains data
                if data:
                    #if user wants to exit, remove from socket list and
                    #tell everyone else they're leaving
                    if data.decode('utf-8').strip('\n') == 'exit':
                        user = next((x for x in server.USER_LIST if x.client == sock), None)
                        server.SOCKET_LIST.remove(sock)
                        sock.send(bytes("You have disconnected.", 'utf-8'))
                        server.transmit(socket, user.username + " HAS DISCONNECTED\n")
                        continue
                    #get username based on whether or not the socket tied to
                    #the username is equivalent to the current socket
                    user = next((x for x in server.USER_LIST if x.client == sock), None)
                    decoded = data.decode('utf-8')
                    #separate and tag words in message
                    words = nltk.word_tokenize(decoded)
                    tagged = nltk.pos_tag(words)
                    counter = 0
                    #iterate through tuples of tagged words
                    for i in tagged:
                      #if the word is a singular or plural noun
                      if i[1] in ["NN", "NNS"]:
                          counter += 1
                    # message = username + message + number of nouns
                    message = user.username + ": " + decoded.strip('\n') + " (contains " + str(counter) + " nouns)\n"
                    server.transmit(sock, message)
                    #sock.send(bytes(user.username + ": ", 'utf-8'))
                #no data
                else:
                    #if user in list, remove and tell everyone
                    #they've disconnected
                    if sock in server.SOCKET_LIST:
                        user = next((x for x in server.USER_LIST if x.client == sock), None)
                        server.SOCKET_LIST.remove(sock)
                        server.transmit(socket, user.username + " HAS DISCONNECTED\n")
                    #tell everyone someone left if user cannot be determined
                    else:
                        server.transmit(socket, 'USER HAS DISCONNECTED\n')
            #something might have messed up with NLTK
            except:
                server.transmit(socket, 'POSSIBLE NLTK ERROR\n')
#close server
server.close()
