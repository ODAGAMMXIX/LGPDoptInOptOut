import datetime
from src.utils import hashing, get_text_from_boolean
from bson.objectid import ObjectId

class Contract():
    def __init__(self, data):
        self.created_date = data.get("created_date") if data.get("created_date") else datetime.datetime.now()
        self.content = data.get("content")
        self.version = data.get("version")
        self.hashed_key = data.get("hashed_key") if data.get("hashed_key") else hashing(self.content)
        self.id = data.get("_id") if data.get("_id") else None

    def asdict(self):
        return {'id': str(self.id), 'created_date': self.created_date, 'content': self.content, 'version': self.version, 'hashed_key': self.hashed_key}


    def save(self, application_db):
        application_collection = application_db["contract"]
        result = application_collection.insert_one(self.asdict())
        self.id = result.inserted_id
    
    @staticmethod
    def get_latest(application_db):
        application_collection = application_db["contract"]
        response = application_collection.find().sort("created_date", -1).limit(1)[0]
        return Contract(response)


class User():
    def __init__(self, data):
        notification = Notification(data)
        self.created_date = data.get("created_date") if data.get("created_date") else datetime.datetime.now()
        self.change_date = data.get("change_date") if data.get("change_date") else datetime.datetime.now()
        self.name = data.get("name")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.document = data.get("document")
        self.notification = data.get("notification") if data.get("notification") else notification.asdict()
        self.history = data.get("history") if data.get("history") else [notification.asdict()]
        self.id = data.get("_id") if data.get("_id") else None

    def asdict(self):
        return {'id':str(self.id), 'created_date':self.created_date,'change_date':self.change_date,'name':self.name,'email':self.email,'phone':self.phone,'document':self.document,'notification':self.notification,'history':self.history}
    
    def save(self, application_db):
        application_collection = application_db["user"]
        result = application_collection.insert_one(self.asdict())
        self.id = result.inserted_id
    
    @staticmethod
    def find_by_email(application_db, email):
        application_collection = application_db["user"]
        result = application_collection.find_one({'email': email})
        return User(result)
    
    @staticmethod
    def update_notifications(email, application_db, notification):
        application_collection = application_db["user"]
        application_collection.update_one({"email": email}, 
                {"$set": {
                    "notification": notification.asdict()
                    },
                "$push": {"history": notification.asdict()}})
    
    def create_setting_message(self):
        return f'Hello {self.name}, you changed your preferences to sms: {get_text_from_boolean(self.notification.get("receive_sms"))}, whatsapp: {get_text_from_boolean(self.notification.get("receive_whatsapp"))},  email: {get_text_from_boolean(self.notification.get("receive_email"))}, call: {get_text_from_boolean(self.notification.get("receive_call"))}'

class Notification():
    def __init__(self, data):
        self.created_date = data.get("created_date") if data.get("created_date") else datetime.datetime.now()
        self.receive_sms = data.get("receive_sms") or False
        self.receive_call = data.get("receive_call") or False
        self.receive_email = data.get("receive_email") or False
        self.receive_whatsapp = data.get("receive_whatsapp") or False
        self.id = data.get("_id") if data.get("_id") else ObjectId()
        self.hashed_key = hashing(f'{self.receive_sms}-{self.receive_call}-{self.receive_email}-{self.receive_whatsapp}-{self.created_date}')

    def asdict(self):
        return {'id':str(self.id), 'created_date':self.created_date,'receive_sms':self.receive_sms,'receive_call':self.receive_call,'receive_whatsapp':self.receive_whatsapp, 'receive_email': self.receive_email, 'hashed_key': self.hashed_key}