#!/usr/bin/env python2
from flask import Flask, jsonify, request
from datetime import datetime
import base
import json

app = Flask(__name__)

@app.route('/chat/app.php.js')
def chat():
	callback = request.args.get('callback')
	cmd = request.args.get('cmd')
	if cmd == 'keep':
		output = json.dumps({"cmd":"keep","res":"1","desc":"keep succeed","events":base.keep()})
		return callback+'('+output+');'
	ID = request.args.get('id')
	to = request.args.get('to')
	if cmd == 'chat':
		base.chat({"to":ID,"from":to,"type":"disconnect","time":datetime.now().strftime("%H:%M%:S")})
		return callback+'('+json.dumps({"cmd":"chat","res":"1","desc":"send succeed"})+');'

if __name__ == "__main__":
        app.run(port=80, debug=False)
