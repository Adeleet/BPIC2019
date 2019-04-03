import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

data = pd.read_csv("Data/1_preprocessing.csv.gz",
                   parse_dates=['event time:timestamp'])


cols = ['case Spend area text',
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
        'case Item',
        'case concept:name',
        'case Goods Receipt',
        'eventID',
        'event User',
        'event org:resource',
        'event concept:name',
        'event Cumulative net worth (EUR)',
        'event time:timestamp']


purchdoc_vars = ['case Company',
                 'case Document Type',
                 'case Purchasing Document',
                 'case Purch. Doc. Category name',
                 'case Vendor',
                 'case Source',
                 'case Name',
                 'case Goods Receipt']

case_concept_vars = ['case Spend area text',
                     'case Sub spend area text',
                     'case Item Type',
                     'case Item Category',
                     'case Spend classification text',
                     'case GR-Based Inv. Verif.',
                     'case Item',
                     'case concept:name']

event_vars = ['eventID',
              'event User',
              'event org:resource',
              'event concept:name',
              'event Cumulative net worth (EUR)',
              'event time:timestamp']


# purchdoc_data = data[purchdoc_vars].groupby(purchdoc_vars).head(n=1)
