"""
Splits preprocessed data into train/test data based on matching category

Generates 12 .csv files, for each of the 4 matching categories:
    - [item category 100%] :        MatchingCategories/[item category].csv
    - [item category 80% sample] :  MatchingCategories/Train/[item category].csv
    - [item category 20% sample] :  MatchingCategories/Test/[item category].csv
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Read preprocessed data, only including necessary columns
data = pd.read_csv("./Data/1_preprocessing.csv.gz",
                   parse_dates=['event time:timestamp'],
                   usecols=['case concept:name',
                            'event concept:name',
                            'event time:timestamp',
                            'case Item Category'],
                   engine='c')


# mapping each of the 4 item categories to a filename
MATCH_CATEGORY_DIR_MAPPING = {'3-way match, invoice before GR': '3-way-invoice-before-GR',
                              '3-way match, invoice after GR': '3-way-invoice-after-GR',
                              '2-way match': '2-way',
                              'Consignment': 'consignment'}


MATCH_PATH = "./Data/MatchingCategories"

for match_category, match_dir in MATCH_CATEGORY_DIR_MAPPING.items():
    # Create df based on the matching category
    df = data[data["case Item Category"] == match_category]

    # Get unique cases (items) for this category
    case_ids = df['case concept:name'].unique()

    # Split into train and test dataset based on cases (items)
    train_case_ids, test_case_ids = train_test_split(case_ids, test_size=0.2)
    df_train = df[df['case concept:name'].isin(train_case_ids)]
    df_test = df[df['case concept:name'].isin(test_case_ids)]

    # Save [train, test, train+test] each to seperate .csv
    df_train.to_csv(f"{MATCH_PATH}/{match_dir}/train.csv", index=False)
    df_train.to_csv(f"{MATCH_PATH}/{match_dir}/test.csv", index=False)
    df_train.to_csv(f"{MATCH_PATH}/{match_dir}/full.csv", index=False)
