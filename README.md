# gpswebtrack

gpswebtrack is a simple gps position tracker. It basically draws a marker on a map
inside your browser, showing in realtime the gps position being fed into the server.
GPS fixes are expected to be accessile either locally or remotely through the well known
gpsd client protocol.

## Main Features
* gpswebtrack is written in Python
* it uses the [Flask](http://flask.pocoo.org/) web framework
* it uses [gevent-socketio](https://github.com/abourget/gevent-socketio) for realtime
communications from server to clients. gevent-socketio is a Python implementation of
the [socket.io](http://socket.io/) based on [gevent](http://www.gevent.org/)
* it uses gpsd python client library bindings for reading gps data

## Requirements
* Python related dependencies are automatically brought in by the installation script,
which is based on virtualenv.
* gps data must be provided by gpsd on its socket based interface. Please refer to gpsd documentation
to setup a working gpsd installation
* you must grant a few packages are installed on your distro before moving on with installation.
The following command should work for Debian based distributions:

<!-- -->

    sudo apt-get install git python-virtualenv python-dev gpsd python-gps

## Installation
    git clone https://github.com/gizero/gpswebtrack.git
    source ./venv_init.sh
    python map.py

## How to test
Connect your browser to: [http://localhost:5000](http://localhost:5000)
