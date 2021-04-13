from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

def init():
    SCOPES = ['https://www.googleapis.com/auth/documents']
    SERVICE_ACCOUNT_FILE = 'keys.json' # Change JSON Key File from (APIs & Services)
    global creds
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    global DOCUMENT_ID 
    DOCUMENT_ID = '8R1QFRlw&P!7oYk6daSTBq3BB?4?APwk'  # Change the Document ID

    global service
    service = build('docs', 'v1', credentials=creds)

    global docs
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()

    global doc_content
    doc_content = doc.get('body').get('content')

    #print(read_strucutural_elements(doc_content))
    index = 1
def startIndex():
    for value in doc_content:
        if 'paragraph' in value:
            index = value.get('startIndex') 
    return index
