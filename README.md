### TODO

-   **Preprocessing**

    -   [x]   [Drop] Purchasing Documents from years other than 2018, 2019, 2020
    -   [ ]   Handle Events happening at the exact same time (Aggregate or add 1ms) if Vendor Creates invoice OR Receive Order Confirmation happens at the same time as Create Purchase Order Item.
    -   [ ]   Aggregate to Purchasing Documents


-   **Process Modeling**
    -   [ ]   4 Separate Petri Nets per Item Category, extract MultiPerspective Explorer results
    -   [ ]   Meta Process Model for PO's, aggregating on the 4+ Item-Level Process Models


-   **Data Analysis & Machine Learning Classification (statistics, correlations, graphs)**
    -   [ ]   Item-level [x, y] = [Item Data, PetriNet Fit]
    -   [ ]   PO level [x, y] = [Item Data, PetriNet Fit]

_Log Move: something was executed while the model said it could not happen at that point_

### ProM Packages for Petri Net Creation

-   Data Aware Heuristic Miner
-   Discover Using State Chart Workbench (M.Leemans)

# 1 Preprocessing

| **name**                          | description                                   | unique values | type     |
| --------------------------------- | --------------------------------------------- | ------------- | -------- |
| **eventID** [Event]               | identifier for events                         | 1595923       | int64    |
| case Spend area text              | type/class of purchase item                   | 21            | string   |
| case Company                      | company from which purchase originated        | 4             | string   |
| case Document Type                | type of order in the case                     | 3             | string   |
| case Sub spend area text          | type of purchase item                         | 136           | string   |
| **case Purchasing Document** [PO] | identifier for cases/purchases                | 76349         | int64    |
| case Purch. Doc. Category name    | category of purchase document                 | 1             | string   |
| case Vendor                       | vendor to which purchase document is sent     | 1975          | string   |
| case Item Type                    | purchase classification                       | 6             | string   |
| case Item Category                | purchase document matching category           | 4             | string   |
| case Spend classification text    | purchase type classification                  | 3             | string   |
| case Source                       | system from which purchase originated         | 1             | string   |
| case Name                         | name/vendor of purchase                       | 1899          | string   |
| case GR-Based Inv. Verif.         | case Goods Received invoice verification      | 2             | bool     |
| case Item                         | item type                                     | 490           | int64    |
| **case concept:name** [Case]      | case identifier                               | 251734        | string   |
| case Goods Receipt                | flag indicating if 3 way matching is required | 2             | bool     |
| event User                        | user identifier of the event                  | 628           | string   |
| event org:resource                | DUPLICATE user identifier of the event        | 628           | string   |
| event concept:name                | event name/type                               | 42            | string   |
| event Cumulative net worth (EUR)  | cost of purchase at the time of the event     | 25221         | float64  |
| event time:timestamp              | timestamp of the event                        | 167432        | datetime |

_Table 1 - Variable Specification_
<br><br><br>

### 1.1 Missing Values

-   3289 **cases**. with missing values in 16294 events.
-   Missing variables:
    -   **case Spend area text**
    -   **case Sub spend area text**
    -   **case Spend classification text**
-   For each case with missing values, each activity in this case is
    missing values for these attributes.
-   These missing values are filled with value **_Missing_**
    -   Cases are not removed, as the fact that these values are missing may not indicate faulty data, but intended design as part of the process. (e.g. particular Spend classification does not fall under the available categories, so is left empty.)
    -   These variables missing from a case may be useful in (causal) analysis of process deviations.

### 1.2 Timestamps

-   Since the BPI Challenge Description specifies that the date is from purchase orders submitted in 2018, we analyze the events, cases and purchase documents occuring before and after 2018.
-   The events prior to 2018 have an interesting distribution of events (Table 2), only 3 types of events out of the 42 occur, and they all occur during midnight.

| event concept:name               | count | unique | top      | freq |
| :------------------------------- | ----: | -----: | :------- | ---: |
| Create Purchase Requisition Item |     7 |      1 | 00:00:00 |    7 |
| Vendor creates debit memo        |    27 |      1 | 23:59:00 |   27 |
| Vendor creates invoice           |   284 |      1 | 23:59:00 |  284 |

_Table 2 - Events occuring before 2018_
<br><br><br>
Furthermore, we look at the amount of purchasing documents starting and ending each year, and see that there is a significant number of purchasing documents starting or ending after 2018 (Table 3). Since they can be scheduled events, we decided to keep all cases and purchasing orders that do not have any events prior to 2018. The other cases and thus purchasing documents are dropped.

| Year |  Events | Purchasing Documents starting | Purchasing Documents ending |
| ---: | ------: | ----------------------------: | --------------------------: |
| 1948 |      10 |                             1 |                           0 |
| 1993 |       9 |                             1 |                           0 |
| 2001 |      22 |                            15 |                           0 |
| 2008 |      45 |                             1 |                           0 |
| 2015 |       3 |                             2 |                           0 |
| 2016 |       6 |                             2 |                           0 |
| 2017 |     223 |                            75 |                           0 |
| 2018 | 1550468 |                         76241 |                       65268 |
| 2019 |   45135 |                            11 |                       11079 |
| 2020 |       2 |                             0 |                           2 |

_Table 3 - Purchasing Documents and Events with Purchasing Order start and end times_
<br><br><br>

##### Additional Findings for 2018

-   Peak in events during day 27-30 of the month
-   Peak in events during 00h-02h, 08h-15h and 21h-24h of the day.
-   Peak in events during January, December in a year.

## 1.3 Redundant columns

-   The columns **case Source** and **case Purch. Doc. Category** name are dropped as they contain only 1 value for the entire dataset. (Table 1)
-   The column **event org:resource** is dropped as it is duplicate to **event User**

## 1.4 Value Counts and Distributions

-   **case Company** is almost always _Company0000_ (99.63%).
-   **case Document Type** is almost always _Document Standard PO_ (96.49%)
-   **case Goods Receipt** is almost True (99.63%), this means that the third category (2-way matching) almost never occurs.

# 2 Entity Relationships

**Which of the variables is our case key?**

-   case Vendor has multiple case Name's, use case Vendor as primary key for case Name
-   case concept:name which corresponds to the Purchase item

-   UML diagram was made
-   What entities do we have?
    **Which attributes are specific to Purchase Document?**


-   "case Spend classification text" is interesting: it is not a Document Variable, since one Purchasing Document does not only have one value for this attribute, but most of Purchase Docs indeed only have one, only very few(2%) have multiple(exactly 2) values of this
    Hypothesis: These are empty values or other values and should be filled in with the most occurring value for a Doc


-   "case Sub spend area text" is unique for 71469 Purchase Documents, the rest has multiple values. We therefore keep it as purchase item attribute, although it is greatly influenced by which purchase doc does the item belong to


-   Most purchase documents only have one single purchase item (in fact, the median amount of purchase items per purchase document is 1, 75 percentile is 2)

-   When looking at the 0.1% of purchase documents with the most purchase items, still 75th percentile is only 131, while maximum amount of purchase items per purchase document is 429.


-   Surprisingly, "case Goods Receipt" is a variable of the Purchasing Document, although GR-based

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

# 3 Petri Nets & Process Models

# 4 Data Analysis
