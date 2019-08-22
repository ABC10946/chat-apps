from flask import Flask, render_template, request, redirect, url_for, session
import os
from pathlib import Path
import base64
app = Flask(__name__)

CHAT_DATA_PATH = 'data/chat_timeline.txt'
USER_DATA_PATH = 'data/users.txt'

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', loggedin = True, username = username)
    else:
        return render_template('index.html', loggedin = False)


@app.route('/read', methods=['GET', 'POST'])
def read():
    if not os.path.isfile(CHAT_DATA_PATH):
        Path(CHAT_DATA_PATH).touch()
    
    if 'username' in session:
        if request.method == 'GET':
                with open(CHAT_DATA_PATH, 'r') as f:
                    raw_text = f.read()
                    lines = raw_text.split('\n')

                return render_template('read.html', lines = lines, username = session['username'])

        elif request.method == 'POST':
            with open(CHAT_DATA_PATH, 'a') as f:
                text = request.form['throw']
                f.write(session['username'] + ':' + text + '\n')
                return redirect(url_for('read'))
    else:
        return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        with open(USER_DATA_PATH) as f:
            userdata = f.read()
            if request.form['username'] + ':' + request.form['password'] in userdata:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return 'your user data not found!</br><a href="/">RETURN TO TOP</a>'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('create_account.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            with open(USER_DATA_PATH, 'a') as f:
                f.write(username + ':' + password + '\n')
                session['username'] = username
                return redirect(url_for('index'))
        else:
            return render_template('create_account.html', alert = 'password and confirm password are not equal.')
    

app.secret_key = 'k*IQ3E%TTv6lB^I3*MZPVKIL'
if __name__ == '__main__':
    app.run()