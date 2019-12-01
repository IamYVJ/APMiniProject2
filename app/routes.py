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
from app.flightScraperV2 import flightSearch
from app.trainscraper import trainSearch
from app.generatePNRCode import generatePNR
from app.gen_qr import genQR
from app.extractData import extractFlight

app.config['OAUTH_CREDENTIALS'] = {
    'google': {
        'id': '356186709623-6tb84gjrptp1ss0cificl90ia45qufa4.apps.googleusercontent.com',
        'secret': 'gJ5hLx6ikRTAC8NlONLZ67Kx'
    }}


a=[]
return1=["","","",""]
passenger={
  "passengersInfo" : [
    {
        "firstName" : "",
        "lastName" : "",
        "emailID" : "",
        "phoneNo" : "",
        "title" : ""
    },
    {
        "firstName" : "",
        "lastName" : "",
        "emailID" : "",
        "phoneNo" : "",
        "title" : ""
    },
    {
        "firstName" : "",
        "lastName" : "",
        "emailID" : "",
        "phoneNo" : "",
        "title" : ""
    }
  ]
}
# global b=0

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        return redirect(next) if next else redirect(url_for('index'))
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
    global return1
    form=FlightForm
    dtoday = str(date.today())
    if request.method == 'POST':
        type=request.form['type']
        if(type=='roundtrip'):
            departureCode = request.form['from']
            arrivalCode = request.form['to']
            dep=request.form['tday'].split('-')
            ret=request.form['rday'].split('-')
            return1[2]=request.form['rday']
        else:
            departureCode = request.form['from']
            arrivalCode = request.form['to']
            dep=request.form['tday'].split('-')
    return1[0]=departureCode
    return1[1]=arrivalCode
    spl=return1[2].split('-')
    print(return1[2])
    print(spl[0])
    print(type)
    print(departureCode)
    print(arrivalCode)
    print(dep)
    # print(ret)
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT count(*) FROM flights")
    #     row=cur.fetchone()
    #     print(row[0])
    # if(row[0]==0):
    if(departureCode=="" or arrivalCode=="" or len(dep)==0):
        return render_template('flights.html',form=form, dtoday = dtoday)
    else:
        flights = flightSearch(departureCode, arrivalCode, dep[2], dep[1], dep[0])
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     for rows in flights:
    #         cur.execute("INSERT INTO flights (flightid, destination ,arrival,airlines,flightno,depart,arrive,duration ,type,price) VALUES (?, ?, ?, ?, ?, ?,?,?,?,?)", (rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9]))
    print(flights)
    global a
    a=flights
    return render_template('flightsearch.html', flights=flights,type=type)

