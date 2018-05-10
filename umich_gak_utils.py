import syslog
from datetime import datetime

class logger:

  def __init__(self, config):
    logs = {
      'local0': syslog.LOG_LOCAL0,
      'local1': syslog.LOG_LOCAL1,
      'local2': syslog.LOG_LOCAL2,
      'local3': syslog.LOG_LOCAL3,
      'local4': syslog.LOG_LOCAL4,
      'local5': syslog.LOG_LOCAL5,
      'local6': syslog.LOG_LOCAL6,
      'local7': syslog.LOG_LOCAL7
    }
    syslog.openlog(facility=logs[config['log_facility']], logoption=syslog.LOG_PID)

  def log(self, message, priority=False, to_stdout=True):
    priorities = {
      'DEBUG'   : {'color':'\033[92m', 'priority':syslog.LOG_DEBUG},
      'WARNING' : {'color':'\033[93m', 'priority':syslog.LOG_WARNING},
      'ERR'     : {'color':'\033[91m', 'priority':syslog.LOG_ERR},
      'INFO'    : {'color':'\033[96m', 'priority':syslog.LOG_INFO}
    }
    syslog.syslog(priorities[priority]['priority'], '[{priority}] {message}'.format(**locals()))
    if to_stdout:
      print('{color}[{timestamp}] {message}\033[0m'.format(color=priorities[priority]['color'], timestamp=datetime.now().strftime('%b %d %H:%M:%S'), message=message))

  def __del__(self):
    syslog.closelog()

