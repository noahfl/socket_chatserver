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
            client.send(bytes("Enter the username you'd like to use:\n", 'utf-8'))
            username_req = client.recv(4096)
            while not username_req:
                client.send("Invalid username. Enter the username you'd like to use:\n")
                username_req = client.recv(4096)
            uname = username_req.decode('utf-8')
            new_user = User(client, address, uname)
            server.add_user(new_user)
            server.add_to_socket_list(client)
            message = uname + " HAS JOINED CHAT\n"
            server.transmit(client, message)
            #http://goo.gl/tn1Jg9
        #client already exists
        else:
            try:
                data = sock.recv(4096)
                #socket contains data
                if data:
                    user = next((x for x in server.USER_LIST if x.client == sock), None)
                    message = user.username + ": " + data.decode('utf-8')
                    server.transmit(sock, message)
                #no data
                else:
                    if sock in server.SOCKET_LIST:
                        user = next((x for x in server.USER_LIST if x.client == sock), None)
                        server.SOCKET_LIST.remove(sock)
                    server.transmit(socket, user.username + " HAS DISCONNECTED\n")
            except:
                server.transmit(socket, 'USER HAS DISCONNECTED\n')

server.close()
