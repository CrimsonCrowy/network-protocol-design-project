import socket
import hashlib 
from Classes.Router import Router
from Classes.Segmenter import Segmenter
from Classes.Packet import Packet
class Server():
    NODE_NAME = 'STAS'

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
        # self.router = Router(localServerIP + ':' + str(localServerRecievePort))
        # self.router = Router(localNodeName)
        # self.router.setServer(self)
        # self.sequencer = Sequencer(localNodeName)
        # self.sequencer.setServer(self)
        print(f"Server Successfully Started at {self.localIP} with port {self.localRecievePort}")    

    def recievePacket(self):
        print("Ive started the listening process.")
        while True:
            # TODO: add packetReceivedFrom to Packet. Grab sender IP from bytesAddressPair[1] and compare to nodes list.
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            rawPacket = bytesAddressPair[0].decode()
            print(rawPacket)
            self.main.handleReceivedPacket(rawPacket)
            # try:
            #     packet = Packet(bytesAddressPair[0].decode())
            #     if not packet.isValid:
            #         continue
            #     self.sequencer.handlePacket(packet)
            # except:
            #     continue

            # self.sendPacket(packet.getACK(), packet.srcNode) #TODO: router.sendPacket() should probably be sending packets to direct neighbours. For general destinations sendPacket() should be probably defined in Router
            
            # address = bytesAddressPair[1]
            # print(message)
            # print(address)


    def sendMsg(self, msgFromClient, finalAddressIP, finalAddressPort):
        # payload = 'MESSAGE|' + msgFromClient
        # packetRaw = 'Furkan|Stas|223|SEGMENT|1s6Ak96|1/2|' + hashlib.md5(payload.encode()).hexdigest() + '|CHAT|' + payload

        # payload = ' second packet'
        # packetRaw2 = 'Furkan|Stas|223|SEGMENT|1s6Ak96|2/2|' + hashlib.md5(payload.encode()).hexdigest() + '|CHAT|' + payload

        # # bytesToSend = str.encode(msgFromClient + "#" + str(finalAddressIP) + "#" + str(finalAddressPort) + "#")
        # bytesToSend = str.encode(packetRaw)
        # bytesToSend2 = str.encode(packetRaw2)
        # address = finalAddressIP, finalAddressPort
        # # print(address)
        # self.UDPServerSocket.sendto(str.encode(''), address)
        # self.UDPServerSocket.sendto(bytesToSend, address)
        # self.UDPServerSocket.sendto(bytesToSend2, address)

        address = finalAddressIP, finalAddressPort
        self.UDPServerSocket.sendto(str.encode(msgFromClient), address)

    def sendPacket(self, rawPacket, address):
        bytesToSend = str.encode(packet)
        address = address.split(":")
        self.UDPServerSocket.sendto(bytesToSend, address)