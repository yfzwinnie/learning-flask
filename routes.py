from flask import Flask, render_template, request, session, redirect, url_for
from forms import SignupForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy has been deprecated
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
app.config['SQLALCHEMY_ECHO'] = True
#db.init_app(app)

db = SQLAlchemy(app)
app.secret_key = "development-key" #a secret key for Flask-WTF to generate secure forms to protect against CSRF attacks.


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(120))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignupForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email #after a user sign up for the app, this creates a new session
            return redirect(url_for('home'))

    elif request.method == "GET":
        return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method =='GET':
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None) #logs the user out by ending session
    return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
