import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")
data=data[['eventID ', 'case Spend area text', 'case Company',
       'case Document Type', 'case Sub spend area text',
       'case Purchasing Document', 'case Purch. Doc. Category name',
       'case Vendor', 'case Item Type', 'case Item Category',
       'case Spend classification text', 'case Name',
       'case GR-Based Inv. Verif.', 'case Item', 'case concept:name',
       'case Goods Receipt', 'event User',
       'event concept:name', 'event Cumulative net worth (EUR)',
       'event time:timestamp']]

data['event time:timestamp']=pd.to_datetime(data['event time:timestamp'], format= '%d-%m-%Y %H:%M:%S.%f')


len(data[data['event time:timestamp']<pd.datetime(2010,1,1)])
len(data[data['event time:timestamp']>pd.datetime(2019,3,1)])
# some clumns have whitespaces in keywords - remove them:
data.columns = data.columns.str.strip()
# Chapter: MISSING VALUES
missing_vars = ['case Spend area text',
                'case Sub spend area text', 'case Spend classification text']

# Fill missing case variables pertaining to case
data = data.fillna("Other")
data





# Chapter: EXPLORATORY DATA ANALYSIS
# stats for numeric vars

data[["case Spend classification text","case concept:name"]].groupby("case concept:name").describe()

data.columns
purchdoc = data.groupby('case Purchasing Document')
draft = purchdoc['case GR-Based Inv. Verif.'].nunique()
draft.value_counts()


Index(['eventID', 'case Spend area text', 'case Company', 'case Document Type',
       'case Sub spend area text', 'case Purchasing Document',
       'case Purch. Doc. Category name', 'case Vendor', 'case Item Type',
       'case Item Category', 'case Spend classification text',
       'case Name', 'case GR-Based Inv. Verif.', 'case Item',
       'case concept:name', 'case Goods Receipt', 'event User', 'event concept:name',
       'event Cumulative net worth (EUR)', 'event time:timestamp'],
      dtype='object')


data.columns
purchdoc_item_counts=data[['case Item','case Purchasing Document']].groupby('case Purchasing Document').nunique()['case Item']

data.groupby('case Purchasing Document').nunique().max()
data.groupby('case concept:name').nunique().max()

purchdoc_item_counts[purchdoc_item_counts==purchdoc_item_counts.max()] #purchasing document 4508073932 has 429 purchase items

purchdoc_item_counts[purchdoc_item_counts>purchdoc_item_counts.quantile(0.999)].describe() #even when looking at the 0.1% of purchdocs with the most items, still 75% of these cases has less than 131 purchdoc_item_counts

data[data['case Purchasing Document']==purchdoc_item_counts[purchdoc_item_counts==purchdoc_item_counts.max()].index[0]]
