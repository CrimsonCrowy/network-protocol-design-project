from Classes.Graph import Graph
from Classes.Segmenter import Segmenter
from Classes.Packet import Packet

class Main():

    def __init__(self, router, server, network, segmenter):
        self.router = router
        self.server = server
        self.network = network
        self.segmenter = segmenter

        self.router.setMain(self)
        self.server.setMain(self)
        self.network.setMain(self)
        self.segmenter.setMain(self)
        


    def handleReceivedPacket(self, raw):
        packet = Packet(raw)
        segment = None

        print(packet.isValid)

        
        # may forward packet or drop it. returns parsed paket if we are destination or if destination is broadcast. null otherwise.
        packet = self.network.handleIncomingPacket(packet) 

        # handles relationship with message queue regarding ACK, ckecks checksum. Parses packet up to payload.
        if packet:
            #segment is the same packet object, but has compiled payload.
            segment = segmentationLayer.handleIncomingPacket(packet)

        if segment:
            segment = encryption.decryptSegment(segment)

        if segment and segment.parts.packetType == 'chat':
            segment = segmentationLayer.handleIncomingPacket(segment)

        if segment and segment.parts.packetType == 'routing':
            segment = router.handleIncomingPacket(segment)


    def sendPayload(self, payload, destination):
        
        #returns null if does not have destination node's key?
        payload = encryption.encryptPayload(payload)

        # array of packets
        if payload:
            packets = segmentationLayer.generatePacketsFromPayload(payload)

        if packets:
            packets = networkLayer.addDataToOutgoingPackets(packets, destination)

        if packets:
            queue.add(packets)




    
