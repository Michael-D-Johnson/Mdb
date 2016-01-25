#!/usr/bin/env python

import os
from gspread import authorize
from json import load
from oauth2client.client import GoogleCredentials
from csv import writer
from datetime import datetime

class GoogleConnect(object):
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        init_credentials = GoogleCredentials.get_application_default()
        credentials = init_credentials.create_scoped(scope)
        gc = authorize(credentials)
        self.gc = gc

    def download_spreadsheet(self,*spreadsheets,**kwargs):
        # Download given Google spreadsheet(s)
        for sheet in spreadsheets:
            worksheet = self.gc.open(sheet).get_worksheet(0)
            now=datetime.now()
            downloaded_csv="%s_%s.csv" % (sheet,now)
            if kwargs['path']:
                path = os.path.join(kwargs['path'],'')
                downloaded_csv = ''.join([path,downloaded_csv])
            write_csv = writer(open(downloaded_csv, 'wb'))
            write_csv.writerows(worksheet.get_all_values())

if __name__ == "__main__":
    jsonfile = os.getenv("JSON_FILE")
    output_path = "%s/sheets/" % os.getenv('MDB_DIR')
    con = GoogleConnect(jsonfile)
    con.download_spreadsheet("CUAS Members","Form Responses",path=output_path)
