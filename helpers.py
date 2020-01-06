import os
import requests
import urllib.parse
import pandas as pd
from sqlalchemy import *
from flask import redirect, render_template, request, session
from functools import wraps

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xml'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rowid():
    row_val = db.execute("SELECT id from texts1 order by ROWID DESC limit 1")
    return row_val([0]["id"])


def total_use(emoji, s_o_r):
    db = SQL("sqlite:///texts1.db")
    emoji = emoji
    count = db.execute("SELECT COUNT(contact_name) FROM texts1 WHERE body LIKE '%' || :emoji || '%' and type = :s_o_r", emoji=emoji, s_o_r=s_o_r )
    return count

def import_file(file, uid):
    # read texts csv into a dataframe : texts1_df
    texts1_df = pd.read_csv(file, header=1)
    df = pd.DataFrame({'texts1_df' : ['protocol','address','date','type','subject','body','toa','sc_toa','service_center','read','status','locked','date_sent','readable_date','contact_name', 'month', 'user_id']})
    # rename the columns of the texts dataframe
    texts1_df.columns = ['protocol','address','date','type','subject','body','toa','sc_toa','service_center','read','status','locked','date_sent','readable_date','contact_name']
    date_columns = ['readable_date']
    texts1_df['readable_date'] = pd.to_datetime(texts1_df['readable_date'], format="%b %d, %Y %I:%M:%S %p")
    texts1_df['month'] = pd.to_datetime(texts1_df['readable_date'], format="%b %d, %Y %I:%M:%S %p").dt.strftime("%m")
    texts1_df['user_id'] = uid
    user_id = uid
    engine = create_engine('sqlite:///texts1.db', echo=True)
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
        'month': INTEGER,
        'user_id': INTEGER,
        })

def get_emoji(string):
    z = string
    x = {
    "grin": "😀",
    "eyesclosedgrin": "😄",
    "Crying Laughing": "😂",
    "❤": "❤",
    "hearteyes": "😍",
    "rofl": "🤣",
    "blushgrin": "😊",
    "kisses": "😘",
    }
    y = x[z]
    print(x[z])
    return y

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code