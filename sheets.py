#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

spreadsheet_id = '1mAkAWTmLzxbU82rZotv1f6KL2fXLCPy09UNk2iIH4C0'
range_name = 'demo!A1:B'

def setup_api():
    """Setup the Google Sheets API"""

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return service

# Call the Sheets API
service = setup_api()
result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
        range=range_name).execute()
values = result.get('values', [])
