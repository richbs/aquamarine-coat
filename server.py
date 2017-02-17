import os
import sys
import gmusicapi
from gmusicapi import Mobileclient

print os.environ

api = Mobileclient()
print 'logging in...'
login = api.login(
    os.environ["EMAIL"], os.environ["PASSWORD"],
    Mobileclient.FROM_MAC_ADDRESS, 'en_GB'
)

from flask import Flask, send_from_directory, jsonify, request, render_template
app = Flask(__name__, static_folder='views')

data = {
  "dreams": [
    "Find and count some sheep",
    "Climb a really tall mountain",
    "Wash the dishes"
  ]
}

@app.route("/")
def hello():

  print 'login = ', login

  print 'getting playlists...'
  playlists = api.get_all_user_playlist_contents()
  print 'playlists got'
  mill = 1000000
  return render_template('index.html', playlists=playlists)

@app.route("/dreams", methods=["GET"])
def get_dreams():
  return jsonify(**data)

@app.route("/dreams", methods=["POST"])
def add_dream():
  data["dreams"].append(request.args["dream"])
  return '"OK"'

@app.route('/<path:path>')
def send_static(path):
  return send_from_directory('public', path)

if __name__ == "__main__":
  app.run()
