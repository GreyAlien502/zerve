from basic import *

def setPreferences(keys):
	usernames = [user['username'] for user in readJSON(folder()+accounts)]
	for username in usernames:
		actuaprefs = prefs(username):
		for key in keys:
			if key not in actuaprefs:
				prefs.update(key:'')
		writeJSON
