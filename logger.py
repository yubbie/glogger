#!/bin/python

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
    flags.add_argument('-d','--date',required=False,help='Start date for report in YYY-MM-DDTHH:MM:SS.MZ format.  Use the word epoch for all available logs')
    flags.add_argument('-s','--save',help='Save last date received into file')
    flags.add_argument('-l','--load',help='Load start date from file')
    flags.add_argument('-v','--verbose',action='count',required=False,help='Raise logging level')
    flags.add_argument('-a','--appname',required=False,default='login',help='Appname for API')
    flags.add_argument('-e','--eventname',required=False,help='Optional Event type for query')
    args = flags.parse_args()
except ImportError:
    flags = None

APPLICATION_NAME = 'VT audit log reader for elk'

def debug(text,level,trigger):
    
    if level >= trigger:
       print('[DEBUG] ' + text)


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
	debug('default starttime ' + start_time,args.verbose,2)

    if args.load:
        try:
          start_time = pickle.load( open( args.load, "rb" ) )	
          debug('loaded start time ' + start_time,args.verbose,2)
        except:
          debug('failed to load pickle ' + args.load,args.verbose,1)

    debug('Final time select is ' + start_time,args.verbose,2)

# Declare a couple variables we'll need later.
    all_logins = []
    page_token = None
    now = datetime.now()
    last_time = start_time

# Define the parameters we'll use for the API call.
    if args.eventname:
       params = {'applicationName': args.appname, 'userKey': 'all', 'startTime': start_time, 'eventName': args.eventname}
    else:
       params = {'applicationName': args.appname, 'userKey': 'all', 'startTime': start_time}
    
# Start an infinite loop to pull data.
    while True:
      try:
    
    # If we've got a page token, set it in the request parameters
        if page_token:
          params['pageToken'] = page_token
    
    # Grab the current page of logins
        current_page = reports_service.activities().list(**params).execute()
        
        all_logins=current_page['items']

    # Try adding the current page's login items to the 'all_logins' list.
#        try:
#          all_logins.extend(current_page['items'])
#        except:
#          pass
    
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
          print(json.dumps(activity))
  	if last_time < activity[u'id'][u'time']:
             last_time = activity[u'id'][u'time']

    if args.save:
        pickle.dump( last_time, open( args.save, "wb" ) )
        debug('saving time ' + last_time,args.verbose,2);

if __name__ == '__main__':
    main()


