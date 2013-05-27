import gps

def run(debug=False, callback=None):

  #session = gps.gps(host='gizdesk.local')
  session = gps.gps(host='192.168.0.10')
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
        if callback:
          callback(lat, lon)
  except StopIteration:
    print "GPSD has terminated"

if __name__ == "__main__":
  run()
