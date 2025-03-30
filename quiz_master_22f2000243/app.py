#Starting of the app
from flask import Flask
from backend.models import db



app=None

def app_setup():
    global app
    app=Flask(__name__)
    app.secret_key = 'SOME KEY'
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Quiz_Data.sqlite3"
    db.init_app(app)
    app.app_context().push() #Direct access to other modules
    app.debug=True
    print("Your app is start")



#Call the setup
app_setup()

from backend.controller import *

if __name__ == "__main__":
    app.run()