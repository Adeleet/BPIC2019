import pandas as pd
import numpy as np

# Read full dataset of aggregrated Purchasing Documents
data = pd.read_csv("Data/2_aggregrate_purchdocs.csv.gz", compression="gzip",
                   parse_dates=['start_date', 'end_date'])

# Read dataset of events that did not fit petri net
violating_purchdocs = pd.read_csv(
    "Data/A_violating_purchdocs.csv.gz", compression="gzip")

# Get unique ids of Purchasing Documents that did not fit the petri net
violating_purchdoc_ids = violating_purchdocs['case Purchasing Document'].unique(
)

# Compute boolean value (y) representing Purchasing Document fit to petri net
data["Petri Net Fitness"] = data["case Purchasing Document"].apply(
    lambda id: id not in violating_purchdoc_ids)