@app.route('/returnflightsearch',methods = ['POST', 'GET'])
def returnflightsearch():
    flight =  str(request.args.get('flightid'))
    flight=int(flight)
    global a
    b=a[flight]
    a=b
    flight=flight+100
    global return1
    dtoday = str(date.today())
    dep=return1[2].split('-')
    print(type)
    flights=flightSearch(return1[1],return1[0],dep[2],dep[1],dep[0])
    
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     for rows in flights:
    #         cur.execute("INSERT INTO flights (flightid, destination ,arrival,airlines,flightno,depart,arrive,duration ,type,price) VALUES (?, ?, ?, ?, ?, ?,?,?,?,?)", (rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9]))
    print(flights)
    return1=flights
    return render_template('returnflightsearch.html', flights=flights,onway=flight)



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
    global a
    flight=int(flight)
    if(flight>999):
        # b={'flightID': 'DELRPRAI46920191206_GALDOM', 'xmlKey': 'GALDOM', 'baggageAllowance': '25 kgs', 'classtype': 'Economy', 'totalStops': '1', 'totalDuration': '03:00', 'totalLayover': '00:00', 'airline': 'Air India', 'airlineCode': 'AI', 'vehicleCode': 'AI', 'flightNo': '469', 'departureCityCode': 'DEL', 'arrivalCityCode': 'RPR', 'departureDate': '2019-12-06', 'arrivalDate': '2019-12-06', 'departureTime': '05:25', 'arrivalTime': '08:25', 'aircraft': 'Airbus A320', 'departureTerminal': 'T-3', 'arrivalTerminal': '', 'mealCost': 'Free Meal', 'baseFare': '3530', 'totalFare': '4153', 'px': 'ADT', 'qt': '1', 'fuelSurcharge': '355', 'PSF': '268', 'userDevelopmentFee': '0', 'goodsAndServiceTax': '0', 'GAST': '0', 'swachhBharatCess': '0', 'krishiKalyanCess': '0', 'cuteFee': '0', 'airportArrivalTax': '0', 'developmentFee': '0', 'otherFlightsInfo': []}
        b=a
        print(b)
        flight=str(flight)
        retflight=flight[:-3]
        print(retflight)
        retflight=int(retflight)-1
        print(retflight)
        global return1
        return1=return1[retflight]
        # return1={'flightID': 'RPRDELAI46920191207_GALDOM', 'xmlKey': 'GALDOM', 'baggageAllowance': '25 kgs', 'classtype': 'Economy', 'totalStops': '1', 'totalDuration': '02:50', 'totalLayover': '00:00', 'airline': 'Air India', 'airlineCode': 'AI', 'vehicleCode': 'AI', 'flightNo': '469', 'departureCityCode': 'RPR', 'arrivalCityCode': 'DEL', 'departureDate': '2019-12-07', 'arrivalDate': '2019-12-07', 'departureTime': '07:45', 'arrivalTime': '10:35', 'aircraft': 'Airbus A320', 'departureTerminal': '', 'arrivalTerminal': 'T-3', 'mealCost': 'Free Meal', 'baseFare': '3530', 'totalFare': '4153', 'px': 'ADT', 'qt': '1', 'fuelSurcharge': '355', 'PSF': '268', 'userDevelopmentFee': '0', 'goodsAndServiceTax': '0', 'GAST': '0', 'swachhBharatCess': '0', 'krishiKalyanCess': '0', 'cuteFee': '0', 'airportArrivalTax': '0', 'developmentFee': '0', 'otherFlightsInfo': []}
        abc=[]
        flight=1000
        abc.append(b)
        abc.append(return1)
        print(return1)
        print(abc)
        return render_template('book.html', row=abc , index=flight)
    else:
        b=a[flight]
        a=b
        abc=[]
        flight=100
        abc.append(a)
        print(abc)
        return render_template('book.html', row=abc , index=flight)


