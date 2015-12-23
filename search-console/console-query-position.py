#!/usr/bin/python
# from https://github.com/google/google-api-python-client/blob/master/samples/searchconsole/search_analytics_api_sample.py

# -*- coding: utf-8 -*-
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example for using the Google Search Analytics API (part of Search Console API).
A basic python command-line example that uses the searchAnalytics.query method
of the Google Search Console API. This example demonstrates how to query Google
search results data for your property. Learn more at
https://developers.google.com/webmaster-tools/
To use:
1) Install the Google Python client library, as shown at https://developers.google.com/webmaster-tools/v3/libraries.
2) Sign up for a new project in the Google APIs console at https://code.google.com/apis/console.
3) Register the project to use OAuth2.0 for installed applications.
4) Copy your client ID, client secret, and redirect URL into the client_secrets.json file included in this package.
5) Run the app in the command-line as shown below.
Sample usage:
  $ python search_analytics_api_sample.py 'https://www.gov.uk/' '2015-11-01' '2015-11-30'
"""

import argparse
import sys
import pandas
from googleapiclient import sample_tools

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))
#argparser.add_argument('keyword', type=str,
#                       help=('keyword being searched for.'))

keyword = raw_input('Enter the search term: ')

url = raw_input('Enter the full URL of the page: ')

#save_table = []

def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')



  # Get the top 1000 queries in India, sorted by click count, descending.
  request = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['date','query'],
      'dimensionFilterGroups': [{
          'filters': [{
              'dimension': 'query',
              'operator': 'contains',
              'expression': keyword
             }, {
              'dimension': 'page',
              'expression': url
          }]
      }],
      'rowLimit': 100
  }
  response = execute_request(service, flags.property_uri, request)
  #print_table(response, 'Workplace Pensions')
  #save_file(response)
  new_file(response)


def execute_request(service, property_uri, request):
  """Executes a searchAnalytics.query request.
  Args:
    service: The webmasters service to use when executing the query.
    property_uri: The site or app URI to request data for.
    request: The request to be executed.
  Returns:
    An array of response rows.
  """
  return service.searchanalytics().query(
      siteUrl=property_uri, body=request).execute()


def print_table(response, title):
  """Prints out a response table.
  Each row contains key(s), clicks, impressions, CTR, and average position.
  Args:
    response: The server response to be printed as a table.
    title: The title of the table.
  """
  print title + ':'

  if 'rows' not in response:
    print 'Empty response'
    return

  rows = response['rows']
  row_format = '{:<20}' + '{:>20}' * 4
  print row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position')
  for row in rows:
    keys = ''
    # Keys are returned only if one or more dimensions are requested.
    if 'keys' in row:
      keys = u','.join(row['keys']).encode('utf-8')
    print row_format.format(
        keys, row['clicks'], row['impressions'], row['ctr'], row['position'])


def new_file(response):
    new_output = []
    if 'rows' not in response:
      print 'Empty response'
      return
    rows = response['rows']
    for row in rows:
        if 'keys' in row:
            keys = u','.join(row['keys']).encode('utf-8')
        #print keys","row['clicks']","row['impressions']","row['ctr']","row['position']
        print '{0},{1},{2},{3},{4}'.format(keys,row['clicks'],row['impressions'],row['ctr'],row['position'])
    print new_output
    #print row ['clicks'], row['impressions'], row['ctr'], row['position']
    #new_output = pandas.DataFrame.from_dict(response, orient = 'columns')
    #new_output.to_csv('output.csv', sep=',')
    #print new_output

"""
def save_file(response):
    rows = response['rows']
    row_format = '{:<20}' + '{:>20}' * 4
    #print row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position')
    for row in rows:
      keys = ''
      # Keys are returned only if one or more dimensions are requested.
      if 'keys' in row:
        keys = u','.join(row['keys']).encode('utf-8')
      row_response = row_format.format(
          keys, row['clicks'], row['impressions'], row['ctr'], row['position'])

    output = pandas.DataFrame(row_response,index=None)
    output.to_csv('output2.csv', sep=',')
"""
if __name__ == '__main__':
  main(sys.argv)
