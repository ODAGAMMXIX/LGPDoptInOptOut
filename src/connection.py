import pymongo
def create_connection():
  
    application_client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@lgpd2022.vsrpt.mongodb.net/?retryWrites=true&w=majority")
    application_db = application_client["lgpd2022"] #DB name
    return application_db    
    
'''def create_connection():
    application_client = pymongo.MongoClient("mongodb://localhost:27017/")
    application_db = application_client["OptInOptOut"] #DB name
    return application_db'''
#m001-mongodb-basics
#'''client = pymongo.MongoClient("mongodb+srv://m001-student:<password>@lgpd2022.vsrpt.mongodb.net/?retryWrites=true&w=majority")
#db = client.test'''