@app.route('/flightbooked',methods = ['POST', 'GET'])
@login_required
def flightbooked():
    global a
    # a={'flightID': 'DELRPRAI47720191204_GALDOM', 'xmlKey': 'GALDOM', 'baggageAllowance': '25 kgs', 'classtype': 'Economy', 'totalStops': '0', 'totalDuration': '01:40', 'totalLayover': '00:00', 'airline': 'Air India', 'airlineCode': 'AI', 'vehicleCode': 'AI', 'flightNo': '477', 'departureCityCode': 'DEL', 'arrivalCityCode': 'RPR', 'departureDate': '2019-12-04', 'arrivalDate': '2019-12-04', 'departureTime': '05:25', 'arrivalTime': '07:05', 'aircraft': 'Airbus A319', 'departureTerminal': 'T-3', 'arrivalTerminal': '', 'mealCost': 'Free Meal', 'baseFare': '3530', 'totalFare': '4153', 'px': 'ADT', 'qt': '1', 'fuelSurcharge': '355', 'PSF': '268', 'userDevelopmentFee': '0', 'goodsAndServiceTax': '0', 'GAST': '0', 'swachhBharatCess': '0', 'krishiKalyanCess': '0', 'cuteFee': '0', 'airportArrivalTax': '0', 'developmentFee': '0', 'otherFlightsInfo': []}
    print(a)
    global passenger
    # passenger={'passengersInfo': [{'firstName': 'Yash', 'lastName': 'Burad', 'emailID': '', 'phoneNo': '9898', 'title': 'Mr.', 'emailId': 'yash.burad_ug21@ashoka.edu.in'}, {'firstName': '', 'lastName': '', 'emailID': '', 'phoneNo': '', 'title': ''}, {'firstName': '', 'lastName': '', 'emailID': '', 'phoneNo': '', 'title': ''}]}
    print(passenger)
    pnr=generatePNR()
    dtoday = str(date.today())
    print(a['departureTime'])
    # user_id,pnr,firstname,lastname, departure,destination,flight_duration,departure_time,arrival_time,date,output,scale
    genQR(current_user.id, pnr, passenger['passengersInfo'][0]['firstName'],passenger['passengersInfo'][0]['lastName'],a['departureCityCode'],a['arrivalCityCode'],a['totalDuration'],a['departureTime'],a['arrivalTime'],dtoday,5)
    details=str(a)
    passengerdetails=str(passenger)
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO orderflights (userId, details ,pnr,passengers) VALUES (?, ?, ?, ?)", (current_user.id,details,pnr,passengerdetails))
    return render_template('flightbooked.html', row=a, passenger=passenger,pnr=pnr)



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
@login_required
def payment():
    email=""
    dtoday = str(date.today())
    if request.method == 'POST':
        email = request.form['email']
        number = request.form['phone']
        title = request.form['title']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
    if (email==""):
        return render_template('flights.html', dtoday = dtoday)
    flight =  str(request.args.get('flightid'))
    print(flight)
    global a
    global return1
    global passenger
    flight=int(flight)
    fare=["","",""]
    if(flight>999):
        fare2=int(a['baseFare'])+int(return1['baseFare'])
        fare[0]=fare2
        fare2=int(a['fuelSurcharge'])+int(return1['fuelSurcharge'])
        fare[1]=fare2
        fare2=int(a['totalFare'])+int(return1['totalFare'])
        fare[2]=fare2
    else:
        fare2=int(a['baseFare'])
        fare[0]=fare2
        fare2=int(a['fuelSurcharge'])
        fare[1]=fare2
        fare2=int(a['totalFare'])
        fare[2]=fare2
    abc=[]
    abc.append(a)
    abc.append(return1)
    print(a)
    print(return1)
    passenger["passengersInfo"][0]["firstName"]=firstname
    passenger["passengersInfo"][0]["lastName"]=lastname
    passenger["passengersInfo"][0]["emailId"]=email
    passenger["passengersInfo"][0]["phoneNo"]=number
    passenger["passengersInfo"][0]["title"]=title
    print(passenger)
    if(flight>999):  
        return render_template('payment.html', row=abc,fare=fare)
    else:
        return render_template('payment.html', row=a,fare=fare)

@app.route('/train',methods = ['POST', 'GET'])
def train():
    # if request.method == 'POST':
    #   result = request.form
    # print(flights)
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("DELETE from flights")
    dtoday = str(date.today())
    print(dtoday)
    # if form.validate_on_submit():
    #     return form.dt.data.strftime('%Y-%m-%d')
    return render_template('train.html', dtoday = dtoday)

