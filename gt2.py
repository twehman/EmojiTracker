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
ej2 = '😂'
ej3 = '❤️'

use = db.execute("SELECT count(*) body, month, sum(case when body LIKE '%' || :ej || '%' then 1 else 0 end) AS Kisses, sum(case when body LIKE '%' || :ej2 || '%' then 1 else 0 end) AS Laughs, sum(case when body LIKE '%' || :ej3 || '%' then 1 else 0 end) AS Hearts from texts1 GROUP BY month", ej=ej, ej2=ej2, ej3=ej3)
df = pd.DataFrame(use, columns=['body','month', 'Kisses', 'Laughs', 'Hearts'])
print(df.index)
print(df)
x = df['month']
y1 = df['Kisses']
y2 = df['Laughs']
y3 = df['Hearts']

y = np.vstack([y1, y2, y3])

labels = ["Kisses", "Laughs", "Hearts"]

fig, ax = plt.subplots()
ax.stackplot(x, y1, y2, y3, labels=('Kisses', 'Laughs', 'Hearts'))
ax.legend(labels)
plt.show()
fig, ax = plt.subplots()
ax.stackplot(x, y)
plt.show()
plt.savefig('test6.jpg')