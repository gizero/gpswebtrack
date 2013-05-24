from flask import Flask, render_template, Response, request
import werkzeug.serving
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.server import SocketIOServer
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

@werkzeug.serving.run_with_reloader
def run_dev_server():
  app.debug = True
  port = 5000
  print "Starting map server..."
  SocketIOServer(('', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
  run_dev_server()
