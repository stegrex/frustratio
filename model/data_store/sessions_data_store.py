import json
import time
import lib.bottle.bottle as bottle
from model.objects.user import User
from model.data_store.drivers.redis_driver import RedisDriver
from model.data_store.users_data_store import UsersDataStore

class SessionsDataStore():

    def __init__(self, sessionDriver=None):
        if sessionDriver:
            self.sessionDriver = sessionDriver
        else:
            self.sessionDriver = RedisDriver()
        #self.usersDataStore = UsersDataStore()

    def start_session(self, user, expireTime=3600):
        #import uuid
        #sessionID = str(uuid.uuid4())
        # TODO: Figure out what the response is supposed to be!
        sessionID = user.id
        response = self.sessionDriver.create(
            sessionID,
            json.dumps(user.to_dictionary()),
            expireTime
        )
        return sessionID

    def get_session_data(self, sessionID):
        response = self.sessionDriver.read(sessionID)
        if response:
            return json.loads(response)
        return response

    def renew_session(self, sessionID, expireTime=3600):
        return self.sessionDriver.renew(sessionID, expireTime)

    def get_remaining_session_time(self, sessionID):
        return self.sessionDriver.ttl(sessionID)

    def end_session(self, sessionID):
        '''Destroy session by deleting server storage.
        '''
        return self.sessionDriver.delete(sessionID)

    def set_cookie(self, key, value, expireTime=3600):
        return bottle.response.set_cookie(
            key,
            value,
            path='/',
            expires=int(time.time()) + expireTime
        )

    def get_cookie(self, key):
        return bottle.request.get_cookie(key)

    def delete_cookie(self, key):
        return bottle.response.set_cookie(
            key,
            '',
            path='/',
            expires=0
        )