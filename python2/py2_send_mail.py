'''
# AUTHOR SY0UYU
# UPDATE 18-5-11
# Version 1.0.0
'''
#!\usr\bin\env python2
#-*- encoding:utf-8 -*-
import requests
import smtplib
import time
import os
from email.mime.text import MIMEText
from email.header import Header


def getvalue(tmp):
	tmp = tmp.split(' ')
	tmp = tmp[2].replace("\n","")
	return tmp


def check_network():
	exit_code = os.system('ping -c 3 -W 3 8.8.8.8')
	if exit_code:
	#run in connect failed
		if "FALSE" == getvalue(newconf[0]):
			newconf[0] = 'OFFLINE = TRUE\n'
		return "OFFLINE"
	else :
		if "TRUE" == getvalue(newconf[0]):
			newconf[0] = 'OFFLINE = FALSE\n'
		return "ONLINE"


def get_ip():
	url = r'http://2017.ip138.com/ic.asp'
	r = requests.get(url)
	txt = r.text
	ip = txt[txt.find("[") + 1: txt.find("]")]
	return ip


def send_ip(ip):
	sender = 'PI@pi.com'
	receivers = ['you@email.com']
	message = MIMEText(ip, 'plain', 'utf-8')
	message['From'] = Header('From', 'utf-8')
	message['To'] = Header('To', 'utf-8')
	subject = 'Python mail'
	message['Subject'] = Header(subject, 'utf-8')

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receivers, message.as_string())
		print "Email send over"
	except smtplib.SMTPException:
		print "ERROR:can't send email"


def writetofile(new):
	pyconf.seek(0)
	pyconf.truncate()
	for pot in range(len(new)):
		pyconf.write(new[pot])


if __name__ == '__main__':
	time.sleep(10)
	pyconf = open("/home/pi/default.conf","r+")
	newconf = pyconf.readlines()
	if "OFFLINE" == check_network():
		writetofile(newconf)
		pyconf.close()
		os.system('sudo bash /home/pi/reboot.sh')
	else :
		ip = get_ip()
		if ip == getvalue(newconf[2]):
			writetofile(newconf)
			pyconf.close()
		else :
			newconf[2] = 'OLDIP = ' + ip + '\n'
			writetofile(newconf)
			pyconf.close()
			send_ip(ip)