@app.route('/trainsearch',methods = ['POST', 'GET'])
def trainsearch():
    srcStn="R"
    srcCity=""
    destStn="HWH"
    destCity=""
    dep=""
    dtoday = str(date.today())
    if request.method == 'POST':
        srcCity = request.form['from']
        destCity = request.form['to']
        dep=request.form['tday'].split('-')
    print(srcCity)
    print(destCity)
    print(dep)
    
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT count(*) FROM flights")
    #     row=cur.fetchone()
    #     print(row[0])
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
    # flights=[[0, 'New Delhi', 'Mumbai', 'Go Air', 'G8-429', '21:35', '23:50', '2h 15m ', 'Non Stop ', '5308'], [1, 'New Delhi', 'Mumbai', 'Go Air', 'G8-338', '10:30', '12:50', '2h 20m ', 'Non Stop ', '5308'], [2, 'New Delhi', 'Mumbai', 'Go Air', 'G8-640', '18:00', '20:20', '2h 20m ', 'Non Stop ', '5308'], [3, 'New Delhi', 'Mumbai', 'Go Air', 'G8-544', '22:40', '01:00+ 1 day', '2h 20m ', 'Non Stop ', '5308'], [4, 'New Delhi', 'Mumbai', 'Go Air', 'G8-446', '19:40', '22:05', '2h 25m ', 'Non Stop ', '5308'], [5, 'New Delhi', 'Mumbai', 'Vistara', 'UK-975', '06:00', '08:00', '2h 00m ', 'Non Stop ', '5518'], [6, 'New Delhi', 'Mumbai', 'Air India', 'AI-887', '07:00', '09:05', '2h 05m ', 'Non Stop ', '5518'], [7, 'New Delhi', 'Mumbai', 'Vistara', 'UK-985', '19:50', '21:55', '2h 05m ', 'Non Stop ', '5518'], [8, 'New Delhi', 'Mumbai', 'Air India', 'AI-805', '20:00', '22:10', '2h 10m ', 'Non Stop ', '5518'], [9, 'New Delhi', 'Mumbai', 'Air India', 'AI-191', '21:00', '23:10', '2h 10m ', 'Non Stop ', '5518'], [10, 'New Delhi', 'Mumbai', 'Vistara', 'UK-927', '09:30', '11:40', '2h 10m ', 'Non Stop ', '5518'], [11, 'New Delhi', 'Mumbai', 'Vistara', 'UK-953', '20:40', '22:50', '2h 10m ', 'Non Stop ', '5518'], [12, 'New Delhi', 'Mumbai', 'Vistara', 'UK-981', '21:40', '23:50', '2h 10m ', 'Non Stop ', '5518'], [13, 'New Delhi', 'Mumbai', 'Vistara', 'UK-933', '15:30', '17:40', '2h 10m ', 'Non Stop ', '5518'], [14, 'New Delhi', 'Mumbai', 'Go Air', 'G8-530', '07:00', '09:10', '2h 10m ', 'Non Stop ', '5518'], [15, 'New Delhi', 'Mumbai', 'Air India', 'AI-665', '08:00', '10:15', '2h 15m ', 'Non Stop ', '5518'], [16, 'New Delhi', 'Mumbai', 'Air India', 'AI-24', '18:00', '20:15', '2h 15m ', 'Non Stop ', '5518'], [17, 'New Delhi', 'Mumbai', 'Vistara', 'UK-995', '10:20', '12:35', '2h 15m ', 'Non Stop ', '5518'], [18, 'New Delhi', 'Mumbai', 'Vistara', 'UK-993', '12:45', '15:00', '2h 15m ', 'Non Stop ', '5518'], [19, 'New Delhi', 'Mumbai', 'Vistara', 'UK-923', '06:40', '09:00', '2h 20m ', 'Non Stop ', '5518'], [20, 'New Delhi', 'Mumbai', 'Vistara', 'UK-963', '08:50', '11:10', '2h 20m ', 'Non Stop ', '5518'], [21, 'New Delhi', 'Mumbai', 'Vistara', 'UK-945', '11:40', '14:00', '2h 20m ', 'Non Stop ', '5518'], [22, 'New Delhi', 'Mumbai', 'Vistara', 'UK-955', '17:45', '20:05', '2h 20m ', 'Non Stop ', '5518'], [23, 'New Delhi', 'Mumbai', 'Vistara', 'UK-977', '18:55', '21:15', '2h 20m ', 'Non Stop ', '5518'], [24, 'New Delhi', 'Mumbai', 'Air Asia', 'I5-881', '05:20', '07:30', '2h 10m ', 'Non Stop ', '5600']]
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     for rows in flights:
    #         cur.execute("INSERT INTO flights (flightid, destination ,arrival,airlines,flightno,depart,arrive,duration ,type,price) VALUES (?, ?, ?, ?, ?, ?,?,?,?,?)", (rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9]))
    # print(flights)
    train=trainSearch(srcStn, srcCity, destStn, destCity, dep[2], dep[1], dep[0])
    global a
    # train=[['GITANJALI EX', '#12859', 'S   M   T   W   T   F   S', '11:35 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '12h 55m', '12:30 PM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'Booking not allowed', 'Updated 3 hrs ago'], ['3 Tier AC', '1165', 'RLWL 24', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 14', 'Updated 3 hrs ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['JNANESWARI DEL', '#12101', 'S   T   W   S', '2:30 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 5m', '3:35 AM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'RLWL 41', 'Updated 1 day ago'], ['3 Tier AC', '1165', 'RLWL 22', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 6', 'Updated 1 day ago'], ['1st Class AC', '2815', 'RLWL 3', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['SNSI HWH SUP EX', '#22893', 'S', '6:10 AM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 20m', '7:30 PM  Sun', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '445', 'RLWL 90', 'Updated 1 day ago'], ['3 Tier AC', '1175', 'RLWL 36', 'Updated 1 day ago'], ['2 Tier AC', '1675', 'Booking not allowed', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['AZAD HIND EX', '#12129', 'S   M   T   W   T   F   S', '2:52 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 23m', '4:15 AM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'RLWL 44', 'Updated 18 hrs ago'], ['3 Tier AC', '1165', 'Booking not allowed', 'Updated 18 hrs ago'], ['2 Tier AC', '1660', 'RLWL 9', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['HOWRAH MAI', '#12809', 'S   M   T   W   T   F   S', '4:10 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 40m', '5:50 AM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'RLWL 49', 'Updated 6 hrs ago'], ['3 Tier AC', '1165', 'RLWL 24', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 9', 'Updated 1 day ago'], ['1st Class AC', '2815', 'RLWL 2', 'Updated 2 days ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['HOWRAH EXPRES', '#12833', 'S   M   T   W   T   F   S', '11:05 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '14h 25m', '1:30 PM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '445', 'RLWL 69', 'Updated 19 hrs ago'], ['3 Tier AC', '1175', 'RLWL 17', 'Updated 9 hrs ago'], ['2 Tier AC', '1675', 'RLWL 16', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['LTT SHALIMAR E', '#18029', 'S   M   T   W   T   F   S', '7:42 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '16h 38m', '12:20 PM  Mon', 'SHMDifferentYou searched for trains arriving in HWH (Kolkata), but this train arrives in SHM (Shalimar).HWH R SHMShalimar', [['Sleeper', '410', 'RLWL 55', 'Updated 23 hrs ago'], ['3 Tier AC', '1120', 'RLWL 17', 'Updated 23 hrs ago'], ['2 Tier AC', '1615', 'RLWL 8', 'Updated 23 hrs ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019']]
    a=train
    print(train[1][8][0])
    return render_template('trainsearch.html', flights=train)

