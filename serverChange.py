#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import ekg

def message_handler(session, uid, type, text, sent_time, ignore_level):
        # Definicje stałych
        text = text.strip()
        
        if text.find("!new") == 0:
                text = text.split(" ")
                f = open('users', 'a')
                f.write('%s:%s\n' % (text[1], text[2]))
                f.close()

ekg.handler_bind('protocol-message-received', message_handler)