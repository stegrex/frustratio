import uuid
from model.data_store.users_data_store import UsersDataStore
from model.data_store.sessions_data_store import SessionsDataStore

class SignonResponse():

    def __init__(self, sessionsDataStore=None, usersDataStore=None):
        if sessionsDataStore:
            self.sessionsDataStore = sessionsDataStore
        else:
            self.sessionsDataStore = SessionsDataStore()
        if usersDataStore:
            self.usersDataStore = usersDataStore
        else:
            self.usersDataStore = UsersDataStore(True)

    def signon(self, displayName):
        user = self.get_user_from_session()
        if user:
            return self.sessionsDataStore.get_cookie('sessionID')
        user = self.usersDataStore.get_empty_user()
        user.id = str(uuid.uuid4())
        user.displayName = displayName
        return self.start_user_session(user)

    def start_user_session(self, user, expireTime=3600):
        sessionID = self.sessionsDataStore.start_session(user, expireTime)
        if sessionID:
            self.sessionsDataStore.set_cookie('sessionID', sessionID, expireTime)
        return sessionID

    def get_user_from_session(self):
        sessionID = self.sessionsDataStore.get_cookie('sessionID')
        if not sessionID:
            return None
            return {'Error' : 'Not logged in.'}
        userDictionary = self.sessionsDataStore.get_session_data(sessionID)
        if not userDictionary:
            return None
            return {'Error' : 'Not logged in.'}
        user = self.usersDataStore.get_empty_user()
        user.from_dictionary(userDictionary)
        self.renew_session(sessionID)
        return user
        '''
        userID = self.session.get_session_data(sessionID).get('id')
        if not userID:
            return None
            return {'Error' : 'Session expired.'}
        user = self.userDataStore.read(userID)
        # Scrub sensitive information from user's data.
        user.remove_sensitive_data()
        if not user:
            return None
            return {'Error' : 'Could not load user.'}
        self.renew_session(sessionID)
        return user
        '''

    def get_user_from_session_id(self, sessionID):
        userDictionary = self.sessionsDataStore.get_session_data(sessionID)
        if not userDictionary:
            return None
            return {'Error' : 'Not logged in.'}
        user = self.usersDataStore.get_empty_user()
        user.from_dictionary(userDictionary)
        return user

    def renew_session(self, sessionID, expireTime=3600):
        if not sessionID:
            return None
        self.sessionsDataStore.set_cookie('sessionID', sessionID, expireTime)
        return self.sessionsDataStore.renew_session(sessionID, expireTime)

    def signout(self, sessionID):
        if not sessionID:
            return None
        self.sessionsDataStore.delete_cookie('sessionID')
        return self.sessionsDataStore.end_session(sessionID)