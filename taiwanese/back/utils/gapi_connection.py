from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from oauth2client import file
from httplib2 import Http


def get_gapi_cred(cred_path, scopes=None):
    """
    Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    :param cred_path: str. indicate the location of credentials
           (the folder that includes token.pickle or credentials.json)
    :return:
    """
    if not scopes:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.compose",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
            'https://www.googleapis.com/auth/documents.readonly'
        ]
    elif not isinstance(scopes, dict):
        raise TabError("scopes have to be aggregated into a dictionary.")
    else:
        SCOPES = scopes

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('{}/token.pickle'.format(cred_path)):
        with open('{}/token.pickle'.format(cred_path), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '{}/credentials.json'.format(cred_path), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('{}/token.pickle'.format(cred_path), 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_drive_service(cred_path):
    creds = get_gapi_cred(cred_path)
    dservice = build('drive', 'v3', credentials=creds)

    return dservice


def get_sheet_service(cred_path):
    creds = get_gapi_cred(cred_path)
    sservice = build('sheets', 'v4', credentials=creds)

    return sservice


def get_calendar_service(cred_path):
    creds = get_gapi_cred(cred_path)
    dservice = build('calendar', 'v3', credentials=creds)

    return dservice


def get_mail_service(cred_path):
    creds = get_gapi_cred(cred_path)
    mservice = build('gmail', 'v1', credentials=creds)

    return mservice


def get_doc_service(cred_path):
    store = file.Storage('{}/token.json'.format(cred_path))
    creds = store.get()
    http = creds.authorize(Http())
    DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
    docs_service = build(
        'docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)

    return docs_service


if __name__ == "__main__":
    pass
