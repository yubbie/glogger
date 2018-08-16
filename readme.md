# glogger

Processes the google activity logs via the activity api and pulls down the
json data for crunching by something else.  Great for shoving into 
filebeats for transfer to elk, for instance.

```
usage: glogger.py [-h] [--auth_host_name AUTH_HOST_NAME]
                  [--noauth_local_webserver]
                  [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                  [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-d DATE] [-s SAVE] [-l LOAD] [-v] [-a APPNAME]
                  [-e EVENTNAME] [-f FILTER] [-m MAXRESULTS]

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
  -d DATE, --date DATE  Start date for report in YYY-MM-DDTHH:MM:SS.MZ format.
                        Use the word epoch for all available logs
  -s SAVE, --save SAVE  Save last date received into file
  -l LOAD, --load LOAD  Load start date from file
  -v, --verbose         Raise logging level
  -a APPNAME, --appname APPNAME
                        Appname for API
  -e EVENTNAME, --eventname EVENTNAME
                        Optional Event type for query
  -f FILTER, --filter FILTER
                        Optional filter for query
  -m MAXRESULTS, --maxresults MAXRESULTS
                        Optional maxResults setting
```

## Installation

Note those first few arguments are from google oauth library.  Make a file called `token.json` in the working directory.  Run it with `--noauth_local_webserver` if you're not somewhere a browser can fork, and follow the oauth dialog.  If you've installed GAM or another similar tool, you've seen this before.  You'll need an api project that enables at least admin.reports.audit.readonly

Anyone who wants to contribute a step by step set of instructions would be great - otherwise I'd go read GAM "do it yourself" instructions.

## Examples:

`glogger.py`

Dump the last hour of data available from the login activities log.

`glogger.py -a drive -d epoch -s timestamp.s -f "doc_type==team_drive"`

Show all events back to the earliest recorded for the drive activity log where the target was a team drive, and save the timestamp of the last event for future use as a starting point.

`glogger.py -a drive -l timestamp.s -s timestamp.s -e ACCESS -f "doc_id==1f99834400349asdf"`

Show drive activity events since the timestamp stored in timestamp.s, where the event type was ACCESS and the document id of the item was 1f99834400349asdf.  Save the last time stamp back into timestamp.s for future use.
