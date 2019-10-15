from flask import Flask, render_template, request, session, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime
import json
from flask_mail import Mail

#reading configs in json.config
with open('config.json', 'r') as c:
    params = json.load(c)['params']

#right now using local server so setting its true.
localserver = True

#used to connect with flask alchemy mysql database
app = Flask(__name__)

#setting secret key
app.secret_key = 'mysecret_key'

#configuring app to send mails using gmail smtplib
app.config.update(
    MAIL_SERVER= 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = 'TRUE',
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)

#function to send mail
mail = Mail(app)
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
    title = db.Column(db.String(180), nullable=False)
    tagline = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.String(120), nullable=True)
    content = db.Column(db.String(10000), nullable=False)
    slug = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    #query to fetch data from db. restricted to posts using params slicing.[0:params['display_posts']]
    posts = Posts.query.filter_by().all()[0:params['display_posts']]
    return render_template('index.html', params=params, posts = posts)



@app.route('/about')
def about():
    return render_template('about.html', params=params)


# @app.route('/post/')
# def post():
#     return render_template('post.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def newpost(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
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
        mail.send_message('Got new message from blog', sender=email,
                          recipients=[params['gmail-user']], body=message+ "\n" + phone)
    return render_template('contact.html', params=params)


# editing the existing posts
@app.route('/edit/<string:sno>', methods = ['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            req_title = request.form.get('title')
            req_tagline = request.form.get('tagline')
            req_slug = request.form.get('slug')
            req_content= request.form.get('content')
            req_date = datetime.now()

            #logic is if sno is zero then  give user admin access to add new posts,
            if sno =='0':
                post = Posts(title = req_title, tagline = req_tagline, slug = req_slug, content = req_content, date=req_date )
                db.session.add(post)
                db.session.commit()

            else:
                post = Posts.query.filter_by(sno = sno).first()
                post.title = req_title
                post.tagline = req_tagline
                post.slug = req_slug
                post.content = req_content
                post.date = req_date
                db.session.commit()
                return redirect('/edit/'+ sno)

        post = Posts.query.filter_by(sno = sno).first()
        return  render_template('edit.html', params = params,sno = sno, post = post)

#dashboard
@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    #checking user already login
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts =posts)
  
    if request.method=='POST':
        #we have to redirect to admin panel
        username = request.form.get('uname')
        userpass = request.form.get('upass')
        if username == params['admin_user'] and userpass == params['admin_pass']:
            #setting session
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts =posts)
    else:
        return render_template('signin.html', params=params)


@app.route('/delete/<string:sno>', methods = ['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno = sno).first()
        db.session.delete(post)
        db.session.commit()
        flash("successfully deleted")
    
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

    
app.run(debug=True)

