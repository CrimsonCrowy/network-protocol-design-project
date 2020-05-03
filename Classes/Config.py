
class Config():

    def __init__(self, nodeName):
        self.__nodeName = nodeName
        getattr(self, 'profile_' + nodeName)()
        self.neighbours = {
            'stas': ("127.0.0.1", 5111),
            'tino': ("127.0.0.1", 5112),
            'olaf': ("127.0.0.1", 5113),
        }

        self.publicKeys = {
            'stas': '76c0ea764d6d4efbc9b49bf0f8ba4f363731000153a914ab1c9975bcb7efde19',
            'tino': '2b8c7293c8324d6bf982a479776a2e3153262c73a8ad951f8cb495175db46e2f',
            'olaf': 'a83c347021403b2d3bbab3d804896b2eb9454ddbbab5a223def6f1b52a411b78',
        }

        #TODO: load address:port from yaml or whatever

    def getMyName(self):
        return self.__nodeName

    def getMyIp(self):
        return self.IP

    def getMyPort(self):
        return self.port

    def getMySecretKey(self):
        return self.secretKey

    def getMyPublicKey(self):
        return self.publicKeys[self.getMyName()]

    def profile_stas(self):
        self.IP = "127.0.0.1"
        self.port = 5111
        self.neighbours = ['tino']
        self.secretKey = '21979c5b0f8a43f9d5e5a77e1cd8d1e7c77d1c2383930096daae743c9bc469cb'

    def profile_tino(self):
        self.IP = "127.0.0.1"
        self.port = 5112
        self.neighbours = ['stas', 'olaf']
        self.secretKey = '53c802ec5c94acb2eca6a10cad685c5bcc4c749b0dd4a1b982673a48aa7397ef'

    def profile_olaf(self):
        self.IP = "127.0.0.1"
        self.port = 5113
        self.neighbours = ['tino']
        self.secretKey = 'acbda0e452ef4d90b6934b6047646a02faad7788bfad5f50f5771d9265f7918a'
        