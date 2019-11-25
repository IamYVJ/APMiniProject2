import smtplib
import email.message
# from threading import Thread

class EmailClass():
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

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# EmailClass.sendEmail("Sai Khurana", "sai.khurana_ug21@ashoka.edu.in", "Casio Watch")
