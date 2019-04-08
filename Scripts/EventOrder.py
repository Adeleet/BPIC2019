from time import time

import numpy as np
import pandas as pd


class EventOrder:
    def __init__(self):
        self.events = None
        self.df_event_order = None
        self.sequences = None

    def __sorted_item_events__(self, groupby):
        return groupby.sort_values(by="Event Timestamp")["Event Name"].values

    def fit(self, df, immediate=True, verbose=False):
        """Fits EventOrder to sequences, create dataframe of order counts"""
        start_time = time()
        self.events = df["Event Name"].unique()
        self.df_event_order = pd.DataFrame(
            columns=self.events, index=self.events, data=0)

        if verbose:
            print("Started generating unique sequences.")

        # For each group (Item), sort by timestamp, return array of events
        self.sequences = df.groupby(
            "Item ID").apply(self.__sorted_item_events__)

        if verbose:
            print("Generated {} sequences, now creating order dataframe (immediate = {}).".format(
                self.sequences.shape[0], str(immediate)))

        # Iterate through each sequence (Item)
        for i in range(self.sequences.shape[0]):
            if verbose:
                if (i % max(1, round(self.sequences.shape[0] / 10)) == 0):
                    print("Sequence {}/{}".format(i +
                                                  1, self.sequences.shape[0]))

            sequence = self.sequences[i]
            # Iterate through each event 1 to n - 1 in sequence
            for i in range(sequence.shape[0] - 1):
                # Get subsequent events col for event i of order dataframe
                subsequent_events = self.df_event_order[sequence[i]]

                if immediate:
                    # Event B occuring IMMEDIATELY after Event A
                    # For that column, increase occurance number for event i + 1
                    subsequent_events[sequence[i + 1]] += 1
                else:
                    # Event B occuring ANY TIME after Event A
                    # For all subsequent events > i, increase occurance number
                    for j in range(i + 1, sequence.shape[0]):
                        subsequent_events[sequence[j]] += 1

                # Reassign subsequent evnts col for event i to order dataframe
                self.df_event_order[sequence[i]] = subsequent_events
        if verbose:
            print("Finished generating sequence order of {} sequences in {} seconds.".format(
                self.sequences.shape[0], str(round(time() - start_time, 1))))

    def first_event_probabilities(self, act1, act2):
        """Returns probability of act1, act2 happening first"""
        if act1 not in self.events or act2 not in self.events:
            raise ValueError(
                "This EventOrder has not been fitted yet! Please call the .fit method with a dataframe")
        n_act1 = self.df_event_order[act1][act2]
        n_act2 = self.df_event_order[act2][act1]
        if n_act1 == 0 and n_act2 == 0:
            return [0, 0]
        else:
            return [n_act1 / (n_act1 + n_act2), n_act2 / (n_act1 + n_act2)]
