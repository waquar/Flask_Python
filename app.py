#static folder is public
#templates folder is private

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Waquar'

@app.route('/new')
def newpage():
    return render_template('index.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/var')
def name():
    fname = 'waquar'
    myage = '27'
    return render_template('about.html', name=fname, age = myage)

if __name__ == '__main__':
    app.run(debug=True)                   #debug=True           for auto reload




