import seaborn
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("BPI_Challenge_2019.csv", encoding='ANSI', engine="c")
# some clumns have whitespaces in keywords - remove them:
data.columns = data.columns.str.strip()

# Chapter: MISSING VALUES
missing_vars = ['case Spend area text',
                'case Sub spend area text', 'case Spend classification text']

# Fill missing case variables pertaining to case
data = data.fillna("Other")


event_category_value_counts = pd.DataFrame(
    {"missing_data": missing_event_categories, "non_missing_data": non_missing_event_categories})
event_category_value_counts.fillna(0, inplace=True)
(event_category_value_counts["non_missing_data"]
 / event_category_value_counts["missing_data"]).sort_values(ascending=False)


# Chapter: EXPLORATORY DATA ANALYSIS
# stats for numeric vars
data.describe()

# based on the bar plots for the categorical variables we see:

exclude = ['eventID', 'case Purchasing Document', 'case Item',
           'event Cumulative net worth (EUR)', 'case concept:name', 'event time:timestamp', 'case Vendor', 'case Name']

c = ''
for c in data.columns:
    if c not in exclude:
        # print(data[c].value_counts())
        figname = "figure" + c + ".png"
        plt.figure(), data[c].value_counts().plot(kind='bar'), plt.title(
            c), plt.savefig(dpi=300, fname=figname, bbox_inches='tight')
