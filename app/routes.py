from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Mia'}
    posts = [
        {
            'club': {'name': 'Math'},
            'body': 'Come to Math Club!'
        },
        {
            'club': {'name': 'Yearbook'},
            'body': 'Reminder to take yearbook photos!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
