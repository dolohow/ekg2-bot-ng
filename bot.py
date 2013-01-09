#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import main
import ekg
from string import Template
from random import choice
import re

def textCommands(session, uid, type, text, sent_time, ignore_level):
    text = text.strip()
    mysql = main.MySQLConnection()
    mysql.query('SELECT command FROM botmsg')
    data = mysql.fetchAll()
    for i in data:
        if text == i[0]:
            fetch = main.MySQLConnection()
            fetch.query('SELECT msg FROM botmsg WHERE command=%s', i[0])
            sendMessage = main.SendMessage()
            sendMessage.setUid(uid)
            sendMessage.setMsg(fetch.fetchOne()[0])
            sendMessage.sendMessageByUid()
            del fetch, sendMessage

    if text == '!acc disk':
        mysql.query('SELECT dysk, pakiet_dysk FROM users WHERE gg=%s', main.createGGNumberFromUid(uid))
        a = mysql.fetchOne()
        sendMessage = main.SendMessage()
        sendMessage.setUid(uid)
        sendMessage.setMsg('%s / %s GB, wykorzystano: %.2s%%' % (a[0], a[1], a[0]/a[1]*100))
        sendMessage.sendMessageByUid()
    if text == '!acc load':
        mysql.query('SELECT akt_down_lacza, akt_upl_lacza, load1, load2, load3 FROM serwery WHERE nazwa=%s', main.getServerNameFromUid(uid))
        a = mysql.fetchOne()
        sendMessage = main.SendMessage()
        sendMessage.setUid(uid)
        sendMessage.setMsg('DL: %.4s MB/s UL: %.4s MB/s   Load: %s %s %s' % (float(a[0])/1024, float(a[1])/1024, a[2], a[3], a[4]))
        sendMessage.sendMessageByUid()
    if text == '!acc transfer':
        mysql.query('SELECT pay_my, sposob_platnosci, id FROM users WHERE gg=%s', main.createGGNumberFromUid(uid))
        a = mysql.fetchOne()
        sendMessage = main.SendMessage()
        sendMessage.setUid(uid)
        if a[0] == 0:
            if a[1] == 'przelew':
                sendMessage.setMsg('Ciekot Grzegorz\nAl. N.M.P.62/27\n42-200 Czestochowa\n\n36 1140 2004 0000 3902 3331 4150\n\ntytuł przelewu: Darowizna x%sx' % a[2])
            if a[1] == 'paypal':
                sendMessage.setMsg('paypal: woox@woox.pl\nproszę zaznaczyć prezent, krewni/znajomi')
            if a[1] == 'przysluga':
                sendMessage.setMsg('Nie musisz nic płacić ;-)')
        if a[0] == 1:
            if a[1] == 'przelew':
                random = ["wilk", "dudek", "puchacz", "żółw", "żaba", "jelonek", "jeż", "sum", "jaszczurka", "sokół", "nietoperz"]
                sendMessage.setMsg('20 1140 2004 0000 3502 7432 5846\ntytuł przelewu: Allegro %s x%sx' % (choice(random), a[2]))
            if a[1] == 'paypal':
                sendMessage.setMsg('paypal: dolohow@gmail.com\nproszę zaznaczyć prezent, krewni/znajomi')
        if a[0] == 2:
            if a[1] == 'przelew':
                sendMessage.setMsg('22 1140 2004 0000 3202 7438 8328\nDarowizna x%sx' % a[2])
            if a[1] == 'paypal':
                sendMessage.setMsg('paypal: reyderti@gmail.com\nproszę zaznaczyć prezent, krewni/znajomi')
        sendMessage.sendMessageByUid()

def sshCommands(session, uid, type, text, sent_time, ignore_level):
    text = text.strip()
    mysql = main.MySQLConnection()
    mysql.query('SELECT command FROM botssh')
    data = mysql.fetchAll()
    for i in data:
        if text == i[0]:
            fetch = main.MySQLConnection()
            ssh = main.SSHConnection()
            server = main.getServerNameFromUid(uid)
            username = main.getUserNameFromUid(uid)
            fetch.query('SELECT execute FROM botssh WHERE command=%s', i[0])
            execute = fetch.fetchOne()
            s = Template(execute[0])
            s = s.safe_substitute(nick=username[0])
            ssh.setConnection(server, 'root', secret.serversList[server])
            ssh.setCommand(s)
            sendMessage = main.SendMessage()
            sendMessage.setUid(uid)
            sendMessage.setMsg(ssh.getResult())
            sendMessage.sendMessageByUid()
            del ssh, fetch, sendMessage
    del mysql

def regexCommand(session, uid, type, text, sent_time, ignore_level):
    checkItOut = text.decode('utf-8')
    mysql = main.MySQLConnection()
    mysql.query('SELECT regex FROM botrex')
    data = mysql.fetchAll()
    for i in data:
        if len(re.findall(i[0], checkItOut, flags=re.IGNORECASE | re.UNICODE)) != 0:
            fetch = main.MySQLConnection()
            fetch.query('SELECT msg FROM botrex WHERE regex=%s', i[0])
            sendMessage = main.SendMessage()
            sendMessage.setUid(uid)
            sendMessage.setMsg(fetch.fetchOne()[0])
            sendMessage.sendMessageByUid()

ekg.handler_bind('protocol-message-received', textCommands)
ekg.handler_bind('protocol-message-received', sshCommands)
ekg.handler_bind('protocol-message-received', regexCommand)