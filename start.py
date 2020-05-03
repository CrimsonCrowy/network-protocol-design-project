# import socket
import threading
import re
from time import sleep
from Classes.Router import Router
from Classes.Server import Server
# from Classes.Graph import Graph
from Classes.Main import Main
from Classes.Network import Network
from Classes.Segmenter import Segmenter
from Classes.Crypto import Crypto
# import Classes * 



def start():
    port = 5124
    server = Server('STAS', "127.0.0.1", port, port, 1024)
    tServer = threading.Thread(target=server.recievePacket, daemon=True)
    tServer.start()
    router = Router()
    network = Network()
    segmenter = Segmenter()
    crypto = Crypto()

    main = Main(router, server, network, segmenter, crypto)






    while(True):
        sleep(0.1)
        msgFromClient = str(input("Please enter a message to the server: "))
        if msgFromClient == 'exit':
            return
        main.sendPayload('MESSAGE|' + msgFromClient, 'STAS', 'CHAT')
        # server.sendMsg(msgFromClient, "127.0.0.1", port)



if __name__ == "__main__":
    start()