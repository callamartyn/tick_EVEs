import sys
import pandas as pd

#read in BLAST result csv
df = pd.read_csv(sys.argv[1])

# first remove sequences with the same start or end position
# sort of e value, lowest (best) evalue is first
df.sort_values('evalue', inplace=True)
# drop hits that match in query name and start position, keeping the lower e-value
df.drop_duplicates(["direction", "position_on_query_start"], inplace=True, keep="first")
# drop hits that match in query name and stop position, keeping the lower e-value
df.drop_duplicates(["direction", "position_on_query_stop"], inplace=True, keep="first")
# reset indices
df.reset_index(inplace=True, drop=True)

# now remove hits that overlap by any amount, keeping the higher blast score
# group the dataframe by query
df_grouped=df.groupby('direction')

# list to store index that are either unique enough or have highest evalue
results = []
# list to save those that have already been added so they can be skiped
to_be_skipped = []

for group_name, df_group in df_grouped:

    for index, row in df_group.iterrows():

        # check if sequence or simmilar sequence already added
        if index in to_be_skipped:
            continue

        # initialize empty simmilar dict
        similar = {}

        for index2, row2 in df_group.iterrows():

            # check if possition start or stop is equal and is not self.
            if index == index2:
                continue

            # check if possition start or stop is equal and is not self.
                # if entry is comparing to itself
            if row[7] == row2[7] and row2[8] == row[8]:
                continue

            elif (row[7] in range(row2[7], row2[8]) or
            row2[7] in range(row[7], row[8]) or
            row[8] in range(row2[7], row2[8]) or
            row2[8] in range(row[7], row[8])):
                # add both indexes of simmilar sequences plus their score to the dict
                similar[index] = row[10]
                similar[index2] = row2[10]

        # check if simmilar sequences have been found
        if len(similar) > 0:

            # get the max score from the simmilar sequences
            max_index = max(similar, key=similar.get)

            # add index with maximum score to results list
            results.append(max_index)

            # add checked indices to be skipped list
            for k,v  in similar.items():
                to_be_skipped.append(k)

        # if seqeunce is unique add index to results
        if len(similar) == 0:
            results.append(index)
            to_be_skipped.append(index)

df_unique = df.loc[results]
df_unique.to_csv(sys.argv[2])