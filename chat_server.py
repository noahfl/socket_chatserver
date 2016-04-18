import socket
import select
from server_classes import User, Server, Request

host = ''
port = 5000
queue = 10

server = Server(host, port, queue)

while True:

    #use select module to find sockets that are ready to be read
    read, write, error = select.select(server.SOCKET_LIST, [], [], 0)
    
    #iterating through ready sockets
    for sock in read:
        #new connection request
        if sock == server.socket:
            client, address = server.socket.accept()
            client.send("Enter the username you'd like to use:\n")
            username_req = client.recv(4096)
            while not username_req:
                client.send("Invalid username. Enter the username you'd like to use:\n")
                username_req = client.recv(4096)
            uname_req = Request(username.decode('utf-8'))
            server.add_user(User(client, address, uname_req.body))
            server.add_to_socket_list(client)

            #http://goo.gl/tn1Jg9




