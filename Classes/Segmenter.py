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
        # self.nodeName = localNodeName 
        self.server = None
        self.graph = None
        self.segs = {}
        

    # def setServer(self, server):
    #     self.server = server

    # def handlePacket(self, packet):
    #     if self._shouldBeForwarded(packet):
    #         self._foward(packet)

    #     elif self._destinationReached(packet):
    #         self._handleReceivedPacket(packet)


    def _shouldBeForwarded(self, packet):
        return self.nodeName != packet.dstNode

    def _foward(self, packet):
        destination = self._extractDestinationFromPacket(packet)
        nextHop = self._getNextHop(destination)
        if nextHop:
            packet = self._modifyPacketBeforeForwarding(packet)
            self.server.sendPacket(packet, nextHop)

    def _destinationReached(self, packet):
        return self.nodeName == packet.dstNode

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

    # def handleFinishedSequence(self, packetType, payload):
    #     # TODO: implement
    #     return True


    def _isUpdatePacket(self, packet):
        # TODO: implement
        return True

    def _handleUpdatePacket(self, packet):
        nodeState = self._extractNodeStateFromPacket(packet)
        if nodeState and self.nodeStateShouldBeUpdated(nodeState):
            self._saveNodeState(nodeState)
            self._floodUpdatePacket(packet)
            self._regenerateTopologyGraph()

        

    def _extractNodeStateFromPacket(self, packet):
        nodeState = packet
        # TODO: implement
        return nodeState

    def nodeStateShouldBeUpdated(self, nodeState):
        # TODO: compare version numbers and return True/False
        return nodeState

    def _floodUpdatePacket(self, packet):
        # TODO: implement
        pass

    def _extractDestinationFromPacket(self, packet):
        # TODO: implement
        return 'E'

    def _getNextHop(self, destination):
        try:
            return self.graph.dijkstra(self.nodeName, destination)[1]
        except:
            return False

    def _modifyPacketBeforeForwarding(self, packet):
        # TODO: decrease packet hops before timeout or whatever
        return packet


