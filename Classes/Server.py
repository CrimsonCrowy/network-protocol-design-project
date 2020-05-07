import socket
import hashlib 
from Classes.Router import Router
from Classes.Segmenter import Segmenter
from Classes.Packet import Packet
class Server():


    def setMain(self, main):
        self.main = main


    def __init__(self, localNodeName, localServerIP, localServerRecievePort, localServerSendPort, bufferSize):
        self.localIP = localServerIP
        self.name = localNodeName
        self.localRecievePort = localServerRecievePort
        self.localSendPort = localServerSendPort
        self.bufferSize = bufferSize
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localRecievePort))
        print(f"Server Successfully Started at {self.localIP} with port {self.localRecievePort}")    


    def recievePacket(self):
        print("Ive started the listening process.")
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            rawPacket = bytesAddressPair[0].decode()
            self.main.handleReceivedPacket(rawPacket)


    def sendMsg(self, msgFromClient, finalAddressIP, finalAddressPort):
        address = finalAddressIP, finalAddressPort
        self.UDPServerSocket.sendto(str.encode(msgFromClient), address)


    def sendPacket(self, packet):
        try:
            nextHop = self.main.router.getNextHop(packet.parts['dstNode'])
            address = self.main.config.addressList[nextHop]
            self.UDPServerSocket.sendto(str.encode(packet.raw), address)
        except:
            pass
