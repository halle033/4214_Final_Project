from flask import render_template, redirect, url_for, flash, session, request
from app import app, db
from app.update_cryptocurrency import post_crypto_prices
from app.forms import LoginForm, CryptoClassForm, CryptoForm
from app.models import User, Crypto_Class, Crypto
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app.functions import *
from app.formatting import *

##### USER MANAGEMENT ##### FOUND: https://www.youtube.com/watch?v=2dEM-s3mRLE
login_manager = LoginManager()
login_manager.init_app(app)

# This method is used to as part of the flask_login code.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/crypto_class', methods=['GET', 'POST'])
@login_required
def crypto_class():
    form = CryptoClassForm()
    user_id = session['user_id']
    if request.method == 'POST':
        crypto_class_name = request.form.get("crypto_class_name")
        allocation_percent = request.form.get("allocation_percent")
        insert_crypto_class(crypto_class_name, allocation_percent)
        return redirect(url_for('crypto_class'))
    crypto_classes = get_crypto_class()
    return render_template('crypto_class.html', form=form, crypto_classes=crypto_classes)

@app.route('/crypto_class_update/<crypto_class_id>/',  methods=['GET', 'POST'])
@login_required
def crypto_class_update(crypto_class_id):
    form = CryptoClassForm()
    if request.method == 'POST':
        crypto_class_name = form.crypto_class_name.data
        allocation_percent = form.allocation_percent.data
        update_crypto_class(crypto_class_name, allocation_percent, crypto_class_id)
        return redirect(url_for('crypto_class'))
    return render_template('crypto_class.html', form=form)

@app.route('/crypto_class_delete/<crypto_class_id>/', methods=['GET', 'POST'])
@login_required
def crypto_class_delete(crypto_class_id):
    delete_crypto_class(crypto_class_id)
    flash(f"The crypto class has been deleted.")
    return redirect(url_for('crypto_class'))

@app.route('/login', methods=['GET', 'POST'])
def login():
     if current_user.is_authenticated:
          return redirect(url_for('dashboard'))
     form = LoginForm()

     # set form data to variables
     form_username = form.username.data
     form_password = form.password.data

     if form.validate_on_submit():
          user = User.query.filter_by(username=form_username).first()

          if user is not None:
               password = user.password

          if user is None or password != form_password:
               flash('Invalid username or passsword')
               return redirect(url_for('login'))
          login_user(user)
          session.permanent = True
          session['user_id'] = user.id
          print(session['user_id'])
          return redirect(url_for('dashboard'))
     return render_template('login.html', title='Sign In', form=form)
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

##### LOGIN STUFF #####
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# This route redirects unauthrozied users to the login page.
@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login'))

@app.route('/crypto_delete/‹crypto_id>/', methods=['GET', 'POST'])
@login_required
def crypto_delete(crypto_id):
    crypto = Crypto.query.get(cryptor_id)
    db.session.delete(crypto)
    db.session.commit()
    flash(f"{crypto.crypto_symbol} has been deleted.")
    return redirect(url_for('cryptos'))

@app.route ('/crypto_update/<crypto_id>/', methods=['GET', 'POST'])
@login_required
def crypto_update (crypto_id):
    crypto = Crypto.query.get(crypto_id)
    crypto.crypto_symbol = request.form.get("crypto_symbol")
    crypto.company_name = request.form.get("company_name")
    crypto.crypto_class_id = request.form.get("crypto_class")
    db.session.commit()
    flash(f" {crypto.crypto_symbol} has been updated.")
    return redirect(url_for('cryptos'))

@app.route('/cryptos', methods= ['GET', 'POST'])
@login_required
def cryptos():
    form = CryptoForm()
    #form.crypto_class.choices = [(crypto_class.crypto_class_id, crypto_class.crypto_class_name) for crypto_class in CryptoClass. query.all)]
    user_id = session['user_id']
    crypto_classes = get_crypto_class()
    form.crypto_class.choices = [(crypto_class['crypto_class_id'], crypto_class ['crypto_class_name']) for crypto_class in crypto_classes]
    if request.method == 'POST':
        crypto_symbol = request.form.get("crypto_symbol")
        company_name = request.form.get("company_name")
        crypto_class = request.form.get("crypto_class")
        crypto = Crypto(crypto_symbol=crypto_symbol, company_name=company_name, current_price=0, crypto_class_id=crypto_class, user_id=user_id)
        db.session.add(crypto)
        db.session.commit()
        flash(f" {crypto.crypto_symbol} has been added.")
        return redirect(url_for('cryptos'))
# This is a join.. the item in the join section is the left table
# Check out the complex order by
#cryptos = db.session. query(Crypto, CryptoClass).join(Crypto).order_by(CryptoClass.crypto_class_name, Crypto.Crypto_symbol)
    cryptos = get_cryptos(user_id)
    return render_template ('crypto.html', form=form, cryptos=cryptos, crypto_classes=crypto_classes)

@app.route('/crypto_price_update')
@login_required
def crypto_price_update():
    post_crypto_prices()
    return redirect(url_for('cryptos'))