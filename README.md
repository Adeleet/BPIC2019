# TODO

-   **Preprocessing**
  -   [Drop] Purchasing Documents from years other than 2018, 2019, 2020
  -   Handle Events happening at the exact same time [Aggregate, add 1ms](<if Vendor Creates invoice OR Receive Order Confirmation happens at the same time as Create Purchase Order Item>)
  -   Aggregate to Purchasing Documents


-   **Process Modeling**
    -   4 Separate Petri Nets per Item Category, extract MultiPerspective Explorer results
    -   Meta Process Model for PO's, aggregating on the 4+ Item-Level Process Models


-   **Data Analysis & Machine Learning Classification (statistics, correlations, graphs)**
    -   Item-level [x, y] = [Item Data, PetriNet Fit]
    -   PO level [x, y] = [Item Data, PetriNet Fit]

_Log Move: something was executed while the model said it could not happen at that point_

# ProM Packages for Petri Net Creation

-   Data Aware Heuristic Miner
-   Discover Using State Chart Workbench (M.Leemans)

# Variable Specification

| name                             | description                                   | unique values | type    |
| -------------------------------- | --------------------------------------------- | ------------- | ------- |
| eventID                          | identifier for events                         | 1595923       | int64   |
| case Spend area text             | type/class of purchase item                   | 21            | object  |
| case Company                     | company from which purchase originated        | 4             | object  |
| case Document Type               | type of order in the case                     | 3             | object  |
| case Sub spend area text         | type of purchase item                         | 136           | object  |
| case Purchasing Document         | identifier for cases/purchases                | 76349         | int64   |
| case Purch. Doc. Category name   | category of purchase document                 | 1             | object  |
| case Vendor                      | vendor to which purchase document is sent     | 1975          | object  |
| case Item Type                   | purchase classification                       | 6             | object  |
| case Item Category               | purchase main document category               | 4             | object  |
| case Spend classification text   | purchase type classification                  | 3             | object  |
| case Source                      | system from which purchase originated         | 1             | object  |
| case Name                        | name/vendor of purchase                       | 1899          | object  |
| case GR-Based Inv. Verif.        | case Goods Received invoice verification      | 2             | bool    |
| case Item                        | item type                                     | 490           | int64   |
| case concept:name                | case identifier                               | 251734        | object  |
| case Goods Receipt               | flag indicating if 3 way matching is required | 2             | bool    |
| event User                       | user identifier of the event                  | 628           | object  |
| event org:resource               | DUPLICATE user identifier of the event        | 628           | object  |
| event concept:name               | event name/type                               | 42            | object  |
| event Cumulative net worth (EUR) | cost of purchase at the time of the event     | 25221         | float64 |
| event time:timestamp             | timestamp of the event                        | 167432        | object  |

# Variables with missing values:

-   3289 cases, with missing values for each variable in 16294 events
-   Missing variables:
    -   case Spend area text
    -   case Sub spend area text
    -   case Spend classification text
-   For each case with missing values, each activity in this case has these values missing
-   Filled these columns for missing values with "Other"
    -   Keep cases because missing does not imply faulty data
    -   Missing of these values might be relevant predictor itself

# Timestamps
-   Converted strings to to np.datetime64 format
-   We only keep the purchasing documents from [2018-2020], drop the rest

| Year | Events  | Purchasing Documents |
| ---- | ------- | -------------------- |
| 1948 | 10      | 1                    |
| 1993 | 9       | 1                    |
| 2001 | 22      | 15                   |
| 2008 | 45      | 1                    |
| 2015 | 3       | 2                    |
| 2016 | 6       | 3                    |
| 2017 | 223     | 76                   |
| 2018 | 1550468 | 76338                |
| 2019 | 45135   | 11079                |
| 2020 | 2       | 2                    |



# Redundant columns
-   Drop "Source" column - has only one unique value]
-   Drop "Event org: resource" - is duplicate to "user" column

# EDA
Bar plots were created for categorical variables. Insights:
- Company0000 occurs way more often than any other variable
- Document Standard PO occurs way more often than Framework order and EC Purchase Other
- Goods receipt = False almost never occurs, which means that the third category (2-way matching) almost never occurs, as can be seen at the case item category distribution as well

# Entity Relationships:
**Which of the variables is our case key?**

-   case Concept Name which corresponds to the Purchase item

-   UML diagram was made
-   What entities do we have?
    **Which attributes are specific to Purchase Document?**


-   "case Spend classification text" is interesting: it is not a Document Variable, since one Purchasing Document does not only have one value for this attribute, but most of Purchase Docs indeed only have one, only very few(2%) have multiple(exactly 2) values of this
    Hypothesis: These are empty values or other values and should be filled in with the most occurring value for a Doc


-   "case Sub spend area text" is unique for 71469 Purchase Documents, the rest has multiple values. We therefore keep it as purchase item attribute, although it is greatly influenced by which purchase doc does the item belong to


-   Most purchase documents only have one single purchase item (in fact, the median amount of purchase items per purchase document is 1, 75 percentile is 2)

-   When looking at the 0.1% of purchase documents with the most purchase items, still 75th percentile is only 131, while maximum amount of purchase items per purchase document is 429.


-   Surprisingly, "case Goods Receipt" is a variable of the Purchasing Document, although GR-based

# Case variable selection

| Variable                       | Purchasing Document (max unique) | case concept:name (max unique) | Choice              |
| ------------------------------ | -------------------------------- | ------------------------------ | ------------------- |
| case Goods Receipt             | 1                                | 1                              | Purchasing Document |
| case Company                   | 1                                | 1                              | Purchasing Document |
| case Document Type             | 1                                | 1                              | Purchasing Document |
| case Purch. Doc. Category name | 1                                | 1                              | Purchasing Document |
| case Vendor                    | 1                                | 1                              | Purchasing Document |
| case Name                      | 1                                | 1                              | Purchasing Document |
| case Source                    | 1                                | 1                              | Purchasing Document |
| case Spend classification text | 2                                | 1                              | case concept:name   |
| case GR-Based Inv. Verif.      | 2                                | 1                              | case concept:name   |
| case Item Type                 | 2                                | 1                              | case concept:name   |
| case Item Category             | 3                                | 1                              | case concept:name   |
| case Spend area text           | 4                                | 1                              | case concept:name   |
| case Sub spend area text       | 7                                | 1                              | case concept:name   |
| case Item                      | 429                              | 1                              | case concept:name   |
