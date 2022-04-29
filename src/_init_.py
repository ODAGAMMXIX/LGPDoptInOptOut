
from flask import Flask
from src.connection import create_connection
app = Flask(__name__)
db = create_connection()


from src import routes, models 
