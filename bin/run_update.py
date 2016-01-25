from Mdb import Mdb
from Mdb import db,models,db_functions,dataframe
from Mdb.googleconnect import GoogleConnect
import os
import sys

# Definitions 
output_path = Mdb.config['SHEETS_DIR']

# Defining workflow for transforming csvs
def transform_form(csvfile):
    df = dataframe.csv_to_df(csvfile)
    df = dataframe.remove_columns(df)
    df = dataframe.rename_columns(df)
    df = dataframe.remove_lower_spaces(df)
    dataframe.add_zero_to_paid(df)
    return df

def transform_members(csvfile):
    df = dataframe.csv_to_df(csvfile)
    df = dataframe.remove_columns(df)
    df = dataframe.rename_columns(df)
    df = dataframe.remove_lower_spaces(df)
    return df

# Download latest sheets 
con = GoogleConnect()
con.download_spreadsheet("Form Responses",path=output_path)

# Use most recent sheets on filesystem
files = sorted(os.listdir(output_path))
latest_member = [m for m in files if m.startswith("CUAS")][-1]
latest_form = [f for f in files if f.startswith("Form")][-1]
# Need to delete earlier versions of sheets after too many being downloaded

# Convert csv into df and transform for DB insert
form_csvfile = os.path.join(output_path,latest_form)
#members_csvfile = os.path.join(output_path,latest_member)

df_form = transform_form(form_csvfile)
#df_members = transform_members(members_csvfile)

# Check if member exists in csv but not in database
db_functions.does_form_exist_in_members(df_form)

# Check form_responses table to see if anyone is paid. If so, move them into 
#    members database. Delete them from form_responses.
db_functions.add_new_member()
db_functions.delete_from_form()

# Check if any memberships have expired 
db_functions.is_expired()

"""
as part of bulk upload, add expires/paid columns
X download
X grab latest
X check if any paid.
X move to members.
X delete from forms
X check if expired
X delete two weeks old expired.
X email those who're at two weeks.
remove rows from google spreadsheet form_members after adding to db?
add user profile page to update members information
how do I want users to login - openid or passwd table?
add new db table that joins to members table on email to store person's password
upload view of db on members side of website - use jinja2 html table
if i have joined foreign keys will it be easier to swap in members across tables that share key?
ask for confirmation of password upon changing
"""
