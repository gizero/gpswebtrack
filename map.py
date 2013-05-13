from flask import Flask, render_template
import werkzeug.serving
from socketio.server import SocketIOServer
from gevent import monkey

app = Flask(__name__)
monkey.patch_all()

lat = 45.864373
lng = 9.430089

@app.route("/")
def map(lat=lat, lng=lng):
  return render_template('map.html', lat=lat, lng=lng)

@werkzeug.serving.run_with_reloader
def run_dev_server():
  app.debug = True
  port = 5000
  SocketIOServer(('', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
  run_dev_server()
