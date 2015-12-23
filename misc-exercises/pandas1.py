# Import all libraries needed for the tutorial

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv
# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number

# Enable inline plotting
%matplotlib inline

print 'Python version ' + sys.version
print 'Pandas version ' + pd.__version__

# Create Data¶
# The data set will consist of 5 baby names and the number of births recorded for that year (1880).

# The inital set of baby names and birth rates
names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]

# To merge these two lists together we will use the zip function.
BabyDataSet = zip(names,births)
BabyDataSet

# We are basically done creating the data set. We now will use the pandas library to export this data set into a csv file.

# df will be a DataFrame object. You can think of this object holding the contents of the BabyDataSet 
# in a format similar to a sql table or an excel spreadsheet. Lets take a look below at the contents inside df.
df = pd.DataFrame(data = BabyDataSet, columns=['Names', 'Births'])
df

# Export the dataframe to a csv file. We can name the file births1880.csv. The function to_csv will be used to export the file. 
# The file will be saved in the same location of the notebook unless specified otherwise.
# The only parameters we will use is index and header. 
# Setting these parameters to True will prevent the index and header names from being exported. 
df.to_csv(r'D:\GitHub\ipython-notebooks\births1880.csv',index=False,header=False)

#Get data
Location = r'D:\GitHub\ipython-notebooks\births1880.csv'
df = pd.read_csv(Location)
# Notice the r before the string. Since the slashes are special characters, prefixing the string with a r will escape the whole string.
df
# This brings us the our first problem of the exercise. The read_csv function treated the first record in the csv file as the header names. 
# This is obviously not correct since the text file did not provide us with header names.
# If we wanted to give the columns specific names, we would have to pass another paramter called names
df = pd.read_csv(Location, names=['Names','Births'])
df