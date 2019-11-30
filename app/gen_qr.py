import pyqrcode

def genQR(user_id,pnr,firstname,lastname, departure,destination,flight_duration,departure_time,arrival_time,date,scale):
    final_str = str(user_id) + ':' + str(pnr) + ':'   + str(firstname) + ':'  + str(lastname) + ':'  + str(departure) + ':' + str(destination) + ':' + str(flight_duration) + 'hrs' + ':' + 'DEP ' + str(departure_time) + ':' + 'ARR ' +str(arrival_time) + ':' + str(date)
    big_code = pyqrcode.create(final_str, mode='binary')
    big_code.png('app/static/QR/' + pnr + '.png', scale=scale)
    return


# if __name__ == "__main__":
#     genQR('1' , 'Bombay' , 'New Delhi' , '48' , '14:40' , '17:00' ,'01-12-2019' ,'BOM-DEL', 5)

