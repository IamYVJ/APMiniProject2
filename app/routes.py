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
from app.hotelsScraper import soupSite,get_source_sel,hotelDetail
from app.emailSend import EmailClass



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
    global return1
    abc=[]
    abc.append(a)
    abc.append(return1)
    # passenger={'passengersInfo': [{'firstName': 'Yash', 'lastName': 'Burad', 'emailID': '', 'phoneNo': '9898', 'title': 'Mr.', 'emailId': 'yash.burad_ug21@ashoka.edu.in'}, {'firstName': '', 'lastName': '', 'emailID': '', 'phoneNo': '', 'title': ''}, {'firstName': '', 'lastName': '', 'emailID': '', 'phoneNo': '', 'title': ''}]}
    print(passenger)
    pnr=generatePNR()
    dtoday = str(date.today())
    print(a['departureTime'])
    # user_id,pnr,firstname,lastname, departure,destination,flight_duration,departure_time,arrival_time,date,output,scale
    genQR(current_user.id, pnr, passenger['passengersInfo'][0]['firstName'],passenger['passengersInfo'][0]['lastName'],a['departureCityCode'],a['arrivalCityCode'],a['totalDuration'],a['departureTime'],a['arrivalTime'],dtoday)
    details=str(a)
    returndetails=str(return1)
    passengerdetails=str(passenger)
    print(abc)
    fare=["","",""]
    if(len(return1)>5):
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
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO orderflights (userId, details ,pnr,passengers,return) VALUES (?, ?, ?, ?,?)", (current_user.id,details,pnr,passengerdetails,returndetails))
    return render_template('flightbooked.html', row=abc, passenger=passenger,pnr=pnr,fare=fare)



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
    fare=['500','1000','1500']
    return render_template('payment.html',fare=fare)
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

    searchDep = ""
    searchArr = ""
    dep=""
    dtoday = str(date.today())
    if request.method == 'POST':
        searchDep = request.form['from']
        searchArr = request.form['to']
        dep=request.form['tday'].split('-')
    # train=trainSearch(srcStn, srcCity, destStn, destCity, dep[2], dep[1], dep[0])
    train = trainSearch(searchDep, searchArr, dep[2], dep[1], dep[0])
    global a
    # train=[['GITANJALI EX', '#12859', 'S   M   T   W   T   F   S', '11:35 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '12h 55m', '12:30 PM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'Booking not allowed', 'Updated 3 hrs ago'], ['3 Tier AC', '1165', 'RLWL 24', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 14', 'Updated 3 hrs ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['JNANESWARI DEL', '#12101', 'S   T   W   S', '2:30 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 5m', '3:35 AM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'RLWL 41', 'Updated 1 day ago'], ['3 Tier AC', '1165', 'RLWL 22', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 6', 'Updated 1 day ago'], ['1st Class AC', '2815', 'RLWL 3', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['SNSI HWH SUP EX', '#22893', 'S', '6:10 AM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 20m', '7:30 PM  Sun', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '445', 'RLWL 90', 'Updated 1 day ago'], ['3 Tier AC', '1175', 'RLWL 36', 'Updated 1 day ago'], ['2 Tier AC', '1675', 'Booking not allowed', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['AZAD HIND EX', '#12129', 'S   M   T   W   T   F   S', '2:52 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 23m', '4:15 AM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'RLWL 44', 'Updated 18 hrs ago'], ['3 Tier AC', '1165', 'Booking not allowed', 'Updated 18 hrs ago'], ['2 Tier AC', '1660', 'RLWL 9', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['HOWRAH MAI', '#12809', 'S   M   T   W   T   F   S', '4:10 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '13h 40m', '5:50 AM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'RLWL 49', 'Updated 6 hrs ago'], ['3 Tier AC', '1165', 'RLWL 24', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 9', 'Updated 1 day ago'], ['1st Class AC', '2815', 'RLWL 2', 'Updated 2 days ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['HOWRAH EXPRES', '#12833', 'S   M   T   W   T   F   S', '11:05 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '14h 25m', '1:30 PM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '445', 'RLWL 69', 'Updated 19 hrs ago'], ['3 Tier AC', '1175', 'RLWL 17', 'Updated 9 hrs ago'], ['2 Tier AC', '1675', 'RLWL 16', 'Updated 1 day ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019'], ['LTT SHALIMAR E', '#18029', 'S   M   T   W   T   F   S', '7:42 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '16h 38m', '12:20 PM  Mon', 'SHMDifferentYou searched for trains arriving in HWH (Kolkata), but this train arrives in SHM (Shalimar).HWH R SHMShalimar', [['Sleeper', '410', 'RLWL 55', 'Updated 23 hrs ago'], ['3 Tier AC', '1120', 'RLWL 17', 'Updated 23 hrs ago'], ['2 Tier AC', '1615', 'RLWL 8', 'Updated 23 hrs ago']], 'R', 'Raipur', 'HWH', 'Kolkata', '01-12-2019']]
    a=train
    # print(train[1][8][0])
    print(train)
    if(len(a)==0):
        flash('No trains found for this route', 'danger')
        return render_template('train.html')
    elif(len(a)==1):
        if(a[0]==1):
            flash('No station found for '+searchArr , 'danger')
        elif(a[0]==0):
            flash('No station found for '+searchDep , 'danger')
        return render_template('train.html')

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
    print(a[ind]["classes"][priceindex])
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
    # b=[]
    # b.append(email)
    # b.append(number)
    # b.append(title)
    # b.append(firstname)
    # b.append(lastname)
    # print(b)
    passenger = {
    "title" : "",
    "firstName" : "",
    "lastName" : "",
    "emailID" : "",
    "phoneNo" : ""
    }
    passenger["title"] = title
    passenger["firstName"] = firstname
    passenger["lastName"] = lastname
    passenger["emailID"] = email
    passenger["phoneNo"] = number
    # a = list(a)
    # a[ind].append(b)
    a[ind]["passengerDetails"] = passenger
    print(a[ind])
    print(a[ind]["classes"][priceindex]["price"])
    # with sqlite3.connect('app/site.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM flights WHERE flightid =" +str(flight))
    #     row=cur.fetchone()
    # print(row)
    return render_template('trainpayment.html', price=a[ind]["classes"][priceindex]["price"], ind=ind,priceindex=priceindex)

