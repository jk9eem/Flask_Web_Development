from .import db    # Import from the current package, which is the 'website' folder and import 'db' OBJECT. It's same as 'from website import db'
                    # 'db' object is defined in __init__.py
from flask_login import UserMixin   # This is a custom class that we can inharit that will give our user object
from sqlalchemy.sql import func

# All of the notes have to conform this
class Note(db.Model): # This inherits from db.model. This is more general database model, schema.
    id = db.Column(db.Integer, primary_key=True)    # When adding a new object, ID will automatically be set(unique, increment)
    data = db.Column(db.String(10000))    # Data associate with note
    date = db.Column(db.DateTime(timezone=True), default=func.now())    
    # Whenever creating note, it'll automatically add by func module -> get current date and time and store to default variable
    

    # Associate different information with different users -> set up a relationship between note object and user object -> FOREIGN KEY
    # FOREIGN KEY is essentially a column in the database that always references a column of another database
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # ID field in User is "Integer", so it has to be matched. Foreign key on the child object references its parent object
    # A valid ID of the existing user must be passed.
    # One to many relationship -> one object has many children -> 'One user' has 'many notes'
    # Why not 'User.id'? because in python, capitals for class, but in SQL, 'User' class is represented by lowercase 'user'
    # Foreignkey -> lowercase


# All of the users have to conform this(should be look like this below) -> All of the information is going to be consistent
class User(db.Model, UserMixin): # Inherit two things.  'UserMixin' -> do with the fact that we're using this flask_login module
    # Define all of the columns that we want to have stored in this table -> defining SCHEMA
    id = db.Column(db.Integer, primary_key=True)    # Define the type of the column in parenthesis() -- all of our objects, we need to have PRIMARY KEY
                        # We need someway to uniquely identify the object, especially integer. ex) How you can differentiate the same first name?
    email = db.Column(db.String(150), unique=True)   # Maximum length of the string is 150, and no user can have the same email as another
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # Everytime creating a note, add into this user's notes relationship that note ID
    # Relationship -> Uppercase

