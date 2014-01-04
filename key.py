#!/usr/bin/python2.7
# -*- coding: ISO-8859-2 -*-

import ekg
import string

def keypress(key):
        current = str(ekg.window_current())
        # F5
        if str(key) == '269':
                ekg.command("msg " + current + " Witaj!")
        if str(key) == '270':
                ekg.command("msg " + current + " Co mogę dla Ciebie zrobić?")
        if str(key) == '271':
                ekg.command("msg " + current + " http://woox.pl/register.php")
        if str(key) == '272':
                ekg.command("msg " + current + " Wyślij do mnie wiadomość (tutaj na gg) o treści !transfer tak jakbyś wysyłał SMS o takiej tresci")
        if str(key) == '273':
                ekg.command("msg " + current + " Pozdrawiam i życzę wysokich transferów :-)")

ekg.handler_bind('ui-keypress', keypress)
