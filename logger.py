#!/usr/bin/python
import yaml, umich_gak_utils, json
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import errors
from apiclient.discovery import build
from datetime import datetime, timedelta  

# Load the config
config = {}
with open('/etc/google-admin-kit.yml') as stream:
  configFile = yaml.load(stream)['google']
config.update(configFile['default'])
if 'google-report-logins' in configFile.keys() and configFile['google-report-logins'] is not None:
  config.update(configFile['google-report-logins'])

# Start up a new logger.
logger = umich_gak_utils.logger(config)

# Merge the gam credentials file into config
gam_credentials = json.load(open(config['credentials_file']))
config.update(gam_credentials)

# Create credentials
try:
  credential = SignedJwtAssertionCredentials(
    config['client_email'], 
    config['private_key'], 
    u'https://www.googleapis.com/auth/admin.reports.audit.readonly',
    sub=config['admin_account']
  )
except:
  logger.log("message='Unable to create credentials. Have you specified them in the admin kit config?'", 'ERR')
  exit(2)  

# Create an request object and authorize it with our credentials
http = credential.authorize(Http())
reports_service = build(u'admin', u'reports_v1', http=http)

# Create a start time of one hour to use to limit results.
start_time = (datetime.utcnow() - timedelta(hours=1)).isoformat('T') + u'Z'

# Declare a couple variables we'll need later.
all_logins = []
page_token = None
now = datetime.now()

# Define the parameters we'll use for the API call.
params = {u'applicationName': u'login', u'userKey': u'all', u'startTime': start_time}

# Start an infinite loop to pull data.
while True:
  try:

    # If we've got a page token, set it in the request parameters
    if page_token:
      params[u'pageToken'] = page_token

    # Grab the current page of logins
    current_page = reports_service.activities().list(**params).execute()
    
    # Try adding the current page's login items to the 'all_logins' list.
    try:
      all_logins.extend(current_page[u'items'])
    except:
      pass

    # Set the page token if one is available, if not, break the master loop.
    page_token = current_page.get(u'nextPageToken')
    if not page_token:
      break

  # Print out any errors that surface from the attempt to grab data.     
  except errors.HttpError as error:
    logger.log("message='{err}'".format(err=error), 'ERR')
    break

# Sometimes there's no source IP associated with the login.
for activity in all_logins:
  for event in activity[u'events']:
    activity.get(u'ipAddress', None)
    logger.log("time={time},user={user},src_ip={src_ip},action={action},app={app},login_type={login_type}".format(time=activity[u'id'][u'time'], user=activity[u'actor'][u'email'], src_ip=activity[u'ipAddress'], action=event[u'name'], app=activity[u'id'][u'applicationName'],login_type=event[u'parameters'][0][u'value']), 'INFO', False)


