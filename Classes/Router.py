from time import sleep
from Classes.Graph import Graph

class Router():
    BROADCAST = 'BROADCAST'

    def setMain(self, main):
        self.main = main

    def __init__(self):
        # self.nodeName = localNodeName 
        self.nodesState = {}
        self.localState = {
            'v': 0, # version 
            'n': {} # neighbours { 'Node name' : (int)weight }
        }

        self.server = None
        self.graph = None
        

    def setServer(self, server):
        self.server = server

    def __saveNodeState(self, nodeState, nodeName):
        self.nodesState[nodeName] = nodeState

    def __regenerateTopologyGraph(self):
        graph = {}
        graphArguments = []
        for originNodeAddress, neighbours in self.nodesState.items():
            if not 'n' in neighbours: 
                continue
            graph[originNodeAddress] = {}
            for neighbourNodeAddress, weight in neighbours['n'].items():
                if neighbourNodeAddress in graph and originNodeAddress in graph[neighbourNodeAddress]:
                    continue
                graph[originNodeAddress][neighbourNodeAddress] = weight
                graphArguments.append((originNodeAddress, neighbourNodeAddress, weight))
                graphArguments.append((neighbourNodeAddress, originNodeAddress, weight))

        # print(graphArguments)
        self.graph = Graph(graphArguments)


    # def handlePacket(self, packet):
    #     if self._shouldBeForwarded(packet):
    #         self._foward(packet)

    #     elif self._destinationReached(packet):
    #         self._handleReceivedPacket(packet)

    #     elif self._isUpdatePacket(packet):
    #         self._handleUpdatePacket(packet)

    # def _shouldBeForwarded(self, packet):
    #     # TODO: implement
    #     return False

    # def _foward(self, packet):
    #     destination = self._extractDestinationFromPacket(packet)
    #     nextHop = self._getNextHop(destination)
    #     if nextHop:
    #         packet = self._modifyPacketBeforeForwarding(packet)
    #         self.server.sendPacket(packet, nextHop)

    # def _destinationReached(self, packet):
    #     # TODO: check if this packet belongs to this node
    #     return False

    # def _handleReceivedPacket(self, packet):
    #     # TODO: implement
    #     return False

    # def _isUpdatePacket(self, packet):
    #     # TODO: implement
    #     return True

    def handleIncomingPacket(self, packet):
        packet = self.__parsePacket(packet)
        if not packet:
            return

        nodeState = self.__extractNodeStateFromPacket(packet)



        if nodeState and self.__nodeStateShouldBeUpdated(nodeState, packet.parts['updateInfoNodeName']):
            self.__saveNodeState(nodeState,packet.parts['updateInfoNodeName'])
            self.__regenerateTopologyGraph()
            self.__floodUpdatePacket(packet)

    def __parsePacket(self, packet):
        try:
            packet.parts['updateInfoNodeName'] = packet.splitted.pop()
            packet.parts['version'] = int(packet.splitted.pop())
            packet.parts['neighbourCount'] = packet.splitted.pop()
            packet.parts['neighbours'] = {}
            for neighbour in packet.splitted:
                nInfo = neighbour.split('&')
                packet.parts['neighbours'][nInfo[0]] = nInfo[1]
        except:
            return None
        return packet

        

    def __extractNodeStateFromPacket(self, packet):
        nodeState = {
            'v': packet.parts['version'],
            'n': packet.parts['neighbours']
        }
        return nodeState

    def __nodeStateShouldBeUpdated(self, nodeState, fromNode):
        if not fromNode in self.nodesState:
            return True
        if self.nodesState[fromNode]['v'] < nodeState['v']:
            return True
        return False

    def __floodUpdatePacket(self, packet):
        # TODO: implement
        pass

    def _extractDestinationFromPacket(self, packet):
        # TODO: implement
        return 'E'

    def getNextHop(self, destination):
        if destination in self.main.config.neighbours:
            return destination
        try:
            return self.graph.dijkstra(self.main.config.getMyName, destination)[1]
        except:
            return False

    def _modifyPacketBeforeForwarding(self, packet):
        # TODO: decrease packet hops before timeout or whatever
        return packet

    def watchNeighbours(self):
        while True:
            # print('watchNeighbours Tick')
            sleep(5)
            












    # method for testing
    def setDummyData(self):
        self.nodesState['A'] = {
            'v': 0,
            'n': {'B': 1, 'C': 5, 'D': 6} 
        }
        self.nodesState['B'] = {
            'v': 0,
            'n': {'A': 1, 'C': 2}
        }
        self.nodesState['C'] = {
            'v': 0,
            'n': {'B': 2, 'A': 5, 'D': 10, 'E': 12} 
        }
        self.nodesState['D'] = {
            'v': 0,
            'n': {'A': 6, 'C': 10}
        }
        self.nodesState['E'] = {
            'v': 0,
            'n': {'C': 12}
        }
        self.nodesState['F'] = {
            'v': 0,
            'n': {'G': 3}
        }
        self.nodesState['G'] = {
            'v': 0,
            'n': {'F': 3}
        }

    # method for testing
    def getPath(self, _from, _to):
        try:
            return self.graph.dijkstra(_from, _to)
        except:
            return 'Destination does not exist'
