import time
import os
import json

def folder():
	return os.getenv('HOME')+"/zerved/"
def readJSON(filename):
	f = open(filename,'r')
	out = json.load(f)
	f.close()
	return out
def writeJSON(filename,content):
	f = open(filename,'w')
	out = f.write(json.dumps(content))
	f.close()
	return out

def home(contents):
	return 'Welcome '+contents['username']+'.'

def log(message):
	logfile = open(folder()+'log','a')
	logfile.write(message)
	logfile.close
