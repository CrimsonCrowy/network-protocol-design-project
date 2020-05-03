import hashlib
# from Classes.Graph import Graph
# from Classes.Segmenter import Segmenter

class Packet():
    SEPARATOR = '|'
    def __init__(self, packetRaw):
        self.raw = packetRaw
        self.__isValid = False
        # print(self.__validateChecksum())
        self.splitted = list(reversed(packetRaw.split(self.SEPARATOR)))
        self.parts = {}
        
        # try:
        #     splitted = list(reversed(packetRaw.split(self.SEPARATOR)))
        #     self.srcNode = splitted.pop()
        #     self.dstNode = splitted.pop()
        #     self.hopCount = int(splitted.pop())-1
        #     self.segmentationType = splitted.pop()
        #     self.messageId = splitted.pop()

        #     segment = splitted.pop().split("/")
        #     self.segmentNumber = segment[0]
        #     self.sequenceLength = segment[1]
        #     if self.segmentationType != Segmenter.ACK:
        #         self.checksum = splitted.pop()
        #         self.packetType = splitted.pop()
        #         self.payload = self.SEPARATOR.join(reversed(splitted))
        #         if self.hopCount > 0 and self.__validateChecksum():
        #             self.isValid = True
        #     elif self.hopCount > 0:
        #         self.isValid = True
        # except:
        #     pass

    def isValid(self):
        if not 'payload' in self.parts or not 'checksum' in self.parts or not 'hopCount' in self.parts:
            return False
        return self.generateMd5(self.parts['payload']) == self.parts['checksum']

    # def __validateChecksum(self):
    #     if not 'payload' in self.parts or not 'checksum' in self.parts or not 'hopCount' in self.parts:
    #         return False
    #     #TODO: implement
    #     #return md5(self.payload) == self.checksum (or something else)
    #     return self.parts['hopCount'] > 0 and self.generateMd5(self.parts['payload']) == self.parts['checksum']

    def generateMd5(self, string):
        return hashlib.md5(string.encode()).hexdigest()

    def getACK(self):
        # if not self.isValid:
        #     return ''
        return (self.parts['dstNode'] + self.SEPARATOR + self.parts['srcNode'] + self.SEPARATOR + str(self.parts['hopCount']) 
            + self.SEPARATOR + 'ACK' + self.SEPARATOR + self.parts['messageId'] + self.SEPARATOR 
            + str(self.parts['segmentNumber']) + '/' + str(self.parts['sequenceLength']))
        

    
