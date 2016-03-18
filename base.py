from basic import *
import json

def chat(destination,content):
	filename = folder() + 'tmp/' + destination
	f = open(filename,'w+')
	try:
		messages = json.load(f)
	except json.JSONDecodeError:
		messages = []
	messages.append(content)
	json.dump(messages,f)
	f.close()

def keep(ID='zerving_hat'):
	filename = folder() + 'tmp/' + ID
	f = open(filename,'w+')
	try:
		messages = json.load(f)
	except json.JSONDecodeError:
		messages = []
	json.dump([],f)
	f.close()
	return messages
