from flask import Flask, render_template

from wtform_fields import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ohyfqbttucxqsk:79ffc643b1766c4490a4f292e6ac45f9529cf65e89c39c07c0cf34388f7651ce@ec2-18-233-32-61.compute-1.amazonaws.com:5432/dbbbh4cqcmtbk2'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username!"

        #Add user to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "inserted into DB!"

    return render_template("index.html", form = reg_form)

if __name__ == "__main__":
    
    app.run(debug=True)