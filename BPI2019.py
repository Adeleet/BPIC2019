import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")
# some clumns have whitespaces in keywords - remove them:
data.columns = data.columns.str.strip()

# Chapter: MISSING VALUES
missing_vars = ['case Spend area text',
                'case Sub spend area text', 'case Spend classification text']

# Fill missing case variables pertaining to case
data = data.fillna("Other")


case_data = data.set_index("case concept:name")


# Chapter: EXPLORATORY DATA ANALYSIS
# stats for numeric vars

data[["case Spend classification text","case concept:name"]].groupby("case concept:name").describe()

data.columns
purchdoc = data.groupby('case Purchasing Document')
purchdoc['case Name'].nunique()
purchdoc.atom://teletype/portal/041734fc-7ffb-4e23-a6ee-c0450ece90e6




data.columns
purchdoc_item_counts=data[['case Item','case Purchasing Document']].groupby('case Purchasing Document').nunique()['case Item']


purchdoc_item_counts.describe()

purchdoc_item_counts[purchdoc_item_counts==purchdoc_item_counts.max()] #purchasing document 4508073932 has 429 purchase items

purchdoc_item_counts[purchdoc_item_counts>purchdoc_item_counts.quantile(0.999)] #purchasing document 4508073932 has 429 purchase items
