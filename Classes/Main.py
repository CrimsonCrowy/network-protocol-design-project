from Classes.Graph import Graph
from Classes.Segmenter import Segmenter
from Classes.Packet import Packet

class Main():

    def __init__(self, router, server, network, segmenter, crypto):
        self.router = router
        self.server = server
        self.network = network
        self.segmenter = segmenter
        self.crypto = crypto

        self.router.setMain(self)
        self.server.setMain(self)
        self.network.setMain(self)
        self.segmenter.setMain(self)
        self.crypto.setMain(self)
        


    def handleReceivedPacket(self, raw):
        packet = Packet(raw)
        segment = None

        # print(packet.isValid)

        
        # may forward packet or drop it. returns parsed paket if we are destination or if destination is broadcast. None otherwise.
        packet = self.network.handleIncomingPacket(packet) 

        # handles relationship with message queue regarding ACK, ckecks checksum. Parses packet up to payload.
        if packet:
            #packet is the same packet object, but has compiled/combined payload.
            packet = self.segmenter.handleIncomingPacket(packet)

        if packet:
            packet = self.crypto.decryptPacket(packet)

        if packet:
            print(packet.parts)

        # if segment and segment.parts.packetType == 'CHAT':
        #     segment = segmentationLayer.handleIncomingPacket(segment)

        # if segment and segment.parts.packetType == 'ROUTING':
        #     segment = router.handleIncomingPacket(segment)


    def sendPayload(self, payload, destination, packetType):
        
        #returns null if does not have destination node's key?
        payload = self.crypto.encryptPayload(payload, destination)

        if payload:
            # array of packets
            packets = self.segmenter.generatePacketsFromPayload(payload, destination, packetType)

        if packets:
            packets = self.network.addDataToOutgoingPackets(packets, destination)

        for packet in packets:
            self.server.sendMsg(packet.raw, "127.0.0.1", 5124)

        # if packets:
        #     queue.add(packets)




    
