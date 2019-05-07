import pandas as pd

sample_purchdoc = pd.read_csv("Data/X_sample_purchdoc.csv.gz")

purchdoc_vars = ['Item Spend Area',
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


class PurchDoc:
    def __init__(self, df_purchdoc):
        purchdoc_data = sample_purchdoc[purchdoc_vars].copy()
        for v in purchdoc_vars:
            print(v, purchdoc_data[v].values[0])
            setattr(self, str(v), 2)
        setattr(self, 'a', 2)


class PurchItem:
    def __init__(self):
        pass


class Event:
    def __init__(self, series):
        print(args[0])
