
class Network():

    def setMain(self, main):
        self.main = main

    def handleIncomingPacket(self, packet):
        try:
            packet.parts['srcNode'] = packet.splitted.pop()
            packet.parts['dstNode'] = packet.splitted.pop()
            packet.parts['hopCount'] = int(packet.splitted.pop())-1
            if packet.parts['hopCount'] < 1:
                return None
        except Exception as e:
            return None

        return packet
        


    def addDataToOutgoingPackets(self, payload, destination):
        pass






    