@app.route('/trainbooked',methods = ['POST', 'GET'])
@login_required
def trainbooked():
    trainid =  str(request.args.get('trainid'))
    ind=(int(trainid[0]))
    priceindex=int(trainid[1])
    global a
    # a= {'trainName': 'JNANESWARISUPDL', 'trainNo': '#12102', 'days': 'S   M   W   T', 'departureTime': '10:50 PM  Thu', 'depStnInfo': 'HWHYou searched for trains departing from HWH(HWH), but this train departs from HWH (Howrah Jn)HWH HWH RHowrah Jn', 'duration': '12h 25m', 'arrivalTime': '11:15 AM  Fri', 'arrStnInfo': 'RYou searched for trains arriving in R (Raipur), but this train arrives in R (Raipur Jn).R HWH RRaipur Jn', 'classes': [{'className': 'Sleeper', 'price': '445', 'availability': 'PQWL 51', 'update': 'Updated 2 hrs ago'}, {'className': '3 Tier AC', 'price': '1175', 'availability': 'PQWL 26', 'update': 'Updated 30 mins ago'}, {'className': '2 Tier AC', 'price': '1675', 'availability': 'PQWL 18', 'update': 'Updated 22 hrs ago'}, {'className': '1st Class AC', 'price': '2835', 'availability': 'PQWL 7', 'update': 'Updated 22 hrs ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': '', 'passengerDetails': {'title': 'Mr.', 'firstName': 'Yash', 'lastName': 'Burad', 'emailID': 'yash.burad_ug21@ashoka.edu.in', 'phoneNo': '9898'}}
    b=a[ind]
    # print(b[ind])
    b["classes"]=b["classes"][priceindex]
    print(b)
    # print(b)
    # b="['GITANJALI EX', '#12859', 'S   M   T   W   T   F   S', '11:35 PM  Mon', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '12h 55m', '12:30 PM  Tue', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', ['3 Tier AC', '1165', 'RLWL 23', 'Updated 8 hrs ago'], 'R', 'Raipur', 'HWH', 'Kolkata', '02-12-2019', ['yash.burad_ug21@ashoka.edu.in', '9898', 'Mr.', 'Yash', 'Burad']]"
    # b={'flightID': 'DELIDR6E503820191215IDRRPR6E25220191215_6EAPI', 'xmlKey': '6EAPI', 'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'totalStops': '1', 'totalDuration': '07:25', 'totalLayover': '04:45', 'airline': '', 'airlineCode': '', 'vehicleCode': '', 'flightNo': '', 'departureCityCode': '', 'arrivalCityCode': '', 'departureDate': '', 'arrivalDate': '', 'departureTime': '', 'arrivalTime': '', 'aircraft': '', 'departureTerminal': '', 'arrivalTerminal': '', 'mealCost': '', 'baseFare': '6091', 'totalFare': '7241', 'px': 'ADT', 'qt': '1', 'fuelSurcharge': '1150', 'PSF': '0', 'userDevelopmentFee': '0', 'goodsAndServiceTax': '0', 'GAST': '0', 'swachhBharatCess': '0', 'krishiKalyanCess': '0', 'cuteFee': '0', 'airportArrivalTax': '0', 'developmentFee': '0', 'otherFlightsInfo': [{'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'airline': 'IndiGo', 'airlineCode': '6E', 'vehicleCode': '6E', 'flightNo': '5038', 'departureCityCode': 'DEL', 'arrivalCityCode': 'IDR', 'departureDate': '2019-12-15', 'arrivalDate': '2019-12-15', 'departureTime': '09:10', 'arrivalTime': '10:35', 'aircraft': 'Airbus A320-100', 'departureTerminal': 'T-3', 'arrivalTerminal': '', 'mealCost': 'Paid Meal'}, {'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'airline': 'IndiGo', 'airlineCode': '6E', 'vehicleCode': '6E', 'flightNo': '252', 'departureCityCode': 'IDR', 'arrivalCityCode': 'RPR', 'departureDate': '2019-12-15', 'arrivalDate': '2019-12-15', 'departureTime': '15:20', 'arrivalTime': '16:35', 'aircraft': 'Airbus A320-100', 'departureTerminal': '', 'arrivalTerminal': '', 'mealCost': 'Paid Meal'}]}
    pnr=generatePNR()
    print(pnr)
    sdetails=str(b)
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO ordertrains (userid, details ,qrcode,pnr) VALUES (?, ?, ?, ?)", (current_user.id,sdetails,pnr,pnr))
    # user_id,pnr,firstname,lastname, departure,destination,flight_duration,departure_time,arrival_time,date,output,scale
    genQR(current_user.id, pnr, b["passengerDetails"]["firstName"],b["passengerDetails"]["lastName"],b["departureStnCode"],b["arrivalStnCode"],b["duration"],b["departureTime"],b["arrivalTime"],b["departureDate"])
    
    return render_template('trainbooked.html', pnr=pnr, row=b)

