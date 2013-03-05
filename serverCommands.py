#!/usr/bin/python

import main
import dddd as secret
import ekg

def serversCommand(bool, command):
	for i in secret.serversList:
		ssh = main.SSHConnection()
		ssh.setConnection(i, 'root', secret.serversList[i])
		ssh.setCommand(command)
		ekg.echo(str(i))
		ekg.echo(ssh.getResult())
		del ssh

def serverCommand(bool, command):
	nick = str(ekg.window_current())
	command = command.replace('%1', nick)
	hostname = main.getServerNameFromNick(nick)
	ssh = main.SSHConnection()
	ssh.setConnection(hostname, 'root', secret.serversList[hostname])
	ssh.setCommand(command)
	ekg.echo(ssh.getResult())


ekg.command_bind('serversCommand', serversCommand)
ekg.command_bind('serverCommand', serverCommand)
