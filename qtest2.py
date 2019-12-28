from cs50 import SQL
from sqlalchemy import *
from datetime import datetime

engine = create_engine('sqlite:///texts1.db', echo=True)
cursor = engine.connect()
db = SQL("sqlite:///texts1.db")

ej = '😘'
ej2 = '😂'
ej3 = '❤️'

x = db.execute("SELECT COUNT(body), month from texts1 where body LIKE '%' || :ej || '%' GROUP BY month", ej=ej)
y = db.execute("SELECT count(*) body, month, sum(case when body LIKE '%' || :ej || '%' then 1 else 0 end) AS Ej1Count, sum(case when body LIKE '%' || :ej2 || '%' then 1 else 0 end) AS Ej2Count, sum(case when body LIKE '%' || :ej3 || '%' then 1 else 0 end) AS Ej3Count from texts1 GROUP BY month", ej=ej, ej2=ej2, ej3=ej3)
print(x)
print(y)