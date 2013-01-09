#!/usr/bin/python2
# -*- coding: utf-8 -*-

import MySQLdb
import paramiko
import ekg
import dddd as secret

class MySQLConnection:
	def __init__(self):
		self.db = MySQLdb.connect(secret.mysql['host'],
			secret.mysql['username'],
			secret.mysql['password'],
			secret.mysql['databasename'],
			connect_timeout=10)
		self.handler = self.db.cursor()
	def query(self, content, *arg):
		self.handler.execute(content, arg)
	def fetchOne(self):
		return self.handler.fetchone()
	def fetchAll(self):
		return self.handler.fetchall()
	def __del__(self):
		self.db.close()

class SSHConnection:
	def __init__(self):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	def setConnection(self, hostname, username, password):
		self.ssh.connect(hostname, username=username, password=password, timeout=10)
	def setCommand(self, command):
		self.stdin, self.stdout, self.stderr = self.ssh.exec_command(command)
	def getResult(self):
		return self.stdout.read()
	def __del__(self):
		self.ssh.close()

class SendMessage():
	def __init__(self):
		ekg.command("session -w praca")
	def setUid(self, uid):
		self.uid = uid
	def setNick(self, nick):
		self.nick = nick
	def setMsg(self, msg):
		self.msg = msg
	def sendMessageByUid(self):
		ekg.command("msg %s %s" % (self.uid, self.msg))
	def sendMessageByNick(self):
		ekg.command("msg %s %s" % (self.nick, self.msg))
	def warningMessage(self):
		self.sendMessageByUid("Nie jesteś klientem WooX")

class CreateDatabaseIteration():
	pass

def createGGNumberFromUid(uid):
	return uid.replace('gg:','')

def getUserNameFromUid(uid):
	mysql = MySQLConnection()
	mysql.query('SELECT nick FROM users WHERE gg=%s', createGGNumberFromUid(uid))
	data = mysql.fetchOne()
	del mysql
	return data

def getServerNameFromUid(uid):
	mysql = MySQLConnection()
	mysql.query('SELECT serwer FROM users WHERE gg=%s', createGGNumberFromUid(uid))
	serverId = mysql.fetchOne()
	mysql.query('SELECT nazwa FROM serwery WHERE id=%s', serverId[0])
	serverName = mysql.fetchOne()
	del mysql
	return serverName[0]

def getServerAdminFromUid(uid):
	mysql = MySQLConnection()
	mysq.query('SELECT serwer FROM users WHERE gg=%s', createGGNumberFromUid(uid))
	serverId = mysql.fetchOne()
	mysql.query('SELECT admin FROM serwery WHERE id=%s', serverId[0])
	if mysql.fetchOne() == '1':
		del mysql
		return "reyder"
	else:
		del mysql
		return "tacajushi"