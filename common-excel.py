## EXAMPLES OF SOME COMMON EXCEL FUNCTIONS PERFORMED IN PYTHON ##
## adding columns
## populating columns with calculated total of other columns
## adding and fuzzy-matching a column
## grouping some dataframe
## formatting the currency
## tidying the table

import pandas as pd
import numpy as np
import difflib
import fuzzywuzzy

# basic import of excel file into dataframe
df = pd.read_excel("excel-comp-data.xlsx")
print df.head()

# adding a new column which will comtain a calculation of other columns
df["total"] = df["Jan"] + df["Feb"] + df["Mar"]
print df.head()

# looking at column totals, means, min & max
print df["Jan"].sum(), df["Jan"].mean(),df["Jan"].min(),df["Jan"].max()

# (1) create df to contain month (and total) totals
sum_row=df[["Jan","Feb","Mar","total"]].sum()
print sum_row

# (2) Transpose this df to make it easier to add to main dataframe
df_sum=pd.DataFrame(data=sum_row).T
print df_sum

# (3) fill in the cells for the other columns reindex does this
df_sum=df_sum.reindex(columns=df.columns)
print df_sum

# (4) now append that totals row to the bottom
df_final=df.append(df_sum,ignore_index=True)
print df_final.tail()

## ADDING SOME FUZZY MATCHING

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
state_to_code = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA": "IA", "Armed Forces Pacific": "AP", "GUAM": "GU",
                 "KANSAS": "KS", "FLORIDA": "FL", "AMERICAN SAMOA": "AS", "NORTH CAROLINA": "NC", "HAWAII": "HI",
                 "NEW YORK": "NY", "CALIFORNIA": "CA", "ALABAMA": "AL", "IDAHO": "ID", "FEDERATED STATES OF MICRONESIA": "FM",
                 "Armed Forces Americas": "AA", "DELAWARE": "DE", "ALASKA": "AK", "ILLINOIS": "IL",
                 "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD", "CONNECTICUT": "CT", "MONTANA": "MT", "MASSACHUSETTS": "MA",
                 "PUERTO RICO": "PR", "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH", "MARYLAND": "MD", "NEW MEXICO": "NM",
                 "MISSISSIPPI": "MS", "TENNESSEE": "TN", "PALAU": "PW", "COLORADO": "CO", "Armed Forces Middle East": "AE",
                 "NEW JERSEY": "NJ", "UTAH": "UT", "MICHIGAN": "MI", "WEST VIRGINIA": "WV", "WASHINGTON": "WA",
                 "MINNESOTA": "MN", "OREGON": "OR", "VIRGINIA": "VA", "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH",
                 "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC", "INDIANA": "IN", "NEVADA": "NV", "LOUISIANA": "LA",
                 "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE", "ARIZONA": "AZ", "WISCONSIN": "WI", "NORTH DAKOTA": "ND",
                 "Armed Forces Europe": "AE", "PENNSYLVANIA": "PA", "OKLAHOMA": "OK", "KENTUCKY": "KY", "RHODE ISLAND": "RI",
                 "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR", "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}

# testing syntax
print process.extractOne("Minnesotta",choices=state_to_code.keys())
print process.extractOne("AlaBAMMazzz",choices=state_to_code.keys(),score_cutoff=80)

# We create our function to take the state column and convert it to a valid abbreviation.
# We use the 75 score_cutoff for this data.

def convert_state(row):
    abbrev = process.extractOne(row["state"],choices=state_to_code.keys(),score_cutoff=75)
    if abbrev:
        return state_to_code[abbrev[0]]
    return np.nan

# this adds an empty column in position 6
df_final.insert(6, "abbrev", np.nan)
df_final.head()

# the apply adds the abbreviations into the correct column
df_final['abbrev'] = df_final.apply(convert_state, axis=1)
print df_final

## ADD SOME SUBTOTAL GROUPINGS

# we want to get some monthly subtotals by state using groupby
df_sub=df_final[["abbrev","Jan","Feb","Mar","total"]].groupby('abbrev').sum()
print df_sub

## SORT OUT CURRENCY

# use applymap in a function to add currency values to all the cells in the df
def money(x):
    return "${:,.0f}".format(x)

formatted_df = df_sub.applymap(money)
print formatted_df

# add a totals row (as before)
sum_row=df_sub[["Jan","Feb","Mar","total"]].sum()
print sum_row

# Transpose the values to columns and format it
df_sub_sum=pd.DataFrame(data=sum_row).T
df_sub_sum=df_sub_sum.applymap(money)
print df_sub_sum

# then append the row to the dataframe
final_table = formatted_df.append(df_sub_sum)
print final_table

# the index column for the final row is '0', so need to rename that
final_table = final_table.rename(index={0:"Total"})
print final_table
