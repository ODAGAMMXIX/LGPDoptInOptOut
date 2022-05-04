
from flask import Flask #CLass

app = Flask(__name__) #create an instance of this class

'''The first argument is the name of the application’s module or package.
__name__ is a convenient shortcut for this that is appropriate for most cases.
This is needed so that Flask knows where to look for resources such as templates and static files.'''

from src.connection import create_connection

db = create_connection()

from src import routes, models 
