import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Load alignment data
alignments = pd.read_csv("../Data/D_final_alignments/D_final_alignments.csv.gz",
                         na_values=np.nan, parse_dates=['Complete Timestamp'])


# Drop redundant columns
alignments = alignments.drop(['dataalignment:movetype', 'year'], axis=1)

# Convert floats that are actually categorical to correct categorical type
for col in ['alignment:movetype', 'alignment:observable', 'case Item']:
    alignments[col] = alignments[col].astype('category')

# This does not work??
alignments['case GR-Based Inv. Verif.'].isna().sum()
alignments.count()
# all rows in which the case item category (and other attributes) are Nan have movetype 2
alignments['alignment:movetype'][alignments['case Item Category'].isna()]


# only keep events that really happened
alignments_filtered = alignments[alignments['alignment:movetype'] != 2]

# BEGIN Y1 - Alignment
alignments_filtered['case Vendor'].value_counts()
lowest_fitness_cases = alignments_filtered[alignments_filtered['(case) alignment:fitness'] < np.percentile(
    alignments_filtered['(case) alignment:fitness'], 0.1)]
lowest_fitness_cases['case Vendor'].value_counts()['vendorID_0046']
(lowest_fitness_cases['case Vendor'].value_counts(
) / alignments_filtered['case Vendor'].value_counts()).sort_values(ascending=False).dropna()

# let's find the vendors with the lowest mean fitness

fitness_vendors = alignments_filtered[[
    'case Vendor', '(case) alignment:fitness']].groupby('case Vendor').agg('mean')
lowfit_vendors = fitness_vendors[fitness_vendors['(case) alignment:fitness'] <= np.percentile(
    fitness_vendors['(case) alignment:fitness'], 1)]  # these vendors have the 1 percent lowest mean fitness

alignments_filtered[alignments_filtered['case Vendor'].isin(
    lowfit_vendors.index)]['case Vendor'].value_counts()

# especially vendor_ID_0582 is worth looking into as there are >1000 events for this vendor and it is in the 1st percentile of mean fitness of vendors


# there are 30 vendors for which more than 99% of their events have a fitness worse than 99% of all events in total

alignments_filtered['day'] = pd.to_datetime(
    alignments_filtered['Complete Timestamp'].astype('str')).dt.dayofyear
alignments_filtered['month'] = pd.to_datetime(
    alignments_filtered['Complete Timestamp'].astype('str')).dt.month
alignments_filtered['year'] = pd.to_datetime(
    alignments_filtered['Complete Timestamp'].astype('str')).dt.year

gen_mean_fitness2018 = alignments_filtered[[
    'month', '(case) alignment:fitness', 'year']][alignments_filtered.year < 2020].groupby(['year', 'month']).agg('mean')
threeway_after_mean_fitness2018 = alignments_filtered[['month', '(case) alignment:fitness', 'year']][(alignments_filtered.year < 2020) & (
    alignments_filtered['case Item Category'] == '3-way match, invoice before GR')].groupby(['year', 'month']).agg('mean')
threeway_before_mean_fitness2018 = alignments_filtered[['month', '(case) alignment:fitness', 'year']][(alignments_filtered.year < 2020) & (
    alignments_filtered['case Item Category'] == '3-way match, invoice after GR')].groupby(['year', 'month']).agg('mean')
Consignment_mean_fitness2018 = alignments_filtered[['month', '(case) alignment:fitness', 'year']][(alignments_filtered.year < 2020) & (
    alignments_filtered['case Item Category'] == 'Consignment')].groupby(['year', 'month']).agg('mean')
twoway_mean_fitness2018 = alignments_filtered[['month', '(case) alignment:fitness', 'year']][(alignments_filtered.year < 2020) & (
    alignments_filtered['case Item Category'] == '2-way match')].groupby(['year', 'month']).agg('mean')


plt.figure(figsize=(15, 10))
plt.plot(gen_mean_fitness2018['(case) alignment:fitness']
         [2018], '-', label='all categories', linewidth=3)
plt.plot(threeway_after_mean_fitness2018['(case) alignment:fitness']
         [2018], ':', label='3-way match, invoice after GR', linewidth=3)
plt.plot(threeway_before_mean_fitness2018['(case) alignment:fitness']
         [2018], ':', label='3-way match, invoice before GR', linewidth=3)
plt.plot(Consignment_mean_fitness2018['(case) alignment:fitness']
         [2018], ':', label='Consignment', linewidth=3)
plt.plot(twoway_mean_fitness2018['(case) alignment:fitness']
         [2018], ':', label='2-way match', linewidth=3)
plt.legend()
plt.xlabel('month')
plt.ylabel('mean case fitness')
# plt.savefig(r"C:\Users\s161975\Google Drive\BPI honors\BPI 2019\Figures about fitness\mean Fitness over months.png")
plt.show()
gen_mean_fitness2018.columns


