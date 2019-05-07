import numpy as np
import pandas as pd

# import cleaned dataset
data = pd.read_csv("Data/1_preprocessing.csv.gz", compression='gzip',
                   parse_dates=['Event Timestamp'])


data.groupby("case Item Category")["case Purchasing Document"].count()
purchdoc_ids = data["case Purchasing Document"].unique()


singular_per_purchdoc = ['Item Spend Area',
                         'PO Company',
                         'PO Doctype',
                         'Item Spend Area - Detailed',
                         'PO ID',
                         'PO Vendor ID',
                         'Item Type',
                         'Item Matching Category',
                         'Item Class',
                         'PO Vendor Name',
                         'Item GR Inv. Verif.',
                         'PO GR']

nonsingular_per_purchdoc = ['Event ID ',
                            'Item Code',
                            'Item ID',
                            'Event User',
                            'Event Cumulative Value (EUR)',
                            'Event Timestamp']


calculated_per_purchdoc = ['Item Code', 'Item ID', 'Event User']


# Initialize dict to be converted to pd.DataFrame
purchdoc_data = dict((k, []) for k in singular_per_purchdoc)

# Add calculated attributes for net_worth, and number_of and mode for
for i in ['total_duration_days', 'longest_event_name', 'longest_event_value', 'net_worth_change', 'mean_net_worth', 'num_events', 'start_date', 'end_date']:
    purchdoc_data[i] = []

for var in calculated_per_purchdoc:
    purchdoc_data["num_" + var] = []
    purchdoc_data["mode_" + var] = []

for i in range(len(purchdoc_ids)):
    # Create pd.DataFrame of purchasing document
    purchdoc = data[data["case Purchasing Document"] == purchdoc_ids[i]]
    if i % 1000 == 0:
        print("{}%".format(round((i / 76331 * 100), 2)))
    # Add first value of singular_per_purchdoc, since they are all the same
    for col in singular_per_purchdoc:
        purchdoc_data[col].append(purchdoc[col].values[0])

    # Add (1) number of unique and (2) mode of variables
    for col in calculated_per_purchdoc:
        purchdoc_data["num_" + col].append(purchdoc[col].nunique())
        purchdoc_data["mode_" + col].append(purchdoc[col].mode()[0])

    # Add (1) Boolean if Cumulative net worth changes and (2) mean net worth
    purchdoc_data['net_worth_change'].append(
        purchdoc['event Cumulative net worth (EUR)'].nunique() > 1)

    # Add mean Cumulative net worth of the purchdoc
    purchdoc_data['mean_net_worth'].append(
        purchdoc['event Cumulative net worth (EUR)'].mean())

    # Add number of events in the purchdoc
    purchdoc_data['num_events'].append(purchdoc.shape[0])

    # Add duration (days) & longest time between 2 events
    purchdoc_data['total_duration_days'].append((purchdoc['Event Timestamp'].max(
    ) - purchdoc['Event Timestamp'].min()).value / 8.64e13)
    purchdoc_data['longest_event_name'].append(purchdoc['event concept:name'].values[purchdoc['Event Timestamp'].diff(
    ).values.argmax() - 1])
    purchdoc_data['longest_event_value'].append(
        purchdoc['Event Timestamp'].diff().max().value / 8.64e13)
    purchdoc_data['start_date'].append(purchdoc['Event Timestamp'].max())
    purchdoc_data['end_date'].append(purchdoc['Event Timestamp'].min())


df_purchdocs = pd.DataFrame(
    purchdoc_data, index=purchdoc_data['PO ID'])

df_purchdocs.to_csv('Data/3_aggregrate_purchdocs.csv.gz', compression='gzip')
