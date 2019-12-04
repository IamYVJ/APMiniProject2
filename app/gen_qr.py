import pyqrcode
from PIL import Image
# from app.OSDetect import osDetect
from pathlib import Path, PureWindowsPath

# def genQR(user_id, pnr,firstname, lastname, departure, arrival, flight_duration, departure_time, arrival_time, date):
#     scale = 20
#     final_str = 'PNR: ' + str(pnr) + '     Date: ' + str(date) + '\nName: '   + str(firstname) + ' '  + str(lastname) + '\nFrom: '  + str(departure) + '     To: ' + str(arrival) + '\nDeparture: ' + str(departure_time) + '     Arrival: ' + str(arrival_time) + '\nDuration: ' + str(flight_duration)
#     big_code = pyqrcode.create(final_str, mode='binary')
#     big_code.png('app/static/QR/' + pnr + '.png', scale=scale)
#     qrlogo("app/static/QR/" + pnr + ".png")
#     return

def genFlightQR(flightdata, pnr):
    scale = 20
    final_str = 'PNR: ' + pnr +'\nAirline: '+ flightdata["airline"]+ '    Flight No: ' + flightdata["flightNo"] + '\nDeparture: ' + flightdata["departureCityCode"]+ '    Arrival: ' + flightdata["arrivalCityCode"] +'\nDeparture Airport: ' + flightdata["departureAirport"] +'    Arrival Airport: ' + flightdata["arrivalAirport"] +'\nDeparture City: ' + flightdata["departureCity"]+ '    Arrival City: ' + flightdata["arrivalCity"] + '\nDeparture Time: ' + flightdata["departureTime"] + '    Arrival Time: ' + flightdata["arrivalTime"] + '\nDeparture Date: ' + flightdata["departureDate"]   + '    Arrival Date: ' + flightdata['arrivalDate'] + '\nDuration: ' + flightdata["totalDuration"] +'    Baggage Allowance: ' + flightdata['baggageAllowance']+'\nClass: ' + flightdata["classtype"]  + '   Fare: Rs' + flightdata["totalFare"]  + '\nPassenger Name: ' + flightdata["passengerDetails"]["title"]+ " " + flightdata["passengerDetails"]["firstName"] + " " + flightdata["passengerDetails"]["lastName"] + '\n\nThank you for choosing QuadCore.com'
    big_code = pyqrcode.create(final_str, mode='binary')
    big_code.png('app/static/QR/' + pnr + '.png', scale=scale)
    qrlogo("app/static/QR/" + pnr + ".png")
    return

def genTrainQR(traindata, pnr):
    scale = 20
    final_str = 'PNR: ' + pnr +'\nTrain Name: '+ traindata["trainName"]+ '    Train No: ' + traindata["trainNo"] + '\nDeparture Station: ' + traindata["departureStnCode"]+ '    Arrival Station: ' + traindata["arrivalStnCode"] +'\nDeparture: ' + traindata["departureStn"] +'    Arrival: ' + traindata["arrivalStn"] +'\nDeparture City: ' + traindata["departureCity"]+ '    Arrival City: ' + traindata["arrivalCity"] + '\nDeparture Time: ' + traindata["departureTime"] + '    Arrival Time: ' + traindata["arrivalTime"] + '\nDeparture Date: ' + traindata["departureDate"]   + '    Duration: ' + traindata["duration"] +'\nClass: ' + traindata["classes"]["className"]  + '   Fare: Rs' + traindata["classes"]["price"]  + '\nPassenger Name: ' + traindata["passengerDetails"]["title"]+ " " + traindata["passengerDetails"]["firstName"] + " " + traindata["passengerDetails"]["lastName"] + '\n\nThank you for choosing QuadCore.com'
    big_code = pyqrcode.create(final_str, mode='binary')
    big_code.png('app/static/QR/' + pnr + '.png', scale=scale)
    qrlogo("app/static/QR/" + pnr + ".png")
    return

# if __name__ == "__main__":
#     genQR('1' , 'Bombay' , 'New Delhi' , '48' , '14:40' , '17:00' ,'01-12-2019' ,'BOM-DEL', 5)
def getPath(s):
    filename = PureWindowsPath(s)
    correct_path = Path(filename) # Convert path to the right format for the current operating system
    return(correct_path)

# import pyqrcode

def qrlogo(qrPath):
    # url = pyqrcode.QRCode('http://www.eqxiu.com',error = 'H')
    # url.png('test.png',scale=20)
    im = Image.open(qrPath)
    im = im.convert("RGBA")
    logo = ""

    # syst = osDetect()
    #
    # if syst=='W':
    #     logo = Image.open(r'app\static\QuadCoreLogo\LogoWW.png')
    #
    # elif syst=='M':
    #     logo = Image.open(r'app/static/QuadCoreLogo/LogoWW.png')
    #
    # elif syst=='L':
    #     logo = Image.open(r'app/static/QuadCoreLogo/LogoWW.png')
    logo = Image.open(getPath("app\\static\\QuadCoreLogo\\LogoWW.png"))

    # box = (220,310,731,320)
    # im.crop(box)
    region = logo
    region = region.resize((1400, 220), 0)
    im.paste(region, (430, 1020) )
    # im.show()
    im.save(qrPath)
# qrlogo()
