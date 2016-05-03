# socket_chatserver

Program that creates a netcat-based chat server. Users can chose a username and chat with other people on the server. The server also used NLTK to report how many nouns are used in each message sent via the server.

##installation
Just download and make sure your NLTK packages are up to date (not doing this will cause the server to break). Also use python3.

##running
There are two ways to access the server: via the browser or via netcat. If you visit the server using the browser it will simply tell you to use netcat to access the server and will provide instructions on how to do so.

To use with netcat:
>nc localhost 5000

Note: You have to press enter after you make the initial request because the server uses the first request to check whether or not you are using a browser.

You will then be asked to enter a username. After that you are free to chat with others on the server (I did most of the testing by chatting with myself, but I set up the chat server on a CIMS PC and had my coworkers ssh to my machine and test it out). To exit the server just type 'exit'.

Note: When typing 'exit' you will be removed from the list of clients, but you have to actually exit netcat manually.
