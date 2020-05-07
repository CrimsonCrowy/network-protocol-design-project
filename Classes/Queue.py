import time
from time import sleep

class Queue():
    SECONDS_TO_RESEND = 3
    TRIES_TO_DROP = 4


    def setMain(self, main):
        self.main = main


    def __init__(self):
        self.queToSend = list()
        self.queOnWait = list()


    def run(self):
        while(True):
            sleep(0.1)
            try:
                now = time.time()
                if len(self.queOnWait) > 0:
                    for e in range(len(self.queOnWait)):
                        if now - self.queOnWait[e][1] > self.SECONDS_TO_RESEND:
                            self.main.server.sendPacket(self.queOnWait[e][0])
                            print('packet resent!')
                            self.queOnWait[e][1] = now
                            self.queOnWait[e][2] += 1
                            if self.queOnWait[e][2] >= self.TRIES_TO_DROP:
                                self.queOnWait.pop(e)

                if len(self.queToSend) > 0:
                    while len(self.queToSend) > 0:
                        
                        packetToSend = self.queToSend.pop(0)
                        self.main.server.sendPacket(packetToSend)
                        
                        self.queOnWait.append([packetToSend, now, 0])
            except:
                continue


    def addToQue(self, packetObject):
        self.queToSend.append(packetObject)


    def receiveACK(self, packet):
        keysToPop = []
        for e in range(len(self.queOnWait)):
            if (self.queOnWait[e][0].parts['dstNode'] == packet.parts['srcNode'] and 
                self.queOnWait[e][0].parts['messageId'] == packet.parts['messageId'] and
                self.queOnWait[e][0].parts['segmentNumber'] == packet.parts['segmentNumber']):
                keysToPop.append(e)

        keysToPop = list(reversed(keysToPop))
        for ktp in keysToPop:
            self.queOnWait.pop(ktp)
