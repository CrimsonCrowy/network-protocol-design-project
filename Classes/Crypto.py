import libnacl.sealed
import libnacl.public
from base64 import b64encode
from base64 import b64decode

class Crypto():

    def setMain(self, main):
        self.main = main

    def __init__(self):
        self.sk = '3976512f3a5b2975e4b9e653a8903ff273988e15b81667c5cdc68b3110021a4a'
        self.pk = '87c0ee06daa600e51d14d02daaae299a109901d0a427dc5e1fd9809743122d22'
        self.decryptBox = libnacl.sealed.SealedBox(bytes.fromhex(self.pk), bytes.fromhex(self.sk))
        
    def encryptPayload(self, payload, destination):
        payload = payload.encode()
        # Box can be initialized inly once per destination and then stored
        box = libnacl.sealed.SealedBox(self.getPublicKeyForDestination(destination))
        ctxt = box.encrypt(payload)
        return b64encode(ctxt).decode("ascii")

    def decryptPacket(self, packet):
        try:
            payload = b64decode(packet.parts['payload'])
            packet.parts['payload'] = self.decryptBox.decrypt(payload).decode('utf-8')
            return packet
        except:
            return None

    def getPublicKeyForDestination(self, destination):
        # TODO: implement
        return bytes.fromhex(self.pk)




    
