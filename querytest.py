from cs50 import SQL
from sqlalchemy import *
def total_use(emoji, s_o_r):
    db = SQL("sqlite:///texts1.db")
    emoji = emoji
    count = db.execute("SELECT COUNT(contact_name) FROM texts1 WHERE body LIKE '%' || :emoji || '%' and type = :s_o_r", emoji=emoji, s_o_r=s_o_r )
    return count