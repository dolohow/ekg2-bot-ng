#!/usr/bin/python2.7
# -*- coding: ISO-8859-2 -*-

import ekg
import urllib
import os

path = "/home/tacajushi/.ekg2/scripts/"

def ping():
        serversList = open(path + 'serversList', 'r')
        read_data = serversList.readlines()
        for i in read_data:
                i = i.replace('\n', '')
                response = os.system("ping -c 1 " + i + "  > /dev/null")
                if response != 0:
                        response2 = os.system("ping -c 3 " + i + "  > /dev/null")
                        if response2 != 0:
                                ekg.echo(i + " nie działa")
        serversList.close()

ekg.timer_bind(900, ping)