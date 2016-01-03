import time
import os
import json
import html

import ezemail
from basic import *

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
	post['title'] = html.escape(post['title'])
	post['contents'] = html.escape(post['contents'])
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
	commentid=contents['data']['comment']
	commentfilename = folder()+'comments/'+str(contents['data']['post'])
	comments = readJSON(commentfilename)['comments']
	def findComment(tree,commentid):
		if tree['time']==commentid:
			return tree
		else:
			for comment in tree['comments']:
				status = findComment(comment,commentid)
				if status:
					return status
			return False

	comment = findComment({'time':contents['data']['post'], 'comments':comments},commentid)

	comment['comments'].append({'time':posttime,'author':contents['username'],'content':contents['data']['content'],'comments':[]})
	writeJSON(commentfilename, {'comments':comments})
	return {'message':'Commented!','post':contents['data']['post']}

def checkPath(path):
	if '..' in path: return 'You cant have a \'..\' in a filename, got it?'
	return False
def checkFilename(name):
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
	for char in name: 
		if char not in alphabet:
			return False
	return True
def files(contents):
	subpath = '/'.join(contents['data']['path'])
	path = folder()+'user/'+contents['username']+'/files/'+ subpath
	if checkPath(path):return checkPath(path)
	if os.path.isdir(path):
		filetype = 'directory'
		return {'type':'directory','files':os.listdir(path),'path':subpath}
	else:
		actuafile = open(path,'r')
		content = actuafile.read()
		actuafile.close()
		return{'type':'file','content':content,'path':subpath}
def addFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return checkPath(path)
	if not checkFilename(path.split('/')[-1]): return 'bad name'
	if contents['data']['type'] == 'file':
		open(path,'w').close()
	else:
		os.mkdir(path)
	return 'success'
def removeFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return checkPath(path)
	if os.path.isdir(path):
		os.rmdir(path)
	else:
		os.remove(path)
	return 'success'
def renameFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return {'error':checkPath(path), 'path':path}
	if not checkFilename(contents['data']['newname']): return {'error':'bad name', 'path':path}
	newpath = '/'.join(path.split('/')[:-1]+ [contents['data']['newname']])
	if checkPath(newpath):return {'error':checkPath(newpath), 'path':path}
	os.rename(path,newpath)
	return {'path':'/'.join(contents['data']['path'][:-1]+ [contents['data']['newname']])}
def editFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return checkPath(path)
	data = contents['data']['data']
	f=open(path,'w')
	f.write(data)
	f.close()
	return 'success'

def messagers(contents):
	messagerlecian = os.listdir(folder()+'user/'+contents['username']+'/messages/')
	return {'messagers':messagerlecian}
def messager(contents):
	targetName = contents['data']['name']
	ownname = contents['username']
	owndir = folder()+'user/'+ownname+'/messages/'
	targetDir = folder()+'user/'+targetName+'/messages/'
	if targetName in os.listdir(owndir):
		return 'already there, dummy'
	else:
		os.mkdir(owndir+targetName)
		os.symlink(owndir+targetName,targetDir+ownname)
		return 'done'
def messages(contents):
	start = contents['data']['end']
	directory = folder()+'user/'+contents['username']+'/messages/'+contents['data']['user']
	messagelecian = os.listdir(directory)
	messagelecian = [float(messagelecian_item) for messagelecian_item in messagelecian]
	messagelecian.sort(reverse=True)
	if start == None:
		startnum = 0
	else:
		startnum = messagelecian.index(start)+1
	#length = prefs(contents['username'])['messagenum']
	length=8
	return {'messages':[readJSON(directory+'/'+str(messagelecian_item)) for messagelecian_item in messagelecian[startnum:startnum+length]]}
def message(contents):
	target = contents['data']['user']
	ownname = contents['username']
	content = contents['data']['content']
	sendtime = time.time()

	filepath = folder()+'user/'+ownname+'/messages/'+target+'/'+str(sendtime)
	writeJSON(filepath,{'time':sendtime,'content':content,'author':ownname})
	targetPrefs = prefs(target)
	if targetPrefs['email messages'] != '':
		ezemail.send(targetPrefs['email address'])
		

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
