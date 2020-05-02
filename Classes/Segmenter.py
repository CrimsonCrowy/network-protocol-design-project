from Classes.Graph import Graph
from Classes.Router import Router
from Classes.Packet import Packet

class Segmenter():
    ACK = 'ACK'
    SEGMENT = 'SEGMENT'
    SEGMENT_SEPARATOR = '/'

    def setMain(self, main):
        self.main = main

    def __init__(self):
        self.segs = {}

    def handleIncomingPacket(self, packet):
        packet = self.__parsePacket(packet)

        if not packet:
            return None

        if packet.parts['segmentationType'] == self.ACK:
            # TODO: pass this packet to queue
            return None

        if packet.parts['segmentationType'] == self.SEGMENT and not packet.isValid():
            return None

        #TODO: send ACK packet

        return self.__combineSegments(packet)

    def __combineSegments(self, packet):
        # Clearing of old self.segs entries can be implemented
        if not packet.parts['srcNode'] in self.segs:
            self.segs[packet.parts['srcNode']] = {}
        if not packet.parts['messageId'] in self.segs[packet.parts['srcNode']]:
            self.segs[packet.parts['srcNode']][packet.parts['messageId']] = {}
        self.segs[packet.parts['srcNode']][packet.parts['messageId']][packet.parts['segmentNumber']] = packet.parts['payload']
        if len(self.segs[packet.parts['srcNode']][packet.parts['messageId']]) == packet.parts['sequenceLength']:
            combinedPayload = ''
            for i in range(1, packet.parts['sequenceLength'] + 1):
                combinedPayload += self.segs[packet.parts['srcNode']][packet.parts['messageId']][i]
            packet.parts['payload'] = combinedPayload
            self.segs[packet.parts['srcNode']].pop(packet.parts['messageId'], None)
            return packet
        return None

    def __parsePacket(self, packet):
        try:
            packet.parts['segmentationType'] = packet.splitted.pop()
            packet.parts['messageId'] = packet.splitted.pop()

            segment = packet.splitted.pop().split(self.SEGMENT_SEPARATOR)
            packet.parts['segmentNumber'] = int(segment[0])
            packet.parts['sequenceLength'] = int(segment[1])
            if packet.parts['segmentationType'] == self.SEGMENT:
                packet.parts['checksum'] = packet.splitted.pop()
                packet.parts['packetType'] = packet.splitted.pop()
                packet.parts['payload'] = Packet.SEPARATOR.join(reversed(packet.splitted))
        except:
            return None
        return packet
