import smtplib
import os
SUBJECT="contact to solve your issue"
s = smtplib.SMTP('smtp.gmail.com',587)
def sendmail(TEXT,email):
    print("sorry we cant process your candidature")
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(#"entet the email id", "enter the password")
    Message  = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s.sendmail("heartdiseaseprediction2021@gmail.com", email, Message)
    s.quit()
