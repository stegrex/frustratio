from model.data_store.drivers.pymongo_driver import PyMongoDriver
from model.objects.user import User

class UsersDataStore():

    def __init__(self, driver=None):
        if driver:
            self.driver = driver
        else:
            self.driver = PyMongoDriver('frustratio', 'users')

    def get_empty_user(self):
        return User()

    def get_protected_fields(self):
        user = User()
        return user.get_protected_fields()

    def create(self, user):
        response = self.driver.insert(user.id, user.to_dictionary())
        # TODO: Throw exception here instead.
        if response:
            return user
        else:
            return None

    def read(self, userID):
        '''Return an User instance given an ID.
        '''
        response = self.driver.get(userID)
        user = User()
        if response:
            user.from_dictionary(response)
        return user

    def read_by_field(self, field, id):
        response = self.driver.get_by_field(field, id)
        user = User()
        if response:
            user.from_dictionary(response)
        return user

    def read_multiple(self, userIDs, asDictionary=True):
        '''Return dictionary (default) or list of User instances.
        Use dictionary for easier indexing.
        Use list for order preservation.
        '''
        response = self.driver.get_multiple(userIDs, asDictionary)
        if asDictionary:
            output = {}
            for x in response:
                output[x] = User()
                output[x].from_dictionary(response[x])
        else:
            output = []
            for x in response:
                user = User()
                user.from_dictionary()
                output.append(user)
        return output

    def update_fields(self, userID, fields={}):
        '''Update a specific User in the data store given its fields.

        Very close to the data store implementation.
        '''
        protectedFields = self.get_protected_fields()
        for x in fields:
            if x in protectedFields:
                return None
        return self.driver.update(userID, fields)

    # TODO: Move this to a parent class or possibly a utility class.
    def _to_dictionary(self, objectsDictionary):
        output = {}
        for x in objectsDictionary:
            output[x] = objectsDictionary[x].to_dictionary()
        return output