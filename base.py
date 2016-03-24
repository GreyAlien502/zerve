from basic import *
import json
import os
from datetime import datetime

def chat(destination,content):
	if destination == None:
		destination = 'zerving_hat'
	filename = folder() + 'tmp/' + destination
	message = {"to":destination,"from":content,"type":"disconnect","time":datetime.now().strftime("%H:%M%:S")}
	try:
		f = open(filename,'r+')
		messages = json.load(f)
		f.seek(0)
	except IOError:
		f = open(filename,'w+')
		print('error')
		messages = []
	messages.append(message)
	json.dump(messages,f)
	f.close()

def keep(ID='zerving_hat'):
	filename = folder() + 'tmp/' + ID
	try:
		f = open(filename,'r')
		messages = json.load(f)
		os.remove(filename)
	except IOError:
		messages = []
	return {"cmd":"keep","res":"1","desc":"keep succeed","events":messages}
