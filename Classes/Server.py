import socket
from Classes.Router import Router
from Classes.Sequencer import Sequencer
from Classes.Packet import Packet
class Server():
    def __init__(self, localNodeName, localServerIP, localServerRecievePort, localServerSendPort, bufferSize):
        self.localIP = localServerIP
        self.name = localNodeName
        self.localRecievePort = localServerRecievePort
        self.localSendPort = localServerSendPort
        self.bufferSize = bufferSize
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localRecievePort))
        # self.router = Router(localServerIP + ':' + str(localServerRecievePort))
        self.router = Router(localNodeName)
        self.router.setServer(self)
        self.sequencer = Sequencer(localNodeName)
        self.sequencer.setServer(self)
        print(f"Server Successfully Started at {self.localIP} with port {self.localRecievePort}")

    def recievePacket(self):
        print("Ive started the listening process.")
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            try:
                packet = Packet(bytesAddressPair[0].decode())
                if not packet.isValid:
                    continue
                self.sequencer.handlePacket(packet)
            except:
                continue

            self.sendPacket(packet.getACK(), packet.srcNode) #TODO: router.sendPacket() should probably be sending packets to direct neighbours. For general destinations sendPacket() should be probably defined in Router
            
            # address = bytesAddressPair[1]
            # print(message)
            # print(address)


    def sendMsg(self, msgFromClient, finalAddressIP, finalAddressPort, flag):

        bytesToSend = str.encode(msgFromClient + "#" + str(finalAddressIP) + "#" + str(finalAddressPort) + "#"
                                 + flag)
        address = finalAddressIP, finalAddressPort
        # print(address)
        self.UDPServerSocket.sendto(bytesToSend, address)

    def sendPacket(self, rawPacket, address):
        bytesToSend = str.encode(packet)
        address = address.split(":")
        self.UDPServerSocket.sendto(bytesToSend, address)