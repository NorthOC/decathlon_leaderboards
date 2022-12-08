import calendar
import time

# Returns a timestamp in the form of a string
def get_timestamp():
  current_GMT = time.gmtime()

  ts = str(calendar.timegm(current_GMT))
  return ts