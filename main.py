#original + while
# import socket
import threading
import re
from time import sleep
from Classes.Router import Router
from Classes.Server import Server
from Classes.Graph import Graph
# import Classes * 



def main():
    port = 5124
    deathServer = Server('Stas', "127.0.0.1", port, port, 1024)
    tServer = threading.Thread(target=deathServer.recievePacket, daemon=True)
    tServer.start()
    while(True):
        sleep(0.1)
        msgFromClient = str(input("Please enter a message to the server: "))
        if msgFromClient == 'exit':
            return
        deathServer.sendMsg(msgFromClient, "127.0.0.1", port, "Echo")



if __name__ == "__main__":
    main()