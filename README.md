

# VARIABLE SPECIFICATION (description, unique values)
  eventID                           - identifier for events (n=1595923)                       int64
  case Spend area text              - type/class of purchase item (n=21)                      object
  case Company                      - company from which purchase originated (n=4)            object
  case Document Type                - type of order in the case (n=3)                         object
  case Sub spend area text          - type of purchase item (n=136)                           object
  case Purchasing Document          - identifier for cases/purchases (n=76349)                int64
  case Purch. Doc. Category name    - category of purchase document (n=1)                     object
  case Vendor                       - vendor to which purchase document is sent (n=1975)      object
  case Item Type                    - purchase classification (n=6)                           object
  case Item Category                - purchase main document category (n=4)                   object
  case Spend classification text    - purchase type classification (n=3)                      object
  case Source                       - system from purchase originated (n=1)                   object
  case Name                         - name/vendor of purchase (n=1899)                        object
  case GR-Based Inv. Verif.         - case Goods Received invoice verification (n=2)          bool
  case Item                         - item type (n=490)                                       int64
  case concept:name                 - case identifier (n=251734)                              object
  case Goods Receipt                - flag indicating if 3 way matching is required (n=2)     bool
  event User                        - user identifier of the event (n=628)                    object
  event org:resource                - DUPLICATE user identifier of the event (n=628)          object
  event concept:name                - event name/type (n=42)                                  object
  event Cumulative net worth (EUR)  - cost of purchase at the time of the event (n=25221)     float64
  event time:timestamp              - timestamp of the event (n=167432)                       object


# VARIABLES WITH MISSING VALUES:
# 16294 missing in all three of them
  case Spend area text
  case Sub spend area text
  case Spend classification text


  <class 'pandas.core.frame.DataFrame'>
  RangeIndex: 1595923 entries, 0 to 1595922
  Data columns (total 22 columns):
  eventID                             1595923 non-null int64
  case Spend area text                1579629 non-null object
  case Company                        1595923 non-null object
  case Document Type                  1595923 non-null object
  case Sub spend area text            1579629 non-null object
  case Purchasing Document            1595923 non-null int64
  case Purch. Doc. Category name      1595923 non-null object
  case Vendor                         1595923 non-null object
  case Item Type                      1595923 non-null object
  case Item Category                  1595923 non-null object
  case Spend classification text      1579629 non-null object
  case Source                         1595923 non-null object
  case Name                           1595923 non-null object
  case GR-Based Inv. Verif.           1595923 non-null bool
  case Item                           1595923 non-null int64
  case concept:name                   1595923 non-null object
  case Goods Receipt                  1595923 non-null bool
  event User                          1595923 non-null object
  event org:resource                  1595923 non-null object
  event concept:name                  1595923 non-null object
  event Cumulative net worth (EUR)    1595923 non-null float64
  event time:timestamp                1595923 non-null object
  dtypes: bool(2), float64(1), int64(3), object(16)
  memory usage: 246.6+ MB
