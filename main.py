from flask import Flask, render_template, request
from flask_sqlalchemy import  SQLAlchemy
from _datetime import datetime

app = Flask(__name__)                  #used to connect with flaskalchemy mysql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/waquar_db'
db = SQLAlchemy(app)

class Contacts(db.Model):       #contact info in database important(name should match with db wasted 2 hours)

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=False, nullable=False )
    mobile = db.Column(db.String(12),unique=True,nullable=False)
    message = db.Column(db.String(1000),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(120),nullable=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":                          #will fetch details from contact.html, attributes i configured
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name,mobile =phone, message=message, date=datetime.now(), email =email)          #will dump in database
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')


@app.route('/post')
def post():
    return render_template('post.html')

app.run(debug=True)