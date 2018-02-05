import sqlite3
import json
import os

def p(x):
	print(x);return x;

from basic import readJSON, folder
r = lambda n:readJSON(folder()+n)

connexion = sqlite3.connect(folder()+'data.sql')
c = connexion.cursor()
c.execute('PRAGMA foreign_keys = ON;')

#USER TABLE
userData = r("accounts")
users = [ user['username'] for user in userData]
c.execute( """
	CREATE TABLE users (
		username TEXT PRIMARY KEY,
		password TEXT
	);
""")
c.executemany(
	"INSERT INTO users VALUES (?, ?);",
	tuple( (user['username'], user['password']) for user in userData )
)

#PREFERENCE TABLE
preferenceData = (
	[
		tuple((
			username,
			'postnumber',
			r('user/'+username+'/preferences')['postnumber']
		))
		for username in users
	]
)
c.execute("""
	CREATE TABLE preferences (
		username TEXT,
		preference TEXT,
		value REAL,

		PRIMARY KEY (username, preference),
		FOREIGN KEY(username) REFERENCES users(username)
	)
""")
c.executemany(
	'INSERT INTO preferences VALUES (?, ?, ?);',
	preferenceData
)


#MESSAGER TABLE
userPairs = [
	(user1,user2)
	for user1 in users
	for user2 in users
	if  user1 in os.listdir(folder()+'user/'+user2+'/messages/')
]
c.execute('''
	CREATE TABLE messagers (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user1 TEXT,
		user2 TEXT,
		
		FOREIGN KEY(user1) REFERENCES users(username),
		FOREIGN KEY(user2) REFERENCES users(username),
		CHECK ( user1 < user2 )
	)
;''')
c.executemany(
	'''
		INSERT INTO messagers(user1,user2)
		VALUES (?, ?)
	''' ,
	[(min(user1,user2),max(user1,user2))
	for user1,user2 in userPairs]
);

#MESSAGE TABLE
c.execute('''
	CREATE TABLE messages (
		usersid INTEGER,
		time REAL PRIMARY KEY,
		author TEXT,
		content TEXT,
		
		FOREIGN KEY(usersid) REFERENCES messagers(id)
		FOREIGN KEY(author) REFERENCES users(username)
	)
;''')
c.executemany(
	'''
		INSERT INTO messages
		SELECT id, ?, ?, ?
		FROM messagers
		WHERE user1=? and user2=?
	;''',
	[
		(
			messageData['time'],
			messageData['author'],
			messageData['content'],

			min(user1,user2),
			max(user1,user2)
		)
		for user1,user2 in userPairs
		for time in os.listdir(folder()+'user/'+user2+'/messages/'+user1)
		for messageData in (r('user/'+user2+'/messages/'+user1+'/'+time),)
	]
)

#POST TABLE
c.execute('''
	CREATE TABLE posts (
		time REAL PRIMARY KEY,
		title TEXT,
		author TEXT,
		content TEXT,
		comments TEXT,
		
		FOREIGN KEY(author) REFERENCES users(username)
	)
;''')
c.executemany(
	'''
		INSERT INTO posts
		VALUES (?, ?, ?, ?, ?)
	;''',
	[
		(
			postData['time'],
			postData['title'],
			postData['author'],
			postData['contents'],
			comments
		)
		for postData,comments in (
			(
				r('posts/'+postFile),
				json.dumps(r('comments/'+postFile)['comments']))
			for postFile in os.listdir(folder()+'posts/')
		)
	]
)



connexion.commit()
