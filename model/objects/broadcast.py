class Broadcast():

    def __init__(self):
        self.id = None
        self.globalID = None
        self.messageID = None
        self.broadcasterID = None
        #self.text = None
        #self.url = None
        self.nextBroadcastIDs = {}
        self.broadcasterData = None
        # Metadata
        self.createdTime = 0
        self.modifiedTime = 0

    def get_protected_fields(self):
        return [
            'id',
            'createdTime',
            'modifiedTime',
        ]

    def from_dictionary(self, broadcastDictionary):
        self.id = broadcastDictionary.get('id')
        self.globalID = broadcastDictionary.get('globalID')
        self.messageID = broadcastDictionary.get('messageID')
        self.broadcasterID = broadcastDictionary.get('broadcasterID')
        self.nextBroadcastIDs = broadcastDictionary.get('nextBroadcastIDs')
        self.broadcasterData = broadcastDictionary.get('broadcasterData')
        self.createdTime = broadcastDictionary.get('createdTime')
        return self.to_dictionary()

    def to_dictionary(self):
        '''Return a dictionary representation of object that's already loaded.
        '''
        output = {
            'id' : self.id,
            'globalID' : self.globalID,
            'messageID' : self.messageID,
            'broadcasterID' : self.broadcasterID,
            'nextBroadcastIDs' : self.nextBroadcastIDs,
            'broadcasterData' : self.broadcasterData,
            'createdTime' : self.createdTime
        }
        return output