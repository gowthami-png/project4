from flask_wtf import FlaskForm
from flask import Flask,render_template,request,redirect,send_file,url_for,Response,session
from werkzeug.utils import secure_filename,send_from_directory
from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField
from wtforms.validators import InputRequired,NumberRange
import os
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app=Flask(__name__)
app.config['SECRET_KEY'] = 'gowthami'
app.config['UPLOAD_FOLDER'] = 'static\\uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


with app.app_context():
    db.create_all(),



@app.route('/')
def index():
    return render_template("Home page.html")

@app.route('/signup',methods=["GET","POST"])
def page1():
    if request.method=="POST":
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template("page 1.html")
@app.route('/login')
def page2():
    session.clear()
    if request.method == "POST":
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session['email'] = user.email
                return redirect('/page 2')
            else:
                return render_template('Home page.html', error='Invalid user')
    return render_template("page 2.html")
if __name__=='__main__':
    app.run()
