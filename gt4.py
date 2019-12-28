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
ej = 'https'
use = db.execute("SELECT count(*) body, month, sum(case when body LIKE '%' || :ej || '%' then 1 else 0 end) AS Kisses FROM texts1 GROUP BY month", ej=ej)
df = pd.DataFrame(use, columns=['body', 'month', 'Kisses'])
print(df.index)
print(df)
plt.figure(figsize=[9, 7])
ax1 = sns.lineplot(df['month'], df['Kisses'], label='Kisses', linewidth=2)
sns.set_context("talk")
plt.ylabel('Number Used')
plt.xlabel('Month')
plt.xticks(np.arange(min(df['month']), max(df['month'])+1, 1.0))
plt.legend(title='Emoji:')
sns.despine()
plt.savefig('test4.jpg')
image = url_for("static", filename="test4.jpg")
print (image)