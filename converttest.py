from cs50 import SQL
from sqlalchemy import *
from helpers import date_convert
from datetime import datetime

db = SQL("sqlite:///texts1.db")

file = open('convert.txt', 'w')
for line in file:
    datetime.strptime("file", "%b %d, %Y %I:%M:%S %p")