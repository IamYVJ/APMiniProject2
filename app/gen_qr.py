import pyqrcode

def genQR(user_id, pnr,firstname, lastname, departure, arrival, flight_duration, departure_time, arrival_time, date, scale):
    final_str = 'PNR: ' + str(pnr) + '     Date: ' + str(date) + '\nName: '   + str(firstname) + ' '  + str(lastname) + '\nFrom: '  + str(departure) + '     To: ' + str(arrival) + '\nDeparture: ' + str(departure_time) + '     Arrival: ' + str(arrival_time) + '\nDuration: ' + str(flight_duration) 
    big_code = pyqrcode.create(final_str, mode='binary')
    big_code.png('app/static/QR/' + pnr + '.png', scale=scale)
    return


# if __name__ == "__main__":
#     genQR('1' , 'Bombay' , 'New Delhi' , '48' , '14:40' , '17:00' ,'01-12-2019' ,'BOM-DEL', 5)
