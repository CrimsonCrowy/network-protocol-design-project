#The reason I used Que instead of Queue, is because they are pronounced the same and for simplicities sake

import time
from time import sleep
#from packet import packet? Make sure this imports proper packet object

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
                        #Change the number bellow to however much time the program needs to check for packet waits(in seconds)
                        if now - self.queOnWait[e][1] > self.SECONDS_TO_RESEND:
                            self.main.server.sendPacket(self.queOnWait[e][0])
                            print('packet resent!')
                            #Send the packet again? Call To send fucnction and new timestamp
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

    #Adding to queue function
    def addToQue(self, packetObject):
        self.queToSend.append(packetObject)

    def receiveACK(self, packet):
        # print(packet.raw)
        keysToPop = []
        for e in range(len(self.queOnWait)):
            #xxx needs to be subsitutted with the proper identifier within the packet object, or if not a value, then the function that gets the identifiers
            if (self.queOnWait[e][0].parts['dstNode'] == packet.parts['srcNode'] and 
                self.queOnWait[e][0].parts['messageId'] == packet.parts['messageId'] and
                self.queOnWait[e][0].parts['segmentNumber'] == packet.parts['segmentNumber']):
                keysToPop.append(e)
                # self.queOnWait.pop(e)

        keysToPop = list(reversed(keysToPop))
        for ktp in keysToPop:
            self.queOnWait.pop(ktp)





# src = packetToSend.parts['srcNode']
# msgId = packetToSend.parts['messageId']
# sgn = packetToSend.parts['segmentNumber']
# if not src in self.queOnWait:
#     self.queOnWait[src] = {}
# if not msgId in self.queOnWait[src]:
#     self.queOnWait[src][msgId] = {}
# if not sgn in self.queOnWait[src][msgId]:
#     self.queOnWait[src][msgId][sgn] = {}
# self.queOnWait[src][msgId][sgn]['time'] = now
# self.queOnWait[src][msgId][sgn]['packet'] = packetToSend