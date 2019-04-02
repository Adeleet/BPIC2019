from sklearn.cluster import KMeans
import time
from sklearn.preprocessing import LabelEncoder
import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# importing main dataset
# data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")
#
# # PREPROCESSING
#
# # Removing whitespace in some columns
# data.columns = data.columns.str.strip()
#
# # Fill missing case variables pertaining to case
# data = data.fillna("Other")
#
# # Convert datetime strings to native datetime64[ns]
# data['event time:timestamp'] = data['event time:timestamp'].apply(lambda t: pd.datetime(
#     int(t[6:10]), int(t[3:5]), int(t[:2]), int(t[11:13]), int(t[14:16]), int(t[17:19])))
#
# # Get 'case Purchasing Document' id's for docs that have events before 2015 & remove outliers
# invalid_purchdocs = data[data['event time:timestamp'].apply(
#     lambda t: t.year) < 2015]['case Purchasing Document'].unique()
#
# # Remove case purchasing documents with an event occuring before 2015 (e.g. 1948)
# data = data[~data['case Purchasing Document'].isin(invalid_purchdocs)]
#
# # Saving cleaned data to comressed .csv
# data.to_csv("data_cleaned.gz", index=False, compression='gzip')

data = pd.read_csv("data_cleaned.gz", compression='gzip',
                   parse_dates=['event time:timestamp'])


non_conforming = pd.read_csv("non_conforming2.csv")
non_conforming_purchdoc_ids = non_conforming['case Purchasing Document'].unique(
)
non_conforming.case
non_conforming_case = non_conforming['case'].unique()

len(non_conforming_case) / data['case concept:name'].nunique()
data["Petri Net Fit"] = True
data["Petri Net Fit"] = data["case Purchasing Document"].apply(
    lambda id: not id in non_conforming_purchdoc_ids)


data["Petri Net Fit"].sum() / data.shape[0]


purchdoc_ids = data["case Purchasing Document"].unique()


singular_per_purchdoc = ['case Spend area text',
                         'case Company',
                         'case Document Type',
                         'case Sub spend area text',
                         'case Purchasing Document',
                         'case Purch. Doc. Category name',
                         'case Vendor',
                         'case Item Type',
                         'case Item Category',
                         'case Spend classification text',
                         'case Source',
                         'case Name',
                         'case GR-Based Inv. Verif.',
                         'case Goods Receipt']
nonsingular_per_purchdoc = ['eventID',
                            'case Item',
                            'case concept:name',
                            'event User',
                            'event org:resource',
                            'event Cumulative net worth (EUR)',
                            'event time:timestamp']
calculated_per_purchdoc = ['case Item',
                           'case concept:name',
                           'event User']


# Initialize dict to be converted to pd.DataFrame
purchdoc_data = dict((k, []) for k in singular_per_purchdoc)

# Add calculated attributes for net_worth, and number_of and mode for
for i in ['total_duration_days', 'longest_event_name', 'longest_event_value', 'net_worth_change', 'mean_net_worth', 'num_events']:
    purchdoc_data[i] = []

for var in calculated_per_purchdoc:
    purchdoc_data["num_" + var] = []
    purchdoc_data["mode_" + var] = []

for i in range(len(purchdoc_ids)):
    # create pd.DataFrame of purchasing document
    purchdoc = data[data["case Purchasing Document"] == purchdoc_ids[i]]
    if i % 1000 == 0:
        print("{}%".format(i / 76331 * 100))
    # Add first value of singular_per_purchdoc, since they are all the same
    for col in singular_per_purchdoc:
        purchdoc_data[col].append(purchdoc[col].values[0])

    # Add (1) number of unique and (2) mode of variables
    for col in calculated_per_purchdoc:
        purchdoc_data["num_" + col].append(purchdoc[col].nunique())
        purchdoc_data["mode_" + col].append(purchdoc[col].mode()[0])

    # Add (1) Boolean if Cumulative net worth changes and (2) mean
    purchdoc_data['net_worth_change'].append(
        purchdoc['event Cumulative net worth (EUR)'].nunique() > 1)

    # Add mean Cumulative net worth of the purchdoc
    purchdoc_data['mean_net_worth'].append(
        purchdoc['event Cumulative net worth (EUR)'].mean())

    # Add number of events in the purchdoc
    purchdoc_data['num_events'].append(purchdoc.shape[0])

    # Add duration (days) & longest time between 2 events
    purchdoc_data['total_duration_days'].append((purchdoc['event time:timestamp'].max(
    ) - purchdoc['event time:timestamp'].min()).value / 8.64e13)
    purchdoc_data['longest_event_name'].append(purchdoc['event concept:name'].values[purchdoc['event time:timestamp'].diff(
    ).values.argmax() - 1])
    purchdoc_data['longest_event_value'].append(
        purchdoc['event time:timestamp'].diff().max().value / 8.64e13)

df_purchdocs = pd.DataFrame(
    purchdoc_data, index=purchdoc_data['case Purchasing Document'])

df_purchdocs.to_csv('df_purchdocs.gz', compression='gzip')


# 22333 variants of events in
purchdoc_item_counts = data[['case Item', 'case Purchasing Document']
                            ].groupby('case Purchasing Document').nunique()['case Item']
purchdoc_item_counts.describe()
# purchasing document 4508073932 has 429 purchase items
purchdoc_item_counts[purchdoc_item_counts == purchdoc_item_counts.max()]
# purchasing document 4508073932 has 429 purchase items
purchdoc_item_counts[purchdoc_item_counts >
                     purchdoc_item_counts.quantile(0.999)]


#data[["case Spend classification text","case concept:name"]].groupby("case concept:name").describe()

purchdoc = data.groupby('case Purchasing Document')
purchdoc['case Name'].nunique()
