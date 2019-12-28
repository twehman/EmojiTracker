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
ej3 = '❤'
ej4 = '😉'
ej5 = '😍'
ej6 = '🤣'
ej7 = '👍'

use = db.execute("SELECT count(*) body, month, sum(case when body LIKE '%' || :ej || '%' then 1 else 0 end) AS Kisses, sum(case when body LIKE '%' || :ej2 || '%' then 1 else 0 end) AS Laughs, sum(case when body LIKE '%' || :ej3 || '%' then 1 else 0 end) AS Hearts, sum(case when body LIKE '%' || :ej4 || '%' then 1 else 0 end) AS Winks, sum(case when body LIKE '%' || :ej5 || '%' then 1 else 0 end) AS HeartEyes, sum(case when body LIKE '%' || :ej6 || '%' then 1 else 0 end) AS ROFL, sum(case when body LIKE '%' || :ej7 || '%' then 1 else 0 end) AS ThumbsUp from texts1 GROUP BY month", ej=ej, ej2=ej2, ej3=ej3, ej4=ej4, ej5=ej5, ej6=ej6, ej7=ej7)
df = pd.DataFrame(use, columns=['body','month', 'Kisses', 'Laughs', 'Hearts', 'Winks', 'HeartEyes', 'ROFL', 'ThumbsUp'])
print(df.index)
print(df)
plt.figure(figsize=[9, 7])
ax1 = sns.lineplot(df['month'], df['Kisses'], label='Kisses', linewidth=2)
ax2 = sns.lineplot(df['month'], df['Laughs'], label='Laughs', linewidth=2)
ax3 = sns.lineplot(df['month'], df['Hearts'], label='Hearts', linewidth=2)
ax4 = sns.lineplot(df['month'], df['Winks'], label='Winks', linewidth=2)
ax5 = sns.lineplot(df['month'], df['HeartEyes'], label='Heart Eyes', linewidth=2)
ax6 = sns.lineplot(df['month'], df['ROFL'], label='ROFL', linewidth=2)
ax7 = sns.lineplot(df['month'], df['ThumbsUp'], label='Thumbs Up', linewidth=2)
sns.set_context("talk")
plt.ylabel('Number Used')
plt.xlabel('Month')
plt.xticks(np.arange(min(df['month']), max(df['month'])+1, 1.0))
plt.legend(title='Emoji:')
sns.despine()
plt.savefig('test4.jpg')