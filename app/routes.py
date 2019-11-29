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
    # print(flights)
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("DELETE from flights")
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
    flights=[]
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
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM flights")
        row=cur.fetchone()
        print(row[0])
    # if(row[0]==0):
    #     if(departureCode=="" or arrivalCode=="" or len(dep)==0):
    #         return render_template('flights.html',form=form, dtoday = dtoday)
    #     # else:
    #         # flights = flightSearch(departureCode, arrivalCode, dep[2], dep[1], dep[0])
    # else:
    #     with sqlite3.connect('app/site.db') as conn:
    #         cur = conn.cursor()
    #         cur.execute("SELECT * FROM flights")
    #         row=cur.fetchall()
    #         for rows in row:
    #             flights.append(rows)
    # print(flights)

    flights=[[0, 'New Delhi', 'Mumbai', 'Go Air', 'G8-429', '21:35', '23:50', '2h 15m ', 'Non Stop ', '5308'], [1, 'New Delhi', 'Mumbai', 'Go Air', 'G8-338', '10:30', '12:50', '2h 20m ', 'Non Stop ', '5308'], [2, 'New Delhi', 'Mumbai', 'Go Air', 'G8-640', '18:00', '20:20', '2h 20m ', 'Non Stop ', '5308'], [3, 'New Delhi', 'Mumbai', 'Go Air', 'G8-544', '22:40', '01:00+ 1 day', '2h 20m ', 'Non Stop ', '5308'], [4, 'New Delhi', 'Mumbai', 'Go Air', 'G8-446', '19:40', '22:05', '2h 25m ', 'Non Stop ', '5308'], [5, 'New Delhi', 'Mumbai', 'Vistara', 'UK-975', '06:00', '08:00', '2h 00m ', 'Non Stop ', '5518'], [6, 'New Delhi', 'Mumbai', 'Air India', 'AI-887', '07:00', '09:05', '2h 05m ', 'Non Stop ', '5518'], [7, 'New Delhi', 'Mumbai', 'Vistara', 'UK-985', '19:50', '21:55', '2h 05m ', 'Non Stop ', '5518'], [8, 'New Delhi', 'Mumbai', 'Air India', 'AI-805', '20:00', '22:10', '2h 10m ', 'Non Stop ', '5518'], [9, 'New Delhi', 'Mumbai', 'Air India', 'AI-191', '21:00', '23:10', '2h 10m ', 'Non Stop ', '5518'], [10, 'New Delhi', 'Mumbai', 'Vistara', 'UK-927', '09:30', '11:40', '2h 10m ', 'Non Stop ', '5518'], [11, 'New Delhi', 'Mumbai', 'Vistara', 'UK-953', '20:40', '22:50', '2h 10m ', 'Non Stop ', '5518'], [12, 'New Delhi', 'Mumbai', 'Vistara', 'UK-981', '21:40', '23:50', '2h 10m ', 'Non Stop ', '5518'], [13, 'New Delhi', 'Mumbai', 'Vistara', 'UK-933', '15:30', '17:40', '2h 10m ', 'Non Stop ', '5518'], [14, 'New Delhi', 'Mumbai', 'Go Air', 'G8-530', '07:00', '09:10', '2h 10m ', 'Non Stop ', '5518'], [15, 'New Delhi', 'Mumbai', 'Air India', 'AI-665', '08:00', '10:15', '2h 15m ', 'Non Stop ', '5518'], [16, 'New Delhi', 'Mumbai', 'Air India', 'AI-24', '18:00', '20:15', '2h 15m ', 'Non Stop ', '5518'], [17, 'New Delhi', 'Mumbai', 'Vistara', 'UK-995', '10:20', '12:35', '2h 15m ', 'Non Stop ', '5518'], [18, 'New Delhi', 'Mumbai', 'Vistara', 'UK-993', '12:45', '15:00', '2h 15m ', 'Non Stop ', '5518'], [19, 'New Delhi', 'Mumbai', 'Vistara', 'UK-923', '06:40', '09:00', '2h 20m ', 'Non Stop ', '5518'], [20, 'New Delhi', 'Mumbai', 'Vistara', 'UK-963', '08:50', '11:10', '2h 20m ', 'Non Stop ', '5518'], [21, 'New Delhi', 'Mumbai', 'Vistara', 'UK-945', '11:40', '14:00', '2h 20m ', 'Non Stop ', '5518'], [22, 'New Delhi', 'Mumbai', 'Vistara', 'UK-955', '17:45', '20:05', '2h 20m ', 'Non Stop ', '5518'], [23, 'New Delhi', 'Mumbai', 'Vistara', 'UK-977', '18:55', '21:15', '2h 20m ', 'Non Stop ', '5518'], [24, 'New Delhi', 'Mumbai', 'Air Asia', 'I5-881', '05:20', '07:30', '2h 10m ', 'Non Stop ', '5600']]
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     for rows in flights:
    #         cur.execute("INSERT INTO flights (flightid, destination ,arrival,airlines,flightno,depart,arrive,duration ,type,price) VALUES (?, ?, ?, ?, ?, ?,?,?,?,?)", (rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9]))
    # print(flights)
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
@login_required
def myaccount():
    return render_template('myaccount.html')

@app.route('/book')
def book():
    flight =  str(request.args.get('flightid'))
    print(flight)
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM flights WHERE flightid =" +str(flight))
        row=cur.fetchone()
    return render_template('book.html', row=row)

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

@app.route('/payment',methods = ['POST', 'GET'])
def payment():
    print("111")
    return render_template('payment.html')