#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:47:35 2021

@author: lucas
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import poplib
from email import parser


def reminder(receiver_email, message):

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "earthtreksreminders@gmail.com"
    password = "Barefoot3*"
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # Send email here
        for email in receiver_email:
            server.sendmail(sender_email, email, message)
            
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
        
def reminder2(receiver_emails, slots):
    
    for receiver_email in receiver_emails:
    
        sender_email = "earthtreksreminders@gmail.com"
        password = "Barefoot3*"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Sign-Up Reminder"
        message["From"] = sender_email
        message["To"] = receiver_email
        if type(slots) == str:
            # Create the plain-text and HTML version of your message
            text = ('There is 1 spot available on {}.'
                    '\nIf you did not sign-up would you like to keep looking? Yes.'
                    '\n\nThis message was sent from Python.').format(slots)
            html = ("""\
            <html>
              <body>
                <p>There is 1 spot available on {}
                   \nIf you did not sign-up, would you like to keep looking? 
                   <b><a href="mailto:earthtreksreminders@gmail.com">Yes.</a><br></b>
                </p>
              </body>
            </html>
            """).format(slots)
        else:
            # Create the plain-text and HTML version of your message
            text = ('There are {0} spots available on {1}.'
                    '\nIf you did not sign-up would you like to keep looking? Yes.'
                    '\n\nThis message was sent from Python.').format(slots[0], slots[1])
            html = ("""\
            <html>
              <body>
                <p>There are {0} spots available on {1}.
                   \nIf you did not sign-up, would you like to keep looking? 
                   <b><a href="mailto:earthtreksreminders@gmail.com">Yes.</a><br></b>
                </p>
              </body>
            </html>
            """).format(slots[0], slots[1])
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
def check_response():
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user('earthtreksreminders@gmail.com')
    pop_conn.pass_('Barefoot3*')
    #Get messages from server:
    resp, lines, octets = pop_conn.retr(1)
    msg_cont = b'\r\n'.join(lines).decode('utf-8')
    msg = parser.Parser().parsestr(msg_cont)
    sender = msg.get('From')
    print(sender)
    pop_conn.quit()
    
    if sender in ['lmcarneiro@smcm.edu', 'Ev.cebotari@gmail.com']:
        return 'Continue'
    else:
        return 'Quit'