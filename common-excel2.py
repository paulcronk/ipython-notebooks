import pandas as pd
import numpy as np

df = pd.read_excel('sample-salesv3.xlsx')
print df.dtypes

# convert date column from object to datetime format
df['date'] = pd.to_datetime(df['date'])
print df.head()

# filtering the data
print df[df["account number"]==307599].head()

# or try
print df[df["quantity"] > 22].head()

# for more complex filtering use map to filter on various criteria. In this example, lets look for items with skus that start with B1
print df[df["sku"].map(lambda x: x.startswith('B1'))].head()

# multiple filtering
print df[df["sku"].map(lambda x: x.startswith('B1')) & (df["quantity"] > 22)].head()


# another filter is isin. . It allows us to define a list of values we want to look for. In this case, we look for all records that include two specific account numbers.
print df[df["account number"].isin([714466,218895])].head()

# Pandas supports another function called query which allows you to efficiently select subsets of data. 
# If you would like to get a list of customers by name, you can do that with a query, similar to the python syntax shown above.
print df.query('name == ["Kulas Inc","Barton LLC"]').head()

# WORKING WITH DATES
# Using pandas, you can do complex filtering on dates. Before doing anything with dates, 
# I encourage you to sort by the date column to make sure the results return what you are expecting.
df = df.sort('date')
print df.head()

# and add a filter too
print df[df['date'] >='20140905'].head()

#  If we want to only look for data more recent than a specific month, we can do so.
print df[df['date'] >='2014-03'].head()

# Or chain the criteria
print df[(df['date'] >='20140701') & (df['date'] <= '20140715')]

# you can express the date value in multiple formats and it will give you the results you expect
print df[df['date'] >= 'Oct-2014'].head()

# or
print df[df['date'] >= '10-10-2014'].head()

# When working with time series data, if we convert the data to use the date as as the index, we can do some more filtering variations.
# Set the new index using set_index
df2 = df.set_index(['date'])
print df2.head()

# then you can slice the data to get a range
print df2["20140101":"20140201"].head()

# and can use various date representations to remove any ambiguity around date naming conventions
print df2["2014-Jan-1":"2014-Feb-1"]

# or
print df2["2014"].head()

# or
print df2["2014-Dec"].head()

