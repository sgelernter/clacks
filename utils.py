   

import imaplib
from imaplib import IMAP4_SSL
import email
from email.header import decode_header

def parse_email(data, command_id_string):
    for response_part in data:
        if isinstance(response_part, tuple):
            # Parse the message into an email object
            msg = email.message_from_bytes(response_part[1])

            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # If it's a bytes type, decode to str
                subject = subject.decode(encoding if encoding else "utf-8")

            # Decode the sender's email address
            from_ = msg.get("From")

            # If the email message is multipart
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" not in content_disposition:
                        # Get the email body
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True)
            else:
                # The email body is not multipart
                body = msg.get_payload(decode=True)
    # TODO: find better way to parse body/store key
    return from_, subject, body.decode().split(command_id_string)[1]

def connect_to_email_client(username, password) -> IMAP4_SSL:
    imap_server = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select('inbox')
    return mail