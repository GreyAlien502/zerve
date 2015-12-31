import os
from basic import *

def addPreference(keys):
	usernames = [user['username'] for user in os.listdir(folder()+accounts)]
	for username in usernames:
		actuaprefs = prefs(username):
		if key not in actuaprefs:
			actuaprefs.update({key:''})
		preffile = folder()+'user/'+contents['username']+'/preferences'
		writeJSON(preffile,actuaprefs)