# alignments_filtered['case Item Category'].value_counts()
# 3-way match, invoice before GR    1233322
# 3-way match, invoice after GR      308836
# Consignment                         36073
# 2-way match                          5327
# Name: case Item Category, dtype: int64


# correlations of fitness and other stuff
alignments_filtered.columns
alignments_filtered[['(case) alignment:fitness', '(case) throughputtime',
                     'event Cumulative net worth (EUR)']].corr()
plt.figure(figsize=(10, 10))
sns.heatmap(alignments_filtered[['(case) alignment:fitness',
                                 '(case) throughputtime', 'event Cumulative net worth (EUR)']].corr(), annot=True)
# plt.savefig(
#    r"C:\Users\s161975\Google Drive\BPI honors\BPI 2019\Figures about fitness\corrs.png")
plt.show()
print('(corrcoef, p-value) of fitness and networth is', stats.pearsonr(
    alignments_filtered['event Cumulative net worth (EUR)'], alignments_filtered['(case) alignment:fitness']))
# END Y1 - Alignment
alignments_filtered.columns

# BEGIN Y2 - Throughput
alignments_filtered_cleaned = pd.read_csv(
    "../Data/D_final_alignments/D_final_alignments_removed_NaNs.csv.gz", parse_dates=["Complete Timestamp"])

cleared_invoices = alignments_filtered_cleaned[alignments_filtered_cleaned["Activity"] == 'Clear Invoice']


def group_users(user):
    """
    Groups event user into 3 categories by removing number suffix:
        user, batch and NONE
    """
    if user == "NONE":
        return user
    else:
        return user[:user.index("_")].upper()


alignments_filtered_cleaned["user type"] = alignments_filtered_cleaned["event User"].apply(
    group_users)

alignments_filtered_cleaned["user type"].nunique()
# Categoricals - low nunique
# case Document Type                        3
# case Spend classification text            4
# case Item Category                        4
# case Company                              4
# case Item Type                            6

# Categoricals - high unique (find outliers)
# case Spend area text                     21
# case Sub spend area text                136
# case Item                               490
# event User                              627
# case Name                              1883
# case Vendor                            1958

# Floats, scatterplot or regression
# event Cumulative net worth(EUR)      25136

# For plotting throughput across time
# Complete Timestamp                   166110

categoricals_short = ['case Company', 'case Document Type', 'case Item Category',
                      'case Item Type', 'case Name', 'case Spend classification text', 'user type']
categoricals_long = ['case Item', 'case Name', 'case Spend area text',
                     'case Sub spend area text', 'case Vendor', 'event User']
floats = 'event Cumulative net worth (EUR)'

invoice_cleared = cleared_invoices.groupby(
    "Case ID")["Complete Timestamp"].min().sort_values()
starting_cases = alignments_filtered_cleaned[[
    'Case ID', 'Complete Timestamp']].groupby('Case ID').min()

inv_thr = pd.concat([invoice_cleared, starting_cases], axis=1, join='inner')
inv_thr.columns = ['End', 'Start']

# inv_thr[cat] = alignments_filtered.groupby("Case ID")[categoricals_long].first()

# inv_thr['Vendor'] = alignments_filtered.groupby("Case ID")["case Vendor"].first()


for cat in categoricals_short:
    inv_thr[cat] = alignments_filtered_cleaned.groupby("Case ID")[cat].first()
for cat in categoricals_long:
    inv_thr[cat] = alignments_filtered_cleaned.groupby("Case ID")[cat].first()
inv_thr['month'] = pd.to_datetime(inv_thr['Start'].astype('str')).dt.month
inv_thr['exact_duration'] = (inv_thr['End'] - inv_thr['Start'])
inv_thr['duration_days'] = inv_thr.exact_duration.apply(lambda x: x.days)
categoricals_short.append('month')
len(categoricals)
for cat in categoricals_short:
    cat_thr = inv_thr.groupby(cat)['duration_days'].mean()
    plt.figure(figsize=(15, 10))
    plt.title(cat)
    plt.bar(cat_thr.index, cat_thr)
    plt.ylabel('Number of cases')
    plt.xlabel('Mean througput')
    plt.savefig('../Figures about fitness/' + cat + '.eps')
