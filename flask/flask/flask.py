from urlparse import urlparse, urljoin
import Flask
import flask-login
import flask-mysql

__author__ = "AlexKShah"
__version__ = "0.1"

# TODO
# - make index.html
# - make config.html
# - make style.css
# - https
# - store user/hashed password in config

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/config')
@login_required
def config():
    return render_template('config.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in...')
        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)
        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html, form=form')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return "Not Authorized!"

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

url_for('static', filename='style.css')
