#Setup:
1. Clone repository:
git clone https://github.com/Michael-D-Johnson/Mdb.git

2. Obtain Google application credentials. This is for downloading initial
members spreadsheet from Google Sheets.
       https://developers.google.com/identity/protocols/OAuth2

3. Add following variables to environment
        MDB_DIR # directory to repository
        MDB_CONFIG # full path to config file
        MDB_SERVER # ip address used by flask
        GOOGLE_APPLICATION_CREDENTIALS # full path to google credentials json file
        MAIL_USERNAME
        MAIL_PASSWORD

4. Setup db:
       python bin/create_db.py

5. Download initial spreadsheet and update db:
       bin/bulk.py

6. Update db:
       bin/run_update.py

7. Run flask:
       python run_server.py
