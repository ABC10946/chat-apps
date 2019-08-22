from flask import Flask, render_template, request, redirect, url_for
import os
from pathlib import Path
app = Flask(__name__)

@app.route('/read', methods=['GET', 'POST'])
def read():
    if not os.path.isfile('database.txt'):
        Path("database.txt").touch()

    if request.method == 'GET':
        with open('database.txt', 'r') as f:
            raw_text = f.read()
            lines = raw_text.split('\n')

        return render_template('index.html', lines = lines)

    elif request.method == 'POST':
        with open('database.txt', 'a') as f:
            text = request.form['throw']
            f.write(text + '\n')
            return redirect(url_for('read'))


if __name__ == '__main__':
    app.run()