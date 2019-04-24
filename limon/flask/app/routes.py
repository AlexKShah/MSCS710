from urlparse import urlparse, urljoin
from flask import Flask
import flask_mysql
import flask_wtf

__author__ = "AlexKShah"
__version__ = "0.1"

# TODO
# - make index.html
# - make config.html
# - make style.css
# - https
# - store user/hashed password in config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config.html', methods=['GET', 'POST'])
@login_required
def config():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO submit config data from forms
    return render_template('config.html')

if __name__ == '__main__':
    app.run()

url_for('static', filename='style.css')