@app.route('/booktrain',methods = ['POST', 'GET'])
def booktrain():
    trainid =  str(request.args.get('trainid'))
    ind=(int(trainid[0])-1)
    priceindex=int(trainid[2])
    print(ind)
    print(priceindex)
    global a
    print(a[ind])
    print(a[ind][8][priceindex])
    dtoday = str(date.today())
    print(dtoday)
    # if form.validate_on_submit():
    #     return form.dt.data.strftime('%Y-%m-%d')
    return render_template('booktrain.html', row = a[ind], ind=priceindex, i=ind)

@app.route('/trainpayment',methods = ['POST', 'GET'])
@login_required
def trainpayment():
    email=""
    dtoday = str(date.today())
    if request.method == 'POST':
        email = request.form['email']
        number = request.form['phone']
        title = request.form['title']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
    if (email==""):
        return render_template('train.html', dtoday = dtoday)
    trainid =  str(request.args.get('trainid'))
    ind=(int(trainid[0]))
    priceindex=int(trainid[1])
    print(ind)
    print(priceindex)
    global a
    b=[]
    b.append(email)
    b.append(number)
    b.append(title)
    b.append(firstname)
    b.append(lastname)
    print(b)
    a = list(a)
    a[ind].append(b)
    print(a[ind])
    print(a[ind][8][priceindex][1])
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM flights WHERE flightid =" +str(flight))
    #     row=cur.fetchone()    
    # print(row)
    return render_template('trainpayment.html', price=a[ind][8][priceindex][1], ind=ind,priceindex=priceindex)

