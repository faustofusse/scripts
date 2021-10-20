import pymongo
from pymongo import MongoClient

originUrl = input('Origin url: ')
# originUrl = 'mongodb://restoarDb:lagarto24@ds117816.mlab.com:17816/restoar'
destinationUrl = input('Destination url: ')
# destinationUrl = 'mongodb://localhost:27017/'
dbName = input('Database name: ')
# dbName = 'restoar'
collection = input('Collection: ')
# collection = 'users'

clientCloud = MongoClient(originUrl)
dbCloud = clientCloud[dbName]
colCloud = dbCloud[collection]

lista = list(colCloud.find())

clientLocal = MongoClient(destinationUrl)
dbLocal = clientLocal[dbName]
colLocal = dbLocal[collection]

colLocal.insert_many(lista)

print('Done!')