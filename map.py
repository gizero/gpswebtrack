from flask import Flask, render_template, Response, request
import werkzeug.serving
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.server import SocketIOServer
import gevent
from gevent import monkey

app = Flask(__name__)
monkey.patch_all()

lat = 45.864373
lng = 9.430089

@app.route("/")
def map(lat=lat, lng=lng):
  return render_template('map.html', lat=lat, lng=lng)

@app.route("/socket.io/<path:rest>")
def stream(rest):
  try:
    socketio_manage(request.environ, {'/stream': StreamNamespace}, request)
  except:
    app.logger.error("Exception while handling socketio connection", exc_info=True)
  return Response()

class StreamNamespace(BaseNamespace):
  sockets = {}
  def recv_connect(self):
    print "Got a socket connection"
    self.sockets[id(self)] = self
  def disconnect(self, *args, **kwargs):
    if id(self) in self.sockets:
      del self.sockets[id(self)]
    super(StreamNamespace, self).disconnect(*args, **kwargs)
  @classmethod
  def broadcast(self, event, message):
    for ws in self.sockets.values():
      ws.emit(event, message)

@app.route("/trigger")
def trigger():
  StreamNamespace.broadcast('message', 'This is the message payload')
  return Response('The trigger has been pulled')

class Generator:
  def __init__(self):
    self.coords = file('test/resegup-kml-test/rawcoords','r').read().split(' ')
    self.mygen = self.next_point_generator_function()

  def next_point_generator_function(self):
    while True:
      for index in range(len(self.coords)):
        yield self.coords[index]

class LatLng:
  def __init__(self, lat, lng):
    self.lat = float(lat)
    self.lng = float(lng)
  def __str__(self):
    return "Lat: %f, Lng: %f" % (self.lat, self.lng)

INTERVAL = 1

def callback(generator):
  pointstr = next(generator.mygen)
  coords = pointstr.split(',')
  point = LatLng(coords[1], coords[0])
  print '! ', point
  StreamNamespace.broadcast('message', '{ "lat": "%f", "lng": "%f" }' % (point.lat, point.lng))

def loop():
  mygen = Generator()
  while True:
    # swap latlng every INTERVAL seconds
    gevent.sleep(INTERVAL)
    callback(mygen)

@werkzeug.serving.run_with_reloader
def run_dev_server():
  app.debug = True
  port = 5000
  print "Starting latlng generator server..."
  gl = gevent.Greenlet.spawn(loop)
  print "Starting map server..."
  SocketIOServer(('', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
  run_dev_server()
