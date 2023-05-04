from flask import render_template, redirect, url_for, flash, session, request
from app import app, db
from app.update_ticker_price import post_ticker_prices
from app.forms import LoginForm, AssetClassForm, TickerForm
from app.models import User, Asset_Class, Ticker
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

@app.route('/asset_class', methods=['GET', 'POST'])
@login_required
def asset_class():
    form = AssetClassForm()
    user_id = session['user_id']
    if request.method == 'POST':
        asset_class_name = request.form.get("asset_class_name")
        allocation_percent = request.form.get("allocation_percent")
        insert_asset_class(asset_class_name, allocation_percent)
        return redirect(url_for('asset_class'))
    asset_classes = get_asset_class()
    return render_template('asset_class.html', form=form, asset_classes=asset_classes)

@app.route('/asset_class_update/<asset_class_id>/',  methods=['GET', 'POST'])
@login_required
def asset_class_update(asset_class_id):
    form = AssetClassForm()
    if request.method == 'POST':
        asset_class_name = form.asset_class_name.data
        allocation_percent = form.allocation_percent.data
        update_asset_class(asset_class_name, allocation_percent, asset_class_id)
        return redirect(url_for('asset_class'))
    return render_template('asset_class.html', form=form)

@app.route('/asset_class_delete/<asset_class_id>/', methods=['GET', 'POST'])
@login_required
def asset_class_delete(asset_class_id):
    delete_asset_class(asset_class_id)
    flash(f"The asset class has been deleted.")
    return redirect(url_for('asset_class'))

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

@app.route('/ticker_delete/‹ticker_id>/', methods=['GET', 'POST'])
@login_required
def ticker_delete(ticker_id):
    ticker = Ticker.query.get(ticker_id)
    db.session.delete(ticker)
    db.session.commit()
    flash(f"{ticker.ticker_symbol} has been deleted.")
    return redirect(url_for('tickers'))

@app.route ('/ticker_update/<ticker_id>/', methods=['GET', 'POST'])
@login_required
def ticker_update (ticker_id):
    ticker = Ticker.query.get(ticker_id)
    ticker.ticker_symbol = request.form.get("ticker_symbol")
    ticker.company_name = request.form.get("company_name")
    ticker.asset_class_id = request.form.get("asset_class")
    db.session.commit()
    flash(f" {ticker.ticker_symbol} has been updated.")
    return redirect(url_for('tickers'))

@app.route('/tickers', methods= ['GET', 'POST'])
@login_required
def tickers():
    form = TickerForm()
    #form.asset_class.choices = [(asset_class.asset_class_id, asset_class.asset_class_name) for asset_class in AssetClass. query.all)]
    user_id = session['user_id']
    asset_classes = get_asset_class()
    form.asset_class.choices = [(asset_class['asset_class_id'], asset_class ['asset_class_name']) for asset_class in asset_classes]
    if request.method == 'POST':
        ticker_symbol = request.form.get("ticker_symbol")
        company_name = request.form.get("company_name")
        asset_class = request.form.get("asset_class")
        ticker = Ticker(ticker_symbol=ticker_symbol, company_name=company_name, current_price=0, asset_class_id=asset_class, user_id=user_id)
        db.session.add(ticker)
        db.session.commit()
        flash(f" {ticker.ticker_symbol} has been added.")
        return redirect(url_for('tickers'))
# This is a join.. the item in the join section is the left table
# Check out the complex order by
#tickers = db.session. query(Ticker, AssetClass).join(Ticker).order_by(AssetClass.asset_class_name, Ticker.ticker_symbol)
    tickers = get_tickers(user_id)
    return render_template ('tickers.html', form=form, tickers=tickers, asset_classes=asset_classes)

@app.route('/ticker_price_update')
@login_required
def ticker_price_update():
    post_ticker_prices()
    return redirect(url_for('tickers'))