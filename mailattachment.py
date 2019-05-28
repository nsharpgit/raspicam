#!/usr/bin/python
import sys
from os import path, access, R_OK  # W_OK for write permission
import string

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 
# My Vars
fromaddr = "XXXXXXXXXXX@XXXXXXXX.com"
passwd = "XXXXXXXXXXXXXXXXXX"
toaddr = "whoever@gmail.com"
 
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "From raspi"
body = "Motion Detected"


######################
#check number of arguments ( 1 = script name only)
if len(sys.argv) == 1:
        print "Supply attachment filepath as argument. Exiting..\n"
        exit(1)


msg.attach(MIMEText(body, 'plain'))
attnum=1
for PATH in sys.argv[1:]:
        #print "PATH = %s" % PATH
        if path.isfile(PATH) and access(PATH, R_OK):
                print "Attachment %d ok" % attnum
 
		filename = "image-%d.jpg" % attnum
		attachment = open(PATH, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)

	else:
		print "%s doesnt exist. Exiting..\n" % PATH
		exit(1)

	if ( attnum ==  (len(sys.argv) - 1) ):
		print "Sending message"
	else:
		attnum+=attnum



## Send mail 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, passwd )
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
