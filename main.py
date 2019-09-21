from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime
import json
#from flask_mail import Mail

#right now using local server so setting its true.
localserver = True

#reading configs in json.config
with open('config.json', 'r') as c:
    params = json.load(c)['params']

#used to connect with flask alchemy mysql database
app = Flask(__name__)
#configuring app to send mails using gmail smtplib
app.config.update(
    MAIL_SERVER= 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = 'TRUE',
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

#function to send mail
#mail = Mail(app)

#checking condition of server its local or prod
if (localserver):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/waquar_db'       #used before using json.config

db = SQLAlchemy(app)
#contact info in database important(name should match with db wasted 2 hours)
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=False, nullable=False )
    mobile = db.Column(db.String(12),unique=True,nullable=False)
    message = db.Column(db.String(1000),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(120),nullable=True)

#made for saving posts in db
class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    tile = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(120), nullable=True)
    content = db.Column(db.String(1000), nullable=False)
    slug = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return render_template('index.html', params=params)

@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post = post)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    # will fetch details from contact form in contact.html, attributes which i configured
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        # will dump in database
        entry = Contacts(name=name, mobile=phone, message=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        #as soon it commits it will send mail to user.
     #   mail.send_message('Got new message from blog', sender=email,
     #                     recipients=[params['gmail-user']], body=message+ "\n" + phone)
    return render_template('contact.html', params=params)

app.run(debug=True)

