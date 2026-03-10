import os

import smtplib
from smtplib import SMTP
import time 
from utils import connect_to_email_client, parse_email
from get_directions import get_route_steps

def open_sms_protocol(email_address, app_key) -> SMTP:
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(email_address, app_key)
    return smtp

def send_sms(email_address, phone_address, message_subject, message_body, smtp):
    smtp.sendmail(email_address, phone_address, f'Subject: {message_subject}\n{message_body}')
    smtp.quit()

def fetch_emails(username, password, command_id_string):
    emails = []
    mail = connect_to_email_client(username, password)
    res, data = mail.search(None, f'(TEXT {command_id_string})')
    if res == 'OK':
        message_ids = data[0].split()
        for message_id in message_ids:
            res, message = mail.fetch(message_id, "(RFC822)")
            from_, subject, body = parse_email(message, command_id_string)
            emails.append((message_id, body))
    mail.logout()
    return emails

def listen_for_emails(email_address, phone_address, app_key, command_id_string, maps_api_key):
    email_ids = set()
    while True:
        print("Polling email...")
        messages = fetch_emails(email_address, app_key, command_id_string)
        for message_id, message_body in messages:
            if message_id not in email_ids:
                email_ids.add(message_id)
                # send along email body
                if f"command:" in message_body:
                    command = message_body.split('command:')[-1]
                    origin, destination = command.split('-->')
                    directions = get_route_steps(origin_address=origin, destination_address=destination, maps_api_key=maps_api_key)
                    try:
                        smtp = open_sms_protocol(email_address, app_key)
                        send_sms(email_address, phone_address, "New directions from HQ: ", directions, smtp)
                    except Exception as e:
                        print(e)
        time.sleep(60)