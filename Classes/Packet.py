import hashlib
from Classes.Graph import Graph
from Classes.Segmenter import Segmenter

class Packet():
    SEPARATOR = '|'
    def __init__(self, packetRaw):
        self.raw = packetRaw
        self.isValid = False
        # print(self.__validateChecksum())
        
        try:
            splitted = list(reversed(packetRaw.split(self.SEPARATOR)))
            self.srcNode = splitted.pop()
            self.dstNode = splitted.pop()
            self.hopCount = int(splitted.pop())-1
            self.segmentationType = splitted.pop()
            self.messageId = splitted.pop()

            segment = splitted.pop().split("/")
            self.segmentNumber = segment[0]
            self.sequenceLength = segment[1]
            if self.segmentationType != Segmenter.ACK:
                self.checksum = splitted.pop()
                self.packetType = splitted.pop()
                self.payload = self.SEPARATOR.join(reversed(splitted))
                if self.hopCount > 0 and self.__validateChecksum():
                    self.isValid = True
            elif self.hopCount > 0:
                self.isValid = True
        except:
            pass

    def isValid(self):
        return self.isValid

    def __validateChecksum(self):
        #TODO: implement
        #return md5(self.payload) == self.checksum (or something else)
        return hashlib.md5(self.payload.encode()).hexdigest() == self.checksum

    def getACK(self):
        if not self.isValid:
            return ''
        return self.srcNode + '|' + self.dstNode + '|' + str(self.hopCount) + '|' + self.segmentationType + '|' + self.messageId + '|' + self.segmentNumber + '/' + self.sequenceLength
        

    
