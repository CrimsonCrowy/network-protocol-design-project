import threading
import re
from time import sleep
from Classes.Router import Router
from Classes.Server import Server
from Classes.Main import Main
from Classes.Network import Network
from Classes.Segmenter import Segmenter
from Classes.Crypto import Crypto
from Classes.Config import Config
from Classes.Queue import Queue


def start():
    nodeName = str(input("Enter your name: "))
    config = Config(nodeName)
    
    server = Server(config.getMyName(), config.getMyIp(), config.getMyPort(), config.getMyPort(), 1024)
    tServer = threading.Thread(target=server.recievePacket, daemon=True)
    tServer.start()

    router = Router()
    tRouter = threading.Thread(target=router.watchNeighbours, daemon=True)
    tRouter.start()

    queue = Queue()
    tQueue = threading.Thread(target=queue.run, daemon=True)
    tQueue.start()


    network = Network()
    segmenter = Segmenter()
    crypto = Crypto()

    main = Main(router, server, network, segmenter, crypto, queue, config)



    while(True):
        sleep(0.1)
        msgFromClient = str(input("Please enter a message to the server: "))
        if msgFromClient == 'exit':
            return
        if msgFromClient == 'graph':
            print(router.nodesState)
            print(router.localState)
            continue
        destination = msgFromClient.split(' ')[0]
        main.sendPayload('MESSAGE|' + msgFromClient, destination, 'CHAT')
        # main.sendPayload('MESSAGE|' + msgFromClient, config.getMyName(), 'CHAT')
        # server.sendMsg(msgFromClient, "127.0.0.1", port)



if __name__ == "__main__":
    start()