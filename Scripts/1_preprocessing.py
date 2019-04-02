import pandas as pd
import numpy as np

# importing main dataset
data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")

# Removing whitespace in some columns
data.columns = data.columns.str.strip()

# Fill missing case variables pertaining to case
data = data.fillna("Other")

# Convert datetime strings to native datetime64[ns]
data['event time:timestamp'] = data['event time:timestamp'].apply(lambda t: pd.datetime(
    int(t[6:10]), int(t[3:5]), int(t[:2]), int(t[11:13]), int(t[14:16]), int(t[17:19])))

# Get 'case Purchasing Document' id's for docs that have events before 2015 & remove outliers
invalid_purchdocs = data[data['event time:timestamp'].apply(
    lambda t: t.year) < 2015]['case Purchasing Document'].unique()

# Remove case purchasing documents with an event occuring before 2015 (e.g. 1948)
data = data[~data['case Purchasing Document'].isin(invalid_purchdocs)]

# Saving cleaned data to comressed .csv
data.to_csv("2_preprocessing.gz", index=False, compression='gzip')
