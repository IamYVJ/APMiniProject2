from app import app , db, bcrypt
from flask import render_template, flash, redirect , url_for , request, session , g
import sqlite3
from app.forms import LoginForm, RegistrationForm , FlightForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date
from app.auth import OAuthSignIn
from app.forms import ResetPasswordRequestForm
from app.emailPasswordReset import send_password_reset_email
from app.forms import ResetPasswordForm
from app.flightscraper import flightSearch

app.config['OAUTH_CREDENTIALS'] = {
    'google': {
        'id': '356186709623-6tb84gjrptp1ss0cificl90ia45qufa4.apps.googleusercontent.com',
        'secret': 'gJ5hLx6ikRTAC8NlONLZ67Kx'
    }}

class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        return redirect(next) if next else redirect(url_for('index'))
    # google = get_google_auth()
    # auth_url, state = google.authorization_url(
    #     Auth.AUTH_URI, access_type='offline', prompt="select_account")
    # session['oauth_state'] = state
    # print(state)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/flights',methods = ['POST', 'GET'])
def flights():
    # if request.method == 'POST':
    #   result = request.form
    dtoday = str(date.today())
    print(dtoday)
    form = FlightForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%Y-%m-%d')
    return render_template('flights.html',form=form, dtoday = dtoday)

