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
# import Classes * 



def start():
    port = 5124
    server = Server('STAS', "127.0.0.1", port, port, 1024)
    tServer = threading.Thread(target=server.recievePacket, daemon=True)
    tServer.start()
    router = Router()
    network = Network()
    segmenter = Segmenter()

    main = Main(router, server, network, segmenter)






    while(True):
        sleep(0.1)
        msgFromClient = str(input("Please enter a message to the server: "))
        if msgFromClient == 'exit':
            return
        server.sendMsg(msgFromClient, "127.0.0.1", port, "Echo")



if __name__ == "__main__":
    start()