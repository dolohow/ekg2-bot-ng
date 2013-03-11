#!/usr/bin/python

import ekg
import time

names = ('dddd', 'main', 'bot', 'key', 'messages', 'ping', 'reminder', 'serverCommands')

def init():
	for i in names:
		ekg.command('python:load %s' % i)
	ekg.command('session -w praca')
	ekg.command('connect')
	ekg.command('session -w freenode')
	ekg.command('connect')
def deinit():
	for i in names:
		ekg.command('python:unload %s' % i)
