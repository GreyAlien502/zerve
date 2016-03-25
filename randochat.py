#!/usr/bin/env python2
from flask import Flask, jsonify, request, Response
from datetime import datetime
from urllib import unquote
import base
import json

app = Flask(__name__)

@app.route('/chat/app.php.js')
def chat():
	callback = unquote(request.args.get('callback'))
	cmd = unquote(request.args.get('cmd'))
	ID = unquote(request.args.get('id'))
	if cmd == 'keep':
		return Response(callback+'('+json.dumps(base.keep(ID))+');',mimetype='application/javascript')
	to = unquote(request.args.get('to'))
	if cmd == 'chat':
		base.chat(ID,to)
		return Response(callback+'('+json.dumps({"cmd":"chat","res":"1","desc":"send succeed"})+');','application/javascript')

if __name__ == "__main__":
        app.run(port=80, debug=False)
