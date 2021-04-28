#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def reminder_no(receiver_email, message):

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "earthtreksreminders@gmail.com"
    password = "jprctklwbhmphjtn"
    
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
        
def reminder(receiver_emails, param):
    
    for receiver_email in receiver_emails:
    
        sender_email = "earthtreksreminders@gmail.com"
        password = "jprctklwbhmphjtn"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Sign-Up Reminder"
        message["From"] = sender_email
        message["To"] = receiver_email
        
        if param['slots'] == 1:
            # Create the plain-text and HTML version of your message
            text = (
                'There is 1 spot available at {0} on {1}.\n'
                'If you did not sign-up, would you like to keep looking? Yes.'
                '\n\nThis message was sent from Python.').format(param['loc'],
                                                                 param['time']
                                                                 )
            html = ("""\
            <html>
              <body>
                <p>There is 1 spot available at {0} on {1}.</p>
                <p>If you did not sign-up, would you like to keep looking?</p>
                   <b><a href="https://earth-treks.herokuapp.com">Yes</a><br>
                   </b>
              </body>
            </html>
            """).format(param['loc'], param['time'])
        elif param['slots'] > 1:
            # Create the plain-text and HTML version of your message
            text = ('There are {0} spots available at {1} on {2}.\nIf '
                    'you did not sign-up would you like to keep looking? Yes.'
                    '\n\nThis message was sent from Python.').format(
                                                                param['slots'], 
                                                                param['loc'],
                                                                param['time'])
            html = ("""\
            <html>
              <body>
                <p>There are {0} spots available at {1} on {2}.</p>
                <p>If you did not sign-up, would you like to keep looking?</p>
                   <b><a href="https://earth-treks.herokuapp.com">Yes</a><br>
                   </b>
              </body>
            </html>
            """).format(param['slots'], param['loc'], param['time'])
            
        elif param['slots'] == 0:
            # Create the plain-text and HTML version of your message
            text = ('Sorry! It looks like no spots opened up for you at {0} on'
                    '{1}.\n'
                    'If you would like to try a new date please click here.'
                    '\n\nThis message was sent from Python.').format(                                                                
                                                                param['loc'],
                                                                param['time'])
            html = ("""\
            <html>
              <body>
                <p>Sorry! It looks like no spots opened up for you at {0} on
                {1}.
                </p>
                <p>If you would like to try a new date please click?</p>
                   <b><a href="https://earth-treks.herokuapp.com">here</a><br>
                   </b>
              </body>
            </html>
            """).format(param['loc'], param['time'])
        
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
