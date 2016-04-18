import socket


class Server:
    USER_LIST = []
    SOCKET_LIST = []

    def __init__(self, host, port, queue):
        self.host = host
        self.port = port
        self.queue = queue
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(queue)
        self.add_to_socket_list(self.socket)
        print("Chat server started at " + str(host) + ":" + str(port))

    def add_to_socket_list(self, socket):
        self.SOCKET_LIST.append(socket)

    def add_user(self, user):
        self.USER_LIST.append(user)

    def transmit(self, socket, message):
        for sock in self.SOCKET_LIST:
            if (sock != self.socket and socket != sock):
                try:
                    sock.send(bytes(message, 'utf-8'))
                except socket.error as e:
                    sock.close()
                    self.SOCKET_LIST.riemove(sock)

    def close(self):
        self.socket.close()
        print("Server closed.")

class User:

    def __init__(self, client, address, username):
        self.client = client
        self.address = address
        self.username = username

class Request:

    def __init__(self, request):
        #for string version
        self.original_request = request

        req_list = request.split('\r\n')

        self.method, self.path, self.http_version = req_list[0].split(' ')

        #starting at index after initial info
        i = 1
        self.headers = {}
        while req_list[i] != '':
            header = req_list[i].split(': ')
            header_name = header[0]
            header_value = header[1]
            self.headers[header_name] = header_value
            i += 1
        #body is index after blank caused by \r\n\r\n
        self.body = req_list[req_list.index('') + 1]

    def __str__(self):
        return self.original_request
