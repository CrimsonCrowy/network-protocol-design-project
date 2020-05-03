from Classes.Packet import Packet

class Network():
    HOP_COUNT = '15'

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

        if packet.parts['dstNode'] == self.main.server.NODE_NAME:
            pass
        return packet
        


    def addDataToOutgoingPackets(self, packets, destination):
        ret = []
        for packet in packets:
            packet.raw = (self.main.config.getMyName() + Packet.SEPARATOR + destination 
                + Packet.SEPARATOR + self.HOP_COUNT + Packet.SEPARATOR + packet.raw)
            packet.parts['dstNode'] = destination
            ret.append(packet)

        return ret #probably returning packets array directly will work too
        






    
