from flask import Flask, render_template
import werkzeug.serving
from socketio.server import SocketIOServer
from gevent import monkey

app = Flask(__name__)
monkey.patch_all()

lat1 = 45.864373
lng1 = 9.430089
lat2 = 45.864373
lng2 = 9.431195

@app.route("/")
def map(lat1=lat1, lng1=lng1, lat2=lat2, lng2=lng2):
  return render_template('map.html', lat1=lat1, lng1=lng1, lat2=lat2, lng2=lng2)

@werkzeug.serving.run_with_reloader
def run_dev_server():
  app.debug = True
  port = 5000
  SocketIOServer(('', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
  run_dev_server()
