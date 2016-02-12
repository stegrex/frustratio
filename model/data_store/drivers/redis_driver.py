import redis

class RedisDriver():

    def __init__(self, dbNumber=0):
        # WARNING: Default DB is 0. If there's any reason where there could be
        # key collisions (for example, multiple apps in a box), pick a unique
        # number for this!
        self.client = redis.StrictRedis(db=dbNumber)

    # Default 24 hr lifetime of data.
    def create(self, id, value, expireTime=86400):
        # WARNING: Be very careful here!
        # According to the Python Redis docs (Redics vs. StrictRedis):
        # "SETEX: Order of ‘time’ and ‘value’ arguments reversed."
        return self.client.setex(id, expireTime, value)

    def read(self, id):
        response = self.client.get(id)
        if response:
            return response.decode('utf-8')
        return response

    def ttl(self, id):
        return self.client.ttl(id)

    def update(self, id, value):
        ttl = self.client.ttl(id)
        return self.create(id, value, ttl)

    def renew(self, id, expireTime=86400):
        response = self.read(id)
        return self.create(id, response, expireTime)

    def delete(self, id):
        return self.client.delete(id)

    def _delete_all(self):
        '''Delete all keys from the current DB only.
        '''
        return self.client.flushdb()