#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

spreadsheet_id = '1mAkAWTmLzxbU82rZotv1f6KL2fXLCPy09UNk2iIH4C0'
range_ = 'demo'

def setup_api():
    """Setup the Google Sheets API"""

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    return service

def append_row(values=[], spreadsheet_id=spreadsheet_id, range_=range_):
    """Appends row to a spreadsheet.
    Input: values -- row's values as list (type: list).

    """

    service = setup_api()
    # How the input data should be interpreted
    value_input_option = 'RAW' # 'RAW' | 'USER_ENTERED'
    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS' # 'OVERWRITE' | 'INSERT_ROWS'
    body = {'values': [values], 'majorDimension': 'ROWS'}
    try:
        r = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                range=range_, valueInputOption=value_input_option,
                insertDataOption=insert_data_option, body=body).execute()
    except Exception as exception:
        return 1
    return r
