import os
import django
import sys
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from helpers import allowed_file, rowid, total_use, import_file, get_emoji, login_required, apology
import pandas as pd
from sqlalchemy import *
from datetime import timedelta, datetime
import threading
from multiprocessing import Process

UPLOAD_FOLDER = '/home/ubuntu/workspace/project/files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xml'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
character_set_server = 'utf8mb4'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Defines upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///texts1.db")

def data_purge():
    import time
    while True:
        access_times = db.execute("SELECT user_id, last_accessed from USERS")
        user_df = pd.DataFrame(access_times, columns=['user_id', 'last_accessed'])
        for rows in range(len(user_df)):
            x = int(user_df.user_id[rows])
            y = db.execute("SELECT last_accessed from users where user_id = :x", x=x)
            z = datetime.strptime(y[0]['last_accessed'], '%Y-%m-%d %H:%M:%S')
            diff = (datetime.now() - z)
            if diff > timedelta(minutes=5):
                db.execute("DELETE from texts1 where user_id = :x", x=x)
                cmd1 = 'static/' + 'test' + str(x) + '.jpg'
                cmd2 = 'files/' + str(x) + 'testupload.xml'
                cmd3 = str(x) + 'txts.csv'
                os.remove(cmd1)
                os.remove(cmd2)
                os.remove(cmd3)
        time.sleep(300)

p = Process(target=data_purge)
p.start()


@app.route("/register", methods=["GET", "POST"])
def register():
    un = request.form.get("username")
    pw = request.form.get("password")
    cn = request.form.get("confirmation")
    exists = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
    if request.method == "POST":
        if not un:
            return apology("must provide username", 400)
        elif not pw:
            return apology("must provide password", 400)
        elif pw != cn:
            return apology("password and confirmation must match!", 400)
        elif exists:
            return apology("that username already exists", 400)
        else:
            db.execute("INSERT INTO users(username, hash) VALUES(:un, :pw)",
                       un=request.form.get("username"), pw=generate_password_hash(request.form.get("password")))
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))
            session["user_id"] = rows[0]["user_id"]
            return redirect("/")
    if request.method == "GET":
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/", methods=["GET"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")



@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            concat_id = str(session["user_id"])
            uid = session["user_id"]
            filename = concat_id + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cmd = 'ruby test.rb' + ' ' + 'files/' + filename
            os.system(cmd)
            csvfilename = concat_id + 'txts.csv'
            import_file(csvfilename, uid)
        return render_template("results.html")
    if request.method == "GET":
        return render_template("upload.html")

@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    if request.method == "POST":
        ej = get_emoji(request.form.get("emoji_list"))
        if ej:
            userid = session["user_id"]
            concat_id = str(session["user_id"])
            print(ej)
            sns.set(font_scale=1.5, style="whitegrid")
            engine = create_engine('sqlite:///texts1.db', echo=True)
            conn = engine
            use = db.execute("SELECT count(*) body, month, sum(case when body LIKE '%' || :ej || '%' then 1 else 0 end) AS Emoji FROM texts1 WHERE user_id = :userid GROUP BY month", ej=ej, userid=userid)
            df = pd.DataFrame(use, columns=['body', 'month', 'Emoji'])
            print(df)
            plt.figure(figsize=[9, 7])
            ax1 = sns.lineplot(df['month'], df['Emoji'], label=request.form.get("emoji_list"), linewidth=2)
            sns.set_context("talk")
            plt.ylabel('Number Used')
            plt.xlabel('Month')
            plt.xticks(np.arange(min(df['month']), max(df['month'])+1, 1.0))
            plt.legend(title='Emoji:')
            sns.despine()
            plt.savefig('static/' + concat_id + 'test3.jpg')
            image = concat_id + 'test3.jpg'
            db.execute("UPDATE users SET last_accessed=DateTime('now') WHERE user_id = :userid", userid=userid)
            return render_template("results1.html", image=image)
    if request.method == "GET":
        return render_template("results.html")

@app.route("/check", methods=["GET"])
def check():
    un_exists = db.execute("SELECT username FROM users WHERE username = :username", username=request.args.get("username"))
    if un_exists:
        return jsonify(False)
    elif not un_exists:
        if len(request.args.get("username")) > 0:
            return jsonify(True)
        else:
            return jsonify(False)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
