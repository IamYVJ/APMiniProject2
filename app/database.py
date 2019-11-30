import sqlite3

#Open database
conn = sqlite3.connect('/Users/raj.burad7/Desktop/APMiniProject2/app/site.db')

#Create table
c=conn.cursor()

# conn.execute("ALTER TABLE user ADD type TEXT ")
# conn.execute('''CREATE TABLE ordertrains
# 		(userid INTEGER ,
# 		orderid INTEGER PRIMARY KEY,
# 		details TEXT,
# 		qrcode TEXT,
# 		pnr TEXT 
# 		)''')

# a={'flightID': 'DELIDR6E503820191215IDRRPR6E25220191215_6EAPI', 'xmlKey': '6EAPI', 'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'totalStops': '1', 'totalDuration': '07:25', 'totalLayover': '04:45', 'airline': '', 'airlineCode': '', 'vehicleCode': '', 'flightNo': '', 'departureCityCode': '', 'arrivalCityCode': '', 'departureDate': '', 'arrivalDate': '', 'departureTime': '', 'arrivalTime': '', 'aircraft': '', 'departureTerminal': '', 'arrivalTerminal': '', 'mealCost': '', 'baseFare': '6091', 'totalFare': '7241', 'px': 'ADT', 'qt': '1', 'fuelSurcharge': '1150', 'PSF': '0', 'userDevelopmentFee': '0', 'goodsAndServiceTax': '0', 'GAST': '0', 'swachhBharatCess': '0', 'krishiKalyanCess': '0', 'cuteFee': '0', 'airportArrivalTax': '0', 'developmentFee': '0', 'otherFlightsInfo': [{'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'airline': 'IndiGo', 'airlineCode': '6E', 'vehicleCode': '6E', 'flightNo': '5038', 'departureCityCode': 'DEL', 'arrivalCityCode': 'IDR', 'departureDate': '2019-12-15', 'arrivalDate': '2019-12-15', 'departureTime': '09:10', 'arrivalTime': '10:35', 'aircraft': 'Airbus A320-100', 'departureTerminal': 'T-3', 'arrivalTerminal': '', 'mealCost': 'Paid Meal'}, {'baggageAllowance': '15 kgs', 'classtype': 'Economy', 'airline': 'IndiGo', 'airlineCode': '6E', 'vehicleCode': '6E', 'flightNo': '252', 'departureCityCode': 'IDR', 'arrivalCityCode': 'RPR', 'departureDate': '2019-12-15', 'arrivalDate': '2019-12-15', 'departureTime': '15:20', 'arrivalTime': '16:35', 'aircraft': 'Airbus A320-100', 'departureTerminal': '', 'arrivalTerminal': '', 'mealCost': 'Paid Meal'}]}
# for i in a["otherFlightsInfo"]:
# 	print(i)
# print(a["otherFlightsInfo"][-1]["arrivalTime"])


a=['GITANJALI EX', '#12859', 'S   M   T   W   T   F   S', '11:35 PM  Sun', 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', '12h 55m', '12:30 PM  Mon', 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', [['Sleeper', '440', 'Booking not allowed', 'Updated 2 hrs ago'], ['3 Tier AC', '1165', 'RLWL 24', 'Updated 1 day ago'], ['2 Tier AC', '1660', 'RLWL 14', 'Updated 2 hrs ago']], 'R', 'Raipur', 'HWH', 'Kolkata']

a[8] = a[8][1]
print(a)

conn.close()


