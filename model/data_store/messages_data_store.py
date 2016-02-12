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
            }
        }
        self.messageKeys = [
            'fuck0',
            'fuck1',
            'unfuck0'
        ]

    def get_message(self, id):
        messageData = self.messagesData.get(id)
        if not messageData:
            return None
        text = messageData.get('text')
        url = messageData.get('url')
        message = Message(id, text, url)
        return message

    def get_all_messages(self):
        messages = []
        for x in self.messageKeys:
            messages.append(self.get_message(x))
        return messages

    def get_all_messages_raw(self):
        return self.messagesData