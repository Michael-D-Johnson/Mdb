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
con.download_spreadsheet("CUAS Members","Form Responses",path=output_path)

# Use most recent sheets on filesystem 
files = sorted(os.listdir(output_path))
latest_member = [m for m in files if m.startswith("CUAS")][-1]
latest_form = [f for f in files if f.startswith("Form")][-1]
# Need to delete earlier versions of sheets after too many being downloaded

# Convert csv into df and transform for DB insert 
form_csvfile = os.path.join(output_path,latest_form)
members_csvfile = os.path.join(output_path,latest_member)

df_form = transform_form(form_csvfile)
df_members = transform_members(members_csvfile)

# Bulk upload of csv into database. For initial dump
db_functions.bulk_member_upload(df_members,db)
db_functions.bulk_form_upload(df_form,db)
