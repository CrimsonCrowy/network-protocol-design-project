from Classes.Graph import Graph
from Classes.Segmenter import Segmenter
from Classes.Packet import Packet

class Main():

    def __init__(self, router, server, network, segmenter, crypto, queue, config, ui):
        self.router = router
        self.server = server
        self.network = network
        self.segmenter = segmenter
        self.crypto = crypto
        self.queue = queue
        self.ui = ui

        self.config = config

        self.router.setMain(self)
        self.server.setMain(self)
        self.network.setMain(self)
        self.segmenter.setMain(self)
        self.crypto.setMain(self)
        self.queue.setMain(self)
        self.ui.setMain(self)

        self.crypto.initialize()
        self.router.initialize()
        

    def handleReceivedPacket(self, raw):
        packet = Packet(raw)
        segment = None
        
        # may forward packet or drop it. returns parsed paket if we are destination or if destination is broadcast. None otherwise.
        packet = self.network.handleIncomingPacket(packet) 

        # handles relationship with message queue regarding ACK, ckecks checksum. Parses packet up to payload.
        if packet:
            #packet is the same packet object, but has compiled/combined payload.
            packet = self.segmenter.handleIncomingPacket(packet)

        if packet:
            packet = self.crypto.decryptPacket(packet)

        if packet and packet.parts['packetType'] == 'CHAT':
            self.ui.postRecievedMessage(packet)

        if packet and packet.parts['packetType'] == 'ROUTING':
            self.router.handleIncomingPacket(packet)


    def __preparePacketsForSending(self, payload, destination, packetType):
        packets = None
        #returns null if does not have destination node's key?
        payload = self.crypto.encryptPayload(payload, destination)

        if payload:
            # array of packets
            packets = self.segmenter.generatePacketsFromPayload(payload, destination, packetType)

        if packets:
            packets = self.network.addDataToOutgoingPackets(packets, destination)

        if packets:
            return packets
        return None


    def sendPayload(self, payload, destination, packetType):
        packets = self.__preparePacketsForSending(payload, destination, packetType)
        if packets:
            for packet in packets:
                self.queue.addToQue(packet)


    def sendPayloadAndForget(self, payload, destination, packetType):
        packets = self.__preparePacketsForSending(payload, destination, packetType)
        if packets:
            for packet in packets:
                self.server.sendPacket(packet)


    def forwardPacket(self, packet):
        self.server.sendPacket(packet)


    
