import pymongo

def create_connection():
    application_client = pymongo.MongoClient("mongodb://localhost:27017/")
    application_db = application_client["OptInOptOut"] #DB name
    return application_db