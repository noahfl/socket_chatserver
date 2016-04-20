import socket
import select
import app
from server_classes import User, Server, Request

host = ''
port = 5000
queue = 10

server = Server(host, port, queue)

while True:
    #TODO: fix flask/socket clash
    try:
        client, address = server.socket.accept()
        req = client.recv(4096).decode('utf-8')
        request = Request(req)
        server.close()
        app.run()
        server = Server(host, port, queue)
    except Exception as e:
        pass

    #use select module to find sockets that are ready to be read
    read, write, error = select.select(server.SOCKET_LIST, [], [], 0)
    
    #iterating through ready sockets
    for sock in read:
        #new connection request
        if sock == server.socket:
            client, address = server.socket.accept()
            client.send(bytes("Enter the username you'd like to use:\n", 'utf-8'))
            username_req = client.recv(4096)
            while not username_req:
                client.send("Invalid username. Enter the username you'd like to use:\n")
                username_req = client.recv(4096)
            uname = username_req.decode('utf-8').strip('\n')
            new_user = User(client, address, uname)
            server.add_user(new_user)
            server.add_to_socket_list(client)
            client.send(bytes("Welcome, " + new_user.username + "! To exit just type 'exit'.\n", 'utf-8'))
            #client.send(bytes(new_user.username + ": ", 'utf-8'))
            message = uname + " HAS JOINED CHAT\n"
            server.transmit(client, message)
        #client already exists
        else:
            try:
                data = sock.recv(4096)
                #socket contains data
                if data:
                    if data.decode('utf-8').strip('\n') == 'exit':
                        user = next((x for x in server.USER_LIST if x.client == sock), None)
                        server.SOCKET_LIST.remove(sock)
                        sock.send(bytes("You have disconnected.", 'utf-8'))
                        server.transmit(socket, user.username + " HAS DISCONNECTED\n")
                        continue
                    user = next((x for x in server.USER_LIST if x.client == sock), None)
                    message = user.username + ": " + data.decode('utf-8')
                    server.transmit(sock, message)
                    #sock.send(bytes(user.username + ": ", 'utf-8'))
                #no data
                else:
                    if sock in server.SOCKET_LIST:
                        user = next((x for x in server.USER_LIST if x.client == sock), None)
                        server.SOCKET_LIST.remove(sock)
                        server.transmit(socket, user.username + " HAS DISCONNECTED\n")
                    else:
                        server.transmit(socket, 'USER HAS DISCONNECTED\n')
            except:
                server.transmit(socket, 'USER HAS DISCONNECTED\n')

server.close()
