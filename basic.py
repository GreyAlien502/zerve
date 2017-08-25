import time
import os
import pathlib
import json

def folder():
	return str(pathlib.Path.home())+"/zerved/"
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

def checkCreds(username,password):
	credlist = readJSON(folder()+"accounts")
	if not username: username = ''
	if not password: password = ''
	if({'username':username,'password':password} in credlist):
		return True
	else:
		return False

def prefs(username):
	return readJSON(folder()+"user/"+username+'/preferences')

def login(contents):
	return {'status':0,'message':'<h1>Welcome. Enjoy your premium <a href="content.html#posts">membership.</a></h1>'}
def home(contents):
	return 'Welcome '+contents['username']+'.'

def log(message):
	logfile = open(folder()+'log','a')
	logfile.write(message)
	logfile.close
