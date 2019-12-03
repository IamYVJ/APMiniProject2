import smtplib
import email.message
# from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path, PureWindowsPath

class EmailClass():

    def getPath(s):
        filename = PureWindowsPath(s)
        correct_path = Path(filename) # Convert path to the right format for the current operating system
        return(correct_path)

    def sendEmail(fullname, receipt_id, order_details):

        # ordermsg = ""
        total = 0.0
        for i in range(0, len(order_details)-1):
            # ordermsg = ordermsg + str(i[0]) + ", "
            total = total + float(order_details[i][1])*float(order_details[i][2])
        # ordermsg = ordermsg + "and " + order_details[-1][0] + "."
        total = total + (float(order_details[-1][1])*float(order_details[-1][2]))
        message = """Hey {a}! <br> <br>
                    Your order is Confirmed! <br> <br>
                    Your Order Total is Rs. {c} <br> <br>
                    For more details, please log onto our website. <br> <br>
                    Thank you for choosing <i> QuadCore.com </i> <br> <br>
                    Sincerely, <br>
                    <b>QuadCore Systems</b>""".format(a=fullname, c = str(total))
        # message = message.encode('utf-8').strip()
        msg = email.message.Message()
        msg['Subject'] = '[QuadCore.com] Order Confirmed!'
        msg['From'] = "systems.quadcore@gmail.com"
        msg['To'] = receipt_id
        msg.add_header('Content-Type','text/html')
        msg.set_payload(message)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("systems.quadcore@gmail.com",
                "Quadcore00")
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()

    def sendEmailTrain(traindata, pnr):
        # Send an HTML email with an embedded image and a plain text message for
        # email clients that don't want to display the HTML.



        # Define these once; use them twice!
        strFrom = 'systems.quadcore@gmail.com'
        strTo = traindata["passengerDetails"]["emailID"]

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = '[QuadCore] Train Booking Confirmed!'
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)

        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText('Dear ' + traindata["passengerDetails"]["firstName"] + ',  <br> <br> Your booking has been confirmed! <br> <br> <b> PNR: ' + pnr +' </b><br><br> <b>Travel Details:</b> <br> Train Name: '+ traindata["trainName"]+ ' <br> Train No: ' + traindata["trainNo"] + '<br> Departure Station: ' + traindata["departureStnCode"]+'<br> Departure Station Name: ' + traindata["departureStn"] +' <br> Departure City: ' + traindata["departureCity"]+ '<br>Departure Time: ' + traindata["departureTime"] + '<br> Departure Date: ' + traindata["departureDate"] + '<br>Arrival Station: ' + traindata["arrivalStnCode"] +'<br> Arrival Station Name: ' + traindata["arrivalStn"] + ' <br> Arrival City: ' + traindata["arrivalCity"] + '<br>Arrival Time: ' + traindata["arrivalTime"] + '<br> Duration: ' + traindata["duration"] +'<br>Class: ' + traindata["classes"]["className"]  + '<br> Fare: Rs' + traindata["classes"]["price"]  + ' <br><br> <b>Passenger Details:</b> <br> Passenger Name: ' + traindata["passengerDetails"]["title"]+ " " + traindata["passengerDetails"]["firstName"] + " " + traindata["passengerDetails"]["lastName"] + '<br> Email ID: ' + traindata["passengerDetails"]["emailID"]  +' <br> Phone No: ' + traindata["passengerDetails"]["phoneNo"] + '<br> <br> Use this QR code to get all your travelling information on the go! <br><br> <img src="cid:image2"> <br><br> We hope you have a great trip! <br> <br> Thank you for choosing <i> QuadCore.com </i> <br> <br> Sincerely, <br><b>QuadCore Systems</b> <br><br> <img src="cid:image1">', 'html')
        msgAlternative.attach(msgText)


        #LOGO
        # This example assumes the image is in the current directory
        fp = open(getPath("app\static\QuadCoreLogo\LogoWW.png"), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)


        #QR CODE
        # This example assumes the image is in the current directory
        fp = open(getPath("app\static\QR\\" + pnr +  ".png"), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image2>')
        msgRoot.attach(msgImage)



        # Send the email (this example assumes SMTP authentication is required)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("systems.quadcore@gmail.com",
                "Quadcore00")
        s.sendmail(strFrom, strTo, msgRoot.as_string())
        s.quit()

def getPath(s):
    filename = PureWindowsPath(s)
    correct_path = Path(filename) # Convert path to the right format for the current operating system
    return(correct_path)

# traindata ={'trainName': 'JNANESWARISUPDL', 'trainNo': '#12102', 'days': 'S   M   W   T', 'departureTime': '10:50 PM  Thu', 'depStnInfo': 'HWHYou searched for trains departing from HWH(Kolkata), but this train departs from HWH (Howrah Jn)HWH HWH RHowrah Jn', 'duration': '12h 25m', 'arrivalTime': '11:15 AM  Fri', 'arrStnInfo': 'RYou searched for trains arriving in R (Raipur), but this train arrives in R (Raipur Jn).R HWH RRaipur Jn', 'classes': {'className': '2 Tier AC', 'price': '1675', 'availability': 'PQWL 22', 'update': 'Updated 8 hrs ago'}, 'departureCity': 'Kolkata', 'departureStnCode': 'HWH', 'departureStn': 'Howrah Junction', 'arrivalCity': 'Raipur Junction', 'arrivalStnCode': 'R', 'arrivalStn': 'Raipur Junction', 'departureDate': '05-12-2019', 'arrivalDate': '', 'passengerDetails': {'title': 'Mr.', 'firstName': 'Yash', 'lastName': 'Burad', 'emailID': 'yash.burad_ug21@ashoka.edu.in', 'phoneNo': '8435966001'}}
# EmailClass.sendEmailTrain(traindata, "DP7ZQ2Q6")
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# EmailClass.sendEmail("Sai Khurana", "sai.khurana_ug21@ashoka.edu.in", "Casio Watch")