inv_thr.groupby('case Item')['duration_days'].mean().mean()
for cat in categoricals_long:
    cat_thr = inv_thr.groupby(cat)['duration_days'].mean()
    mean_duration = cat_thr.mean()
    std = cat_thr.std()
    quantile = cat_thr.quantile(0.99)
    in_99th_percentile = cat_thr[cat_thr > quantile]
    two_std_higher = cat_thr[cat_thr > mean_duration + 2 * std]
    print('Mean duration = ' + str(mean_duration) + ', standard deviation = ' +
          str(std) + ', 99-th percentile = ' + str(quantile))
    print(cat + ' mean case duration in 99-th percentile:')
    print(in_99th_percentile)
    print(cat + ' mean case duration more than two standard deviations higher than mean')
    print(two_std_higher)
alignments_filtered.apply(lambda row: row["Case ID"], axis=1)

days_distr = inv_thr['days'].value_counts()


# Distribution of througput
plt.figure(figsize=(15, 10))
plt.title('Througput distribution')
plt.bar(days_distr.index, days_distr)
plt.ylabel('Number of cases')
plt.xlabel('Mean througput')
plt.savefig('../Figures about fitness/Throughput_ditribution.eps')
#
#
plt.figure(figsize=(10, 10))
sns.heatmap(inv_thr.corr(), annot=True)
plt.show()
print('(corrcoef, p-value) of fitness and networth is', stats.pearsonr(
    alignments_filtered['event Cumulative net worth (EUR)'], alignments_filtered['(case) alignment:fitness']))

# END Y2 - throughput


# BEGIN Y3 - Matching (Invoice - GR)

# Create a sample to speed up prototyping
sample_case_ids = pd.DataFrame(
    alignments_filtered["Case ID"].unique()).sample(2500)[0].values

alignments_sampled = alignments_filtered[alignments_filtered["Case ID"].isin(
    sample_case_ids)]

# Create dataframe slices for both 3-way matching categories
DF_3_way = alignments_filtered[alignments_filtered['case Item Category'].isin(
    ['3-way match, invoice before GR', '3-way match, invoice after GR'])]


# Dropna for alignment:activityid, these are not part of the original (+15% more matches)
DF_3_way = DF_3_way.dropna(subset=['alignment:activityid'])

# If two events are identical on these variables, remove them (+ 5% more matches)
event_identifiers = ['Activity', 'Case ID', 'Complete Timestamp',
                     'event Cumulative net worth (EUR)', 'event User']
DF_3_way = DF_3_way.drop_duplicates(subset=event_identifiers)

# Create DataFrame to hold PER case Match results
DF_3_way_items = pd.DataFrame(
    index=DF_3_way["Case ID"].unique())


def item_creation_value(case):
    """
    Calculates total value of item creation
    """
    return case[case["Activity"] == 'Create Purchase Order Item']["event Cumulative net worth (EUR)"].sum()


def item_GR_value(case):
    """
    Sums the net worths of all GR recorded, minus the net worths of GR cancels
    """
    value_goods_receipt = case[case["Activity"] ==
                               'Record Goods Receipt']["event Cumulative net worth (EUR)"].sum()
    value_goods_receipt_cancels = case[case["Activity"] ==
                                       'Cancel Goods Receipt']["event Cumulative net worth (EUR)"].sum()
    return value_goods_receipt - value_goods_receipt_cancels


def item_IR_value(case):
    """
    Sum all invoices (incl. subsequent if found) and service entry sheets
    """
    first_invoice_value = case[case["Activity"] ==
                               'Record Invoice Receipt']["event Cumulative net worth (EUR)"].sum()
    if np.isnan(first_invoice_value):
        first_invoice_value = 0
    subsequent_invoice_values = case[case["Activity"] ==
                                     'Record Subsequent Invoice Receipt']["event Cumulative net worth (EUR)"].sum()
    if np.isnan(subsequent_invoice_values):
        subsequent_invoice_values = 0
    service_entry_values = case[case["Activity"] ==
                                'Record Service Entry Sheet']["event Cumulative net worth (EUR)"].sum()
    if np.isnan(service_entry_values):
        service_entry_values = 0
    return max([first_invoice_value + subsequent_invoice_values, service_entry_values])


# Groupby case and get Activity and Net Worths to check 3-way matching
DF_3_way_groupby_case = DF_3_way.groupby(
    "Case ID")[["Activity", "event Cumulative net worth (EUR)"]]

# Runs the matching checkers for each of the factors in 3-way matching
DF_3_way_items["Item Creation"] = DF_3_way_groupby_case.apply(
    item_creation_value)
DF_3_way_items["Goods Receipt"] = DF_3_way_groupby_case.apply(item_GR_value)
DF_3_way_items["Invoice Receipt"] = DF_3_way_groupby_case.apply(item_IR_value)


