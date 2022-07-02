from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib import get_user_credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText
import base64

SCOPES = ['https://mail.google.com/']

class SendGmail:
    def __init__(self):
        self.creds = self.get_creds()
        self.service = build('gmail', 'v1', credentials=self.get_creds())

    def get_creds(self):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    
    def send_mail(self, to_email, from_email, subject, body):
        msg = MIMEText(body)
        msg["subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        
        raw = base64.urlsafe_b64encode(msg.as_bytes())
        raw= raw.decode()
        body = {'raw':raw}

        msg = (self.service.users().messages().send(userId='me', body=body).execute())
        print(msg)