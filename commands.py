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
	if path[0]=='/': return 'You cant have a \./\' start a filename, k?'
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
