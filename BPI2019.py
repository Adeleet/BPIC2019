import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")

# this is the column which has exactly 251734 unique values

data['case concept:name'].unique().shape
data['case Purchasing Document'].unique().shape

data['event time:timestamp'].max()

data['case concept:name'].unique()[0]
data.groupby("case Item Category")[
    ["case GR-Based Inv. Verif.", "case Goods Receipt"]].describe()
data.head()

# comment to check the updates
# comment 2


data.count().plot(kind='bar', logy=True)
