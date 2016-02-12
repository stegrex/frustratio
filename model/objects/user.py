class User():

    def __init__(self):
        self.id = None
        #self.email = None
        #self.userName = None
        self.displayName = None
        #self.passwordHash = None
        #self.fbUserID = None
        # Metadata
        self.createdTime = 0
        self.modifiedTime = 0
        self.removeSensitiveData = False

    def get_protected_fields(self):
        return [
            'id',
            'createdTime',
            'modifiedTime',
            'fbUserID'
        ]

    def from_dictionary(self, userDictionary):
        self.id = userDictionary.get('id')
        #self.email = userDictionary.get('email')
        #self.userName = userDictionary.get('userName')
        self.displayName = userDictionary.get('displayName')
        #self.passwordHash = userDictionary.get('passwordHash')
        #self.fbUserID = userDictionary.get('fbUserID')
        self.createdTime = userDictionary.get('createdTime')
        #if self.createdTime != None:
        #    self.createdTime = int(self.createdTime)
        #self.modifiedTime = userDictionary.get('modifiedTime')
        #if self.modifiedTime != None:
        #    self.modifiedTime = int(self.modifiedTime)
        return self.to_dictionary()

    def to_dictionary(self):
        '''Return a dictionary representation of object that's already loaded.
        '''
        output = {
            'id' : self.id,
            #'email' : self.email,
            #'userName' : self.userName,
            'displayName' : self.displayName,
            #'passwordHash' : self.passwordHash,
            #'fbUserID' : self.fbUserID,
            #'createdTime' : self.createdTime,
            #'modifiedTime' : self.createdTime
        }
        #if self.removeSensitiveData:
        #    del output['passwordHash']
        return output

    def remove_sensitive_data(self):
        self.removeSensitiveData = True
        self.passwordHash = None