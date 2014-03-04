#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import ekg
import urllib
import main
from datetime import date

domain = "http://woox.pl/API/api.php?"

def blokada(zablokuj, uid):
	day = date.today()
	podziel = uid.split(',')
        sendMessage = main.SendMessage()
        sendMessage.setUid(podziel)
        sendMessage.setMsg("Z dniem", day.isoformat(), "konto zostało zablokowane")
        sendMessage.sendMessageByUid()

def wplaty(deadbeats, bool):
        day = date.today()
        get = urllib.urlopen(domain + "deadbeats")
        const = get.read()
        const = const.split('|')
        x = -1
        biggest = 0
        for i in const:
                x = x + 1
                if x % 2 == 0:
                        if biggest < len(const[x]):
                                biggest = len(const[x])
        x = -1
        for j in const:
                x = x + 1
                if x % 2 == 0:
                        subtract = const[x+1].split('-')
                        for k in range(3): 
                                subtract[k] = int(subtract[k])
                        y = date(subtract[0], subtract[1], subtract[2])
                        left = y - day
                        left = left - left - left
                        expressionSize = len(const[x])
                        if expressionSize < biggest:
                                shift = biggest - expressionSize
                                const[x] = const[x] + " " * shift
                        ekg.echo(const[x] + "  " + const[x+1] + "  " + str(left.days))

def info(self, bool):
	nick = str(ekg.window_current())
	mysql = main.MySQLConnection('remote')
	mysql.query('SELECT oplata_konta, sposob_platnosci, pay_my, vnc, rl, warn, dysk, pakiet_dysk, pakiet_cena, blokada, adnotacje FROM users WHERE nick=%s', nick)
	data = mysql.fetchOne()
	temp = []
	temp.append(['Waznosc', str(data[0])])
	temp.append(['Platnosc', data[1]])
	if data[2] != 0:
		temp.append(['Mine', '*'])
	else:
		temp.append(['Mine', ''])
	if data[3] == 1:
		temp.append(['VNC', '*'])
	else:
		temp.append(['VNC', ''])
	if data[4] == 1:
		temp.append(['RL', '*'])
	else:
		temp.append(['RL', ''])
	temp.append(['Warn', data[5]])
	# Nie działą zamiana na liczbę całkowitą
	temp.append(['Dysk', str(int(data[6]))+'/'+str(data[7])])
	temp.append(['Cena', data[8]])
	if data[9] == 1:
		temp.append(['Blokada', '*'])
	else:
		temp.append(['Blokada', ''])
	temp.append(['Notatka', data[10]])
	j = 0
	for i in temp:
		if len(str(i[0])) >= len(str(i[1])):
			temp[j].append(len(str(i[0])))
			j = j + 1
		else:
			temp[j].append(len(str(i[1])))
			j = j + 1
	ekg.echo('%-{0}s %-{1}s %-{2}s %-{3}s %-{4}s %-{5}s %-{6}s %-{7}s %-{8}s %-{9}s'.format(temp[0][2], temp[1][2], temp[2][2], temp[3][2], temp[4][2], temp[5][2], temp[6][2], temp[7][2], temp[8][2], temp[9][2]) % (temp[0][0], temp[1][0], temp[2][0], temp[3][0], temp[4][0], temp[5][0], temp[6][0], temp[7][0], temp[8][0], temp[9][0]))
	ekg.echo('%-{0}s %-{1}s %-{2}s %-{3}s %-{4}s %-{5}s %-{6}s %-{7}s %-{8}s %-{9}s'.format(temp[0][2], temp[1][2], temp[2][2], temp[3][2], temp[4][2], temp[5][2], temp[6][2], temp[7][2], temp[8][2], temp[9][2]) % (temp[0][1], temp[1][1], temp[2][1], temp[3][1], temp[4][1], temp[5][1], temp[6][1], temp[7][1], temp[8][1], temp[9][1]))

def advert(msg, uid):
        podziel = uid.split(',')
        sendMessage = main.SendMessage()
        sendMessage.setUid(podziel)
        sendMessage.setMsg(msg)
        sendMessage.sendMessageByUid()

def message_to_everyone_from_list(self, file_name, msg):
		f = open(file_name, 'r').readlines()
		sendMessage = main.SendMessage()
		sendMessage.setUid(f)
		sendMessage.setMsg(msg)
		sendMessage.sendMessageByUid()

ekg.command_bind('blokada', blokada)
ekg.command_bind('deadbeats', wplaty)
ekg.command_bind('info', info)
ekg.command_bind('advert', advert)
ekg.command_bind('announce', message_to_everyone_from_list)
