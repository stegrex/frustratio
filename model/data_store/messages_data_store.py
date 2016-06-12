from model.objects.message import Message

class MessagesDataStore():

    def __init__(self):
        self.messagesData = {
            'fuck0' : {
                'text' : 'Fuck!',
                'url' : '/static/audio/fuck0.wav'
            },
            'fuck1' : {
                'text' : 'Fuuuuuck...',
                'url' : '/static/audio/fuck1.wav'
            },
            'unfuck0' : {
                'text' : 'This needs to be unfucked.',
                'url' : '/static/audio/unfuck0.wav'
            },
            'dang0' : {
                'text' : 'Dangit!',
                'url' : '/static/audio/dang0.mp3'
            },
            'crap0' : {
                'text' : 'Crap.',
                'url' : '/static/audio/crap0.mp3'
            },
            'nuts0' : {
                'text' : 'Aw, nuts.',
                'url' : '/static/audio/nuts0.mp3'
            }
        }
        self.messageKeys = {
            '' : [
                'fuck0',
                'fuck1',
                'unfuck0'
            ],
            'CLEAN' : [
                'dang0',
                'crap0',
                'nuts0'
            ]
        }

    def get_message(self, id):
        messageData = self.messagesData.get(id)
        if not messageData:
            return None
        text = messageData.get('text')
        url = messageData.get('url')
        message = Message(id, text, url)
        return message

    def get_all_messages(self, appType=None):
        messages = []
        if not appType:
            appType = ''
        for x in self.messageKeys[appType]:
            messages.append(self.get_message(x))
        return messages

    def get_all_messages_raw(self):
        return self.messagesData