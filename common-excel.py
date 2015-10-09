## EXAMPLES OF SOME COMMON EXCEL FUNCTIONS PERFORMED IN PYTHON ##
## adding columns
## populating columns

import pandas as pd
import numpy as np

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
