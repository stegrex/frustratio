from model.objects.message import Message

class MessagesDataStore():

    def __init__(self):
        self.messagesData = {
            'goddammit0' : {
                'text' : 'Goddammit.',
                'url' : 'X'
            },
            'goddammit1' : {
                'text' : 'GodDAMMit!!!',
                'url' : 'X'
            }
        }
        self.messageKeys = [
            'goddammit0',
            'goddammit1'
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