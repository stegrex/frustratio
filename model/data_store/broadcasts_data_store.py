import json
import time
from model.data_store.drivers.pymongo_driver import PyMongoDriver
from model.data_store.drivers.redis_driver import RedisDriver
from model.objects.broadcast import Broadcast

class BroadcastsDataStore():

    def __init__(self, driver=None, cache=None):
        if driver:
            self.driver = driver
        else:
            self.driver = PyMongoDriver('frustratio', 'broadcasts')
        if cache:
            self.cache = cache
        else:
            self.cache = RedisDriver()

    def get_empty_broadcast(self):
        return Broadcast()

    def create(self, broadcast):
        '''Store a newly created Broadcast instance.
        '''
        broadcast.createdTime = int(time.time())
        head = self.read_head()
        if head:
            if 'GLOBAL' in broadcast.nextBroadcastIDs:
                broadcast.nextBroadcastIDs['GLOBAL'].append(head.globalID)
            else:
                broadcast.nextBroadcastIDs['GLOBAL'] = [head.globalID]
            response = self.driver.replace(
                'GLOBAL_HEAD',
                broadcast.to_dictionary()
            )
        else:
            response = self.driver.insert(
                'GLOBAL_HEAD',
                broadcast.to_dictionary()
            )
        response = self.driver.insert(
            broadcast.id,
            broadcast.to_dictionary()
        )
        # Push to cache.
        self.cache.create(
            broadcast.id,
            json.dumps(broadcast.to_dictionary())
        )
        self.cache.create(
            'GLOBAL_HEAD',
            json.dumps(broadcast.to_dictionary())
        )
        # TODO: Throw exception here instead.
        if response:
            return broadcast
        else:
            return None

    def read_head(self, namespace='GLOBAL'):
        '''Return the current head of the Broadcasts list.
        '''
        return self.read(namespace + '_HEAD')

    def read(self, id=None):
        '''Return a Broadcast instance given an ID.
        '''
        cacheResponse = self.cache.read(id)
        if cacheResponse:
            response = json.loads(cacheResponse)
        else:
            response = self.driver.get(id)
        if not response:
            return None
        broadcast = Broadcast()
        broadcast.from_dictionary(response)
        return broadcast

    def get_last(self, n):
        output = []
        count = 0
        node = self.read_head()
        #print(node.to_dictionary())
        while node and count < n:
            output.append(node)
            #print(node.to_dictionary())
            nextBroadcastIDs = node.nextBroadcastIDs.get('GLOBAL')
            if nextBroadcastIDs and len(nextBroadcastIDs) >= 1:
                nextNodeID = node.nextBroadcastIDs.get('GLOBAL')[0]
            else:
                nextNodeID = None
            node = self.read(nextNodeID)
            count += 1
        return output

    # TODO: Implement caching for this.
    def read_multiple(self, ids=[]):
        '''Return a list/dict of Broadcast instances given a list of IDs.
        '''
        if not ids:
            return {}
        response = self.driver.get_multiple(ids)
        output = {}
        for x in response:
            output[x] = Broadcast()
            output[x].from_dictionary(response[x])
        return output