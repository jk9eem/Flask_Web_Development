from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash   # Convert the string type of password into secured hash type password
# Hasing function is a function that has NO INVERSE -> for the security
# Same password -> Same hash, Same hash -> NOT the same password
from . import db

# If it's not logged in, home button should be disappeared. If it's already logged in, sign up and log in button should be disappeared -> Use flask login module
from flask_login import login_user, login_required, logout_user, current_user
# This is the reason why UserMixin on models.py. So, I can use the 'current_user' object to access all of the information about the currently logged in user.



auth = Blueprint('auth', __name__)

# Define log in, log out, sign up
@auth.route('/login', methods=['GET','POST']) # Strings for type of requests that this route can accept
def login():
    # During the signing in, not getting the page, request the email and the password from the forms
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # User is a database name
        user = User.query.filter_by(email=email).first() # When looking for specific entry, user, or column in the database
        if user:    # If I found the user
            # Check if the password typed in is equal to the hash that stored on the server
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # Remember the fact that this user is logged in. This is going to store in the flask session -> restart flask, no longer be true
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        # If the user doesn't exist
        else:
            flash('Email does not exist.', category='error')


    data = request.form # Access form of attribute of our request which has all of the data that was sent as a part of a form
    print(data) # When the user input the information, it prints out that request data - need to store the data in a database and create the user account below.
    # return render_template("login.html", text="Testing passing value with variable name text at login", user="Jun", boolean=True)
    # We can pass the variables or values (text, user) to templates
    return render_template("login.html", user=current_user) # Pass current_user to check if the user is logged in or not

@auth.route('/logout')
@login_required # Make sure users cannot access this page or route unless the user is locked in
def logout():
    # return "<p>Logout</p>"
    logout_user()
    return redirect(url_for('auth.login'))  # Which is def login() above
    
@auth.route('/sign-up', methods=['GET','POST']) # Strings for type of requests that this route can accept
def sign_up():
    # In the above def login(), it only assigned request data and print it. Also GET and POST requests were not differentiated.
    # Differentiate the GET and POST requests
    if request.method == 'POST':
        # Get all of information from my form.
        email = request.form.get('email')   # Use 'get()' to get a specific attributes or values
        # firstName = request.form.get('firstName')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # When new user signs up, make sure that that user doesn't already exist -> email should not exist in the database
        user = User.query.filter_by(email=email).first()

        if user:    # if there actually is a user
            flash('Email already exists.', category='error')

        # Verity these information datas are valid -> Going to use flask method called 'message flashing'
        elif len(email) < 4:
            flash('Email must be at least 5 characters', category='error')
        # elif len(firstName) < 2:
        elif len(first_name) < 2:
            flash('Firstname must be at least 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Passward must be at least 7 characters', category='error')
        else:
            # Creating user -> It's defined at models.py -> import it!
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            
            # add user to database
            db.session.add(new_user)
            # There are some changes, update it
            db.session.commit()

            login_user(user, remember=True) # Now, the current status is logged in. So, remember this user

            flash('Account created!', category='success')   # The messages need to be displayed -> Go to base.html and add codes for it

            # Redirect the user to the homepage of the website after sign up
            return redirect(url_for('views.home'))  #Blueprint name.function name

    return render_template("sign_up.html", user=current_user)   # Pass current_user to check if the user is logged in or not