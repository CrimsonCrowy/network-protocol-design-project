import time
from time import sleep
from Classes.Graph import Graph

class Router():
    ROUTING = 'ROUTING'
    SECONDS_TILL_CONSIDERED_OFFLINE = 12

    def setMain(self, main):
        self.main = main

    def __init__(self):
        self.nodesState = {}
        self.localState = {
            'v': 0, # version 
            'n': {} # neighbours { 'Node name' : (int)weight }
        }

        self.server = None
        self.graph = None
        self.neighbours = {}
        self.reachableNodes = []
        

    def initialize(self):
        for neighbour in self.main.config.getMyNeighbours():
            self.neighbours[neighbour] = {
                'isOnline': False,
                'lastUpdateReceived': 0
            }


    def __saveNodeState(self, nodeState, nodeName):
        self.nodesState[nodeName] = nodeState

    
    def __regenerateTopologyGraph(self):
        graph = {}
        graphArguments = []
        self.reachableNodes = []
        rNodes = {}
        for originNodeAddress, neighbours in self.nodesState.items():
            if not 'n' in neighbours: 
                continue
            graph[originNodeAddress] = {}
            for neighbourNodeAddress, weight in neighbours['n'].items():
                rNodes[neighbourNodeAddress] = True
                if neighbourNodeAddress in graph and originNodeAddress in graph[neighbourNodeAddress]:
                    continue
                graph[originNodeAddress][neighbourNodeAddress] = weight
                graphArguments.append((originNodeAddress, neighbourNodeAddress, weight))
                graphArguments.append((neighbourNodeAddress, originNodeAddress, weight))

        rNodes.pop(self.main.config.getMyName(), None)
        for nodeName, n in rNodes.items():
            self.reachableNodes.append(nodeName)

        for neighbour in self.main.config.getMyNeighbours():
            if self.neighbours[neighbour]['isOnline'] and not neighbour in self.reachableNodes:
                self.reachableNodes.append(neighbour)

        self.graph = Graph(graphArguments)


    def handleIncomingPacket(self, packet):
        packet = self.__parsePacket(packet)
        if not packet:
            return

        nodeState = self.__extractNodeStateFromPacket(packet)

        if nodeState:
            self.__handleIfIsUpdatePacketFromNeighbour(packet.parts['updateInfoNodeName'])

        if nodeState and self.__nodeStateShouldBeUpdated(nodeState, packet.parts['updateInfoNodeName']):
            self.__saveNodeState(nodeState,packet.parts['updateInfoNodeName'])
            self.__regenerateTopologyGraph()
            self.__sendStateToAllNeighbours(nodeState, packet.parts['updateInfoNodeName'], packet.parts['srcNode'])


    def __parsePacket(self, packet):
        packet.splitPayload()
        try:
            packet.parts['updateInfoNodeName'] = packet.splitted.pop()
            packet.parts['version'] = int(packet.splitted.pop())
            packet.parts['neighbourCount'] = int(packet.splitted.pop())
            packet.parts['neighbours'] = {}
            for neighbour in packet.splitted:
                try:
                    nInfo = neighbour.split('&')
                    packet.parts['neighbours'][nInfo[0]] = int(nInfo[1])
                except:
                    pass
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
        if fromNode == self.main.config.getMyName():
            return False
        if not fromNode in self.nodesState:
            return True
        if self.nodesState[fromNode]['v'] < nodeState['v']:
            return True
        return False


    def __handleIfIsUpdatePacketFromNeighbour(self, fromNode):
        if fromNode in self.neighbours:
            self.neighbours[fromNode]['lastUpdateReceived'] = time.time()
            if not self.neighbours[fromNode]['isOnline']:
                self.neighbours[fromNode]['isOnline'] = True
                self.localState['n'][fromNode] = 1 # weight can be some random number
                self.localState['v'] += 1
                self.__regenerateTopologyGraph()
                self.__sendNodeFullTopology(fromNode)
                self.__sendStateToAllNeighbours(self.localState, self.main.config.getMyName())


    def __sendNodeFullTopology(self, nodeName):
        for stateNodeName, state in self.nodesState.items():
            self.main.sendPayload(self.__compilePayloadFromState(state, stateNodeName), nodeName, self.ROUTING)
        self.main.sendPayload(self.__compilePayloadFromState(self.localState, self.main.config.getMyName()), nodeName, self.ROUTING)


    def __compilePayloadFromState(self, state, nodeName):
        nodes = []
        for node, weight in state['n'].items():
            nodes.append(node + '&' + str(weight))
        return nodeName + '|' + str(state['v']) + '|' + str(len(state['n'])) + '|' + '|'.join(nodes)


    def __sendStateToAllNeighbours(self, nodeState, stateOwnerName, exceptNode = ''):
        for nodeName, weight in self.localState['n'].items():
            if nodeName != exceptNode:
                self.main.sendPayload(self.__compilePayloadFromState(nodeState, stateOwnerName), nodeName, self.ROUTING)


    def getNextHop(self, destination):
        if destination in self.main.config.getMyNeighbours():
            return destination
        try:
            return self.graph.dijkstra(self.main.config.getMyName(), destination)[1]
        except:
            return False


    def watchNeighbours(self):
        secsAfterLastNeighbourBroadcast = 10
        while True:
            secsAfterLastNeighbourBroadcast += 1
            sleep(1)
            if secsAfterLastNeighbourBroadcast >= 10:
                secsAfterLastNeighbourBroadcast = 0
                for neighbour in self.main.config.getMyNeighbours():
                    if neighbour != self.main.config.getMyName():
                        self.main.sendPayloadAndForget(self.__compilePayloadFromState(self.localState, self.main.config.getMyName()), neighbour, self.ROUTING)

            for neighbour in self.main.config.getMyNeighbours():
                if (self.neighbours[neighbour]['isOnline'] 
                    and time.time() - self.neighbours[neighbour]['lastUpdateReceived'] > self.SECONDS_TILL_CONSIDERED_OFFLINE):
                    self.neighbours[neighbour]['isOnline'] = False
                    self.localState['n'].pop(neighbour, None)
                    self.localState['v'] += 1
                    self.__regenerateTopologyGraph()
                    self.__sendStateToAllNeighbours(self.localState, self.main.config.getMyName())
                    














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
