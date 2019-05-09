import numpy as np
import pandas as pd


def unique_variants(df, case_col='case concept:name', event_col='event concept:name', timestamp_col='event time:timestamp'):
    # For each (case), sort based on timestamp
    df.sort_values(by=[case_col, timestamp_col])

    # Create a groupby object of unique cases
    df_traces = df.groupby(case_col)

    traces = df_traces[event_col].apply(lambda events: list(events))

    # List to hold the unique variant events
    variants_event = []

    # List to hold the unique variant case id's
    variants_id = []

    # Iterate through each trace i
    # If event sequence of i is not in variants_events[], append its id to variants_id[]
    for case_id, trace in traces.items():
        if trace not in variants_event:
            variants_event.append(trace)
            variants_id.append(case_id)

    # Create dataframe of unique variants
    df_variants = df[df[case_col].isin(variants_id)]
    return df_variants


data = pd.read_csv("./Data/MatchingCategories/3-way-invoice-after-GR.csv",
                   parse_dates=['event time:timestamp'])


data[data["event concept:name"]]
unique_variants(data).to_csv("kek.csv.gz",compression='gzip',index=False)
