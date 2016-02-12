import pymongo
import time

class PyMongoDriver():

    def __init__(self, dbName, collectionName):
        self.client = pymongo.MongoClient()
        self.db = self.client[dbName]
        self.collection = self.db[collectionName]

    # TODO: Look into using upsert.
    def insert(self, id=None, document=None, createdTime=None):
        # Make sure all '_id' keys are used internally in PyMongoDriver only.
        if 'id' in document:
            del document['id']
        document['_id'] = id
        if createdTime:
            document['createdTime'] = createdTime
        else:
            document['createdTime'] = int(time.time())
        if document:
            try:
                insertedID = self.collection.insert_one(document).inserted_id
                document['id'] = document['_id']
                del document['_id']
                return insertedID
            except pymongo.errors.DuplicateKeyError:
                # TODO: Figure out how to properly handle exceptions.
                # Do not return pymongo.errors.DuplicateKeyError due to issues
                # of portability when changing data stores.
                return None
                raise DuplicateKeyError('Duplicate key error.')

    def get(self, documentID):
        response = self.collection.find_one({'_id' : documentID})
        if response:
            response['id'] = response['_id']
            del response['_id']
        return response

    def get_by_field(self, field, id):
        response = self.collection.find_one({field : id})
        if response:
            response['id'] = response['_id']
            del response['_id']
        return response

    def get_by_fields(self, keyValues):
        if 'id' in keyValues:
            keyValues['_id'] = keyValues['id']
            del keyValues['id']
        response = self.collection.find(keyValues)
        output = {}
        for x in response:
            x['id'] = x['_id']
            del x['_id']
            output[x['id']] = x
        return output

    def get_multiple(self, documentIDs, asDictionary=True):
        response = self.collection.find({'_id' : {'$in' : documentIDs}})
        if asDictionary:
            output = {}
        else:
            output = []
        for x in response:
            x['id'] = x['_id']
            del x['_id']
            if asDictionary:
                output[x['id']] = x
            else:
                output.append(x)
        return output

    # TODO: Look into using upsert.
    def update(self, documentID, fields={}):
        # WARNING! Property modified_count is better but current environment
        # uses MongoDB 2.4.9. Property modified_count requires 2.6 or higher.
        fields['modifiedTime'] = int(time.time())
        return self.collection.update_one(
            {'_id' : documentID},
            {'$set' : fields}
        ).matched_count

    def replace(self, documentID, document):
        '''Completely replace the document contents.
        '''
        return self.collection.replace_one(
            {'_id' : documentID},
            document
        )

    def _delete(self, documentID):
        return self.collection.delete_many({'_id' : documentID})

    def _delete_all(self):
        return self.collection.delete_many({})

    def _drop_collection(self):
        return self.collection.drop()

    def _drop_db(self):
        return self.client.drop_database(self.db)

class DuplicateKeyError(pymongo.errors.DuplicateKeyError):
    pass