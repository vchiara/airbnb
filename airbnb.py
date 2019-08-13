import pandas as pd
from pandas.plotting import scatter_matrix
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

#set palette
airbnb_pal = ["#F16664","#FFF6E6","#79CCCD","#6BB7B9","#007D8C"]

calendar = pd.read_csv('calendar.csv')

calendar.describe()

#listing_id  minimum_nights  maximum_nights
#count  1.095501e+07    1.095501e+07    1.095501e+07
#mean   1.558958e+07    2.864251e+00    1.735882e+05
#std    9.877383e+06    1.122438e+01    1.825943e+07
#min    2.077000e+03    1.000000e+00    1.000000e+00
#25%    6.597128e+06    1.000000e+00    3.000000e+01
#50%    1.541572e+07    2.000000e+00    1.124000e+03
#75%    2.387418e+07    3.000000e+00    1.125000e+03
#max    3.291271e+07    3.650000e+02    2.147484e+09

print('There are', calendar.date.nunique(), 'days and', calendar.listing_id.nunique(), 'unique listings in the calendar data.')
#There are 366 days and 30013 unique listings in the calendar data.

calendar.date.min(), calendar.date.max()
#('2019-03-08', '2020-03-07')

calendar.available.value_counts()
#t    6980816
#f    3974196
#Name: available, dtype: int64

calendar.columns.values
#array(['listing_id', 'date', 'available', 'price', 'adjusted_price', 'minimum_nights', 'maximum_nights'], dtype=object)

#classify as available or busy
calendar_new = calendar[['date', 'available']]
calendar_new['busy'] = calendar_new.available.map(lambda x: 0 if x == 't' else 1)
calendar_new = calendar_new.groupby('date')['busy'].mean().reset_index()
calendar_new['date'] = pd.to_datetime(calendar_new['date'])
calendar_new

#%busy plot
sns.set_style("darkgrid")
busy_plot = sns.lineplot(x = "date", y = "busy", data = calendar_new, color = "#F16664")
busy_plot.set_title("Airbnb Rome Calendar")
plt.show()

#monthly price changes
calendar['price'] = calendar['price'].str.replace('$', '')
calendar['price'] = calendar['price'].str.replace(',', '')
calendar['price'] = pd.to_numeric(calendar['price'])
calendar['date'] = pd.to_datetime(calendar['date'])
avg_price = calendar.groupby(calendar['date'].dt.strftime('%m'))['price'].mean()

#average monthly price plot
avg_price_plot = sns.barplot(avg_price.index, avg_price.values, color = "#79CCCD")
avg_price_plot.set_title('Monthly Airbnb Prices in Rome', fontsize = 16, weight = 'bold')
avg_price_plot.set_xlabel('Month')
avg_price_plot.set_ylabel('Average Monthly Price')
avg_price_plot.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

#daily price changes
calendar['price'] = calendar['price'].str.replace('$', '')
calendar['price'] = calendar['price'].str.replace(',', '')
calendar['price'] = pd.to_numeric(calendar['price'])
calendar['date'] = pd.to_datetime(calendar['date'])
week_price = calendar.groupby(calendar['date'].dt.strftime('%w'))['price'].mean()

#average daily price plot
week_price_plot = sns.lineplot(week_price.index, week_price.values, color = "#007D8C")
week_price_plot.set_title('Daily Airbnb Prices in Rome', fontsize = 16, weight = 'bold')
week_price_plot.set_xlabel('Day of the Week')
week_price_plot.set_ylabel('Average Daily Price')
week_price_plot.set_xticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
plt.show()