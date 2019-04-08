import pandas as pd

from EventOrder import EventOrder

data = pd.read_csv("../Data/1_preprocessing.csv.gz", compression='gzip',
                   parse_dates=['Event Timestamp'])


sample_data = data[data["Item ID"].isin(data["Item ID"].unique()[:500])]


order = EventOrder()
order.fit(sample_data, immediate=False, verbose=True)
order.predict_first_event(
    'Create Purchase Order Item',
    'Receive Order Confirmation')


order.predict_first_event_probabilities(
    'Create Purchase Order Item',
    'Receive Order Confirmation')
