class Message():

    def __init__(self, id, text, url):
        self.id = id
        self.text = text
        self.url = url

    def to_dictionary(self):
        '''Return a dictionary representation of object that's already loaded.
        '''
        output = {
            'id' : self.id,
            'text' : self.text,
            'url' : self.url
        }
        return output