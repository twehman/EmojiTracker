import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from sqlalchemy import *
from cs50 import SQL
from datetime import datetime
from helpers import rowid

db = SQL("sqlite:///texts1.db")

sns.set(font_scale=1.5, style="whitegrid")

engine = create_engine('sqlite:///texts1.db', echo=True)

conn = engine


ej = '😘'
use = db.execute("SELECT COUNT(body) AS use_rate, month AS month from texts1 where body LIKE '%' || :ej || '%' GROUP BY month", ej=ej)
print(use)
df = pd.DataFrame(use, columns=['use_rate', 'month'])
print(df)

g = sns.FacetGrid(df, palette=None, height=10)
g.map(plt.scatter, "month", "use_rate", s=50, alpha=.7, linewidth=.5, edgecolor="white")
g.add_legend();

plt.savefig('test1.jpg')