import libnacl.sealed
import libnacl.public
from base64 import b64encode
from base64 import b64decode

class Crypto():

    def setMain(self, main):
        self.main = main

    def initialize(self):
        self.sk = self.main.config.getMySecretKey()
        self.pk = self.main.config.getMyPublicKey()
        self.decryptBox = libnacl.sealed.SealedBox(bytes.fromhex(self.pk), bytes.fromhex(self.sk))
        
    def encryptPayload(self, payload, destination):
        try:
            # Box can be initialized inly once per destination and then stored
            box = libnacl.sealed.SealedBox(self.getPublicKeyForDestination(destination))
            payload = payload.encode()
            ctxt = box.encrypt(payload)
            return b64encode(ctxt).decode("ascii")
        except:
            return None

    def decryptPacket(self, packet):
        try:
            payload = b64decode(packet.parts['payload'])
            packet.parts['payload'] = self.decryptBox.decrypt(payload).decode('utf-8')
            return packet
        except:
            return None

    def getPublicKeyForDestination(self, destination):
        return bytes.fromhex(self.main.config.publicKeys[destination])




    
