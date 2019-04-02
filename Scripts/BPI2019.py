

# # 22333 variants of events in
# purchdoc_item_counts = data[['case Item', 'case Purchasing Document']
#                             ].groupby('case Purchasing Document').nunique()['case Item']
# purchdoc_item_counts.describe()
# # purchasing document 4508073932 has 429 purchase items
# purchdoc_item_counts[purchdoc_item_counts == purchdoc_item_counts.max()]
# # purchasing document 4508073932 has 429 purchase items
# purchdoc_item_counts[purchdoc_item_counts
#                      > purchdoc_item_counts.quantile(0.999)]


#data[["case Spend classification text","case concept:name"]].groupby("case concept:name").describe()
#
# purchdoc = data.groupby('case Purchasing Document')
# purchdoc['case Name'].nunique()
