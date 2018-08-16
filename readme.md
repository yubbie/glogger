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