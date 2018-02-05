import time
import os
import json
import html
import sqlite3

import ezemail
from basic import *

connection = sqlite3.connect(folder()+'data.sql', check_same_thread=False)
connection.cursor().execute('PRAGMA foreign_keys = ON;')

def checkCreds(username,password):
	return connection.cursor().execute(
		'SELECT password FROM users where username=?',
		(username,)
	).fetchone() != password
def prefs(username):
	return dict( connection.cursor().execute(
		'''SELECT preference, value from preferences
		WHERE username == ?''',
		(username,)
	).fetchall() )
def login(contents):
	return {'status':0,'message':'<h1>Welcome. Enjoy your premium <a href="content.html#posts">membership.</a></h1>'}

def posts(contents):
	start = contents['data']['start']
	length = int(prefs(contents['username'])['postnumber'])
	return {'posts': [
		{
			'time':message[0],
			'title':message[1],
			'author':message[2],
			'contents':message[3]
		}
		for message in connection.cursor().execute(
			'''
				SELECT * from (
					SELECT * from (
						SELECT 
							time,
							title,
							author,
							content
						FROM posts
						ORDER BY time DESC
						LIMIT ?
					)
					ORDER BY time ASC
					LIMIT  ?
				)
				ORDER BY time DESC
			;''',
			(
				start+length,
				length
			)
		).fetchall()
	],'start':start}
def post(contents):
	post = contents['data']
	connection.cursor().execute(
		'''
			INSERT INTO posts
			VALUES (?, ?, ?, ?, ?)
		''',(
			time.time(),
			html.escape(post['title']),
			contents['username'],
			html.escape(post['contents']),
			'[]'
		)
	)
	connection.commit()
	return {'status':0}

def comments(contents):
	postnum = contents['data']['post']
	post = connection.cursor().execute(
		'''
			SELECT 
				time,
				title,
				author,
				content,
				comments
			FROM posts
			WHERE time=?
		;''',
		(postnum,)
	).fetchone()
	return {
		'post':{
			'time':post[0],
			'title':post[1],
			'author':post[2],
			'contents':post[3]
		},
		'comments':json.loads(post[4]),
	}
def comment(contents):
	posttime = time.time()
	commentid=contents['data']['comment']
	post = contents['data']['post']
	comments = json.loads(connection.cursor().execute(
		'''
			SELECT (comments) FROM posts
			WHERE time=?
		;''',(
			post,
		)
	).fetchone()[0])#TODO: prevent race condition, someone else could comment in this time
	def findComment(tree,commentid):
		if tree['time']==commentid:
			return tree
		else:
			for comment in tree['comments']:
				status = findComment(comment,commentid)
				if status:
					return status
			return False

	comment = findComment(
		{'time':contents['data']['post'],'comments':comments},
		commentid
	)
	comment['comments'].append(
		{
			'time':posttime,
			'author':contents['username'],
			'content':contents['data']['content'],
			'comments':[]
	})
	connection.cursor().execute(
		'''
			UPDATE posts
			SET comments = ?
			WHERE time=?
		''',(
			json.dumps(comments),
			post
		)
	)
	connection.commit()
	return {'message':'Commented!'}

def checkPath(path):
	if '..' in path: return {'status':0,'excuse':'You cant have a \'..\' in a filename, got it?'}
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
	if not checkFilename(path.split('/')[-1]): return {'status':1,'excuse':'bad name'}
	if contents['data']['type'] == 'file':
		open(path,'w').close()
	else:
		os.mkdir(path)
	return {'status':'0'}
def removeFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return checkPath(path)
	if os.path.isdir(path):
		os.rmdir(path)
	else:
		os.remove(path)
	return {'status':'0'}
def renameFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return checkPath(path)
	if not checkFilename(contents['data']['newname']): return {'status':1,'excuse':'bad name', 'path':path}
	newpath = '/'.join(path.split('/')[:-1]+ [contents['data']['newname']])
	if checkPath(newpath):return checkPath(newpath)
	os.rename(path,newpath)
	return {'path':'/'.join(contents['data']['path'][:-1]+ [contents['data']['newname']])}
def editFile(contents):
	path = folder()+'user/'+contents['username']+'/files/'+ '/'.join(contents['data']['path'])
	if checkPath(path):return checkPath(path)
	data = contents['data']['data']
	f=open(path,'w')
	f.write(data)
	f.close()
	return {'status':'0'}

def messagers(contents):
	def otherUser(pair, user):
		return pair[ (pair.index(user)+1) % 2 ]
	username = contents['username']
	return {'messagers':[
		otherUser(userPair,username)
		for userPair in connection.cursor().execute(
			'''
				SELECT user1, user2
				FROM messagers
				WHERE user1=? or user2=?
			;''',
			(username,)*2
		).fetchall()
	]}
def messager(contents):
	targetName = contents['data']['name']
	ownname = contents['username']
	owndir = folder()+'user/'+ownname+'/messages/'
	targetDir = folder()+'user/'+targetName+'/messages/'
	
	connection.cursor().execute(
		'''
			INSERT INTO messagers(user1,user2)
			VALUES (?,?)
		''',
		(min(targetName,ownname),max(targetName,ownname))
	)
	connection.commit()
	#if targetName in os.listdir(owndir):
	#	return {'status':1,'excuse':'already there, dummy'}
	return {'status':'0'}

def messages(contents):
	start = contents['data']['end']
	if start == None: start=1e100
	username = contents['username']
	target = contents['data']['user']
	#length = prefs(contents['username'])['messagenum']
	return {'messages': [
		{
			'time':message[0],
			'author':message[1],
			'content':message[2]
		}
		for message in connection.cursor().execute(
			'''
				SELECT time, author, content
				FROM messages
				JOIN messagers
				ON messages.usersid=messagers.id
				WHERE time<?
				AND user1=?
				AND user2=?
				ORDER BY time DESC
				LIMIT 8
			;''',
			(
				start,
				min(username,target),
				max(username,target)
			)
		).fetchall()
	]}
def updateMessages(contents):
	end = contents['data']['start']
	username = contents['username']
	target = contents['data']['user']
	return {'messages': [
		{
			'time':message[0],
			'author':message[1],
			'content':message[2]
		}
		for message in connection.cursor().execute(
			'''
				SELECT time, author, content
				FROM messages
				JOIN messagers
				ON messages.usersid=messagers.id
				WHERE time>?
				AND user1=?
				AND user2=?
				ORDER BY time DESC
				LIMIT 8
			;''',
			(
				end,
				min(username,target),
				max(username,target)
			)
		).fetchall()
	]}
def message(contents):
	target = contents['data']['user']
	ownname = contents['username']
	content = contents['data']['content']
	sendtime = time.time()

	connection.cursor().execute(
		'''
			INSERT INTO messages
			SELECT id, ?, ?, ?
			FROM messagers
			WHERE user1=? and user2=?
		;''',
		(
			sendtime,
			ownname,
			content,

			min(ownname,target),
			max(ownname,target)
		)
	)
	connection.commit()

def preferences(contents):
	return {'prefs':prefs(contents['username'])}
def preference(contents):
	connection.cursor().executemany('''
		UPDATE preferences
		SET value = ?
		WHERE username = ? AND preference = ?;
	''',[
		(value, contents['username'], preference)
		for preference, value in contents['data'].items()
	]);
	connection.commit()
	return {'status':'0'}


def cat(contents):
	to = contents['data']['to']
	catfile = open(folder()+'cats/clients','a')
	catfile.write(to+'\n')
	return {'status':'0'}
