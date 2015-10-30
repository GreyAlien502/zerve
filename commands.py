import time
import os
import json

def folder():
	return os.getenv('HOME')+"/zerved/"

def checkCreds(username,password):
	userfile = open(folder()+"accounts",'r')
	credlist = userfile.read().splitlines()
	if(username+'|'+password in credlist):
		return True
	else:
		return False

def prefs(username):
	return json.load(open(folder()+"user/"+username+'/preferences'))

def login(contents):
	return '<h1>Welcome. Enjoy your premium <a href="content.html#posts">membership.</a></h1>'
def home(contents):
	return 'Welcome '+contents['username']+'.'

def posts(contents):
	postnames = os.listdir(folder()+'posts');
	postnames.sort(reverse=True)
	start = contents['data']['start']
	length = prefs(contents['username'])['postnumber']
	if start+length > len(postnames):
		toSend = postnames[start:]
	else:
		toSend = postnames[start:start+length]
	toSend = [json.load(open(folder()+'posts/'+postname)) for postname in toSend]
	return {'posts':toSend,'start':start}
def post(contents):
	post = contents['data']
	posttime = time.time()
	post.update({'time':posttime,'author':contents['username'],'comments':[]})
	post = json.dumps(post)
	postfile = open(folder()+'posts/'+str(posttime),'w')
	postfile.write(post)
	postfile.close()
	commentfile = open(folder()+'comments/'+str(posttime),'w')
	commentfile.write('{"comments":[]}')
	commentfile.close()
	return 'Sent!'

def comments(contents):
	postnum = str(contents['data']['post'])
	post     = json.load(open(folder()+'posts/'   +postnum))
	comments = json.load(open(folder()+'comments/'+postnum))
	comments = comments['comments']
	return {'post':post,'comments':comments} 
def comment(contents):
	posttime = time.time()
	commentfilename = folder()+'comments/'+str(contents['data']['post'])
	comments = json.load(open(commentfilename))
	comment = comments
	for i in contents['data']['comment']:
		comment = comment['comments'][i]
	comment['comments'].append({'time':posttime,'author':contents['username'],'content':contents['data']['content'],'comments':[]})
	commentfile = open(commentfilename,'w')
	commentfile.write(json.dumps(comments))
	commentfile.close()
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

def cat(contents):
	to = contents['to']

