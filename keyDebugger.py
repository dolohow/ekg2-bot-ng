#!/usr/bin/python2.7
# -*- coding: ISO-8859-2 -*-

import ekg
import string

def keypress(key):
        ekg.echo("Przycisk " + str(key))

ekg.handler_bind('ui-keypress', keypress)