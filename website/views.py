# For creating first website route -> store standard routes for our website where users actually go to.
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user   # Copied from auth.py. current_user -> To detect whether a user is logged in or not
# With using 'current_user', change 'navbar' to display the correct icons
# 'curren_user' module can provide all the information of user, name, email, notes, and etc. If the user is not logged in, it won't be authenticated

from .models import Note    # In order to add a note
from . import db    # In order to access to db
import json # In order to seding a delete note request


# Define that this file is our blueprint of our application -> bunch of roots inside.
views = Blueprint('views', __name__) # views is now our blueprint

# @->signifies a DECORATOR
@views.route('/', methods=['GET', 'POST'])      # connecting URL to the return value of function
                                                # In order to add 'user's note' -> Allow post method
@login_required # Now the users cannot get to the homepage unless they logged in
def home(): # this function will run whenever we go to the slash route
            # So, whenever user request this URL, the response from the server is whatever the return value of this function, for now, "<h1>Test</h1>"

        if request.method == 'POST':
        
                note = request.form.get('note')

                # Make sure the least length of the note
                if len(note) < 1:
                        flash('Note is too short!', category='error')
                else:
                    # Adding a note
                    new_note = Note(data=note, user_id=current_user.id)
                    # new_note will store whatever the text that was passed for the from(note=request.form.get('note'))
                    db.session.add(new_note)
                    db.session.commit()
                    flash('Note added!', category='success')


        return render_template("home.html", user=current_user)   
        # In order to check if the user is logged in, pass to home 'current_user'
        # This means, in the template, reference this 'current_user' and check if it's authenticated

@views.route('/delete-note', methods=['POST'])
# Going to look for the noteID that was sent to here
def delete_note():
    # It's sending a request not as a form. The request is coming in the data parameter of the request object -> Need to load it as JSON!
    note = json.loads(request.data) # 'note' takes 'request.data' which is a string.
                                    # The string is what just sent from index.js which is 'noteID' in the index.js
                                    # Takes the string from views.py turning into a dictionary object, 'json.loads(request.data)'
    noteID = note['noteID']         # So, I can then access the 'noteID' which is going to field 'noteID'
    note = Note.query.get(noteID)   # Find this note. When I get it access as the primary key
    if note:    # If note is exist
        if note.user_id == current_user.id:
            db.session.delete(note) # This is how delete an object which is queried
            db.session.commit()
    return jsonify({})  # Turn this into a json object that I can return