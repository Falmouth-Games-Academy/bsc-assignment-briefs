import sys
import socket
import threading
import datetime

from queue import *
from commands import *


messageQueue = Queue()

clientIndex = 0
currentClients = {}
currentClientsLock = threading.Lock()

host = ''
port = 0

def debug_print(text):
    print(str(datetime.datetime.now()) + ':' + text)


def sendString(socket,str):

    data= bytes(str,'utf-8')
    try:
        if socket.send(len(data).to_bytes(2, byteorder='big')) == 0:
            raise socket.error

        if socket.send(data) == 0:
            raise socket.error
    except:
        return False

    return True



def clientReceive(sock):

    clientValid = True

    clientName = ''

    currentClientsLock.acquire()

    if sock in currentClients:
        clientName = currentClients[sock]
    else:
        clientName = 'N/A'
        currentClientsLock.release()
        return


    currentClientsLock.release()

    debug_print(clientName + ':clientReceive running')

    while clientValid == True:
        try:
            data = sock.recv(2)

            currentClientsLock.acquire()

            if sock in currentClients:
                clientName = currentClients[sock]
            else:
                clientName = 'N/A'
                clientValid = False
            currentClientsLock.release()

            if len(data) == 0:
                # on OSX, 'closed' sockets send 0 bytes, so trap this
                raise socket.error

            size = int.from_bytes(data, byteorder='big')

            data = sock.recv(size)

            if len(data) > 0:
                incoming_msg = data.decode('utf-8')

                debug_print('recv:' + clientName + ':' + incoming_msg)

                messageQueue.put(ClientMessage(sock,incoming_msg) )
            else:
                raise socket.error
        except socket.error:
            debug_print(clientName +':clientReceive - lost client')
            clientValid = False
            messageQueue.put(ClientLost(sock))


def acceptClients(serversocket):
    debug_print('acceptThread running')
    while(True):
        (clientsocket, address) = serversocket.accept()
        messageQueue.put(ClientJoined(clientsocket))


def handleClientLost(command):
    currentClientsLock.acquire()
    try:
        debug_print('Removing lost client:' + currentClients[command.socket])

        del currentClients[command.socket]
    except:
        pass

    currentClientsLock.release()

def handleClientJoined(command):
    global clientIndex

    clientName = 'client-' + str(clientIndex)
    clientIndex += 1

    currentClientsLock.acquire()
    currentClients[command.socket] = clientName
    currentClientsLock.release()

    message = 'Joined server as:' + clientName
    debug_print('send:' + clientName + ':' + message)

    sendString(command.socket, message)

    thread = threading.Thread(target=clientReceive, args=(command.socket,))
    thread.start()

def handleClientMessage(command):

    currentClientsLock.acquire()
    clientName = currentClients[command.socket]
    currentClientsLock.release()

    debug_print('send:' + clientName + ':'+command.message)

    if sendString(command.socket, 'Server says client sent message:'+ command.message) == False:
        messageQueue.put(ClientLost(command.socket))

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = 'localhost'
    port = 9000

    if len(sys.argv) > 1:
        host = sys.argv[1]

        if len(sys.argv) > 2:
            port = sys.argv[2]

    try:
        serversocket.bind((host, port))
    except socket.error as err:
        debug_print('Can\'t start server, is another instance running?')
        debug_print(format(err))
        exit()

    debug_print(host +':' + str(port))

    serversocket.listen(5)

    thread = threading.Thread(target=acceptClients,args=(serversocket,))
    thread.start()

    while True:

        if messageQueue.qsize()>0:
            command = messageQueue.get()

            if isinstance(command, ClientJoined):
                handleClientJoined(command)

            if isinstance(command, ClientLost):
                handleClientLost(command)

            if isinstance(command, ClientMessage):
                handleClientMessage(command)


if __name__ == '__main__':
    main()