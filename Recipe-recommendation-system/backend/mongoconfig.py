import pymongo

URL = 'mongodb://localhost:27017'
# URL = 'mongodb+srv://Edison:edison123@cluster0.usdxd.mongodb.net/?retryWrites=true&w=majority'
CLIENT = pymongo.MongoClient(URL)
DBNAME = 'newdb'
