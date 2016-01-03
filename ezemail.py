import smtplib
from basic import folder

def sendEmail(TO,SUBJECT,TEXT):
	f = open(folder()+'emailpassword','r')
	gmail_passwd = f.read()
	f.close()
	gmail_sender = 'greyalien502@gmail.com'

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(gmail_sender, gmail_passwd)

	BODY = '\r\n'.join(['To: %s' % TO,
	'From: %s' % gmail_sender,
	'Subject: %s' % SUBJECT,
	'', TEXT])

	try:
		server.sendmail(gmail_sender, [TO], BODY)
		print ('email sent')
	except:
		print ('error sending mail')
	server.quit()
