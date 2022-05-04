import datetime
from src.utils import hashing, get_text_from_boolean
from bson.objectid import ObjectId

class Contract():
    def __init__(self, data): #Constructor - Method
        self.created_date = data.get("created_date") or datetime.datetime.now() #priority from left 2 right
        self.content = data.get("content")
        self.version = data.get("version")
        #self.hashed_key = data.get("hashed_key") or hashing(self.content)
        self.id = data.get("_id") or None

    def asdict(self): #json = dictionary mapping Python obj 2 json
        #return {'id': str(self.id), 'created_date': self.created_date, 'content': self.content, 'version': self.version, 'hashed_key': self.hashed_key}
        return {'id': str(self.id), 'created_date': self.created_date, 'content': self.content, 'version': self.version}

    def save(self, application_db): #db connection; see connection.py
        application_collection = application_db["contract"] #collection
        result = application_collection.insert_one(self.asdict())#pymongo
        self.id = result.inserted_id #get id created by Mongo
    
    @staticmethod # alternative to reading all doc from collection #Class handles it all
    def get_latest(application_db):
        application_collection = application_db["contract"]
        response = application_collection.find().sort("created_date", -1).limit(1)[0]
        return Contract(response) #Class


class User():
    def __init__(self, data):
        notification = Notification(data)
        self.created_date = data.get("created_date") or datetime.datetime.now()#priority from left 2 right
        self.change_date = data.get("change_date") or datetime.datetime.now()#priority from left 2 right
        self.name = data.get("name")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.document = data.get("document")
        self.contract = data.get("contract")
        self.notification = data.get("notification") or notification.asdict()#priority from left 2 right
        self.history = data.get("history") or [notification.asdict()]#priority from left 2 right
        self.id = data.get("_id") or None#priority from left 2 right

    def asdict(self): #json = dictionary mapping Python obj 2 json
        return {'id':str(self.id), 'created_date':self.created_date,'change_date':self.change_date,'name':self.name,'email':self.email,'phone':self.phone,'document':self.document, 'contract': self.contract,'notification':self.notification,'history':self.history}
    
    def save(self, application_db):
        application_collection = application_db["user"]
        result = application_collection.insert_one(self.asdict())
        self.id = result.inserted_id
    
    @staticmethod # alternative to reading all doc from collection #Class handles it all
    def find_by_email(application_db, email):
        application_collection = application_db["user"]
        result = application_collection.find_one({'email': email})
        return User(result)
    
    @staticmethod # alternative to reading all doc from collection #Class handles it all
    def update_notifications(email, application_db, notification):
        application_collection = application_db["user"]
        application_collection.update_one({"email": email}, #find, set, push
                {"$set": {
                    "notification": notification.asdict() #write userś preferences 4 notification
                    },
                "$push": {"history": notification.asdict()}}) #stack
    @staticmethod # alternative to reading all doc from collection #Class handles it all
    def update_contract(email, application_db, contract):
        application_collection = application_db["user"]
        application_collection.update_one({"email": email}, 
                {"$set": {"contract": contract}})
    
    def create_setting_message(self): #RECEIPT 4 preferences of notification
        return f'Hello {self.name}, you changed your preferences to sms: {get_text_from_boolean(self.notification.get("receive_sms"))}, whatsapp: {get_text_from_boolean(self.notification.get("receive_whatsapp"))},  email: {get_text_from_boolean(self.notification.get("receive_email"))}, call: {get_text_from_boolean(self.notification.get("receive_call"))}'

    def create_contract_message(self):  #RECEIPT contract version
        return f'Hello {self.name}, you accept contract version {self.contract}'

class Notification(): #PREFERENCES 0F NOTIFICATIONS
    def __init__(self, data):
        self.created_date = data.get("created_date") or datetime.datetime.now()
        self.receive_sms = data.get("receive_sms") or False
        self.receive_call = data.get("receive_call") or False
        self.receive_email = data.get("receive_email") or False
        self.receive_whatsapp = data.get("receive_whatsapp") or False
        self.id = data.get("_id") or ObjectId()
        #self.hashed_key = hashing(f'{self.receive_sms}-{self.receive_call}-{self.receive_email}-{self.receive_whatsapp}-{self.created_date}')

    def asdict(self):
        #return {'id':str(self.id), 'created_date':self.created_date,'receive_sms':self.receive_sms,'receive_call':self.receive_call,'receive_whatsapp':self.receive_whatsapp, 'receive_email': self.receive_email, 'hashed_key': self.hashed_key}
            return {'id':str(self.id), 'created_date':self.created_date,'receive_sms':self.receive_sms,'receive_call':self.receive_call,'receive_whatsapp':self.receive_whatsapp, 'receive_email': self.receive_email}