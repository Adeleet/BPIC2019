# Import pandas for data processing and numpy for operations
import numpy as np
import pandas as pd

# Import gzipped .csv of BPI2019 event lgos, source: from icpmconference.org
data = pd.read_csv("Data/0_raw_data.csv.gz",
                   encoding='ANSI', engine="c")

# Drop 'case Source', 'case Purch. Doc. Category name' (#unique = 1)
# Drop 'event org:resource' (Duplicate of event User)
data = data.drop(
    ["case Source", "case Purch. Doc. Category name", "event org:resource"], axis=1)

# Rename columns to clearer format [trace, name]
column_renaming = {
    'eventID ':                         'Event ID',
    'case Spend area text':             'Item Spend Area',
    'case Company':                     'PO Company',
    'case Document Type':               'PO Doctype',
    'case Sub spend area text':         'Item Spend Area - Detailed',
    'case Purchasing Document':         'PO ID',
    'case Vendor':                      'PO Vendor ID',
    'case Item Type':                   'Item Type',
    'case Item Category':               'Item Matching Category',
    'case Spend classification text':   'Item Class',
    'case Name':                        'PO Vendor Name',
    'case GR-Based Inv. Verif.':        'Item GR Inv. Verif.',
    'case Item':                        'Item Code',
    'case concept:name':                'Item ID',
    'case Goods Receipt':               'PO GR',
    'event User':                       'Event User',
    'event concept:name':               'Event Name',
    'event Cumulative net worth (EUR)': 'Event Cumulative Value (EUR)',
    'event time:timestamp':             'Event Timestamp'}

data.columns = column_renaming.values()
data = data.reindex(sorted(data.columns, reverse=True), axis=1)

# Fill missing values for 3 variables, appearing in 16294 in 3289 items.
data = data.fillna("UNKNOWN")

# Convert datetime strings to native datetime64[ns]
data['Event Timestamp'] = data['Event Timestamp'].apply(lambda t: pd.datetime(
    int(t[6:10]), int(t[3:5]), int(t[:2]), int(t[11:13]), int(t[14:16]), int(t[17:19])))


# Create year column for easy access/sorting
data['Year'] = data['Event Timestamp'].apply(lambda t: t.year)

# Get PO_IDs that have ANY event before 2018
POs_before_2018 = data[data['Year'] < 2018]['PO ID'].unique()

# Remove PO's with ANY event occuring before 2018
data = data[~data['PO ID'].isin(POs_before_2018)]


def groupby_duration(group):
    """Returns duration in days for each group"""
    timedeltas = group['Event Timestamp'].max(
    ) - group['Event Timestamp'].min()
    return timedeltas.apply(lambda t: round(t.value / 8.64e13, 1))


def immediate_events(group):
    """Returns boolean indexer for events with zero duration in a group"""
    return group.diff() == np.timedelta64(0)


# Get events with zero duration
immediate_events = data[data.groupby(
    "Item ID")["Event Timestamp"].apply(immediate_events)]


# Compute duration (d) for PO and Item
data['PO Duration (d)'] = groupby_duration(
    data.groupby("PO ID"))[data['PO ID']].values
data['Item Duration (d)'] = groupby_duration(
    data.groupby("Item ID"))[data['Item ID']].values


# Remove PO with duration < 1 day
# short_POs = data[data['PO Duration (d)'] < 1]['PO ID'].unique()
# data = data[~data['PO ID'].isin(short_POs)]


# Save preprocessed data to comressed .csv
data.to_csv("Data/1_preprocessing.csv.gz", index=False, compression='gzip')
