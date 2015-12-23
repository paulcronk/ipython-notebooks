## TOP SOCIAL SHARING script using sharedcount.com

import urllib2
import json
import pandas as pd
import csv

# Upload posts CSV file into a pandas dataframe
posts_df = pd.read_csv('pages.csv')
print posts_df.head()

# Add the 'https://www.gov.uk' onto every URL slug in the posts_df['Page'] column
posts_df['Page'] = 'https://www.gov.uk' + posts_df['Page'].astype(str)
print posts_df.head()

# Define a function that calls up data from Sharedcount.com for each URL and uses my API key
def get_social_metrics(url, api_key):
    sharedcount_response = urllib2.urlopen('https://free.sharedcount.com/?url=' + url + '&apikey=' + api_key)
    return json.load(sharedcount_response)

# API key defined. Runs function against each row in that column, placing data into a new column.
SHAREDCOUNT_API_KEY = '2c8787d463e1be55a6ef68b1a341ccc0ccb41697'
posts_df['sharedcount_metrics'] = map(lambda Page: get_social_metrics(Page, SHAREDCOUNT_API_KEY), posts_df['Page'])
print posts_df.head()

# Extract selected fields from the sharedcount.com data and put them in their own columns
posts_df['Twitter'] = map(lambda sharedcount: sharedcount['Twitter'], posts_df['sharedcount_metrics'])
posts_df['LinkedIn'] = map(lambda sharedcount: sharedcount['LinkedIn'], posts_df['sharedcount_metrics'])
posts_df['Facebook shares'] = map(lambda sharedcount: sharedcount['Facebook']['share_count'], posts_df['sharedcount_metrics'])
posts_df['Facebook likes'] = map(lambda sharedcount: sharedcount['Facebook']['like_count'], posts_df['sharedcount_metrics'])
posts_df['Facebook comments'] = map(lambda sharedcount: sharedcount['Facebook']['comment_count'], posts_df['sharedcount_metrics'])
print posts_df.head()

# Writes dataframe to CSV
posts_df.to_csv('social-shares.csv')
