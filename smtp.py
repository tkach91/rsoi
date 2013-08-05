#!/usr/bin/python

import sys
import base64

from smtplib import SMTP_SSL as SMTP
from email.MIMEText import MIMEText


smtp_port = 25
smtp_server = 'smtp.yandex.ru'

sender = 'rsoi100@yandex.ru'
destination = ['rsoi100@yandex.ru']

user = 'rsoi100@yandex.ru'
password = 'number2128506'

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


#with open("test.gif", "rb") as image_file:
#    content = base64.b64encode(image_file.read()) 

content = base64.b64encode('Content. Thats all\nInteresting things')

subject="Sent from Python"


try:
    msg = MIMEText(content, text_subtype)
    msg['Subject'] = subject
    msg['From'] = sender 
    # some SMTP servers will do this automatically, not all


    conn = SMTP(SMTPserver, 465)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()
        print "OK"

except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message
