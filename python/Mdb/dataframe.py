import pandas

def remove_columns(df):
    if "Add another family member?" in df.columns:
        df= df.drop(df.filter(regex="Add another family member?"),axis=1)
    if "Is this a family membership?" in df.columns:
        df = df.drop("Is this a family membership?",axis=1)
    if "Please let us know any comments or questions you might have." in df.columns:
        df = df.drop("Please let us know any comments or questions you might have.",axis=1)
    if "What type of membership are you interested in?" in df.columns:
        df = df.drop("What type of membership are you interested in?",axis=1)
    return df

def csv_to_df(csvfile):
	df = pandas.read_csv(csvfile)
	return df

def remove_lower_spaces(df):
    for key,value in df.iteritems():
        newkey = key.replace(' ','_').lower().strip()
        df=df.rename(columns = {key:newkey})
    return df

def rename_columns(df):
    replaced = {'1.':'first','2.':'second','3.':'third','4.':'fourth','5.':'fifth'}
    for key,value in df.iteritems():
        for num,word in replaced.iteritems():
            newkey = key.replace(num,word)
            df=df.rename(columns = {key:newkey})
    return df

def add_zero_to_paid(df):
    df['paid'] = df['paid'].fillna(False)
