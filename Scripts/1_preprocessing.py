"""
This script does preprocessing of the raw data.
    - Duplicate columns
    - Missing data
    - Invalid data or noise
"""

# Import pandas for data processing and numpy for operations
import numpy as np
import pandas as pd

# Import gzipped .csv of BPI2019 event logs, source: from icpmconference.org
data = pd.read_csv("./Data/0_raw_data.csv.gz",
                   encoding='ANSI', engine="c")

# Drop 'case Source', 'case Purch. Doc. Category name' (#unique = 1)
# Drop 'event org:resource' (Duplicate of event User)
data = data.drop(
    ["case Source", "case Purch. Doc. Category name", "event org:resource"],
    axis=1)


# Fill missing values for 3 variables, appearing in 16294 in 3289 items.
data = data.fillna("UNKNOWN")


def parse_str_datetime(s):
    """
    Return ns.datetime64 format from parsed string
    Format expected: MM-dd-yyyy HH:MM:SS.fff
    """
    return pd.datetime(
        int(s[6:10]),   # year
        int(s[3:5]),    # month
        int(s[:2]),     # day
        int(s[11:13]),  # hour
        int(s[14:16]),  # minute
        int(s[17:19]))  # second


# Convert datetime strings to native datetime64[ns]
data['event time:timestamp'] = data['event time:timestamp'].apply(
    parse_str_datetime)


# Create year column for easy access/sorting
data['year'] = data['event time:timestamp'].apply(lambda t: t.year)

# Get PO_IDs that have ANY event before 2018
POs_before_2018 = data[data['year'] < 2018]
PO_ids_before_2018 = POs_before_2018['case Purchasing Document'].unique()

# Remove PO's with ANY event occuring before 2018
data = data[~data['case Purchasing Document'].isin(PO_ids_before_2018)]


def groupby_duration(group, timestamp_column='event time:timestamp'):
    """
    Returns duration in days for each group
    Normally expects a groupby object with an 'event time:timestamp column'
    """
    timedeltas = group[timestamp_column].max(
    ) - group[timestamp_column].min()
    return timedeltas.apply(lambda t: round(t.value / 8.64e13, 1))


def immediate_events(group):
    """
    Returns boolean indexer for events with zero duration in a group
    """
    return group.diff() == np.timedelta64(0)


# For each case, get the events that have zero duration
# immediate_events = data[data.groupby("case concept:name")[
#     "event time:timestamp"].apply(immediate_events)]


# Compute duration (d) for PO and Item
# data['PO Duration (d)'] = groupby_duration(
#     data.groupby("case Purchasing Document"))[data['case concept:name']].values
# data['Case Duration (d)'] = groupby_duration(
#     data.groupby("case concept:name"))[data['case concept:name']].values


# Remove PO with duration < 1 day
# short_POs = data[data['PO Duration (d)'] < 1]['PO ID'].unique()
# data = data[~data['PO ID'].isin(short_POs)]


# Save preprocessed data to comressed .csv
data.to_csv("./Data/1_preprocessing.csv.gz", index=False, compression='gzip')
