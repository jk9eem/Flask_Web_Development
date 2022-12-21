from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager    # In order to login, find a user

# Define a new database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) # Initialize flask
    app.config['SECRET_KEY'] = 'hfdukjalhf fdhiualfhsdijaksl'   # Encript / secure the cookies and session data related to the website. inside of '', put random chars
                                                                # DO NOT SHARE THE SECREY KEY!!
    # Need a file to store data -> Using sqLite3
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # It means, my SQL alchemy database is stored we're located at this location, sqlite:///database name
    # Initialize the database
    db.init_app(app)  # Take this database that we defined above(db), and tell this is the app that we going to use with this database, the flask app that we just created
    # In order to create the database model, goto the 'models.py'

    

    
    # Importing blueprints that contain different views or URL for the application
    from .views import views # import the name of blueprint of views
    from .auth import auth # import the name of blueprint of auth

    # Then register the imported blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Check before running this server everytime if the database is created yet
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # It allows the flask redirect if the user is not logged in and login requred
    login_manager.init_app(app) # Telling login manager which app that is using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # It looks for the primary key. When using get(), no need to specifiy id like id=...
                                        # Check if it's equal to whatever is passes which is the introversion of whatever ids passed to this load user
    
    return app

# Check the database already exists, if it's not, it's going to create it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # db.create_all(app=app)
        with app.app_context():
            db.create_all()
        print('Created Database!')