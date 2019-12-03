import pyqrcode
from PIL import Image
from app.OSDetect import osDetect

def genQR(user_id, pnr,firstname, lastname, departure, arrival, flight_duration, departure_time, arrival_time, date):
    scale = 20
    final_str = 'PNR: ' + str(pnr) + '     Date: ' + str(date) + '\nName: '   + str(firstname) + ' '  + str(lastname) + '\nFrom: '  + str(departure) + '     To: ' + str(arrival) + '\nDeparture: ' + str(departure_time) + '     Arrival: ' + str(arrival_time) + '\nDuration: ' + str(flight_duration)
    big_code = pyqrcode.create(final_str, mode='binary')
    big_code.png('app/static/QR/' + pnr + '.png', scale=scale)
    qrlogo("app/static/QR/" + pnr + ".png")
    return



# if __name__ == "__main__":
#     genQR('1' , 'Bombay' , 'New Delhi' , '48' , '14:40' , '17:00' ,'01-12-2019' ,'BOM-DEL', 5)


# import pyqrcode

def qrlogo(qrPath):
    # url = pyqrcode.QRCode('http://www.eqxiu.com',error = 'H')
    # url.png('test.png',scale=20)
    im = Image.open(qrPath)
    im = im.convert("RGBA")
    logo = ""

    syst = osDetect()

    if syst=='W':
        logo = Image.open(r'app\static\QuadCoreLogo\LogoWW.png')

    elif syst=='M':
        logo = Image.open(r'app/static/QuadCoreLogo/LogoWW.png')

    elif syst=='L':
        logo = Image.open(r'app/static/QuadCoreLogo/LogoWW.png')


    # box = (220,310,731,320)
    # im.crop(box)
    region = logo
    region = region.resize((700, 110), 0)
    im.paste(region, (340, 640) )
    im.show()
    im.save(qrPath)
# qrlogo()
