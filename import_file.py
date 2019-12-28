import pandas as pd
from cs50 import SQL
from sqlalchemy import *
from datetime import datetime
db = SQL("sqlite:///texts1.db")

engine = create_engine('sqlite:///texts1.db', echo=True)
# read census.csv into a dataframe : census_df
texts1_df = pd.read_csv("txts.csv", header=1)
df = pd.DataFrame({'texts1_df' : ['protocol','address','date','type','subject','body','toa','sc_toa','service_center','read','status','locked','date_sent','readable_date','contact_name', 'month']})
# rename the columns of the census dataframe
texts1_df.columns = ['protocol','address','date','type','subject','body','toa','sc_toa','service_center','read','status','locked','date_sent','readable_date','contact_name']
date_columns = ['readable_date']
texts1_df['readable_date'] = pd.to_datetime(texts1_df['readable_date'], format="%b %d, %Y %I:%M:%S %p")
texts1_df['month'] = pd.to_datetime(texts1_df['readable_date'], format="%b %d, %Y %I:%M:%S %p").dt.strftime("%m")
texts1_df.to_sql(name="texts1", con=engine, if_exists="append", index=False, chunksize=1000,
dtype={
    'protocol': BOOLEAN,
    'address': VARCHAR(length=20),
    'date': NVARCHAR(length=20),
    'type': INTEGER,
    'subject': TEXT,
    'body': TEXT,
    'toa': BOOLEAN,
    'sc_toa': BOOLEAN,
    'service_center': NVARCHAR(length=20),
    'read': BOOLEAN,
    'status': INTEGER,
    'locked': BOOLEAN,
    'date_sent': NVARCHAR(length=20),
    'readable_date': DateTime(),
    'contact_name': NVARCHAR(length=255),
    'month': INTEGER
    })