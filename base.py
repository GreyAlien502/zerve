from basic import *
import json
import os

def chat(destination,content):
	if destination == None:
		destination = 'zerving_hat'
	filename = folder() + 'tmp/' + destination
	print(filename)
	try:
		f = open(filename,'r+')
		f.seek(0)
		messages = json.load(f)
		f.seek(0)
	except IOError:
		f = open(filename,'w')
		messages = []
	messages.append(content)
	json.dump(messages,f)
	f.truncate()
	f.close()

def keep(ID='zerving_hat'):
	filename = folder() + 'tmp/' + ID
	try:
		f = open(filename,'r')
		messages = json.load(f)
		os.remove(filename)
	except IOError:
		messages = []
	return messages
