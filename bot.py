#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import main
import ekg
from string import Template
from random import choice
from datetime import date
import re
import dddd as secret

def messagesForEveryone(uid, mysql, text):
	mysql.query('SELECT command FROM botmsg')
	data = mysql.fetchAll()
	for i in data:
		if text == i[0]:
			mysql.query('SELECT msg FROM botmsg WHERE command=%s', i[0])
			sendMessage = main.SendMessage()
			sendMessage.setUid(uid)
			sendMessage.setMsg(mysql.fetchOne()[0])
			sendMessage.sendMessageByUid()
			break

def accountCommands(uid, mysql, text):
	if main.checkUserExistence(uid):
		if text == '!disk':
			mysql.query('SELECT dysk, pakiet_dysk FROM users WHERE gg=%s', main.createGGNumberFromUid(uid))
			a = mysql.fetchOne()
			sendMessage = main.SendMessage()
			sendMessage.setUid(uid)
			sendMessage.setMsg('%.0f / %s GB, wykorzystano: %.0f%%' % (a[0], a[1], a[0]/a[1]*100))
			sendMessage.sendMessageByUid()
		elif text == '!load':
			mysql.query('SELECT akt_down_lacza, akt_upl_lacza, load1, load2, load3 FROM serwery WHERE nazwa=%s', main.getServerNameFromUid(uid))
			a = mysql.fetchOne()
			sendMessage = main.SendMessage()
			sendMessage.setUid(uid)
			sendMessage.setMsg('DL: %.4s MB/s UL: %.4s MB/s   Load: %s %s %s' % (float(a[0])/1024, float(a[1])/1024, a[2], a[3], a[4]))
			sendMessage.sendMessageByUid()
		elif text == '!transfer':
			mysql.query('SELECT pay_my, sposob_platnosci, id FROM users WHERE gg=%s', main.createGGNumberFromUid(uid))
			a = mysql.fetchOne()
			sendMessage = main.SendMessage()
			sendMessage.setUid(uid)
			if a[0] == 0:
				if a[1] == 'przelew':
				    sendMessage.setMsg('Ciekot Grzegorz\nAl. N.M.P.62/27\n42-200 Czestochowa\n\n36 1140 2004 0000 3902 3331 4150\n\ntytuł przelewu: Darowizna x%sx' % a[2])
				elif a[1] == 'paypal':
				    sendMessage.setMsg('paypal: woox@woox.pl\nproszę zaznaczyć prezent, krewni/znajomi')
				elif a[1] == 'przysluga':
				    sendMessage.setMsg('Nie musisz nic płacić ;-)')
			elif a[0] == 1:
				if a[1] == 'przelew':
				    random = ["wilk", "dudek", "puchacz", "żółw", "żaba", "jelonek", "jeż", "sum", "jaszczurka", "sokół", "nietoperz"]
				    sendMessage.setMsg('20 1140 2004 0000 3502 7432 5846\ntytuł przelewu: Allegro %s x%sx' % (choice(random), a[2]))
				elif a[1] == 'paypal':
				    sendMessage.setMsg('paypal: tacajushi@woox.pl\nproszę zaznaczyć prezent, krewni/znajomi')
			elif a[0] == 2:
				if a[1] == 'przelew':
				    sendMessage.setMsg('22 1140 2004 0000 3202 7438 8328\nDarowizna x%sx' % a[2])
				elif a[1] == 'paypal':
				    sendMessage.setMsg('paypal: reyderti@gmail.com\nproszę zaznaczyć prezent, krewni/znajomi')
			sendMessage.sendMessageByUid()
		elif text == '!valid':
			today = date.today()
			mysql.query('SELECT oplata_konta FROM users WHERE gg=%s', main.createGGNumberFromUid(uid))
			a = mysql.fetchOne()
			sendMessage = main.SendMessage()
			sendMessage.setUid(uid)
			sendMessage.setMsg('Ważność konta %s, pozostało %s dni' % (str(a[0]), str((a[0]-today).days)))
			sendMessage.sendMessageByUid()
		elif text == '!upload limit':
		        mysql.query('SELECT transfer_used FROM users WHERE gg=%s', main.createGGNumberFromUid(uid))
			a = mysql.fetchOne()
			sendMessage = main.SendMessage()
			sendMessage.setUid(uid)
		        sendMessage.setMsg(a[0])
			sendMessage.sendMessageByUid()

def sshCommands(uid, mysql, text):
	if main.checkUserExistence(uid):
		mysql.query('SELECT command FROM botssh')
		data = mysql.fetchAll()
		for i in data:
			if text.find(i[0]) == 0:
				ssh = main.SSHConnection()
				server = main.getServerNameFromUid(uid)
				username = main.getUserNameFromUid(uid)
				mysql.query('SELECT execute FROM botssh WHERE command=%s', i[0])
				execute = mysql.fetchOne()
				s = Template(execute[0])
				s = s.safe_substitute(nick=username[0], name=re.split(' ', text, 2)[1])
				ssh.setConnection(server, 'root', secret.serversList[server])
				ssh.setCommand(s)
				sendMessage = main.SendMessage()
				sendMessage.setUid(uid)
				sendMessage.setMsg(ssh.getResult())
				sendMessage.sendMessageByUid()
				break

def messageHandler(session, uid, type, text, sent_time, ignore_level):
	text = ' '.join(text.split())
	if text.find('!') == 0:
		mysql_local = main.MySQLConnection('local')
		mysql_remote = main.MySQLConnection('remote')

		messagesForEveryone(uid, mysql_local, text)
		sshCommands(uid, mysql_local, text)
		accountCommands(uid, mysql_remote, text)

ekg.handler_bind('protocol-message-received', messageHandler)