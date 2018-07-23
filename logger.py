from __future__ import print_function
from apiclient.discovery import build
import apiclient
from httplib2 import Http
from oauth2client import file, client, tools

import httplib2
import os
#import StringIO
from datetime import datetime, timedelta
from apiclient import errors
import json
import pickle


try:
    import argparse
    flags  = argparse.ArgumentParser(parents=[tools.argparser])
    flags.add_argument('-d','--date',required=False)
    flags.add_argument('-s','--save',help='Save last date received into file')
    flags.add_argument('-l','--load',help='Load start date from file')
    flags.add_argument('-v','--verbose',action='count',required=False)
    args = flags.parse_args()
except ImportError:
    flags = None

APPLICATION_NAME = 'VT audit log reader for elk'


def main():

    SCOPES = 'https://www.googleapis.com/auth/admin.reports.audit.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store, args)
    reports_service = build('admin', 'reports_v1', http=creds.authorize(Http()))

#Code goes here.

# Create a start time of one hour to use to limit results.
    if args.date:
        if args.date == "epoch":
	   start_time="1970-01-01T00:00:00.0Z"
        else:
	   start_time = args.date
    else:
        start_time = (datetime.utcnow() - timedelta(hours=1)).isoformat('T') + 'Z'

    if args.load:
        start_time = pickle.load( open( args.load, "rb" ) )	

# Declare a couple variables we'll need later.
    all_logins = []
    page_token = None
    now = datetime.now()
    
# Define the parameters we'll use for the API call.
    params = {'applicationName': 'login', 'userKey': 'all', 'startTime': start_time}
    
# Start an infinite loop to pull data.
    while True:
      try:
    
    # If we've got a page token, set it in the request parameters
        if page_token:
          params['pageToken'] = page_token
    
    # Grab the current page of logins
        current_page = reports_service.activities().list(**params).execute()
        
    # Try adding the current page's login items to the 'all_logins' list.
        try:
          all_logins.extend(current_page['items'])
        except:
          pass
    
    # Set the page token if one is available, if not, break the master loop.
        page_token = current_page.get('nextPageToken')
        if not page_token:
          break
    
  # Print out any errors that surface from the attempt to grab data.     
      except errors.HttpError as error:
        print("message='{err}'".format(err=error), 'ERR')
        break
    
# Sometimes there's no source IP associated with the login.
    for activity in all_logins:
      for event in activity['events']:
        activity.get('ipAddress', None)
#        logger.log("time={time},user={user},src_ip={src_ip},action={action},app={app},login_type={login_type}".format(time=activity[u'id'][u'time'], user=activity[u'actor'][u'email'], src_ip=activity[u'ipAddress'], action=event[u'name'], app=activity[u'id'][u'applicationName'],login_type=event[u'parameters'][0][u'value']), 'INFO', False)
        print(json.dumps(activity))
        last_time = activity[u'id'][u'time']

    if args.save:
        pickle.dump( last_time, open( args.save, "wb" ) )


if __name__ == '__main__':
    main()


