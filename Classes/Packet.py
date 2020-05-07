import hashlib

class Packet():
    SEPARATOR = '|'
    def __init__(self, packetRaw):
        self.raw = packetRaw
        self.__isValid = False
        self.splitted = list(reversed(packetRaw.split(self.SEPARATOR)))
        self.parts = {}


    def isValid(self):
        if not 'payload' in self.parts or not 'checksum' in self.parts or not 'hopCount' in self.parts:
            return False
        return self.generateMd5(self.parts['payload']) == self.parts['checksum']

    def splitPayload(self):
        try:
            self.splitted = list(reversed(self.parts['payload'].split(self.SEPARATOR)))
        except:
            pass
        

    def generateMd5(self, string):
        return hashlib.md5(string.encode()).hexdigest()


    def getACK(self):
        return (self.parts['dstNode'] + self.SEPARATOR + self.parts['srcNode'] + self.SEPARATOR + str(self.parts['hopCount']) 
            + self.SEPARATOR + 'ACK' + self.SEPARATOR + self.parts['messageId'] + self.SEPARATOR 
            + str(self.parts['segmentNumber']) + '/' + str(self.parts['sequenceLength']))
        

    
