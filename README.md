# ipython-notebooks
Somewhere to put a range of borrowed and adapted ipython notebooks

### Coursera ipynb
This is adapted from http://adilmoujahid.com/posts/2015/03/coursera-data-mining/. This notebook:

- downloads data from 3 free Coursera APIs
- structures this data into 3 dataframes
- indexes each of the dataframes around the ID columns
- creates a function that maps IDs to names
- changes IDs to names in a master dataframe
- looks up additional data on social media sharing from the sharedcount.com API
- orders the master dataframe by the most shared courses

### Top blog posts
My script. This notebook:

- reads a local csv file (a simple GA file with Page title, slug and pageviews)
- adds 'https://' onto every slug in that column
- defines a function which uses an API key to get data off SharedCount for a URL
- runs this for every URL in the column and places it in a new column
- selects subsections of the data in that column in several new columns
- writes this dataframe back to a csv
