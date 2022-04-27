import datetime
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
        self.created_date = data.get("created_date") if data.get("created_date") else datetime.datetime.now()
        self.change_date = data.get("change_date") if data.get("change_date") else datetime.datetime.now()
        self.name = data.get("name")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.document = data.get("document")
        self.receive_sms = data.get("receive_sms")
        self.receive_call = data.get("receive_call")
        self.receive_whatsapp = data.get("receive_whatsapp")
        self.receive_email = data.get("receive_email")
        self.history = data.get("history") if data.get("history") else [History(data).asdict()]
        self.id = data.get("_id") if data.get("_id") else None

    def asdict(self):
        return {'id':str(self.id), 'created_date':self.created_date,'change_date':self.change_date,'name':self.name,'email':self.email,'phone':self.phone,'document':self.document,'receive_sms':self.receive_sms,'receive_call':self.receive_call,'receive_whatsapp':self.receive_whatsapp,'history':self.history}
    
    def save(self, application_db):
        application_collection = application_db["user"]
        result = application_collection.insert_one(self.asdict())
        self.id = result.inserted_id
    
    @staticmethod #crazy stuff
    def find_by_email(application_db, email):
        application_collection = application_db["user"]
        result = application_collection.find_one({'email': email})
        return User(result)
    
    def create_setting_message(self):
        return f'Hello {self.name}, you changed your preferences to receive: sms: {get_text_from_boolean(self.receive_sms)}, whatsapp: {get_text_from_boolean(self.receive_whatsapp)},  email: {get_text_from_boolean(self.receive_email)}, call: {get_text_from_boolean(self.receive_call)}'

class History():
    def __init__(self, data):
        self.created_date = data.get("created_date") if data.get("created_date") else datetime.datetime.now()
        self.receive_sms = data.get("receive_sms")
        self.receive_call = data.get("receive_call")
        self.receive_email = data.get("receive_email")
        self.receive_whatsapp = data.get("receive_whatsapp")
        self.id = data.get("_id") if data.get("_id") else ObjectId()

    def asdict(self):
        return {'id':str(self.id), 'created_date':self.created_date,'receive_sms':self.receive_sms,'receive_call':self.receive_call,'receive_whatsapp':self.receive_whatsapp}