@app.route('/flightsearch',methods = ['POST', 'GET'])
def flightsearch():
    departureCode= ""
    arrivalCode=""
    dep = ""
    ret = ""
    form=FlightForm
    dtoday = str(date.today())
    if request.method == 'POST':
        departureCode = request.form['from']
        arrivalCode = request.form['to']
        dep=request.form['tday'].split('-')
        ret=request.form['rday'].split('-')
    print(departureCode)
    print(arrivalCode)
    print(dep)
    print(ret)
    if(departureCode=="" or arrivalCode=="" or len(dep)==0):
        return render_template('flights.html',form=form, dtoday = dtoday)
    flights = flightSearch(departureCode, arrivalCode, dep[2], dep[1], dep[0])
    # flights = [['New Delhi', 'Raipur', 'Air India', 'AI-469', '05:15', '07:05', '1h 50m ', 'Non Stop ', '4153'], ['New Delhi', 'Raipur', 'IndiGo', '6E-2757', '06:45', '08:35', '1h 50m ', 'Non Stop ', '4773'], ['New Delhi', 'Raipur', 'IndiGo', '6E-2393', '08:25', '10:15', '1h 50m ', 'Non Stop ', '5300'], ['New Delhi', 'Raipur', 'Vistara Premium Economy', 'UK-793', '06:40', '08:20', '1h 40m ', 'Non Stop '], ['New Delhi', 'Raipur', 'IndiGo', '6E-2912', '17:25', '19:15', '1h 50m ', 'Non Stop ', '5928'], ['New Delhi', 'Raipur', 'Vistara', 'UK-793', '06:40', '08:20', '1h 40m ', 'Non Stop ', '6554'], ['New Delhi', 'Raipur', 'Vistara', 'UK-797', '18:00', '19:45', '1h 45m ', 'Non Stop ', '6554'], ['New Delhi', 'Raipur', 'IndiGo', '6E-2201', '12:30', '14:20', '1h 50m ', 'Non Stop ', '6558'], ['New Delhi', 'Raipur', 'Vistara Premium Economy', 'UK-797', '18:00', '19:45', '1h 45m ', 'Non Stop '], ['New Delhi', 'Raipur', 'IndiGo', '6E-656/811', '05:25', '09:00', '3h 35m ', '1 Stop(s)', '8244'], ['New Delhi', 'Raipur', 'Air India', 'AI-435/9683', '05:55', '17:00', '11h 05m ', '1 Stop(s)', '9456'], ['New Delhi', 'Raipur', 'Air India', 'AI-417/9720', '11:10', '15:20', '4h 10m ', '1 Stop(s)', '9666'], ['New Delhi', 'Raipur', 'Air India', '9I-9843/9683', '05:55', '17:00', '11h 05m ', '1 Stop(s)', '10558'], ['New Delhi', 'Raipur', 'Air India', 'AI-191/651', '21:00', '11:50+ 1 day', '14h 50m ', '1 Stop(s)', '10978'], ['New Delhi', 'Raipur', 'Air India', 'AI-805/651', '20:00', '11:50+ 1 day', '15h 50m ', '1 Stop(s)', '10978'], ['New Delhi', 'Raipur', 'Air India', 'AI-24/651', '18:00', '11:50+ 1 day', '17h 50m ', '1 Stop(s)', '10978'], ['New Delhi', 'Raipur', 'Air India', 'AI-665/651', '08:00', '11:50+ 1 day', '27h 50m ', '1 Stop(s)', '10978'], ['New Delhi', 'Raipur', 'IndiGo', '6E-5038/252', '09:10', '16:35', '7h 25m ', '1 Stop(s)', '11107'], ['New Delhi', 'Raipur', 'Air India', 'AI-863/651', '23:00', '11:50+ 1 day', '12h 50m ', '1 Stop(s)', '11157'], ['New Delhi', 'Raipur', 'Air India', 'AI-102/651', '17:00', '11:50+ 1 day', '18h 50m ', '1 Stop(s)', '11293'], ['New Delhi', 'Raipur', 'Air India', 'AI-865/651', '10:40', '11:50+ 1 day', '25h 10m ', '1 Stop(s)', '11293'], ['New Delhi', 'Raipur', 'Air India', '9I-9643/9683', '18:45', '17:00+ 1 day', '22h 15m ', '1 Stop(s)', '11503'], ['New Delhi', 'Raipur', 'Air India', 'AI-437/9683', '20:00', '17:00+ 1 day', '21h 00m ', '1 Stop(s)', '12028'], ['New Delhi', 'Raipur', 'Air India', 'AI-441/651', '17:50', '11:50+ 1 day', '18h 00m ', '1 Stop(s)', '12763'], ['New Delhi', 'Raipur', 'Air India', 'AI-19/30/651', '05:00', '11:50+ 1 day', '30h 50m ', '2 Stop(s)']]
    # flights=[['New Delhi', 'Mumbai', 'Air India', 'AI-865', '10:40', '12:40', '2h 00m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Air India', 'AI-665', '08:00', '10:15', '2h 15m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Air Asia', 'I5-716', '11:55', '14:15', '2h 20m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'SpiceJet', 'SG-8911', '10:35', '12:45', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-171', '04:55', '07:05', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Go Air', 'G8-338', '10:30', '12:50', '2h 20m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Air India', 'AI-887', '07:00', '09:05', '2h 05m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'SpiceJet', 'SG-8723', '08:30', '10:35', '2h 05m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'SpiceJet', 'SG-8161', '15:50', '18:05', '2h 15m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'SpiceJet', 'SG-8153', '06:05', '08:35', '2h 30m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Go Air', 'G8-530', '07:00', '09:10', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Go Air', 'G8-334', '08:00', '10:10', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Vistara', 'UK-933', '15:30', '17:40', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Vistara', 'UK-995', '10:20', '12:35', '2h 15m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Vistara', 'UK-945', '11:40', '14:00', '2h 20m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-5335', '05:35', '07:45', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-755', '16:00', '18:15', '2h 15m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-5339', '10:00', '12:20', '2h 20m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-181', '09:20', '11:45', '2h 25m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Vistara', 'UK-975', '06:00', '08:00', '2h 00m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Air India', 'AI-641/628', '23:30', '09:20+ 1 day', '9h 50m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-957', '11:30', '13:40', '2h 10m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'IndiGo', '6E-179', '08:25', '10:40', '2h 15m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Vistara', 'UK-683/656', '13:40', '18:15', '4h 35m ', 'Non Stop '], ['New Delhi', 'Mumbai', 'Air India', 'AI-475/646', '12:55', '13:35+ 1 day', '24h 40m ', 'Non Stop ']]
    print(flights)
    return render_template('flightsearch.html', flights=flights)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/gCallback/<provider>')
def oauth_callback(provider):
    print(provider)
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    email = oauth.callback()
    if email is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user=User.query.filter_by(email=email).first()
    if not user:
        username = email.split('@')[0]
        stri=" "
        user=User(username=username, email=email,password=bcrypt.generate_password_hash(stri).decode('utf-8'))
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    return redirect(url_for('index'))

@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('login'))
        flash('Email Id not registered. Please Sign Up.')
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title = 'Reset Password', form=form)
