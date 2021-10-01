from socket import *
import sys

def main():
    serverPort = int(input("Enter the port number you would like to use"))

    # Create a new socket for the client
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare server socket
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Ready to Serve")

    while True:
        # Establish connection
        connectionSocket, addr = serverSocket.accept()

        # Receive messages from client
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:], "r")

            # Send one HTTP header line into socket
            connectionSocket.sendall(str.encode("HTTP/1.0 200 OK\n", 'iso-8859-1'))
            connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
            connectionSocket.send(str.encode('\r\n'))

            for line in f.readlines():
                connectionSocket.sendall(str.encode("" + line + "", "iso-8859-1"))
                line = f.read(1024)

            # Signify EOF
            connectionSocket.sendall(str.encode("\r\n", 'iso-8859-1'))

            f.close()

            # Close client socket
            connectionSocket.close()

        except IOError:
            # Send response message for file not found
            connectionSocket.sendall(str.encode("HTTP/1.0 404 Not Found\n", 'iso-8859-1'))

            # Close client socket
            connectionSocket.close()

    # Close server socket
    serverSocket.close()    # This code is unreachable I don't know why we have it here?

    # Exit system
    sys.exit(0)

if __name__ == "__main__":
    main()
