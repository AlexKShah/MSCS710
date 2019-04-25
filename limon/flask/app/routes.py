from flask import Flask, render_template

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
def config():
    return render_template('config.html')

if __name__ == '__main__':
    app.run(debug=TRUE)
