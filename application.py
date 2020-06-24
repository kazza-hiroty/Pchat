from flask import Flask, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256

from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit
from wtform_fields import *
from models import *



app = Flask(__name__)
app.secret_key = 'replace later'

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ohyfqbttucxqsk:79ffc643b1766c4490a4f292e6ac45f9529cf65e89c39c07c0cf34388f7651ce@ec2-18-233-32-61.compute-1.amazonaws.com:5432/dbbbh4cqcmtbk2'
db = SQLAlchemy(app)

#Initialise Flask-SocketIO
socketio = SocketIO(app)


#Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        #Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('login'))

    return render_template("index.html", form = reg_form)



@app.route("/login", methods=['GET', 'POST']) 
def login():
    login_form =LoginForm()

    #allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))   

    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():

    # if not current_user.is_authenticated:
    #     flash('Please login.', 'danger') #category name can be anything but 'danger' matches the name of Bootstrap class
    #     return redirect(url_for('login'))

    return render_template('chat.html')

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))

@socketio.on('message')
def message(data):

    send(data)




if __name__ == "__main__":    
    socketio.run(app, debug=True)
    #it is in documentation of flask-socketio