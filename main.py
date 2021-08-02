# packages
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app, db
from dashboard import create_dash_application
# main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
@login_required
def index():
    return render_template('index.html')



app = create_app() # initialize flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    create_dash_application(app) # create the dash aplication
    app.run(debug=True) # run the flask app on debug mode