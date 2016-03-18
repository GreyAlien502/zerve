from basic import *
import json

def chat(destination,content):
	filename = folder() + 'tmp/' + destination
	f = open(filename,'w+')
	try:
		messages = json.load(f)
	except JSONDecodeError:
		messages = []
	messages.append(content)
	json.dump(messages,f)
	f.close()

def keep(id=None):
	filename = folder() + 'tmp/' + 'zerving_hat'
	f = open(filename,'w+')
	messages = json.load(f)
	json.dump([],f)
	f.close()
	return messages
