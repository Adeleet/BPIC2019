
# VARIABLE SPECIFICATION (description, unique values)
|name|description|unique values|type|
|--|--|--|--|
  | eventID| identifier for events|1595923 |                      int64 |
  | case Spend area text              | type/class of purchase item|21 |                     object|
  | case Company                      | company from which purchase originated|4 |           object|
  | case Document Type                | type of order in the case|3 |                        object|
  | case Sub spend area text          | type of purchase item|136 |                          object|
  | case Purchasing Document          | identifier for cases/purchases|76349 |               int64|
  | case Purch. Doc. Category name    | category of purchase document|1 |                    object|
  | case Vendor                       | vendor to which purchase document is sent|1975 |     object|
  | case Item Type                    | purchase classification|6 |                          object|
  | case Item Category                | purchase main document category|4 |                  object|
  | case Spend classification text    | purchase type classification|3 |                     object|
  | case Source                       | system from which purchase originated|1 |            object|
  | case Name                         | name/vendor of purchase|1899 |                       object|
  | case GR-Based Inv. Verif.         | case Goods Received invoice verification|2 |         bool|
  | case Item                         | item type|490 |                                      int64|
  | case concept:name                 | case identifier|251734 |                             object|
  | case Goods Receipt                | flag indicating if 3 way matching is required|2 |    bool|
  | event User                        | user identifier of the event|628 |                   object|
  | event org:resource                | DUPLICATE user identifier of the event|628 |         object|
  | event concept:name                | event name/type|42 |                                 object|
  | event Cumulative net worth (EUR)  | cost of purchase at the time of the event|25221 |    float64|
  | event time:timestamp              | timestamp of the event|167432 |                      object|
  
  

# Variables with missing values:

- 3289 cases, with missing values for each variable in 16294 events

- Missing variables:
  - case Spend area text
  - case Sub spend area text
  - case Spend classification text

- For each case with missing values, each activity in this case has these values missing

- Filled these columns for missing values with "Other"
  - (1) Keep cases because missing does not imply faulty data
  - (2) Missing of these values might be relevant predictor itself

  
  

# EDA

Bar plots were created for categorical variables. Insights:

 1. Company0000 occurs way more often than any other variable
 2. Document Standard PO occurs way more often than Framework order and EC Purchase Other
 3. Goods receipt = False almost never occurs, which means that the third category (2-way matching) almost never occurs, as can be seen at the case item category distribution as well

# Timestamps

- Convert to datetime

- Dropped cases with timestamp of the year 1948
- Need to handle other values; events happening in 2008, 2020, etc.

# Redundant columns

- Drop "Source" column - has only one unique value

- Drop "Event org: resource" - is duplicate to "user" column

  

# Entity Relationships:

**Which of the variables is our case key?**

 - case Concept Name which corresponds to the Purchase item
   
 - UML diagram was made
 - What entities do we have?
   
 **Which attributes are specific to Purchase Document?**

  

- "case Spend classification text" is interesting: it is not a Document Variable, since one Purchasing Document does not only have one value for this attribute, but most of Purchase Docs indeed only have one, only very few(2%) have multiple(exactly 2) values of this
Hypothesis: These are empty values or other values and should be filled in with the most occurring value for a Doc




  

- "case Sub spend area text" is unique for 71469 Purchase Documents, the rest has multiple values. We therefore keep it as purchase item attribute, although it is greatly influenced by which purchase doc does the item belong to

  

- Most purchase documents only have one single purchase item (in fact, the median amount of purchase items per purchase document is 1, 75 percentile is 2)

- When looking at the 0.1% of purchase documents with the most purchase items, still 75th percentile is only 131, while maximum amount of purchase items per purchase document is 429.

  

- Surprisingly, "case Goods Receipt" is a variable of the Purchasing Document, although GR-based

  

**Which attributes are specific to Purchase Item? (case concept:name)**

  

- 'case Spend area text'

- 'case Company'

- 'case Document Type'

- 'case Sub spend area text'

- 'case Purchasing Document'

  
  

# Datetime outside range handling

  

There is large amount of events that happen in the future - in 2019 so we also decide to keep 2019 and 2020.

We drop purchase documents that contain events that happen before 2015 (around 18 docs dropped)

  
|Year|Number of Events  |
|--|--|
|2018 |1550468|
|2019|45135|
|2017| 223|
|2008| 45|
|2001 |22|
|1948 |10|
|1993 |9|
|2016 |6|
|2015 |3|
|2020 |2|