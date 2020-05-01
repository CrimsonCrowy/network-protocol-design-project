from Classes.Graph import Graph

class Router():
    BROADCAST = 'BROADCAST'
    def __init__(self, localNodeName):
        self.nodeName = localNodeName 
        self.nodesState = {}
        self.localState = {
            'v': 0, # version 
            'n': {} # neighbours { 'Node name' : (int)weight }
        }

        self.server = None
        self.graph = None
        

    def setServer(self, server):
        self.server = server

    def _saveNodeState(self, nodeAddress, nodeState):
        self.nodesState[nodeAddress] = nodeState

    def _regenerateTopologyGraph(self):
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


    def handlePacket(self, packet):
        if self._shouldBeForwarded(packet):
            self._foward(packet)

        elif self._destinationReached(packet):
            self._handleReceivedPacket(packet)

        elif self._isUpdatePacket(packet):
            self._handleUpdatePacket(packet)

    def _shouldBeForwarded(self, packet):
        # TODO: implement
        return False

    def _foward(self, packet):
        destination = self._extractDestinationFromPacket(packet)
        nextHop = self._getNextHop(destination)
        if nextHop:
            packet = self._modifyPacketBeforeForwarding(packet)
            self.server.sendPacket(packet, nextHop)

    def _destinationReached(self, packet):
        # TODO: check if this packet belongs to this node
        return False

    def _handleReceivedPacket(self, packet):
        # TODO: implement
        return False

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
