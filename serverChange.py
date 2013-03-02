#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import ekg
import re

def message_handler(session, uid, type, text, sent_time, ignore_level):
        # Definicje stałych
        text = text.strip()
        checkItOut = text.decode('utf-8')
        
        if len(re.findall(u"new login has[łl]o", checkItOut, flags=re.IGNORECASE)) != 0:
        	ekg.command("msg %s zastąp słowa login, hasło swoimi danymi do konta, które ma zostać utworzone na serwerze!!" % uid)
        elif text.find("!new") == 0:
                text = text.split(" ")
                f = open('users', 'a')
                f.write('%s:%s\n' % (text[1], text[2]))
                f.close()

ekg.handler_bind('protocol-message-received', message_handler)