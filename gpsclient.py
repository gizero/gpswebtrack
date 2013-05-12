import gps

debug=False

session = gps.gps(host='gizdesk.local')
session.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)

try:
  while True:
    report = session.next()
    if debug:
      print report
    if report['class'] == 'TPV':
      lat = report.lat
      lon = report.lon
      print 'LAT: %s; LON: %s' % (lat, lon)
except StopIteration:
  print "GPSD has terminated"
