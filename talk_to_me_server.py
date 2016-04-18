import socket
import random
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host, port = '', 5000
queue = 5

s.bind((host, port))
s.listen(queue)
print('Server started')

hi_list = ['hi', 'hello', 'howdy', 'hey', 'hola']
random_phrases = ["That's neat!\n", "Rad.\n", "Oh that's a little weird...\n", "Siiiiiiiick.\n"]
bye_list = ['bye', 'later', 'ttyl']

client, address = s.accept()
#sent before data received to emulate terminal
client.send(bytes("> ", 'utf-8'))
data = client.recv(4096)

#always accepting new connections
while True:
    while data:
        data_text = data.decode('utf-8')
        data_text = data_text.strip('\n').lower()
        #text appended with '> ' to emulate terminal
        if data_text in hi_list:
            client.send(bytes("Hi, I'm a server!\n> ", 'utf-8'))
            data = client.recv(4096)
        elif data_text in bye_list:
            client.send(bytes("See ya later!", 'utf-8'))
            client.close()
            #reset connection for the next client
            client, address = s.accept()
            data = client.recv(4096)
        else:
            #random response from random_phrases list
            response = random_phrases[random.randint(0, len(random_phrases) - 1)] + '> '
            client.send(bytes(response, 'utf-8'))
            data = client.recv(4096)

