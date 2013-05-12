from flask import Flask, render_template
app = Flask(__name__)

lat = 45.864373
lng = 9.430089

@app.route("/")
def map(lat=lat, lng=lng):
  return render_template('map.html', lat=lat, lng=lng)

if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0')

