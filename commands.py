import time
import os
import json

import ezemail

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

def checkCreds(username,password):
	userfile = open(folder()+"accounts",'r')
	credlist = userfile.read().splitlines()
	if not username: username = ''
	if not password: password = ''
	if(username+'|'+password in credlist):
		return True
	else:
		return False

def prefs(username):
	return readJSON(folder()+"user/"+username+'/preferences')
def message(username,content):
	address = prefs(username)['message address']
	ezemail.sendEmail()

def login(contents):
	return '<h1>Welcome. Enjoy your premium <a href="content.html#posts">membership.</a></h1>'
def home(contents):
	return 'Welcome '+contents['username']+'.'

def posts(contents):
	postnames = os.listdir(folder()+'posts')
	postnames.sort(reverse=True)
	start = contents['data']['start']
	length = int(prefs(contents['username'])['postnumber'])
	if start+length > len(postnames):
		toSend = postnames[start:]
	else:
		toSend = postnames[start:start+length]
	toSend = [readJSON(folder()+'posts/'+postname) for postname in toSend]
	return {'posts':toSend,'start':start}
def post(contents):
	post = contents['data']
	posttime = time.time()
	post.update({'time':posttime,'author':contents['username'],'comments':[]})
	writeJSON(folder()+'posts/'+str(posttime),post)
	writeJSON(folder()+'comments/'+str(posttime),{"comments":[]})
	return 'Sent!'
	

def comments(contents):
	postnum = str(contents['data']['post'])
	post     = readJSON(folder()+'posts/'   +postnum)
	comments = readJSON(folder()+'comments/'+postnum)
	comments = comments['comments']
	return {'post':post,'comments':comments}
def comment(contents):
	posttime = time.time()
	commentfilename = folder()+'comments/'+str(contents['data']['post'])
	comments = readJSON(commentfilename)
	comment = comments
	for i in contents['data']['comment']:
		comment = comment['comments'][i]
	comment['comments'].append({'time':posttime,'author':contents['username'],'content':contents['data']['content'],'comments':[]})
	writeJSON(commentfilename, comments)
	return {'message':'Commented!','post':contents['data']['post']}

def files(contents):
	subpath = contents['data']['path']
	path = folder()+'user/'+contents['username']+'/files/'+ subpath
	if '..' in path: return 'You cant have a \'..\' in a filename, got it?'
	if os.path.isdir(path):
		filetype = 'directory'
		return {'type':'directory','files':os.listdir(path),'path':subpath}
	else:
		actuafile = open(path,'r')
		content = actuafile.read()
		actuafile.close()
		return{'type':'file','content':content,'path':subpath}
def file(contents):
	subpath = contents['data']['path']+contents['data']['title']
	content = contents['data']['content']
	path = folder()+'user/'+contents['username']+'/files/'+ subpath
	if '..' in path: return 'You cant have a \'..\' in a filename, got it?'
	dest = open(path,'w')
	dest.write(content)
	dest.close()

def preferences(contents):
	return prefs(contents['username'])

def preference(contents):
	preffile = folder()+'user/'+contents['username']+'/preferences'
	writeJSON(preffile,contents['data'])
	return 'success'


def cat(contents):
	to = contents['data']['to']
	catfile = open(folder()+'cats/clients','a')
	catfile.write(to+'\n')
	return 'success'
