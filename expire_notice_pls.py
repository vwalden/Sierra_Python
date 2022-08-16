#!/usr/bin/env python3

"""Produces and sends expiration warning e-mails to patrons whose cards expired 30 days ago

Author: Jeremy Goldstein (jgoldstein@minlib.net), based on code by Gem Stone-Logan, 2018
Edited for PLS by: Vanessa Walden (walden@plsinfo.org), 2022
"""

#Package to connect to PostgreSQL database
import psycopg2
#package to create CSV files
import csv
#packages to manipulate values in CSV files
import itertools
import operator
#packages to create and send email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
from email import encoders
from datetime import date
from dateutil.relativedelta import relativedelta

#Use file to gather stats for how many messages are generated each day
#Compare numbers with Expiring_Patrons.csv to see how many patrons renewed in the 30 day window

#Variables for the email that will be sent

emailhost = ''
emailport = ''
emailfrom= ''
emailsubject = 'Library Card Expiration Warning'

#Connect to Sierra PostgreSQL database with error reporting
try:
    conn = psycopg2.connect("dbname='' user='' host='' port='' password='' sslmode='require'")
except psycopg2.Error as e:
    print ("Unable to connect to database: " + str(e))

#Opening a session and querying the database for weekly new items
cursor = conn.cursor()
cursor.execute(open("expired_patrons.sql","r").read())
    
#For now, just storing the data in a variable. We'll use it later.
rows = cursor.fetchall()
conn.close()

#Sending the email message
smtp = smtplib.SMTP(emailhost, emailport)

for rownum, row in enumerate(rows):
	
    #Variable emailto can send to multiple addresses by separating emails with commas
    emailto = [str(row[3])]
    #Plain text email version
    text = '''Dear {} {} {},
     
    Your library card will expire on {}.  Renewing your card is easy: bring photo identification and proof of your current home address to any public library in San Mateo County. Library staff will renew your card in just a few minutes.

If you have any questions or are unable to come in, please email us at jurisdiction@plsinfo.org, call us at (650) XXX-XXXX or text us at (650) XXX-XXXX.

Please do not respond to this message. Replies will be delivered to an unmonitored mailbox. Thank You.'''.format(str(row[0]),str(row[1]),str(row[2]),str(row[5]))

    msg = MIMEMultipart('alternative')
    part1 = MIMEText(text,'plain')
    msg['From'] = emailfrom
    if type(emailto) is list:
        msg['To'] = ', '.join(emailto)
    else:
        msg['To'] = emailto
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = emailsubject
    msg.attach (part1)
    
    smtp.sendmail(emailfrom, emailto, msg.as_string())
    rownum+1

smtp.quit()
