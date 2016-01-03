import os
from basic import *

def addPreference(key):
	usernames = [user for user in os.listdir(folder()+'user')]
	for username in usernames:
		actuaprefs = prefs(username)
		if key not in actuaprefs:
			actuaprefs.update({key:''})
		preffile = folder()+'user/'+username+'/preferences'
		print(actuaprefs)
		writeJSON(preffile,actuaprefs)