def item_matching_result(row):
    """
    Returns categorical matching result for Item Creation, Goods Receipt and Invoice Receipt
    """
    matching_factors = ["Item Creation", "Goods Receipt", "Invoice Receipt"]
    missing_factors = [col.upper().replace(" ", "_")
                       for col in matching_factors if row[col] == 0]
    if len(missing_factors) > 0:
        return "MISSING_" + "_".join(missing_factors)
    if (row["Item Creation"] == 0):
        return "NO_ITEM_CREATION"
    if (row["Goods Receipt"] == 0):
        return "NO_GOODS_RECEIPT"
    if (row["Item Creation"] == 0):
        return "NO_INVOICE_RECEIPT"
    if (row["Item Creation"] == row["Goods Receipt"]) & (row["Goods Receipt"] == row["Invoice Receipt"]):
        return "FULL_MATCH"
    if (row["Item Creation"] == row["Goods Receipt"]) & (row["Goods Receipt"] != row["Invoice Receipt"]):
        return "ITEM_CREATION_GOODS_RECEIPT"
    if (row["Item Creation"] != row["Goods Receipt"]) & (row["Goods Receipt"] == row["Invoice Receipt"]):
        return "GOODS_RECEIPT_INVOICE_RECEIPT"
    else:
        return "NO_MATCH"


# Assigns matching results to item level dataframe
DF_3_way_items["Match"] = DF_3_way_items.apply(item_matching_result, axis=1)

# Create dictionary and assign item-level matching results to full dataframe
DICT_3_way_match = DF_3_way_items["Match"].to_dict()
DF_3_way["Match"] = DF_3_way["Case ID"].apply(lambda id: DICT_3_way_match[id])

# Create item level dataframe with X (...) and y (Match)
DF_train = DF_3_way[["Case ID", "case Company", "case Item Category",
                     "case Document Type", "case Spend classification text",
                     "case Item Type", "case Spend area text",
                     "case Sub spend area text", "case Item", "Match"]].drop_duplicates()

# Remove categorical with high unique values
DF_train_low_nunique = DF_train[DF_train.nunique()[
    DF_train.nunique() < 10].keys()]


X = DF_train_low_nunique.drop("Match", axis=1)
X_dummies = pd.get_dummies(X)
y = DF_train_low_nunique["Match"]


# Run decision tree to analyze predictive variabels for matching
dec_tree = DecisionTreeClassifier()

# Create train/test split for validation
train_X, test_X, train_y, test_y = train_test_split(
    X_dummies, y, test_size=0.20)

# Fit and compute test score
dec_tree_score = dec_tree.fit(train_X, train_y).score(test_X, test_y)
dec_tree_score

DF_dec_tree_results = pd.DataFrame(
    data={"Dummy Name": X_dummies.columns, "Feature Importance": dec_tree.feature_importances_})


def dummy_to_categorical(dummy_name):
    """
    Converts a dummy variable var_value to its original value
    """
    return dummy_name[:dummy_name.index("_")]


# Convert dummies back to their variable name to analyze which variables are important
DF_dec_tree_results["Variable"] = DF_dec_tree_results["Dummy Name"].apply(
    dummy_to_categorical)

# Plots variable importance for Match
DF_dec_tree_results.groupby("Variable").sum().plot(kind='bar', rot=0, color='teal', figsize=(
    15, 8)), plt.savefig("../Figures/Alignments_Y3_Variable_Feature_Importance.png", dpi=800)

# Since case Item Type is most important, plot Item Type Match Results
grouped_value_counts = DF_train.groupby("case Item Type")[
    "Match"].value_counts(normalize=True)
grouped_value_counts.unstack(level=-1).plot(kind='bar', rot=0, figsize=(
    15, 8)), plt.savefig("../Figures/Alignments_Y3_Case_Item_Type.png", dpi=800)

# For Service, plot the matching results
DF_train[DF_train["case Item Type"] == "Service"]["Match"].value_counts(
    normalize=True).plot(kind='bar', rot=30, color='#993855', figsize=(25, 6)), plt.savefig("../Figures/Alignments_Y3_Service_Match.png", dpi=800)


DICT_3_duration = DF_3_way.groupby("Case ID")["Complete Timestamp"].apply(
    lambda t: t.max() - t.min()).to_dict()


DF_train["Duration"] = DF_train["Case ID"].apply(
    lambda id: DICT_3_duration[id].days)


DF_3_way["isMatch"] = DF_3_way["Match"] == "FULL_MATCH"

DF_PO_3way = DF_3_way[['case Document Type',
                       'case Vendor',
                       'case Purchasing Document',
                       'case Name',
                       'case Item Type',
                       'case Goods Receipt',
                       'alignment:movetype',
                       'alignment:observable',
                       'case Company', 'isMatch']].groupby("case Purchasing Document")

Matching_results_PO = DF_PO_3way["isMatch"].min().value_counts(normalize=True)


# Invoice only cleared if Goods receipt == Invoice Receipt == Create Item


# END Y3 - Matching (Invoice - GR)
