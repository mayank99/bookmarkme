import json
import os
import random
import sys
import requests
import re
import time

import xmltodict
from flask import Flask, request, jsonify

from pymongo import MongoClient

app = Flask(__name__)

# Webhook for all requests
@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  log('Recieved {}'.format(data))
  
  msg = ''
  if data['name'] != os.getenv('BOT_NAME'):
    text = data['text'].lower()
    if text.startswith(os.getenv('TRIGGER_ADD')):
      add_bookmark(text)
    # if text.startswith(os.getenv('TRIGGER_SHOW')):
    msg = 'ok'
  send_message(msg)
  return "ok", 200

# Extracts relevant text and saves to db
def add_bookmark(full_text):
  text = full_text[len(os.getenv('TRIGGER_ADD')) + 1:]
  save_message(text)

# Adds message to database, deleting all the ones older than 24h
def save_message(text):
  db = get_db()
  doc = { 'text': text, 'timestamp': str(time.time()) }
  db.messages.insert_one(doc)
  db.messages.remove({'timestamp': { '$lt': str(time.time() - 86400) } })

# Finds the last message that contains the given substring
def find_message(text):
  db = get_db()
  regx = re.compile(".*" + text + ".*", re.IGNORECASE)
  return db.messages.find_one({ 'text': {'$regex': regx} }, sort=[('timestamp', -1)])

# Returns the MongoDB instance
def get_db():
  uri = os.getenv('MONGODB_URI')
  db_name = uri[uri.index('/') + 1 : uri.index(':', 10)]
  client = MongoClient(uri)
  return client.db_name

# Sends the chosen message to the chat
def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'
  data = {
          'bot_id' : os.getenv('BOT_ID'),
          'text'   : msg,
         }
  requests.post(url, data)  

# Debug
def log(msg):
  print(str(msg))
  sys.stdout.flush()
