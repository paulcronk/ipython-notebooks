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


import argparse
import sys
import pandas as pd
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

# an example of the command line might be:
# $ python search_analytics_api_sample.py 'https://www.gov.uk/' '2015-11-01' '2015-11-30'

keyword = raw_input('Enter the search term (or leave it blank for all searches): ')

url = raw_input('Enter the full URL of the page (or a partial match): ')

#save_table = []

def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')


  # For a given landing page, which search terms bring traffic to that page (impressions, clicks and CTR)
  # and what position does the page appear? How does this change over time?

  # This is set up to request three dimensions (date, query/keyword, landing page) and
  # is filtered by keyword and landing page. The filter is 'contains'.

  request = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['date','query','page'],
      'dimensionFilterGroups': [{
          'filters': [{
              'dimension': 'query',
              'operator': 'contains',
              'expression': keyword
             }, {
              'dimension': 'page',
              'operator': 'contains',
              'expression': url
          }]
      }],
      'rowLimit': 5000
  }
  response = execute_request(service, flags.property_uri, request)
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

def new_file(response):
    new_output = []
    if 'rows' not in response:
      print 'Empty response'
      return
    rows = response['rows']
    for row in rows:
        temp_list = []
        if 'keys' in row:
            keys = u','.join(row['keys']).encode('utf-8')
        temp_list = (keys,row['clicks'],row['impressions'],row['ctr'],row['position'])
        new_output.append(temp_list)
    print new_output
    new_output = pd.DataFrame(new_output)
    new_output.columns = ['date,query,url', 'clicks', 'impressions', 'ctr', 'position']
    new_output.to_csv('output.csv', sep=',')

if __name__ == '__main__':
  main(sys.argv)