@app.route('/hotels',methods = ['POST', 'GET'])
def hotels():
    dtoday = str(date.today())
    print(dtoday)
    return render_template('hotels.html', dtoday = dtoday)

@app.route('/myorders',methods = ['POST', 'GET'])
def myorders():
    dtoday = str(date.today())
    print(dtoday)
    return render_template('myorders.html', dtoday = dtoday)

@app.route('/hotelsearch',methods = ['POST', 'GET'])
def hotelsearch():
    if request.method == 'POST':
        destination = request.form['place']
        rooms = request.form['rooms']
        checkin = request.form['inday']
        checkout = request.form['outday']
        adults = request.form['adults']
    print(destination)
    print(rooms)
    print(checkin)
    print(checkout)
    print(adults)
    row=soupSite(get_source_sel(destination,checkin,checkout,rooms,adults))
    global a
    a=row
    print(a)
    dtoday = str(date.today())
    # row=[[0, 'Courtyard by Marriott Raipur', 'Raipur', '4,680', 'https://thumbnails.trvl-media.com/eE9z7pDtp1yjX_Bg5neHpTD4nUY=/455x235/smart/images.trvl-media.com/hotels/14000000/13400000/13396500/13396463/c2d22074_b.jpg', '4.8/5', 'Exceptional', '15'], [1, 'Hyatt Raipur', 'Viewed', '6,250', 'https://thumbnails.trvl-media.com/ogtUmbfUQd5cXKkVsVq2PGTW96k=/455x235/smart/images.trvl-media.com/hotels/8000000/7070000/7065500/7065412/38c7f465_b.jpg', '4.1/5', 'Very Good', '50'], [2, 'Courtyard by Marriott Raipur', 'Raipur', '4,680', 'https://thumbnails.trvl-media.com/gNYraClYJIVqrY3_nANKYV_e-lo=/455x235/smart/images.trvl-media.com/hotels/14000000/13400000/13396500/13396463/b1aa54ca_w.jpg', '4.8/5', 'Exceptional', '15'], [3, 'Hotel Sayaji Raipur', 'Viewed', '7,350', 'https://thumbnails.trvl-media.com/8BopfeA7_HctEpYJObkaJf2XKII=/1200x800/smart/images.trvl-media.com/hotels/19000000/18350000/18341000/18340918/c4bc0712_w.jpg', '4.0/5', 'Very Good', '8'], [4, 'Hyatt Raipur', 'Viewed', '6,250', 'https://thumbnails.trvl-media.com/CdV7xdS6tJV5XyBSUMUUjw438aA=/1200x800/smart/images.trvl-media.com/hotels/8000000/7070000/7065500/7065412/38c7f465_w.jpg', '4.1/5', 'Very Good', '50'], [5, 'Singhania Sarovar Portico', 'Viewed', '3,699', 'https://thumbnails.trvl-media.com/JOpjEtnpV-2AoadE8uQ_tTM1-Yc=/1200x800/smart/images.trvl-media.com/hotels/23000000/22200000/22196300/22196226/6366c4de_w.jpg', '4.5/5', 'Wonderful', '4'], [6, 'Hotel Babylon Inn', 'Viewed', '3,675', 'https://thumbnails.trvl-media.com/8hys69DaSuteA4B-6oJEKnBcGQw=/1200x800/smart/images.trvl-media.com/hotels/9000000/8830000/8821700/8821682/4dca0f0e_w.jpg', '4.3/5', 'Excellent', '6'], [7, 'OYO 6325 Hotel Kiran', 'Viewed', '2,804', 'https://thumbnails.trvl-media.com/DoPpGnIU3jgNRULoofWCN7sUdzs=/1200x800/smart/images.trvl-media.com/hotels/24000000/23180000/23172200/23172134/22d0d28b_w.jpg', '5/5', 'Excellent', 449], [8, 'Hotel Piccadily Raipur', 'Viewed', '3,284', 'https://thumbnails.trvl-media.com/DFBMUSlCUtkYhBuVp3SWopCLIuc=/1200x800/smart/images.trvl-media.com/hotels/37000000/36690000/36690000/36689993/859392c2_w.jpg', '5/5', 'Excellent', 197], [9, 'iStay Hotels Raipur Junction', 'Viewed', '2,101', 'https://thumbnails.trvl-media.com/V3K6ozgA5LMAzaLnoTDpQCAhe9k=/1200x800/smart/images.trvl-media.com/hotels/18000000/17790000/17786800/17786798/738d97a8_w.jpg', '4.0/5', 'Very Good', '1'], [10, 'Hotel Venkatesh International', 'Viewed', '50,000', 'https://thumbnails.trvl-media.com/cZNxlWjUVTHTH53ZkqXn9FBqPNU=/1200x800/smart/images.trvl-media.com/hotels/38000000/37110000/37103400/37103360/041a91e0_w.jpg', '4/5', 'Very Good', 205], [11, 'Clarks Inn suites Raipur', 'Viewed', '5,300', 'https://thumbnails.trvl-media.com/nuf_yMBMv1CGfk9_Uvc8Brj93PQ=/1200x800/smart/images.trvl-media.com/hotels/36000000/35880000/35879700/35879613/944d39d0_w.jpg', '5/5', 'Very Good', '1'], [12, 'Hotel Grand Rajputana', 'Viewed', '2,499', 'https://thumbnails.trvl-media.com/f-7bovMMjzUI5aAU7pMpQOiLWSU=/1200x800/smart/images.trvl-media.com/hotels/20000000/19940000/19935400/19935311/ba1868eb_w.jpg', '5/5', 'Very Good', 416], [13, 'Landmark Hotel', 'Viewed', '2,850', 'https://thumbnails.trvl-media.com/JwSsRk474eP9RO7Ji9fcz4Z2c8s=/1200x800/smart/images.trvl-media.com/hotels/38000000/37630000/37625300/37625256/168d14c7_w.jpg', '5/5', 'Very Good', 1466], [14, 'SPOT ON 37254 Hotel Krishna', 'Viewed', '914', 'https://thumbnails.trvl-media.com/RxT1Rj2ajlMVDEd_f7ynSlzZkY8=/1200x800/smart/images.trvl-media.com/hotels/43000000/42580000/42573200/42573199/0a6469d7_w.jpg', '4/5', 'Very Good', 846], [15, 'Le ROI Raipur', 'Viewed', '1,999', 'https://thumbnails.trvl-media.com/UjrFjmyDivsmGEeCKV4tBrYmLlo=/1200x800/smart/images.trvl-media.com/hotels/11000000/10990000/10984200/10984119/77ef0366_w.jpg', '4.3/5', 'Excellent', '7'], [16, 'Mayfair Lake Resort', 'Viewed', '7,000', 'https://thumbnails.trvl-media.com/0DrbcEqNYmcSVq61OEzqVsl9Fds=/1200x800/smart/images.trvl-media.com/hotels/34000000/33800000/33797900/33797883/f171c84b_w.jpg', '5/5', 'Excellent', 1177], [17, 'OYO 27933 Hotel Green Valley', 'Viewed', '3,281', 'https://thumbnails.trvl-media.com/MbRwphfqMnsE2qT8_9MhpFP0gcE=/1200x800/smart/images.trvl-media.com/hotels/41000000/40160000/40152100/40152028/0bf2efc1_w.jpg', '5/5', 'Excellent', 174], [18, 'Hotel Shamrock', 'Viewed', '2,600', 'https://images.trvl-media.com:443/hotels/4000000/3500000/3494500/3494475/372180e0_y.jpg', '3.7/5', 'Good', '6'], [19, 'Hotel Aditya', 'Viewed', '2,189', 'https://thumbnails.trvl-media.com/qvCk_UF2Gd5b4mv_Cer0FteqGT8=/1200x800/smart/images.trvl-media.com/hotels/36000000/35180000/35170600/35170506/aa16ec26_w.jpg', '5/5', 'Good', 943]]
    print(dtoday)
    return render_template('hotelsearch.html', dtoday = dtoday, row=row, inday=checkin, outday=checkout,place=destination)

@app.route('/hoteldescription',methods = ['POST', 'GET'])
def hoteldescription():
    hotelid =  str(request.args.get('hotelid'))
    print(hotelid)
    hotelid=int(hotelid)
    global a
    row=hotelDetail(a[hotelid][8])
    print(row)
    return render_template('hoteldescription.html')

@app.route('/trainhistory',methods = ['POST', 'GET'])
@login_required
def trainhistory():
    with sqlite3.connect('app/site.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ordertrains WHERE userid="+str(current_user.id))
        row=cur.fetchall()
    b=[] 
    for j in row:  
        i=extractFlight(j[2]) 
        b.append(i)
    return render_template('trainhistory.html',row=b)


