from Classes.Graph import Graph
from Classes.Router import Router

class Sequencer():
    ACK = 'ACK'
    SEGMENT = 'SEGMENT'
    def __init__(self, localNodeName):
        self.nodeName = localNodeName 
        self.server = None
        self.graph = None
        self.seqs = {}
        

    def setServer(self, server):
        self.server = server

    def handlePacket(self, packet):
        if self._shouldBeForwarded(packet):
            self._foward(packet)

        elif self._destinationReached(packet):
            self._handleReceivedPacket(packet)


    def _shouldBeForwarded(self, packet):
        return self.nodeName != packet.dstNode

    def _foward(self, packet):
        destination = self._extractDestinationFromPacket(packet)
        nextHop = self._getNextHop(destination)
        if nextHop:
            packet = self._modifyPacketBeforeForwarding(packet)
            self.server.sendPacket(packet, nextHop)

    def _destinationReached(self, packet):
        return return self.nodeName == packet.dstNode

    def _handleReceivedPacket(self, packet):
        if not packet.srcNode in self.seqs:
            self.seqs[packet.srcNode] = {}
        if not packet.messageId in self.seqs[packet.srcNode]:
            self.seqs[packet.srcNode][packet.messageId] = {}
        self.seqs[packet.srcNode][packet.messageId][packet.segmentNumber] = packet.payload #probably not only the payload, but the whole packet should be saved
        if len(self.seqs[packet.srcNode][packet.messageId]) == int(packet.sequenceLength):
            combinedPayload = ''
            for i in range(1, int(packet.sequenceLength)+1):
                combinedPayload += self.seqs[packet.srcNode][packet.messageId][i]
            self.handleFinishedSequence(packet.packetType, combinedPayload)



    def handleFinishedSequence(self, packetType, payload):
        # TODO: implement
        return True


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


