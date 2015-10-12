__author__ = 'maoshanshi'
import pymongo

class myMongo(object):
    def __init__(self):
        conn=pymongo.MongoClient()
        conn.database_names()
        db=conn.get_database('test')
        self.userCollection = db.get_collection('users')

    def find_one(self,filter):
        print(filter)
        print(self.userCollection.count())
        return self.userCollection.find_one(filter)

if __name__ == '__main__':
    mm=myMongo()
    rs=mm.find_one({'password': 'admin'})
    print(rs!=None)