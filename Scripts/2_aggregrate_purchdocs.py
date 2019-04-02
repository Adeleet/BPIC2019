import pandas as pd
import numpy as np

# import cleaned dataset
data = pd.read_csv("2_preprocessing.gz", compression='gzip',
                   parse_dates=['event time:timestamp'])


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
for i in ['total_duration_days', 'longest_event_name', 'longest_event_value', 'net_worth_change', 'mean_net_worth', 'num_events', 'start_date', 'end_date']:
    purchdoc_data[i] = []

for var in calculated_per_purchdoc:
    purchdoc_data["num_" + var] = []
    purchdoc_data["mode_" + var] = []

for i in range(len(purchdoc_ids)):
    # create pd.DataFrame of purchasing document
    purchdoc = data[data["case Purchasing Document"] == purchdoc_ids[i]]
    if i % 1000 == 0:
        print("{}%".format(round((i / 76331 * 100), 2))
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
    purchdoc_data['start_date'].append(purchdoc['event time:timestamp'].max())
    purchdoc_data['end_date'].append(purchdoc['event time:timestamp'].min())


df_purchdocs=pd.DataFrame(
    purchdoc_data, index=purchdoc_data['case Purchasing Document'])

df_purchdocs.to_csv('3_df_purchdocs.gz', compression='gzip')