import uuid
import cgi
from model.data_store.broadcasts_data_store import BroadcastsDataStore
from model.data_store.messages_data_store import MessagesDataStore

class BroadcastsResponse():

    def __init__(self, appType=None, broadcastsDataStore=None, messagesDataStore=None):
        self.appType = appType
        if broadcastsDataStore:
            self.broadcastsDataStore = broadcastsDataStore
        else:
            self.broadcastsDataStore = BroadcastsDataStore()
        if messagesDataStore:
            self.messagesDataStore = messagesDataStore
        else:
            self.messagesDataStore = MessagesDataStore()

    def get_all_messages_response(self):
        return self.messagesDataStore.get_all_messages_raw()

    def get_all_messages(self):
        return self.messagesDataStore.get_all_messages(self.appType)

    def process_broadcast(self, messageID, broadcaster):
        message = self.messagesDataStore.get_message(messageID)
        broadcast = self.broadcastsDataStore.get_empty_broadcast()
        broadcastID = str(uuid.uuid4())
        broadcast.id = broadcastID
        broadcast.globalID = broadcastID
        broadcast.messageID = messageID
        broadcast.broadcasterID = broadcaster.id
        broadcast.broadcasterData = broadcaster.to_dictionary()
        self.broadcastsDataStore.create(broadcast, self.appType)
        return message, broadcastID

    def get_last_broadcasts_response(self, n):
        broadcasts = self.get_last_broadcasts(n, self.appType)
        for x in range(len(broadcasts)):
            displayName = cgi.escape(broadcasts[x].broadcasterData['displayName'])
            broadcasts[x].broadcasterData['displayName'] = displayName
            broadcasts[x] = broadcasts[x].to_dictionary()
        return broadcasts

    def get_last_broadcasts(self, n, appType=None):
        return self.broadcastsDataStore.get_last(n, appType)