import pandas as pd
import numpy as np

# Read full dataset of aggregrated Purchasing Documents
data = pd.read_csv("3_df_purchdocs.gz", compression="gzip",
                   parse_dates=['start_date', 'end_date'])

# Read dataset of events that did not fit petri net
non_conforming_purchdocs = pd.read_csv(
    "purchdocs_non_conforming.gz", compression="gzip")

# Get unique ids of Purchasing Documents that did not fit the petri net
non_conforming_purchdoc_ids = non_conforming_purchdocs['case Purchasing Document'].unique(
)

# Compute boolean value (y) representing Purchasing Document fit to petri net
data["Petri Net Fitness"] = data["case Purchasing Document"].apply(
    lambda id: id not in non_conforming_purchdoc_ids)
