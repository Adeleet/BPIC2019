import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")
#runs 7 mins:
#data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c", parse_dates= ['event time:timestamp'], infer_datetime_format = True)

#PREPROCES
# some clumns have whitespaces in keywords - remove them:
data.columns = data.columns.str.strip()

# Fill missing case variables pertaining to case
data = data.fillna("Other")

# Convert datetime strings to native datetime64[ns]
data['event time:timestamp'] = data['event time:timestamp'].apply(lambda t: pd.datetime(int(t[6:10]),int(t[3:5]),int(t[:2]),int(t[11:13]),int(t[14:16]),int(t[17:19])))

# Get 'case Purchasing Document' id's for docs that have events before 2015 & remove outliers
invalid_purchdocs = data[data['event time:timestamp'].apply(lambda t: t.year) < 2015]['case Purchasing Document'].unique()
data = data[~data['case Purchasing Document'].isin(invalid_purchdocs)]








purchdoc_item_counts=data[['case Item','case Purchasing Document']].groupby('case Purchasing Document').nunique()['case Item']
purchdoc_item_counts.describe()
purchdoc_item_counts[purchdoc_item_counts==purchdoc_item_counts.max()] #purchasing document 4508073932 has 429 purchase items
purchdoc_item_counts[purchdoc_item_counts>purchdoc_item_counts.quantile(0.999)] #purchasing document 4508073932 has 429 purchase items


#data[["case Spend classification text","case concept:name"]].groupby("case concept:name").describe()

purchdoc = data.groupby('case Purchasing Document')
purchdoc['case Name'].nunique()
