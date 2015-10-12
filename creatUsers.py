__author__ = 'triThirty'

import pymongo

conn=pymongo.MongoClient()
conn.database_names()
db=conn.get_database('test')
userCollection = db.get_collection('users')
# resultCollection = userCollection.find_one({'password':'amdin1'})
# print(resultCollection)
# for i in userCollection:
#     print(i)
for i in range(10):
    user={
        'nickname':'',
        'password':'',
        'img':'',
        'lastLoginTime':'',
    }
    id=userCollection.insert_one(user)
    print(id)