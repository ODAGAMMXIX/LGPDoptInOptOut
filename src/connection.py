import pymongo

def create_connection():
    application_client = pymongo.MongoClient("mongodb://localhost:27017/")
    application_db = application_client["OptInOptOut"]
    return application_db

###########44444444444444444##########


