import json
import os
import random
import sys
import requests
import re
import time

from flask import Flask, request, jsonify

from pymongo import MongoClient

app = Flask(__name__)

# Webhook for all requests
@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  msg = ''

  if data['name'] != os.getenv('BOT_NAME'):
    text = data['text']
    sender = data['name']

    if text.startswith(os.getenv('TRIGGER_ADD')):
      msg = add_bookmark(sender, text[len(os.getenv('TRIGGER_ADD')) + 1:])
    elif text.startswith(os.getenv('TRIGGER_SHOW')):
      bookmark = find_bookmark(text[len(os.getenv('TRIGGER_SHOW')) + 1:])
      msg = bookmark['name'] + ": " + bookmark['text']
    elif text.startswith(os.getenv('TRIGGER_ALL')):
      bookmarks = get_db().saved.find({})
      for bookmark in bookmarks:
        short_text =  bookmark['text'] if len(bookmark['text']) < 20 else bookmark['text'][:20] + '...'
        msg += bookmark['name'] + ": " + short_text + '\n'
    elif text.startswith(os.getenv('TRIGGER_DELETE')):
      msg = delete_bookmark(text[len(os.getenv('TRIGGER_DELETE')) + 1:])
    else: # save all messages that are not commands
      save_message(sender, text)

  if msg != '':
    # time.sleep(0.5)
    send_message(msg)
  return "ok", 200

# Bookmarks a string within double quotes or an older message if w/o quotes
def add_bookmark(sender, text):
  db = get_db()
  name = sender
  if text.startswith("\""):
    text = text[1:-1]
  else: # save a previously sent message
    message = find_message(text)
    text = message['text']
    name = message['name']

  saved = find_bookmark(text)
  if saved != None and saved['text'] == text:
    return 'That one was already saved. 😕'

  doc = { 'text': text, 'name': name, 'timestamp': str(time.time()) }
  db.saved.insert_one(doc)
  return 'Saved. 🎉'

# Finds the latest bookmark that contains the given text
def find_bookmark(text):
  db = get_db()
  regx = re.compile(".*" + text + ".*", re.IGNORECASE)
  return db.saved.find_one({ 'text': {'$regex': regx} }, sort=[('timestamp', -1)])

# Finds a saved bookmark that contains the given substring and then deletes it
def delete_bookmark(text):
  bookmark = find_bookmark(text)
  get_db().saved.delete_one({ 'text': bookmark['text'] })
  short_text = bookmark['text'] if len(bookmark['text']) < 50 else bookmark['text'][:50] + '...'
  return 'Deleted bookmark: ' + short_text 

# Adds message to database, deleting all the ones older than 24h
def save_message(sender, text):
  db = get_db()
  doc = { 'text': text, 'name': sender, 'timestamp': str(time.time()) }
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
  db_name = uri[uri.rindex('/') + 1 :]
  client = MongoClient(uri)
  return client[db_name]

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