@app.route('/trainbooked',methods = ['POST', 'GET'])
@login_required
def trainbooked():
    # trainid =  str(request.args.get('trainid'))
    # ind=(int(trainid[0]))
    # priceindex=int(trainid[1])
    # global a
    # b=a[ind]
    # print(b)
    # print(b[ind])
    # b[8]=b[8][priceindex]
    # print(b)
    # b="['GITANJALI EX', '#12859', 'S   M   T   W   T   F   S', '11:35 PM  Mon', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '12h 55m', '12:30 PM  Tue', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', ['3 Tier AC', '1165', 'RLWL 23', 'Updated 8 hrs ago'], 'R', 'Raipur', 'HWH', 'Kolkata', '02-12-2019', ['yash.burad_ug21@ashoka.edu.in', '9898', 'Mr.', 'Yash', 'Burad']]"
    b={'flightID': 'DELIDR6E503820191215IDRRPR6E25220191215_6EAPI', 'xmlKey': '6EAPI', 'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'totalStops': '1', 'totalDuration': '07:25', 'totalLayover': '04:45', 'airline': '', 'airlineCode': '', 'vehicleCode': '', 'flightNo': '', 'departureCityCode': '', 'arrivalCityCode': '', 'departureDate': '', 'arrivalDate': '', 'departureTime': '', 'arrivalTime': '', 'aircraft': '', 'departureTerminal': '', 'arrivalTerminal': '', 'mealCost': '', 'baseFare': '6091', 'totalFare': '7241', 'px': 'ADT', 'qt': '1', 'fuelSurcharge': '1150', 'PSF': '0', 'userDevelopmentFee': '0', 'goodsAndServiceTax': '0', 'GAST': '0', 'swachhBharatCess': '0', 'krishiKalyanCess': '0', 'cuteFee': '0', 'airportArrivalTax': '0', 'developmentFee': '0', 'otherFlightsInfo': [{'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'airline': 'IndiGo', 'airlineCode': '6E', 'vehicleCode': '6E', 'flightNo': '5038', 'departureCityCode': 'DEL', 'arrivalCityCode': 'IDR', 'departureDate': '2019-12-15', 'arrivalDate': '2019-12-15', 'departureTime': '09:10', 'arrivalTime': '10:35', 'aircraft': 'Airbus A320-100', 'departureTerminal': 'T-3', 'arrivalTerminal': '', 'mealCost': 'Paid Meal'}, {'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'airline': 'IndiGo', 'airlineCode': '6E', 'vehicleCode': '6E', 'flightNo': '252', 'departureCityCode': 'IDR', 'arrivalCityCode': 'RPR', 'departureDate': '2019-12-15', 'arrivalDate': '2019-12-15', 'departureTime': '15:20', 'arrivalTime': '16:35', 'aircraft': 'Airbus A320-100', 'departureTerminal': '', 'arrivalTerminal': '', 'mealCost': 'Paid Meal'}]}
    pnr=generatePNR()
    print(pnr)
    sdetails=str(b)
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO ordertrains1 (userid, details ,qrcode,pnr) VALUES (?, ?, ?, ?)", (current_user.id,sdetails,pnr,pnr))
    # user_id,pnr,firstname,lastname, departure,destination,flight_duration,departure_time,arrival_time,date,output,scale
    # genQR(current_user.id, pnr, b[14][3],b[14][4],b[10],b[12],b[5],b[3],b[6],b[13],5)
    return render_template('trainbooked.html', pnr=pnr, row=b)
